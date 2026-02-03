"""
format_registry.py — ChemWorkBench v2.2
=======================================

LLM‑friendly commentary
-----------------------
This module defines the v2.2 File‑Sniffer Format Registry.

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

Only the formats/loaders currently enabled in the v2.2 ingestion
pipeline are included here.
"""

from __future__ import annotations
from typing import Dict, Type

# ----------------------------------------------------------------------
# Active universal loaders (trimmed to match v2.2 ingestion)
# ----------------------------------------------------------------------

from chemworkbench.utils.loaders.csv_loader import CSVLoader
from chemworkbench.utils.loaders.ascii_2col_loader import ASCII2ColLoader
from chemworkbench.utils.loaders.ascii_multicol_loader import ASCIIMultiColLoader
from chemworkbench.utils.loaders.jcamp_loader import JCAMPDXLoader


# ======================================================================
# FORMAT REGISTRY (minimal v2.2 set)
# ======================================================================

FORMAT_REGISTRY: Dict[str, Type] = {

    # ------------------------------------------------------------
    # Universal formats
    # ------------------------------------------------------------
    "generic_csv_headered": CSVLoader,
    "two_column_ascii": ASCII2ColLoader,
    "multi_column_ascii": ASCIIMultiColLoader,
    "jcamp_dx": JCAMPDXLoader,

    # ------------------------------------------------------------
    # All vendor formats are intentionally disabled for now.
    # They will be re‑enabled one‑by‑one as loaders are updated.
    # ------------------------------------------------------------

    # "agilent_uvvis_dad": AgilentDUVVisLoader,
    # "agilent_chrom_masshunter": AgilentDChromLoader,
    # "agilent_lcms_masshunter": AgilentDMSLoader,

    # "bruker_opus_binary": BrukerOPUSLoader,
    # "bruker_nmr_dir": BrukerNMRLoader,
    # "bruker_epr_dir": BrukerEPRLoader,

    # "thermo_spc_binary": ThermoSPCLoader,
    # "thermo_spa_ascii": ThermoSPALoader,
    # "thermo_srs_ascii": ThermoSRSLoader,

    # "shimadzu_spc_binary": ShimadzuSPCLoader,
    # "shimadzu_irx_ascii": ShimadzuIRXLoader,
    # "shimadzu_uvs_ascii": ShimadzuUVSLoader,
    # "shimadzu_lcd_binary": ShimadzuLCDLoader,

    # "perkinelmer_sp_ascii": PerkinElmerSPLoader,
    # "perkinelmer_spc_binary": PerkinElmerSPCLoader,

    # "waters_raw_dir": WatersRAWLoader,

    # "jeol_jdf_binary": JEOLJDFLoader,

    # "varian_fid_dir": VarianNMRLoader,

    # "raman_dpt_ascii": DPTLoader,
    # "raman_rruf_ascii": RRUFFLoader,
    # "raman_rruf_gzip": RRUFFGZLoader,

    # "horiba_fluor_ascii": HoribaFluorescenceLoader,

    # "chi_dta_ascii": CHIDTALoader,
}
