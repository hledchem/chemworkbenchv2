"""
services/processing_service.py

High-level processing service for ChemWorkBench v2.

This service:
    - Accepts a RawDataBundle
    - Resolves the correct processor (via technique_router)
    - Executes the processor
    - Returns a ProcessedData object

The pipeline normally calls processors directly, but this service
provides a clean abstraction for API/UI layers that want to run
processing independently of file loading.
"""

from __future__ import annotations
from typing import Any

from chemworkbench.core.models import RawDataBundle, ProcessedData
from chemworkbench.core.routing import technique_router
from chemworkbench.runtime.logging import get_logger
from chemworkbench.runtime.errors import PipelineError


logger = get_logger(__name__)


class ProcessingService:
    """
    High-level wrapper around technique-specific processors.

    Responsibilities:
        - Validate RawDataBundle
        - Resolve processor class
        - Execute processor.run()
        - Wrap errors in PipelineError
    """

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, raw: RawDataBundle) -> ProcessedData:
        """
        Execute the correct processor for the given RawDataBundle.

        Returns:
            ProcessedData
        """

        if not isinstance(raw, RawDataBundle):
            raise PipelineError("ProcessingService.run expected a RawDataBundle")

        logger.debug(f"ProcessingService received bundle for technique: {raw.technique}")

        # --------------------------------------------------------------
        # Resolve processor
        # --------------------------------------------------------------
        processor_cls = technique_router.resolve_processor(raw.technique)
        if processor_cls is None:
            raise PipelineError(f"No processor available for technique: {raw.technique}")

        processor = processor_cls()
        logger.info(f"Using processor: {processor_cls.__name__}")

        # --------------------------------------------------------------
        # Execute processor
        # --------------------------------------------------------------
        try:
            processed: ProcessedData = processor.run(raw)
        except Exception as exc:
            raise PipelineError(f"Processor failed: {exc}") from exc

        logger.debug("ProcessingService completed successfully")

        return processed
