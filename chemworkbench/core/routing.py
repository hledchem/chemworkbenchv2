"""
core/routing.py

Technique → Processor routing for ChemWorkBench v2.

This module maps each analytical technique to the correct processor class.
The pipeline uses this router after the loader returns a RawDataBundle.
"""

from __future__ import annotations
from typing import Dict, Optional, Type

from chemworkbench.core.models import Technique

# Base processor
from chemworkbench.processors.base_processor import BaseProcessor

# Technique-specific processors
from chemworkbench.processors.uvvis.processor import UVVisProcessor

# Future processors (stubs or real implementations)
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
        """Register a processor for a technique."""
        self._routes[technique] = processor_cls

    def register_plugin(self, technique: Technique, processor_cls: Type[BaseProcessor]):
        """Register a plugin processor."""
        self._plugins[technique] = processor_cls

    # ------------------------------------------------------------------
    # Built-in technique → processor mappings
    # ------------------------------------------------------------------

    def _register_builtin_routes(self):
        # UV-Vis
        self.register(Technique.UVVIS, UVVisProcessor)

        # Future techniques (enable when implemented)
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
        """

        # 1. Built-in processors
        if technique in self._routes:
            return self._routes[technique]

        # 2. Plugin processors
        if technique in self._plugins:
            return self._plugins[technique]

        # 3. No processor available
        return None


# ----------------------------------------------------------------------
# Singleton instance
# ----------------------------------------------------------------------

technique_router = TechniqueRouter()
