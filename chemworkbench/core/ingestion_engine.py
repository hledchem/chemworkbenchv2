"""
ChemWorkBench v2.2 — Ingestion Engine
=====================================

Purpose
-------
The ingestion engine is the central orchestrator of the v2.2 data pipeline.
It coordinates:

    1. Structural format detection (FormatDetector)
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

Design Principles (v2.2)
------------------------
• Format detection, loading, technique detection, and processing are fully decoupled.
• Loader resolution is structural-family based, not technique-based.
• Technique detection is handled by the anchor engine, not loaders.
• Processing is optional and pluggable.
• The engine is deterministic and introspectable.
• Plugins may override any stage of the pipeline.

Future-Proofing Notes
---------------------
This engine is designed for:
• Multi-technique files (future extension)
• Multi-stage processing pipelines
• AI-driven loader/processor selection
• Plugin ecosystems
• Batch ingestion
• Cloud ingestion services

Public API
----------
- IngestionEngine.ingest(path: Path) → PipelineResult
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Any, Mapping

from chemworkbench.core.models import (
    RawDataBundle,
    PipelineResult,
    Technique,
    Scan,
)
from chemworkbench.core.format_registry import FormatRegistry
from chemworkbench.core.loader_registry import LoaderRegistry
    # loader.load_raw(), loader.extract_metadata(), loader.to_universal()
from chemworkbench.core.technique_detection_engine import TechniqueEngine
from chemworkbench.core.routing import ProcessorRouter
from chemworkbench.file_sniffer.format_detection_engine import FormatDetector


# ======================================================================
# Ingestion Engine
# ======================================================================

class IngestionEngine:
    """
    Canonical v2.2 ingestion orchestrator.

    Responsibilities
    ----------------
    • Detect structural format (FormatDetector)
    • Resolve loader (FormatRegistry + LoaderRegistry)
    • Load universal data (loader)
    • Convert universal → RawDataBundle
    • Infer technique (TechniqueEngine)
    • Route to processor (ProcessorRouter)
    • Produce PipelineResult

    Non-Responsibilities
    --------------------
    • File sniffing heuristics (handled by FormatDetector)
    • Loader logic (handled by loader classes)
    • Technique inference logic (handled by TechniqueEngine)
    • Processing logic (handled by processors)
    • Plotting logic (handled by plotting subsystem)
    """

    def __init__(
        self,
        format_registry: FormatRegistry,
        loader_registry: LoaderRegistry,
        technique_engine: TechniqueEngine,
        processor_router: ProcessorRouter,
        detector: Optional[FormatDetector] = None,
    ) -> None:
        self.format_registry = format_registry
        self.loader_registry = loader_registry
        self.technique_engine = technique_engine
        self.processor_router = processor_router
        self.detector = detector or FormatDetector()

    # ------------------------------------------------------------------
    # Universal → RawDataBundle conversion
    # ------------------------------------------------------------------

    def _to_rawdatabundle(self, universal: Any, detected) -> RawDataBundle:
        """
        Convert universal loader output into a RawDataBundle.
        This is the canonical v2.2 ingestion pivot point.

        Supported universal structures:
        • {"x": [...], "y": [...], "label": ...}  → spectral Scan
        • list-of-dicts → tabular RawDataBundle (CSV, multi-column)
        """

        # Case 1 — Spectral universal structure (UV‑Vis, IR, Raman, etc.)
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

        # Case 2 — Tabular universal structure (CSV, multi-column ASCII)
        if isinstance(universal, list) and universal and isinstance(universal[0], dict):
            return RawDataBundle(
                scans=[],
                technique=Technique.UNKNOWN,
                tabular=universal,
            )

        raise ValueError(
            f"Unsupported universal structure for RawDataBundle: {type(universal)}"
        )

    # ------------------------------------------------------------------
    # Main API
    # ------------------------------------------------------------------

    def ingest(self, path: Path) -> PipelineResult:
        """
        Ingest a file and return a fully assembled PipelineResult.

        Steps:
        1. Detect structural format
        2. Resolve loader
        3. Load universal data
        4. Convert universal → RawDataBundle
        5. Infer technique
        6. Route to processor
        7. Produce PipelineResult
        """

        # --------------------------------------------------------------
        # 1. Structural format detection
        # --------------------------------------------------------------
        detected = self.detector.detect(path)

        # --------------------------------------------------------------
        # 2. Resolve loader via FormatRegistry + LoaderRegistry
        # --------------------------------------------------------------
        fmt_desc = self.format_registry.get(detected.format_id)
        loader_cls = self.loader_registry.get(fmt_desc.loader_key)
        loader = loader_cls()

        # --------------------------------------------------------------
        # 3. Load universal data
        # --------------------------------------------------------------
        raw_data = loader.load_raw(path)
        metadata = loader.extract_metadata(raw_data)
        universal = loader.to_universal(raw_data, metadata)

        # --------------------------------------------------------------
        # 4. Convert universal → RawDataBundle
        # --------------------------------------------------------------
        raw = self._to_rawdatabundle(universal, detected)

        # --------------------------------------------------------------
        # 5. Technique inference (anchor engine)
        # --------------------------------------------------------------
        tech_result = self.technique_engine.detect(raw, detected)
        raw.technique = tech_result.technique

        # --------------------------------------------------------------
        # 6. Route to processor (optional)
        # --------------------------------------------------------------
        processor = self.processor_router.resolve(raw.technique)
        processed = processor.process(raw)

        # --------------------------------------------------------------
        # 7. Assemble PipelineResult
        # --------------------------------------------------------------
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
        """
        Return a structured description of the ingestion engine for
        debugging, UI, or LLM reasoning.
        """
        return {
            "format_registry_size": len(self.format_registry),
            "loader_registry_size": len(self.loader_registry),
            "detector": self.detector.__class__.__name__,
            "technique_engine": self.technique_engine.__class__.__name__,
            "processor_router": self.processor_router.__class__.__name__,
        }
