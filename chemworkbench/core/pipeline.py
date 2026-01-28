"""
chemworkbench.core.pipeline

Unified Processing Pipeline — ChemWorkBench v2.2
===============================================

LLM‑friendly commentary
-----------------------
This module implements the canonical v2.2 ingestion pipeline for ChemWorkBench.
It orchestrates the full sequence:

    1. File sniffing (technique + loader selection)
    2. Loader execution (universal structure output)
    3. Processor routing (Technique → ProcessorClass)
    4. Processor pipeline:
         - validate
         - preprocess
         - process
         - postprocess
         - metadata
         - QC
    5. Plot generation
    6. PipelineResult assembly

Responsibilities:
- Orchestrate the ingestion pipeline deterministically
- Ensure each stage receives the correct data structure
- Provide a single entrypoint for CLI, API, and UI layers

Non‑responsibilities:
- Technique detection logic (handled by the sniffer/anchor engine)
- Loader selection logic (handled by the loader registry)
- Scientific interpretation (handled by processors)
- Plotting logic (handled by the plotting service)
"""

from __future__ import annotations

from pathlib import Path

from chemworkbench.core.models import (
    RawDataBundle,
    PipelineResult,
    DetectedFormat,
)
from chemworkbench.utils.file_sniffer.file_sniffer import sniff_file
from chemworkbench.utils.loaders.registry import select_loader_for_path
from chemworkbench.core.routing import get_processor_for_technique
from chemworkbench.services.plotting_service import PlottingService
from chemworkbench.runtime.logging import get_logger
from chemworkbench.runtime.errors import PipelineError


logger = get_logger(__name__)


# ======================================================================
# Pipeline Orchestrator (v2.2)
# ======================================================================

class Pipeline:
    """
    Canonical v2.2 ingestion pipeline orchestrator.

    This class is intentionally small and deterministic. It wires together:
        - file sniffing
        - loader selection + execution
        - processor routing + execution
        - plotting
        - result assembly

    All scientific logic lives in loaders, processors, and services.
    """

    def __init__(self) -> None:
        self.plotting_service = PlottingService()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self, path: str | Path) -> PipelineResult:
        """
        Execute the full v2.2 ingestion pipeline.

        Steps:
            1. Sniff file → DetectedFormat
            2. Select loader
            3. Load raw data (universal structure)
            4. Resolve processor
            5. Processor pipeline:
                 validate → preprocess → process → postprocess
            6. Build metadata + QC
            7. Generate plots
            8. Assemble PipelineResult
        """
        path = Path(path)

        if not path.exists():
            raise PipelineError(f"File not found: {path}")

        logger.info(f"Starting pipeline for: {path}")

        # --------------------------------------------------------------
        # 1. Sniff file (technique + basic format)
        # --------------------------------------------------------------
        fmt: DetectedFormat = sniff_file(path)
        logger.debug(f"Detected format: {fmt}")

        # --------------------------------------------------------------
        # 2. Select loader
        # --------------------------------------------------------------
        loader_cls = select_loader_for_path(path)
        if loader_cls is None:
            raise PipelineError(f"No loader available for file: {path}")

        loader = loader_cls()
        logger.info(f"Using loader: {loader_cls.__name__}")

        # --------------------------------------------------------------
        # 3. Load raw data (universal structure)
        # --------------------------------------------------------------
        try:
            raw_bundle: RawDataBundle = loader.load(path)
        except Exception as exc:
            raise PipelineError(f"Loader failed: {exc}") from exc

        logger.debug(f"Loaded raw data bundle: {raw_bundle}")

        # --------------------------------------------------------------
        # Inject technique from sniffer (single source of truth)
        # --------------------------------------------------------------
        raw_bundle.technique = fmt.technique

        # --------------------------------------------------------------
        # 4. Resolve processor
        # --------------------------------------------------------------
        processor_cls = get_processor_for_technique(fmt.technique)
        if processor_cls is None:
            raise PipelineError(f"No processor available for technique: {fmt.technique}")

        processor = processor_cls()
        logger.info(f"Using processor: {processor_cls.__name__}")

        # v2.2 rule: processors expose instance‑level config only
        if not hasattr(processor, "config"):
            raise PipelineError(
                f"Processor {processor_cls.__name__} does not define an instance‑level 'config'"
            )

        config = processor.config

        # --------------------------------------------------------------
        # 5. Processor pipeline (universal data flow)
        # --------------------------------------------------------------
        try:
            validated = processor.validate(raw_bundle.data, config)
            preprocessed = processor.preprocess(validated, config)
            processed = processor.process(preprocessed, config)
            postprocessed = processor.postprocess(processed, config)
        except Exception as exc:
            raise PipelineError(f"Processor failed: {exc}") from exc

        # --------------------------------------------------------------
        # 6. Metadata + QC
        # --------------------------------------------------------------
        try:
            metadata = processor.build_metadata(postprocessed, config)
            qc = processor.compute_qc(postprocessed, config)
        except Exception as exc:
            raise PipelineError(f"Metadata/QC computation failed: {exc}") from exc

        # --------------------------------------------------------------
        # 7. Plot generation
        # --------------------------------------------------------------
        try:
            plot_payload = postprocessed.get("plots", [])
            plots = self.plotting_service.render(plot_payload)
        except Exception as exc:
            raise PipelineError(f"Plotting failed: {exc}") from exc

        logger.info(f"Generated {len(plots)} plots")

        # --------------------------------------------------------------
        # 8. Assemble result
        # --------------------------------------------------------------
        result = PipelineResult(
            raw=raw_bundle,
            processed=postprocessed,
            metadata=metadata,
            qc=qc,
            plots=plots,
        )

        logger.info("Pipeline completed successfully")
        return result


# ======================================================================
# Singleton instance
# ======================================================================

pipeline = Pipeline()


# ======================================================================
# Backwards‑compatible functional entrypoint
# ======================================================================

def run_pipeline(path: str | Path) -> PipelineResult:
    """
    Backwards‑compatible wrapper for tests, notebooks, and legacy code.
    """
    return pipeline.run(path)
