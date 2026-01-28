"""
api/run_processing.py

ChemWorkBench v2.2 — Processing API Layer
-----------------------------------------

This module provides stable, high-level entrypoints for:
    - CLI commands
    - HTTP API endpoints
    - UI integrations
    - Notebook workflows

Design goals (v2.2):
- Thin wrapper around the pipeline and processing service
- No scientific logic
- No loader or processor selection logic
- Clean error boundaries (PipelineError)
- JSON‑friendly return structures for UI/HTTP layers

Responsibilities:
- Validate inputs
- Delegate to pipeline or processing service
- Normalize exceptions into PipelineError
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from chemworkbench.core.pipeline import pipeline
from chemworkbench.services.file_service import file_service
from chemworkbench.services.processing_service import ProcessingService
from chemworkbench.core.models import RawDataBundle, PipelineResult
from chemworkbench.runtime.errors import PipelineError
from chemworkbench.runtime.logging import get_logger


logger = get_logger(__name__)

processing_service = ProcessingService()


# ======================================================================
# Public API
# ======================================================================

def run_processing_from_file(path: str | Path) -> PipelineResult:
    """
    Run the full v2.2 ingestion pipeline on a file path.

    Equivalent to:
        pipeline.run(path)

    Returns:
        PipelineResult
    """
    try:
        normalized = file_service.ensure_exists(path)
        logger.info(f"API: Running full pipeline on file: {normalized}")
        return pipeline.run(normalized)
    except Exception as exc:
        raise PipelineError(f"API processing failed: {exc}") from exc


def run_processing_from_raw(raw: RawDataBundle) -> Dict[str, Any]:
    """
    Run processing on an already-loaded RawDataBundle.

    Useful for:
        - UI workflows
        - Notebook experiments
        - Custom loaders
        - Plugin integrations

    Returns a JSON‑serializable dict containing:
        - technique
        - processed metadata
        - number of plots
    """
    if not isinstance(raw, RawDataBundle):
        raise PipelineError("run_processing_from_raw expected a RawDataBundle")

    logger.info(f"API: Running processing on RawDataBundle ({raw.technique})")

    try:
        processed = processing_service.run(raw)
    except Exception as exc:
        raise PipelineError(f"Processing failed: {exc}") from exc

    return {
        "technique": processed.technique.name,
        "metadata": processed.metadata,
        "num_plots": len(processed.plots),
    }
