# utils/loaders/loader_registry.py

from __future__ import annotations

from typing import Dict, Tuple, Type

from .base_loader import BaseVendorLoader

# -------------------------
# Import all loaders
# -------------------------

# Agilent
from .agilent.agilent_chrom_loader import AgilentChromLoader
from .agilent.agilent_d_uvvis_loader import AgilentDUVVisLoader
from .agilent.agilent_ir_loader import AgilentIRLoader
from .agilent.agilent_ms_loader import AgilentMSLoader
from .agilent.agilent_uv_loader import AgilentUVLoader

# Bruker
from .bruker.bruker_nmr_loader import BrukerNMRLoader
from .bruker.bruker_opus_loader import BrukerOPUSLoader
from .bruker.bruker_epr_loader import BrukerEPRLoader

# CH Instruments
from .ch_instruments.chi_dta_loader import CHIDTALoader

# Horiba
from .horiba.horiba_fluor_loader import HoribaFluorescenceLoader

# JEOL
from .jeol.jeol_jdf_loader import JEOLJDFLoader

# PerkinElmer
from .perkinelmer.perkinelmer_sp_loader import PerkinElmerSPLoader
from .perkinelmer.perkinelmer_spc_loader import PerkinElmerSPCLoader

# Raman
from .raman.dpt_loader import DPTLoader
from .raman.rruf_loader import RRUFFLoader
from .raman.rruf_gz_loader import RRUFFGZLoader

# Shimadzu
from .shimadzu.shimadzu_irx_loader import ShimadzuIRXLoader
from .shimadzu.shimadzu_lcd_loader import ShimadzuLCDLoader
from .shimadzu.shimadzu_spc_loader import ShimadzuSPCLoader
from .shimadzu.shimadzu_uvs_loader import ShimadzuUVSLoader

# Thermo
from .thermo.thermo_spa_loader import ThermoSPALoader
from .thermo.thermo_spc_loader import ThermoSPCLoader
from .thermo.thermo_srs_loader import ThermoSRSLoader

# Varian
from .varian.varian_nmr_loader import VarianNMRLoader

# Waters
from .waters.waters_raw_loader import WatersRAWLoader

# Universal
from .csv_loader import CSVLoader
from .jcamp_loader import JCAMPLoader
from .xlsx_loader import XLSXLoader


# ---------------------------------------------------------
# Canonical registry: (vendor, format) → loader class
# ---------------------------------------------------------

LOADER_REGISTRY: Dict[Tuple[str, str], Type[BaseVendorLoader]] = {
    # -------------------------
    # Agilent
    # -------------------------
    ("agilent", "chrom"): AgilentChromLoader,
    ("agilent", "d_uvvis"): AgilentDUVVisLoader,
    ("agilent", "ir"): AgilentIRLoader,
    ("agilent", "ms"): AgilentMSLoader,
    ("agilent", "uv"): AgilentUVLoader,

    # -------------------------
    # Bruker
    # -------------------------
    ("bruker", "epr"): BrukerEPRLoader,
    ("bruker", "nmr"): BrukerNMRLoader,
    ("bruker", "opus"): BrukerOPUSLoader,

    # -------------------------
    # CH Instruments
    # -------------------------
    ("ch_instruments", "dta"): CHIDTALoader,

    # -------------------------
    # Horiba
    # -------------------------
    ("horiba", "fluor"): HoribaFluorescenceLoader,

    # -------------------------
    # JEOL
    # -------------------------
    ("jeol", "jdf"): JEOLJDFLoader,

    # -------------------------
    # PerkinElmer
    # -------------------------
    ("perkinelmer", "sp"): PerkinElmerSPLoader,
    ("perkinelmer", "spc"): PerkinElmerSPCLoader,

    # -------------------------
    # Raman
    # -------------------------
    ("raman", "dpt"): DPTLoader,
    ("raman", "rruf"): RRUFFLoader,
    ("raman", "rruf_gz"): RRUFFGZLoader,

    # -------------------------
    # Shimadzu
    # -------------------------
    ("shimadzu", "irx"): ShimadzuIRXLoader,
    ("shimadzu", "lcd"): ShimadzuLCDLoader,
    ("shimadzu", "spc"): ShimadzuSPCLoader,
    ("shimadzu", "uvs"): ShimadzuUVSLoader,

    # -------------------------
    # Thermo
    # -------------------------
    ("thermo", "spa"): ThermoSPALoader,
    ("thermo", "spc"): ThermoSPCLoader,
    ("thermo", "srs"): ThermoSRSLoader,

    # -------------------------
    # Varian
    # -------------------------
    ("varian", "nmr"): VarianNMRLoader,

    # -------------------------
    # Waters
    # -------------------------
    ("waters", "raw"): WatersRAWLoader,

    # -------------------------
    # Universal
    # -------------------------
    ("universal", "csv"): CSVLoader,
    ("universal", "jcamp"): JCAMPLoader,
    ("universal", "xlsx"): XLSXLoader,
}


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def get_loader(vendor: str, fmt: str) -> Type[BaseVendorLoader]:
    key = (vendor.lower(), fmt.lower())
    if key not in LOADER_REGISTRY:
        raise KeyError(f"No loader registered for vendor='{vendor}', format='{fmt}'")
    return LOADER_REGISTRY[key]


def all_loaders() -> Dict[Tuple[str, str], Type[BaseVendorLoader]]:
    return dict(LOADER_REGISTRY)


def iter_loaders():
    for cls in LOADER_REGISTRY.values():
        yield cls()
