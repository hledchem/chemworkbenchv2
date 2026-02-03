"""
ChemWorkBench v2.2 — Ingestion Engine
=====================================

Purpose
-------
The ingestion engine is the central orchestrator of the v2.2 data pipeline.
It coordinates:

    1. Structural format detection (FormatDetectionEngine)
    2. Format resolution (FormatRegistry)
    3. Loader resolution (LoaderRegistry)
    4. Data loading (Loader → universal structure)
    5. Universal → RawDataBundle conversion
    6. Technique inference (TechniqueEngine)
    7. Optional processing (ProcessorRouter)
    8. PipelineResult assembly

This module is intentionally simple, explicit, and LLM-friendly. It is the
single entry point for turning a file path into a fully processed
PipelineResult.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Any

from chemworkbench.core.models import (
    RawDataBundle,
    PipelineResult,
    Technique,
    Scan,
)
from chemworkbench.core.format_registry import FormatRegistry
from chemworkbench.core.loader_registry import LoaderRegistry
from chemworkbench.core.technique_detection_engine import TechniqueEngine
from chemworkbench.core.routing import ProcessorRouter

from chemworkbench.utils.file_sniffer.format_detection_engine import (
    FormatDetectionEngine,
)


# ======================================================================
# Ingestion Engine
# ======================================================================

class IngestionEngine:
    """
    Canonical v2.2 ingestion orchestrator.
    """

    def __init__(
        self,
        format_registry: FormatRegistry,
        loader_registry: LoaderRegistry,
        technique_engine: TechniqueEngine,
        processor_router: ProcessorRouter,
        detector: Optional[FormatDetectionEngine] = None,
    ) -> None:
        self.format_registry = format_registry
        self.loader_registry = loader_registry
        self.technique_engine = technique_engine
        self.processor_router = processor_router
        self.detector = detector or FormatDetectionEngine()

    # ------------------------------------------------------------------
    # Universal → RawDataBundle conversion
    # ------------------------------------------------------------------

    def _to_rawdatabundle(self, universal: Any, detected) -> RawDataBundle:
        """
        Convert universal loader output into a RawDataBundle.
        Supported universal structures:
        • {"x": [...], "y": [...], "label": ...}
        • list-of-dicts
        • {"tabular": [...], "scans": [...], "metadata": {...}}   ← v2.2
        """

        # --------------------------------------------------------------
        # Case 1 — Legacy spectral universal structure
        # --------------------------------------------------------------
        if isinstance(universal, dict) and "x" in universal and "y" in universal:
            scan = Scan(
                x=universal["x"],
                y=universal["y"],
                label=universal.get("label", "Scan"),
            )
            return RawDataBundle(
                scans=[scan],
                technique=Technique.UNKNOWN,
            )

        # --------------------------------------------------------------
        # Case 2 — Legacy tabular universal structure
        # --------------------------------------------------------------
        if isinstance(universal, list) and universal and isinstance(universal[0], dict):
            return RawDataBundle(
                scans=[],
                technique=Technique.UNKNOWN,
                tabular=universal,
            )

        # --------------------------------------------------------------
        # Case 3 — v2.2 universal structure (tabular + scans + metadata)
        # --------------------------------------------------------------
        if (
            isinstance(universal, dict)
            and "scans" in universal
            and "tabular" in universal
        ):
            scans = universal.get("scans", [])
            tabular = universal.get("tabular", [])
            metadata = universal.get("metadata", {})

            return RawDataBundle(
                scans=scans,
                tabular=tabular,
                metadata=metadata,
                technique=Technique.UNKNOWN,
            )

        # --------------------------------------------------------------
        # Unsupported structure
        # --------------------------------------------------------------
        raise ValueError(
            f"Unsupported universal structure for RawDataBundle: {type(universal)}"
        )

    # ------------------------------------------------------------------
    # Main API
    # ------------------------------------------------------------------

    def ingest(self, path: Path) -> PipelineResult:
        """
        Ingest a file and return a fully assembled PipelineResult.
        """

        detected = self.detector.detect(path)

        fmt_desc = self.format_registry.get(detected.format_id)
        loader_cls = self.loader_registry.get(fmt_desc.loader_key)
        loader = loader_cls()

        raw_data = loader.load_raw(path)
        metadata = loader.extract_metadata(raw_data)
        universal = loader.to_universal(raw_data, metadata)

        raw = self._to_rawdatabundle(universal, detected)
        raw.source_path = str(path)

        tech_result = self.technique_engine.detect(raw, detected)
        raw.technique = tech_result.technique

        processor = self.processor_router.resolve(raw.technique)
        processed = processor.process(raw)

        return PipelineResult(
            raw=raw,
            processed=processed.payload,
            metadata=processed.metadata,
            qc=processed.qc,
            plots=processed.plots,
        )

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def describe(self) -> dict:
        return {
            "format_registry_size": len(self.format_registry),
            "loader_registry_size": len(self.loader_registry),
            "detector": self.detector.__class__.__name__,
            "technique_engine": self.technique_engine.__class__.__name__,
            "processor_router": self.processor_router.__class__.__name__,
        }
