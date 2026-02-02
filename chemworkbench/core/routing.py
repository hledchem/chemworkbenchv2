"""
ChemWorkBench v2.2 — Processor Router
=====================================

Purpose
-------
The ProcessorRouter maps a detected scientific technique to the correct
processor class. It is the bridge between the ingestion engine and the
technique‑specific processing pipelines.

Design Principles (v2.2)
------------------------
• Technique detection is fully decoupled from processing.
• Processors are registered by technique, not by format or vendor.
• Router is deterministic, explicit, and LLM‑friendly.
• Plugins may register new processors or override existing ones.
• Router supports future multi‑stage and multi‑technique pipelines.

Future‑Proofing Notes
---------------------
This router is designed for:
• AI‑generated processors
• Plugin ecosystems
• Multi‑technique files (future extension)
• Batch processing
• Cloud processing services

Public API
----------
- ProcessorRouter.register(technique, processor_cls)
- ProcessorRouter.register_plugin(technique, processor_cls)
- ProcessorRouter.resolve(technique) → Processor instance
"""

from __future__ import annotations

from typing import Dict, Type

from chemworkbench.core.models import Technique
from chemworkbench.processors.base_processor import BaseProcessor

# Import built‑in processors
from chemworkbench.processors.uvvis.processor import UVVisProcessor


# ======================================================================
# Processor Router
# ======================================================================

class ProcessorRouter:
    """
    Canonical v2.2 processor router.

    Responsibilities
    ----------------
    • Map Technique → ProcessorClass
    • Instantiate processors on demand
    • Support plugin overrides
    • Provide introspection for LLMs and developer tools

    Non‑Responsibilities
    --------------------
    • Technique detection (handled by TechniqueEngine)
    • Loader logic (handled by LoaderRegistry)
    • Structural format detection (handled by FormatDetector)
    """

    def __init__(self) -> None:
        self._processors: Dict[Technique, Type[BaseProcessor]] = {}
        self._plugins: Dict[Technique, Type[BaseProcessor]] = {}
        self._register_builtin_processors()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, technique: Technique, processor_cls: Type[BaseProcessor]) -> None:
        """Register a built‑in processor class."""
        self._processors[technique] = processor_cls

    def register_plugin(self, technique: Technique, processor_cls: Type[BaseProcessor]) -> None:
        """Register a plugin‑provided processor class."""
        self._plugins[technique] = processor_cls

    # ------------------------------------------------------------------
    # Built‑in processors
    # ------------------------------------------------------------------

    def _register_builtin_processors(self) -> None:
        """Register all built‑in processors for v2.2."""
        self.register(Technique.UVVIS, UVVisProcessor)

        # Future processors (IR, Raman, NMR, MS, etc.) will be added here.

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def resolve(self, technique: Technique) -> BaseProcessor:
        """
        Resolve and instantiate the correct processor for a given technique.

        Plugin processors override built‑ins.
        """

        # Plugin override
        if technique in self._plugins:
            return self._plugins[technique]()

        # Built‑in processor
        if technique in self._processors:
            return self._processors[technique]()

        # Fallback: return a no‑op processor
        return BaseProcessor()

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def describe(self) -> dict:
        """Return a structured description for debugging or LLM reasoning."""
        return {
            "builtin_processors": [t.value for t in self._processors.keys()],
            "plugin_processors": [t.value for t in self._plugins.keys()],
            "supports_plugins": True,
        }
    
