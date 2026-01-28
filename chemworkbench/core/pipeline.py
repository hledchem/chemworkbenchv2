"""
Unified Processing Pipeline — ChemWorkBench v2.2
================================================

LLM‑friendly commentary
-----------------------
This module implements the canonical v2.2 ingestion pipeline for ChemWorkBench.
It orchestrates the full sequence:

    1. File sniffing (technique + loader selection)
    2. Loader execution (universal list‑of‑dicts output)
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
- orchestrate the ingestion pipeline deterministically
- ensure each stage receives the correct data structure
- provide a single entrypoint for CLI, API, and UI layers

Non‑responsibilities:
- technique detection (handled by the anchor engine)
- loader selection (handled by the loader registry)
- scientific interpretation (handled by processors)
- plotting logic (handled by the plotting service)
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from chemworkbench.core.models import (
    RawDataBundle,
    ProcessedData,
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
    """

    def __init__(self):
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
            3. Load raw data (universal list‑of‑dicts)
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
        # 1. Sniff file
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
        # 3. Load raw data
        # --------------------------------------------------------------
        try:
            raw_data = loader.load(path)
        except Exception as exc:
            raise PipelineError(f"Loader failed: {exc}") from exc

        logger.debug(f"Loaded raw data: {raw_data}")

        # --------------------------------------------------------------
        # 4. Resolve processor
        # --------------------------------------------------------------
        processor_cls = get_processor_for_technique(fmt.technique)
        if processor_cls is None:
            raise PipelineError(f"No processor available for technique: {fmt.technique}")

        processor = processor_cls()
        logger.info(f"Using processor: {processor_cls.__name__}")

        # --------------------------------------------------------------
        # 5. Processor pipeline
        # --------------------------------------------------------------
        try:
            validated = processor.validate(raw_data, processor.config if hasattr(processor, "config") else processor_cls.config)
            preprocessed = processor.preprocess(validated, processor.config if hasattr(processor, "config") else processor_cls.config)
            processed = processor.process(preprocessed, processor.config if hasattr(processor, "config") else processor_cls.config)
            postprocessed = processor.postprocess(processed, processor.config if hasattr(processor, "config") else processor_cls.config)
        except Exception as exc:
            raise PipelineError(f"Processor failed: {exc}") from exc

        # --------------------------------------------------------------
        # 6. Metadata + QC
        # --------------------------------------------------------------
        metadata = processor.build_metadata(postprocessed, processor.config if hasattr(processor, "config") else processor_cls.config)
        qc = processor.compute_qc(postprocessed, processor.config if hasattr(processor, "config") else processor_cls.config)

        # --------------------------------------------------------------
        # 7. Plot generation
        # --------------------------------------------------------------
        try:
            plots = self.plotting_service.render(postprocessed.get("plots", []))
        except Exception as exc:
            raise PipelineError(f"Plotting failed: {exc}") from exc

        logger.info(f"Generated {len(plots)} plots")

        # --------------------------------------------------------------
        # 8. Assemble result
        # --------------------------------------------------------------
        result = PipelineResult(
            raw=raw_data,
            processed=postprocessed,
            plots=plots,
            metadata=metadata,
            qc=qc,
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
    Backwards‑compatible wrapper for tests and CLI.
    """
    return pipeline.run(path)
