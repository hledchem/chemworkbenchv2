"""
core/pipeline.py

Unified processing pipeline for ChemWorkBench v2.

This orchestrates:
    1. File sniffing
    2. Loader resolution
    3. Vendor loader execution
    4. Technique routing
    5. Processor execution
    6. Plot generation
    7. PipelineResult assembly

This is the main entrypoint for all CLI, API, and UI workflows.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional

from chemworkbench.core.models import (
    RawDataBundle,
    ProcessedData,
    PipelineResult,
)
from chemworkbench.core.models import DetectedFormat

from chemworkbench.utils.file_sniffer.file_sniffer import sniff_file
from chemworkbench.core.registry import loader_registry
from chemworkbench.core.routing import technique_router

from chemworkbench.services.plotting_service import PlottingService
from chemworkbench.runtime.logging import get_logger
from chemworkbench.runtime.errors import PipelineError


logger = get_logger(__name__)


class Pipeline:
    """
    Main orchestrator for ChemWorkBench v2.
    """

    def __init__(self):
        self.plotting_service = PlottingService()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, path: str | Path) -> PipelineResult:
        """
        Execute the full pipeline on a file path.

        Steps:
            1. Sniff file → DetectedFormat
            2. Resolve loader
            3. Load raw data → RawDataBundle
            4. Resolve processor
            5. Process data → ProcessedData
            6. Generate plots
            7. Return PipelineResult
        """

        path = Path(path)

        if not path.exists():
            raise PipelineError(f"File not found: {path}")

        logger.info(f"Starting pipeline for: {path}")

        # --------------------------------------------------------------
        # 1. Sniff file
        # --------------------------------------------------------------
        fmt: DetectedFormat = sniff_file(str(path))
        logger.debug(f"Detected format: {fmt}")

        # --------------------------------------------------------------
        # 2. Resolve loader
        # --------------------------------------------------------------
        loader_cls = loader_registry.resolve_loader(fmt)
        if loader_cls is None:
            raise PipelineError(f"No loader found for detected format: {fmt}")

        loader = loader_cls()
        logger.info(f"Using loader: {loader_cls.__name__}")

        # --------------------------------------------------------------
        # 3. Load raw data
        # --------------------------------------------------------------
        try:
            raw: RawDataBundle = loader.load(path)
        except Exception as exc:
            raise PipelineError(f"Loader failed: {exc}") from exc

        logger.debug(f"Loaded raw data bundle: {raw}")

        # --------------------------------------------------------------
        # 4. Resolve processor
        # --------------------------------------------------------------
        processor_cls = technique_router.resolve_processor(raw.technique)
        if processor_cls is None:
            raise PipelineError(f"No processor available for technique: {raw.technique}")

        processor = processor_cls()
        logger.info(f"Using processor: {processor_cls.__name__}")

        # --------------------------------------------------------------
        # 5. Process data
        # --------------------------------------------------------------
        try:
            processed: ProcessedData = processor.run(raw)
        except Exception as exc:
            raise PipelineError(f"Processor failed: {exc}") from exc

        logger.debug(f"Processed data: {processed}")

        # --------------------------------------------------------------
        # 6. Generate plots
        # --------------------------------------------------------------
        try:
            plots = self.plotting_service.render(processed.plots)
        except Exception as exc:
            raise PipelineError(f"Plotting failed: {exc}") from exc

        logger.info(f"Generated {len(plots)} plots")

        # --------------------------------------------------------------
        # 7. Assemble result
        # --------------------------------------------------------------
        result = PipelineResult(
            raw=raw,
            processed=processed,
            plots=processed.plots,
        )

        logger.info("Pipeline completed successfully")
        return result


# ----------------------------------------------------------------------
# Singleton instance
# ----------------------------------------------------------------------

pipeline = Pipeline()

# ----------------------------------------------------------------------
# Backwards-compatible functional entrypoint for tests and CLI
# ----------------------------------------------------------------------

def run_pipeline(path: str | Path) -> PipelineResult:
    """
    Thin wrapper around the Pipeline singleton to maintain compatibility
    with tests and external callers expecting a module-level function.
    """
    return pipeline.run(path)

# ----------------------------------------------------------------------
# Test-only helper for example scripts
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Test-only helper for example scripts
# ----------------------------------------------------------------------

def run_pipeline(processor, config, data):
    """
    Compatibility helper for example tests.
    """

    # Instantiate config if a class was passed
    if isinstance(config, type):
        config = config()

    # Run processor with explicit config
    processed = processor.process(data, config)

    # Generate plots
    plots = processor.make_plots(processed)

    return PipelineResult(
        raw=data,
        processed=processed,
        plots=plots,
    )
