"""
core/registry.py

Unified loader registry for ChemWorkBench v2.

This registry maps:
    DetectedFormat → LoaderClass

It supports:
- universal loaders (CSV, JCAMP, XLSX, etc.)
- vendor-specific loaders (Agilent, Bruker, Horiba, etc.)
- plugin loaders
- technique-aware resolution
"""

from __future__ import annotations
from typing import Dict, Type, Optional

from chemworkbench.core.models import DetectedFormat, Technique

# Universal loaders
from chemworkbench.utils.loaders.csv_loader import CSVLoader
from chemworkbench.utils.loaders.xlsx_loader import XLSXLoader
from chemworkbench.utils.loaders.jcamp_loader import JCAMPLoader

# Vendor loaders
from chemworkbench.utils.loaders.agilent.agilent_uv_loader import AgilentUVLoader
from chemworkbench.utils.loaders.agilent.agilent_sp_loader import AgilentSPLoader
from chemworkbench.utils.loaders.agilent.agilent_d_uvvis_loader import AgilentDUVVisLoader
from chemworkbench.utils.loaders.agilent.agilent_d_chrom_loader import AgilentDChromLoader
from chemworkbench.utils.loaders.agilent.agilent_d_ms_loader import AgilentDMSLoader

from chemworkbench.utils.loaders.bruker.bruker_opus_loader import BrukerOPUSLoader
from chemworkbench.utils.loaders.bruker.bruker_nmr_loader import BrukerNMRLoader
from chemworkbench.utils.loaders.bruker.bruker_epr_loader import BrukerEPRLoader

from chemworkbench.utils.loaders.thermo.thermo_spa_loader import ThermoSPALoader
from chemworkbench.utils.loaders.thermo.thermo_spc_loader import ThermoSPCLoader
from chemworkbench.utils.loaders.thermo.thermo_srs_loader import ThermoSRSLoader

from chemworkbench.utils.loaders.shimadzu.shimadzu_spc_loader import ShimadzuSPCLoader
from chemworkbench.utils.loaders.shimadzu.shimadzu_irx_loader import ShimadzuIRXLoader
from chemworkbench.utils.loaders.shimadzu.shimadzu_uvs_loader import ShimadzuUVSLoader
from chemworkbench.utils.loaders.shimadzu.shimadzu_lcd_loader import ShimadzuLCDLoader

from chemworkbench.utils.loaders.perkinelmer.perkinelmer_sp_loader import PerkinElmerSPLoader
from chemworkbench.utils.loaders.perkinelmer.perkinelmer_spc_loader import PerkinElmerSPCLoader

from chemworkbench.utils.loaders.waters.waters_raw_loader import WatersRAWLoader

from chemworkbench.utils.loaders.jeol.jeol_jdf_loader import JEOLJDFLoader
from chemworkbench.utils.loaders.varian.varian_nmr_loader import VarianNMRLoader

# Raman loaders
from chemworkbench.utils.loaders.raman.dpt_loader import DPTLoader
from chemworkbench.utils.loaders.raman.rruf_loader import RRUfLoader
from chemworkbench.utils.loaders.raman.rruf_gz_loader import RRUfGZLoader

# Horiba fluorescence
from chemworkbench.utils.loaders.horiba.horiba_fluor_loader import HoribaFluorLoader

# CH Instruments electrochemistry
from chemworkbench.utils.loaders.ch_instruments.chi_dta_loader import CHIDTALoader


# ----------------------------------------------------------------------
# Loader Registry
# ----------------------------------------------------------------------

class LoaderRegistry:
    """
    Central registry for all loaders.
    Maps (vendor, technique, subtype) → LoaderClass
    """

    def __init__(self):
        self._registry: Dict[str, Type] = {}
        self._plugins: Dict[str, Type] = {}

        self._register_builtin_loaders()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, key: str, loader_cls: Type):
        """Register a loader class under a canonical key."""
        self._registry[key] = loader_cls

    def register_plugin(self, key: str, loader_cls: Type):
        """Register a plugin loader."""
        self._plugins[key] = loader_cls

    # ------------------------------------------------------------------
    # Built-in loader registration
    # ------------------------------------------------------------------

    def _register_builtin_loaders(self):
        # Universal
        self.register("csv", CSVLoader)
        self.register("xlsx", XLSXLoader)
        self.register("jcamp_dx", JCAMPDXLoader)

        # Agilent
        self.register("agilent_uv", AgilentUVLoader)
        self.register("agilent_sp", AgilentSPLoader)
        self.register("agilent_d_uvvis", AgilentDUVVisLoader)
        self.register("agilent_d_chrom", AgilentDChromLoader)
        self.register("agilent_d_ms", AgilentDMSLoader)

        # Bruker
        self.register("bruker_opus", BrukerOpusLoader)
        self.register("bruker_nmr", BrukerNMRLoader)
        self.register("bruker_epr", BrukerEPRLoader)

        # Thermo
        self.register("thermo_spa", ThermoSPALoader)
        self.register("thermo_spc", ThermoSPCLoader)
        self.register("thermo_srs", ThermoSRSLoader)

        # Shimadzu
        self.register("shimadzu_spc", ShimadzuSPCLoader)
        self.register("shimadzu_irx", ShimadzuIRXLoader)
        self.register("shimadzu_uvs", ShimadzuUVSLoader)
        self.register("shimadzu_lcd", ShimadzuLCDLoader)

        # PerkinElmer
        self.register("perkinelmer_sp", PerkinElmerSPLoader)
        self.register("perkinelmer_spc", PerkinElmerSPCLoader)

        # Waters
        self.register("waters_raw", WatersRAWLoader)

        # JEOL
        self.register("jeol_jdf", JeolJDFLoader)

        # Varian
        self.register("varian_nmr", VarianNMRLoader)

        # Raman
        self.register("raman_dpt", DPTLoader)
        self.register("raman_rruf", RRUfLoader)
        self.register("raman_rruf_gz", RRUfGZLoader)

        # Horiba
        self.register("horiba_fluor", HoribaFluorLoader)

        # CH Instruments
        self.register("chi_dta", CHIDTALoader)

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def resolve_loader(self, fmt: DetectedFormat) -> Optional[Type]:
        """
        Resolve a loader class from a DetectedFormat.
        """

        # 1. Try vendor + subtype
        if fmt.vendor and fmt.subtype:
            key = f"{fmt.vendor.lower()}_{fmt.subtype.lower()}"
            if key in self._registry:
                return self._registry[key]

        # 2. Try vendor + technique
        if fmt.vendor:
            key = f"{fmt.vendor.lower()}_{fmt.technique.value}"
            if key in self._registry:
                return self._registry[key]

        # 3. Try technique-only loaders
        key = fmt.technique.value
        if key in self._registry:
            return self._registry[key]

        # 4. Try plugins
        for key, cls in self._plugins.items():
            if key.startswith(fmt.vendor or ""):
                return cls

        # 5. No match
        return None


# ----------------------------------------------------------------------
# Singleton instance
# ----------------------------------------------------------------------

loader_registry = LoaderRegistry()
