"""
format_registry.py — ChemWorkBench v2.2
=======================================

LLM‑friendly commentary
-----------------------
This module defines the v2.2 Format Registry.

Responsibilities (v2.2):
- map structural format_id strings to loader classes
- provide a single source of truth for loader routing
- remain deterministic and free of side effects

Non‑responsibilities:
- running detectors (handled by format_detection_engine)
- selecting techniques (handled by technique_detection_engine)
- performing I/O or loading files
- interpreting scientific meaning

This registry is intentionally simple: a dictionary mapping
format_id → loader_class.
"""

from __future__ import annotations

from typing import Dict, Type

# Universal loaders
from chemworkbench.loaders.csv_loader import CSVLoader
from chemworkbench.loaders.xlsx_loader import XLSXLoader
from chemworkbench.loaders.jcamp_loader import JCampLoader
from chemworkbench.loaders.2col_ascii_loader import TwoColumnASCIILoader
from chemworkbench.loaders.multicol_ascii_loader import MultiColumnASCIILoader

# Vendor loaders
from chemworkbench.loaders.agilent.agilent_d_uvvis_loader import AgilentDUVVisLoader
from chemworkbench.loaders.agilent.agilent_d_chrom_loader import AgilentDChromLoader
from chemworkbench.loaders.agilent.agilent_d_ms_loader import AgilentDMSLoader

from chemworkbench.loaders.bruker.bruker_opus_loader import BrukerOpusLoader
from chemworkbench.loaders.bruker.bruker_nmr_loader import BrukerNMRLoader
from chemworkbench.loaders.bruker.bruker_epr_loader import BrukerEPRLoader

from chemworkbench.loaders.thermo.thermo_spc_loader import ThermoSPCLoader
from chemworkbench.loaders.thermo.thermo_spa_loader import ThermoSPALoader
from chemworkbench.loaders.thermo.thermo_srs_loader import ThermoSRSLoader

from chemworkbench.loaders.shimadzu.shimadzu_spc_loader import ShimadzuSPCLoader
from chemworkbench.loaders.shimadzu.shimadzu_irx_loader import ShimadzuIRXLoader
from chemworkbench.loaders.shimadzu.shimadzu_uvs_loader import ShimadzuUVSLoader
from chemworkbench.loaders.shimadzu.shimadzu_lcd_loader import ShimadzuLCDLoader

from chemworkbench.loaders.perkinelmer.perkinelmer_sp_loader import PerkinElmerSPLoader
from chemworkbench.loaders.perkinelmer.perkinelmer_spc_loader import PerkinElmerSPCLoader

from chemworkbench.loaders.waters.waters_raw_loader import WatersRAWLoader

from chemworkbench.loaders.jeol.jeol_jdf_loader import JeolJDFLoader
from chemworkbench.loaders.varian.varian_nmr_loader import VarianNMRLoader

from chemworkbench.loaders.raman.dpt_loader import DPTLoader
from chemworkbench.loaders.raman.rruf_loader import RRUFLoader
from chemworkbench.loaders.raman.rruf_gz_loader import RRUFGZLoader

from chemworkbench.loaders.horiba.horiba_fluor_loader import HoribaFluorLoader
from chemworkbench.loaders.ch_instruments.chi_dta_loader import CHIDTALoader


# ======================================================================
# FORMAT REGISTRY
# ======================================================================

FORMAT_REGISTRY: Dict[str, Type] = {
    # ------------------------------------------------------------
    # Universal formats
    # ------------------------------------------------------------
    "generic_csv_headered": CSVLoader,
    "generic_csv_no_header": CSVLoader,
    "generic_xlsx": XLSXLoader,
    "jcamp_dx": JCampLoader,
    "two_column_ascii": TwoColumnASCIILoader,
    "multi_column_ascii": MultiColumnASCIILoader,

    # ------------------------------------------------------------
    # Agilent MassHunter directory formats
    # ------------------------------------------------------------
    "agilent_uvvis_dad": AgilentDUVVisLoader,
    "agilent_chrom_masshunter": AgilentDChromLoader,
    "agilent_lcms_masshunter": AgilentDMSLoader,

    # ------------------------------------------------------------
    # Bruker formats
    # ------------------------------------------------------------
    "bruker_opus_binary": BrukerOpusLoader,
    "bruker_nmr_dir": BrukerNMRLoader,
    "bruker_epr_dir": BrukerEPRLoader,

    # ------------------------------------------------------------
    # Thermo formats
    # ------------------------------------------------------------
    "thermo_spc_binary": ThermoSPCLoader,
    "thermo_spa_ascii": ThermoSPALoader,
    "thermo_srs_ascii": ThermoSRSLoader,

    # ------------------------------------------------------------
    # Shimadzu formats
    # ------------------------------------------------------------
    "shimadzu_spc_binary": ShimadzuSPCLoader,
    "shimadzu_irx_ascii": ShimadzuIRXLoader,
    "shimadzu_uvs_ascii": ShimadzuUVSLoader,
    "shimadzu_lcd_binary": ShimadzuLCDLoader,

    # ------------------------------------------------------------
    # PerkinElmer formats
    # ------------------------------------------------------------
    "perkinelmer_sp_ascii": PerkinElmerSPLoader,
    "perkinelmer_spc_binary": PerkinElmerSPCLoader,

    # ------------------------------------------------------------
    # Waters formats
    # ------------------------------------------------------------
    "waters_raw_dir": WatersRAWLoader,

    # ------------------------------------------------------------
    # JEOL formats
    # ------------------------------------------------------------
    "jeol_jdf_binary": JeolJDFLoader,

    # ------------------------------------------------------------
    # Varian formats
    # ------------------------------------------------------------
    "varian_fid_dir": VarianNMRLoader,

    # ------------------------------------------------------------
    # Raman formats
    # ------------------------------------------------------------
    "raman_dpt_ascii": DPTLoader,
    "raman_rruf_ascii": RRUFLoader,
    "raman_rruf_gzip": RRUFGZLoader,

    # ------------------------------------------------------------
    # Fluorescence formats
    # ------------------------------------------------------------
    "horiba_fluor_ascii": HoribaFluorLoader,

    # ------------------------------------------------------------
    # Electrochemistry formats
    # ------------------------------------------------------------
    "chi_dta_ascii": CHIDTALoader,
}
