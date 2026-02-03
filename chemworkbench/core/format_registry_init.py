"""
ChemWorkBench v2.2 — Default Format Registry Initialization
===========================================================

Purpose
-------
Registers all *built-in* structural data formats supported by ChemWorkBench v2.2.
These formats represent structural families, not techniques or vendors, and map
directly to loader keys used by the LoaderRegistry.

This file is intentionally explicit, deterministic, and LLM-friendly.

Format Families (v2.2)
----------------------
• csv
• ascii
• jcamp
• nmr_dir
• spc
• vendor_dir
• jdf

Public API
----------
- build_default_format_registry() → FormatRegistry
"""

from __future__ import annotations

from chemworkbench.core.format_registry import FormatRegistry, FormatDescriptor


def build_default_format_registry() -> FormatRegistry:
    """
    Construct and return the canonical v2.2 FormatRegistry containing all
    built-in structural format descriptors.

    Notes
    -----
    • Plugins may extend or override these formats at runtime.
    • Loader keys must match those registered in LoaderRegistry.
    • Format IDs must remain stable across versions for reproducibility.
    """

    reg = FormatRegistry()

    # ================================================================
    # CSV FAMILY
    # ================================================================
    reg.register(FormatDescriptor(
        id="generic_csv_headered",
        family="csv",
        vendor=None,
        version=None,
        loader_key="csv_loader",
    ))

    # ================================================================
    # ASCII FAMILY
    # ================================================================
    reg.register(FormatDescriptor(
        id="two_column_ascii",
        family="ascii",
        vendor=None,
        version=None,
        loader_key="ascii_2col_loader",
    ))

    reg.register(FormatDescriptor(
        id="multi_column_ascii",
        family="ascii",
        vendor=None,
        version=None,
        loader_key="ascii_multicol_loader",
    ))

    # ================================================================
    # JCAMP FAMILY
    # ================================================================
    reg.register(FormatDescriptor(
        id="jcamp_dx",
        family="jcamp",
        vendor=None,
        version=None,
        loader_key="jcamp_loader",
    ))

    # ================================================================
    # NMR DIRECTORY FORMATS (DISABLED FOR NOW)
    # ================================================================
    # reg.register(FormatDescriptor(
    #     id="bruker_nmr_dir",
    #     family="nmr_dir",
    #     vendor="bruker",
    #     version=None,
    #     loader_key="bruker_nmr_loader",
    # ))

    # ================================================================
    # WATERS RAW DIRECTORY (DISABLED FOR NOW)
    # ================================================================
    # reg.register(FormatDescriptor(
    #     id="waters_raw_dir",
    #     family="vendor_dir",
    #     vendor="waters",
    #     version=None,
    #     loader_key="waters_raw_loader",
    # ))

    # ================================================================
    # JEOL JDF FAMILY (DISABLED FOR NOW)
    # ================================================================
    # reg.register(FormatDescriptor(
    #     id="jeol_jdf_binary",
    #     family="jdf",
    #     vendor="jeol",
    #     version=None,
    #     loader_key="jeol_jdf_loader",
    # ))

    # ================================================================
    # THERMO SPC FAMILY (DISABLED FOR NOW)
    # ================================================================
    # reg.register(FormatDescriptor(
    #     id="thermo_spc_binary",
    #     family="spc",
    #     vendor="thermo",
    #     version=None,
    #     loader_key="thermo_spc_loader",
    # ))

    return reg
