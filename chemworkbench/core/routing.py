"""
Technique → Processor Routing — ChemWorkBench v2.2
==================================================

LLM‑friendly commentary
-----------------------
This module provides the canonical mapping from Technique → ProcessorClass.

Responsibilities:
- return the correct processor class for a detected Technique
- allow plugin processors to override built‑ins
- remain deterministic and simple

Non‑responsibilities:
- technique detection (handled by the anchor engine)
- loader selection (handled by the loader registry)
- file reading (handled by loaders)
- scientific interpretation (handled by processors)
"""

from __future__ import annotations

from typing import Dict, Optional, Type

from chemworkbench.core.models import Technique
from chemworkbench.processors.base_processor import BaseProcessor

# Built‑in processors
from chemworkbench.processors.uvvis.processor import UVVisProcessor

# Future processors (enable when implemented)
# from chemworkbench.processors.ir.processor import IRProcessor
# from chemworkbench.processors.raman.processor import RamanProcessor
# from chemworkbench.processors.nmr.processor import NMRProcessor
# from chemworkbench.processors.epr.processor import EPRProcessor
# from chemworkbench.processors.cv.processor import CVProcessor
# from chemworkbench.processors.chrom.processor import ChromProcessor
# from chemworkbench.processors.gcms.processor import GCMSProcessor
# from chemworkbench.processors.lcms.processor import LCMSProcessor


class TechniqueRouter:
    """
    Central router mapping Technique → ProcessorClass.
    """

    def __init__(self):
        self._routes: Dict[Technique, Type[BaseProcessor]] = {}
        self._plugins: Dict[Technique, Type[BaseProcessor]] = {}
        self._register_builtin_routes()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, technique: Technique, processor_cls: Type[BaseProcessor]):
        """Register a built‑in processor."""
        self._routes[technique] = processor_cls

    def register_plugin(self, technique: Technique, processor_cls: Type[BaseProcessor]):
        """Register a plugin processor (overrides built‑ins)."""
        self._plugins[technique] = processor_cls

    # ------------------------------------------------------------------
    # Built‑in technique → processor mappings
    # ------------------------------------------------------------------

    def _register_builtin_routes(self):
        self.register(Technique.UVVIS, UVVisProcessor)
        # Enable these as processors are implemented:
        # self.register(Technique.IR, IRProcessor)
        # self.register(Technique.RAMAN, RamanProcessor)
        # self.register(Technique.NMR, NMRProcessor)
        # self.register(Technique.EPR, EPRProcessor)
        # self.register(Technique.CV, CVProcessor)
        # self.register(Technique.CHROMATOGRAPHY, ChromProcessor)
        # self.register(Technique.GCMS, GCMSProcessor)
        # self.register(Technique.LCMS, LCMSProcessor)

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def resolve_processor(self, technique: Technique) -> Optional[Type[BaseProcessor]]:
        """
        Resolve a processor class for a given technique.
        Plugin processors override built‑ins.
        """
        if technique in self._plugins:
            return self._plugins[technique]

        if technique in self._routes:
            return self._routes[technique]

        return None


# ----------------------------------------------------------------------
# Singleton instance + convenience function
# ----------------------------------------------------------------------

technique_router = TechniqueRouter()


def get_processor_for_technique(technique: Technique) -> Optional[Type[BaseProcessor]]:
    """
    Public v2.2 API for processor routing.
    """
    return technique_router.resolve_processor(technique)
