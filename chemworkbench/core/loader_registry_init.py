"""
ChemWorkBench v2.2 — Default Loader Registry Initialization
===========================================================

Registers all *built‑in* loader classes used by the v2.2 ingestion engine.
Loader keys defined here must match the loader_key values used in
FormatDescriptor objects inside format_registry_init.py.

This file is intentionally explicit, deterministic, and LLM‑friendly.
"""

from __future__ import annotations

from chemworkbench.core.loader_registry import LoaderRegistry

# ----------------------------------------------------------------------
# UNIVERSAL LOADERS (CSV, ASCII, JCAMP)
# ----------------------------------------------------------------------
from chemworkbench.utils.loaders.csv_loader import CSVLoader
from chemworkbench.utils.loaders.ascii_2col_loader import ASCII2ColLoader
from chemworkbench.utils.loaders.ascii_multicol_loader import ASCIIMultiColLoader
from chemworkbench.utils.loaders.jcamp_loader import JCAMPDXLoader

# ----------------------------------------------------------------------
# NMR LOADERS
# ----------------------------------------------------------------------
from chemworkbench.utils.loaders.bruker_nmr_loader import BrukerNMRLoader
# If you have Varian, uncomment:
# from chemworkbench.utils.loaders.varian_nmr_loader import VarianNMRLoader

# ----------------------------------------------------------------------
# THERMO LOADERS (SPC)
# ----------------------------------------------------------------------
from chemworkbench.utils.loaders.thermo_spc_loader import ThermoSPCLoader

# ----------------------------------------------------------------------
# WATERS RAW DIRECTORY
# ----------------------------------------------------------------------
from chemworkbench.utils.loaders.waters_raw_loader import WatersRAWLoader

# ----------------------------------------------------------------------
# JEOL JDF
# ----------------------------------------------------------------------
from chemworkbench.utils.loaders.jeol_jdf_loader import JEOLJDFLoader


# ======================================================================
# Loader Registry Initialization
# ======================================================================

def build_default_loader_registry() -> LoaderRegistry:
    """
    Construct and return the canonical v2.2 LoaderRegistry containing all
    built‑in loader classes.

    Notes
    -----
    • Plugins may extend or override these loaders at runtime.
    • Loader keys must match those referenced in FormatDescriptor objects.
    """

    reg = LoaderRegistry()

    # ================================================================
    # UNIVERSAL LOADERS
    # ================================================================
    reg.register("csv_loader", CSVLoader)
    reg.register("ascii_2col_loader", ASCII2ColLoader)
    reg.register("ascii_multicol_loader", ASCIIMultiColLoader)
    reg.register("jcamp_loader", JCAMPDXLoader)

    # ================================================================
    # NMR LOADERS
    # ================================================================
    reg.register("bruker_nmr_loader", BrukerNMRLoader)
    # reg.register("varian_nmr_loader", VarianNMRLoader)

    # ================================================================
    # THERMO LOADERS
    # ================================================================
    reg.register("thermo_spc_loader", ThermoSPCLoader)

    # ================================================================
    # WATERS RAW DIRECTORY
    # ================================================================
    reg.register("waters_raw_loader", WatersRAWLoader)

    # ================================================================
    # JEOL JDF
    # ================================================================
    reg.register("jeol_jdf_loader", JEOLJDFLoader)

    return reg
