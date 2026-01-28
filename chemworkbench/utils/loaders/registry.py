"""
Loader Registry — ChemWorkBench v2.2
====================================

LLM‑friendly commentary
-----------------------
This module provides the canonical registry of all loader classes.

In v2.2, loader selection is *format‑based*, not technique‑based.
Loaders are responsible only for reading file formats, not detecting
technique or vendor.

Public API:
- iter_loader_classes()
- select_loader_for_path(path)
"""

from __future__ import annotations

from typing import Dict, Tuple, Type, List, Optional
from pathlib import Path

from .base_loader import BaseVendorLoader

# ---------------------------------------------------------
# Import all loaders
# ---------------------------------------------------------

# Agilent
from .agilent.agilent_d_chrom_loader import AgilentDChromLoader
from .agilent.agilent_d_ms_loader import AgilentDMSLoader
from .agilent.agilent_d_uvvis_loader import AgilentDUVVisLoader
from .agilent.agilent_sp_loader import AgilentSPLoader
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
from .perkinelmer.perkinelmer_spc_loader import PerkinelmerSPCLoader

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
# Canonical list of loader classes
# ---------------------------------------------------------

LOADER_CLASSES: List[Type[BaseVendorLoader]] = [
    # Agilent
    AgilentDChromLoader,
    AgilentDMSLoader,
    AgilentDUVVisLoader,
    AgilentSPLoader,
    AgilentUVLoader,

    # Bruker
    BrukerNMRLoader,
    BrukerOPUSLoader,
    BrukerEPRLoader,

    # CH Instruments
    CHIDTALoader,

    # Horiba
    HoribaFluorescenceLoader,

    # JEOL
    JEOLJDFLoader,

    # PerkinElmer
    PerkinElmerSPLoader,
    PerkinelmerSPCLoader,

    # Raman
    DPTLoader,
    RRUFFLoader,
    RRUFFGZLoader,

    # Shimadzu
    ShimadzuIRXLoader,
    ShimadzuLCDLoader,
    ShimadzuSPCLoader,
    ShimadzuUVSLoader,

    # Thermo
    ThermoSPALoader,
    ThermoSPCLoader,
    ThermoSRSLoader,

    # Varian
    VarianNMRLoader,

    # Waters
    WatersRAWLoader,

    # Universal
    CSVLoader,
    JCAMPLoader,
    XLSXLoader,
]


# ---------------------------------------------------------
# Public API
# ---------------------------------------------------------

def iter_loader_classes():
    """Yield all loader classes."""
    for cls in LOADER_CLASSES:
        yield cls


def select_loader_for_path(path: str | Path) -> Optional[Type[BaseVendorLoader]]:
    """
    Return the first loader class whose sniff() method claims the file.
    """
    path = Path(path)

    for cls in LOADER_CLASSES:
        try:
            if cls().sniff(path):
                return cls
        except Exception:
            continue  # Loaders must never break detection

    return None
