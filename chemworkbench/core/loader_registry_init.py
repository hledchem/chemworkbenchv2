"""
ChemWorkBench v2.2 — Default Loader Registry Initialization
===========================================================

Purpose
-------
This module registers all *built-in* loader classes used by the v2.2
ingestion engine. Loader keys defined here must match the loader_key
values used in FormatDescriptor objects inside format_registry_init.py.

This file is intentionally explicit, deterministic, and LLM-friendly.

Loader Families (v2.2)
----------------------
• csv_loader
• ascii_2col_loader
• ascii_multicol_loader
• jcamp_loader
• bruker_nmr_loader
• varian_nmr_loader
• thermo_spc_loader
• thermo_spa_loader
• thermo_srs_loader
• waters_raw_loader
• jeol_jdf_loader
• agilent_masshunter_loader
• rruf_loader
• rruf_gz_loader
• chi_dta_loader

Public API
----------
- build_default_loader_registry() → LoaderRegistry
"""

from __future__ import annotations

from chemworkbench.core.loader_registry import LoaderRegistry

# ----------------------------------------------------------------------
# Universal loaders
# ----------------------------------------------------------------------
from chemworkbench.loaders.csv_loader import CSVLoader
from chemworkbench.loaders.jcamp_loader import JCampLoader
from chemworkbench.loaders.2col_ascii_loader import ASCII2ColLoader
from chemworkbench.loaders.multicol_ascii_loader import ASCIIMultiColLoader

# ----------------------------------------------------------------------
# NMR loaders
# ----------------------------------------------------------------------
from chemworkbench.loaders.bruker.bruker_nmr_loader import BrukerNMRLoader
from chemworkbench.loaders.varian.varian_nmr_loader import VarianNMRLoader

# ----------------------------------------------------------------------
# Thermo loaders
# ----------------------------------------------------------------------
from chemworkbench.loaders.thermo.thermo_spc_loader import ThermoSPCLoader
from chemworkbench.loaders.thermo.thermo_spa_loader import ThermoSPALoader
from chemworkbench.loaders.thermo.thermo_srs_loader import ThermoSRSLoader

# ----------------------------------------------------------------------
# Waters loaders
# ----------------------------------------------------------------------
from chemworkbench.loaders.waters.waters_raw_loader import WatersRAWLoader

# ----------------------------------------------------------------------
# JEOL loaders
# ----------------------------------------------------------------------
from chemworkbench.loaders.jeol.jeol_jdf_loader import JeolJDFLoader

# ----------------------------------------------------------------------
# Agilent loaders
# ----------------------------------------------------------------------
from chemworkbench.loaders.agilent.agilent_d_ms_loader import AgilentDMSLoader
# NOTE: MassHunter loader is the structural loader for .D directories
AgilentMassHunterLoader = AgilentDMSLoader

# ----------------------------------------------------------------------
# Raman loaders
# ----------------------------------------------------------------------
from chemworkbench.loaders.raman.rruf_loader import RRUFLoader
from chemworkbench.loaders.raman.rruf_gz_loader import RRUFGZLoader

# ----------------------------------------------------------------------
# Electrochemistry loaders
# ----------------------------------------------------------------------
from chemworkbench.loaders.ch_instruments.chi_dta_loader import CHIDTALoader


# ======================================================================
# Loader Registry Initialization
# ======================================================================

def build_default_loader_registry() -> LoaderRegistry:
    """
    Construct and return the canonical v2.2 LoaderRegistry containing all
    built-in loader classes.

    Notes
    -----
    • Plugins may extend or override these loaders at runtime.
    • Loader keys must match those referenced in FormatDescriptor objects.
    • Loader classes must implement .load(path, detected) → RawDataBundle.
    """

    reg = LoaderRegistry()

    # ================================================================
    # UNIVERSAL LOADERS
    # ================================================================
    reg.register("csv_loader", CSVLoader)
    reg.register("ascii_2col_loader", ASCII2ColLoader)
    reg.register("ascii_multicol_loader", ASCIIMultiColLoader)
    reg.register("jcamp_loader", JCampLoader)

    # ================================================================
    # NMR LOADERS
    # ================================================================
    reg.register("bruker_nmr_loader", BrukerNMRLoader)
    reg.register("varian_nmr_loader", VarianNMRLoader)

    # ================================================================
    # THERMO LOADERS
    # ================================================================
    reg.register("thermo_spc_loader", ThermoSPCLoader)
    reg.register("thermo_spa_loader", ThermoSPALoader)
    reg.register("thermo_srs_loader", ThermoSRSLoader)

    # ================================================================
    # WATERS RAW DIRECTORY
    # ================================================================
    reg.register("waters_raw_loader", WatersRAWLoader)

    # ================================================================
    # JEOL JDF
    # ================================================================
    reg.register("jeol_jdf_loader", JeolJDFLoader)

    # ================================================================
    # AGILENT MASSHUNTER DIRECTORY (.D)
    # ================================================================
    reg.register("agilent_masshunter_loader", AgilentMassHunterLoader)

    # ================================================================
    # RAMAN SPECIAL FORMATS
    # ================================================================
    reg.register("rruf_loader", RRUFLoader)
    reg.register("rruf_gz_loader", RRUFGZLoader)

    # ================================================================
    # ELECTROCHEMISTRY (CHI .dta)
    # ================================================================
    reg.register("chi_dta_loader", CHIDTALoader)

    return reg
