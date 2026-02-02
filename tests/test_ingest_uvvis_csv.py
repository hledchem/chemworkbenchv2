import pytest
from pathlib import Path

from chemworkbench.core.ingestion_engine import IngestionEngine
from chemworkbench.core.format_registry import FormatRegistry
from chemworkbench.core.loader_registry import LoaderRegistry
from chemworkbench.core.technique_detection_engine import TechniqueEngine
from chemworkbench.core.routing import ProcessorRouter
from chemworkbench.core.models import RawDataBundle, Technique

from chemworkbench.core.format_registry_init import register_builtin_formats
from chemworkbench.core.loader_registry_init import register_builtin_loaders


def test_ingest_uvvis_synthetic_csv():
    """
    End‑to‑end ingestion test for a UV‑Vis synthetic CSV file.
    Validates:
        • format detection
        • loader resolution
        • universal → RawDataBundle conversion
        • technique detection
        • processor routing
        • PipelineResult assembly
    """

    # --------------------------------------------------------------
    # Build ingestion engine
    # --------------------------------------------------------------
    format_registry = FormatRegistry()
    loader_registry = LoaderRegistry()
    tech_engine = TechniqueEngine()
    router = ProcessorRouter()

    register_builtin_formats(format_registry)
    register_builtin_loaders(loader_registry)

    engine = IngestionEngine(
        format_registry=format_registry,
        loader_registry=loader_registry,
        technique_engine=tech_engine,
        processor_router=router,
    )

    # --------------------------------------------------------------
    # Ingest the synthetic UV‑Vis CSV
    # --------------------------------------------------------------
    csv_path = Path("tests/synthetic_data/uvvis_synthetic_500nm.csv")
    result = engine.ingest(csv_path)

    # --------------------------------------------------------------
    # Assertions
    # --------------------------------------------------------------

    # RawDataBundle exists
    assert isinstance(result.raw, RawDataBundle)

    # Should contain at least one scan for UV‑Vis
    assert len(result.raw.scans) == 1

    # Technique should be UV‑Vis
    assert result.raw.technique == Technique.UVVIS

    # Processed payload should exist
    assert result.processed is not None

    # Metadata and QC should exist
    assert result.metadata is not None
    assert result.qc is not None

    # Plots should be present (block pipeline)
    assert isinstance(result.plots, dict)
