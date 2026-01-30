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

# ----------------------------------------------------------------------
# Universal loaders
# ----------------------------------------------------------------------

from chemworkbench.utils.loaders.csv_loader import CSVLoader
from chemworkbench.utils.loaders.xlsx_loader import XLSXLoader
from chemworkbench.utils.loaders.jcamp_loader import JCAMPLoader
from chemworkbench.utils.loaders.ascii_2col_loader import ASCII2ColLoader
from chemworkbench.utils.loaders.ascii_multicol_loader import ASCIIMultiColLoader

# ----------------------------------------------------------------------
# Vendor loaders
# ----------------------------------------------------------------------

from chemworkbench.utils.loaders.agilent.agilent_d_uvvis_loader import AgilentDUVVisLoader
from chemworkbench.utils.loaders.agilent.agilent_d_chrom_loader import AgilentDChromLoader
from chemworkbench.utils.loaders.agilent.agilent_d_ms_loader import AgilentDMSLoader

from chemworkbench.utils.loaders.bruker.bruker_opus_loader import BrukerOPUSLoader
from chemworkbench.utils.loaders.bruker.bruker_nmr_loader import BrukerNMRLoader
from chemworkbench.utils.loaders.bruker.bruker_epr_loader import BrukerEPRLoader

from chemworkbench.utils.loaders.thermo.thermo_spc_loader import ThermoSPCLoader
from chemworkbench.utils.loaders.thermo.thermo_spa_loader import ThermoSPALoader
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

from chemworkbench.utils.loaders.raman.dpt_loader import DPTLoader
from chemworkbench.utils.loaders.raman.rruf_loader import RRUFFLoader
from chemworkbench.utils.loaders.raman.rruf_gz_loader import RRUFFGZLoader

from chemworkbench.utils.loaders.horiba.horiba_fluor_loader import HoribaFluorescenceLoader
from chemworkbench.utils.loaders.ch_instruments.chi_dta_loader import CHIDTALoader


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
    "jcamp_dx": JCAMPLoader,
    "two_column_ascii": ASCII2ColLoader,
    "multi_column_ascii": ASCIIMultiColLoader,

    # ------------------------------------------------------------
    # Agilent MassHunter directory formats
    # ------------------------------------------------------------
    "agilent_uvvis_dad": AgilentDUVVisLoader,
    "agilent_chrom_masshunter": AgilentDChromLoader,
    "agilent_lcms_masshunter": AgilentDMSLoader,

    # ------------------------------------------------------------
    # Bruker formats
    # ------------------------------------------------------------
    "bruker_opus_binary": BrukerOPUSLoader,
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
    "jeol_jdf_binary": JEOLJDFLoader,

    # ------------------------------------------------------------
    # Varian formats
    # ------------------------------------------------------------
    "varian_fid_dir": VarianNMRLoader,

    # ------------------------------------------------------------
    # Raman formats
    # ------------------------------------------------------------
    "raman_dpt_ascii": DPTLoader,
    "raman_rruf_ascii": RRUFFLoader,
    "raman_rruf_gzip": RRUFFGZLoader,

    # ------------------------------------------------------------
    # Fluorescence formats
    # ------------------------------------------------------------
    "horiba_fluor_ascii": HoribaFluorescenceLoader,

    # ------------------------------------------------------------
    # Electrochemistry formats
    # ------------------------------------------------------------
    "chi_dta_ascii": CHIDTALoader,
}
