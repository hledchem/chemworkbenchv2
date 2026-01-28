"""
Technique Anchor Library — ChemWorkBench v2.2
=============================================

LLM‑friendly commentary
-----------------------
This module defines the canonical anchor blocks for all analytical
techniques supported by ChemWorkBench v2.2.

Anchors are:
- deterministic
- explainable
- plugin‑safe
- LLM‑safe
- compatible with future ML scoring

Each anchor block is validated against BASE_TECHNIQUE_TEMPLATE to ensure:
- no missing fields
- no extra fields
- correct weighting structure
- correct metadata structure
"""

from __future__ import annotations

import copy
from chemworkbench.core.models import Technique


# ======================================================================
# Anchor Library Versioning
# ======================================================================

ANCHOR_LIBRARY_VERSION = "1.0.0"


# ======================================================================
# Base template for all technique anchor definitions
# ======================================================================

BASE_TECHNIQUE_TEMPLATE = {
    # Structural signals
    "extensions": [],
    "directory_markers": [],
    "glob_patterns": [],
    "required_files": [],

    # Semantic signals
    "header_keywords": [],
    "keywords": [],

    # Numeric signals
    "numeric_ranges": {},

    # Vendor signals
    "vendor_hints": [],

    # Binary signals (NMR/EPR only)
    "binary_patterns": {},

    # Negative signals
    "negative_markers": [],

    # Metadata
    "metadata": {
        "description": "",
        "source": "",
        "confidence": 1.0,
        "last_updated": "2026-01-27",
        "tags": [],
    },

    # Categories (for LLM reasoning)
    "categories": {
        "structural": ["extensions", "directory_markers", "glob_patterns", "required_files"],
        "semantic": ["header_keywords", "keywords"],
        "numeric": ["numeric_ranges"],
        "vendor": ["vendor_hints"],
        "binary": ["binary_patterns"],
        "negative": ["negative_markers"],
    },

    # Versioning
    "version": "1.0.0",
}


# ======================================================================
# Template cloning
# ======================================================================

def clone_template():
    """Return a deep copy of the base technique template."""
    return copy.deepcopy(BASE_TECHNIQUE_TEMPLATE)


# ======================================================================
# Schema validation
# ======================================================================

def validate_anchors(anchors: dict):
    required_keys = set(BASE_TECHNIQUE_TEMPLATE.keys())

    for tech, block in anchors.items():
        block_keys = set(block.keys())

        missing = required_keys - block_keys
        extra = block_keys - required_keys

        if missing:
            raise ValueError(f"Technique {tech} missing keys: {missing}")
        if extra:
            raise ValueError(f"Technique {tech} has unknown keys: {extra}")

        # Validate weighted lists
        for key in [
            "extensions", "directory_markers", "glob_patterns",
            "required_files", "header_keywords", "keywords",
            "vendor_hints", "negative_markers",
        ]:
            for item in block[key]:
                if isinstance(item, tuple):
                    if not isinstance(item[0], str) or not isinstance(item[1], (int, float)):
                        raise ValueError(f"Invalid weighted entry in {tech}.{key}: {item}")

        # Validate numeric ranges
        for axis, rng in block["numeric_ranges"].items():
            if not (isinstance(rng, tuple) and len(rng) == 2):
                raise ValueError(f"Invalid numeric range for {tech}.{axis}: {rng}")

        # Validate metadata
        meta = block["metadata"]
        if not isinstance(meta.get("description", ""), str):
            raise ValueError(f"Invalid metadata.description for {tech}")
        if not isinstance(meta.get("source", ""), str):
            raise ValueError(f"Invalid metadata.source for {tech}")
        if not isinstance(meta.get("confidence", 1.0), (int, float)):
            raise ValueError(f"Invalid metadata.confidence for {tech}")
        if not isinstance(meta.get("tags", []), list):
            raise ValueError(f"Invalid metadata.tags for {tech}")


# ======================================================================
# Technique Anchor Registry
# ======================================================================

TECHNIQUE_ANCHORS = {}

# ----------------------------------------------------------------------
# UV‑Vis spectroscopy (UVVIS)
# ----------------------------------------------------------------------

_uvvis = clone_template()
_uvvis.update({
    # Structural anchors
    "extensions": [
        (".uv", 6), (".spc", 5), (".jdx", 5), (".dx", 4),
        (".csv", 4), (".txt", 3), (".tsv", 3), (".dat", 3),
        (".asc", 3), (".xls", 2),
    ],

    "directory_markers": [
        ("UVSignal", 6), ("UV_Data", 6), ("Absorbance", 5),
        ("UVVis", 5), ("UV-Vis", 5), ("UV_VIS", 5),
        ("UV", 4), ("Spectra", 4), ("Scan", 3),
        ("Signals", 3), ("Data", 2), ("Results", 2),
    ],

    "glob_patterns": [
        ("*UV*.CSV", 6), ("*ABS*.CSV", 6),
        ("*Absorbance*.txt", 5), ("*Spectrum*.txt", 4),
        ("*Spectra*.txt", 4), ("*Scan*.csv", 4),
        ("*UV*.dat", 4), ("*UV*.jdx", 5), ("*UV*.spc", 5),
    ],

    "required_files": [],

    # Semantic anchors
    "header_keywords": [
        ("wavelength", 6), ("lambda", 5), ("nm", 5),
        ("nanometers", 4), ("absorbance", 6), ("absorb", 4),
        ("abs", 3), ("au", 4), ("baseline", 3),
        ("reference", 3), ("transmittance", 5),
        ("%t", 4), ("percent_transmittance", 4),
        ("optical density", 5), ("optical_density", 5),
        ("spectrum", 3), ("spectra", 3), ("scan", 3),
    ],

    "keywords": [
        ("uvvis", 6), ("uv-vis", 6), ("uv_vis", 6),
        ("uv/vis", 6), ("uv vis", 6), ("uv-vis-nir", 6),
        ("uv/vis/nir", 6), ("uvvisnir", 6),
        ("uv", 4), ("vis", 3),
        ("absorbance", 6), ("absorb", 4), ("abs", 3), ("au", 4),
        ("transmittance", 5), ("%t", 4), ("percent_transmittance", 4),
        ("wavelength", 6), ("lambda", 5), ("nm", 5), ("nanometers", 4),
        ("optical", 4), ("optical_density", 5), ("od", 3),
        ("spectrum", 3), ("spectra", 3), ("scan", 3),
    ],

    # Numeric anchors
    "numeric_ranges": {
        "x": (180.0, 1100.0),
    },

    # Vendor anchors
    "vendor_hints": [
        ("agilent", 4), ("cary", 5), ("shimadzu", 4),
        ("uvprobe", 4), ("thermo", 3), ("evolution", 3),
        ("perkinelmer", 4), ("lambda", 4),
        ("ocean optics", 4), ("avantes", 4), ("stellarnet", 4),
        ("malvern", 3), ("hitachi", 3),
    ],

    # Binary anchors
    "binary_patterns": {},

    # Negative anchors
    "negative_markers": [
        ("fid", -8), ("acqus", -8), ("procs", -8),
        ("ppm", -6), ("cm-1", -6), ("raman", -6),
        ("ms1", -6), ("ms2", -6), ("chrom", -4),
    ],

    # Metadata
    "metadata": {
        "description": "Anchor terms and patterns for UV‑Vis and UV‑Vis‑NIR spectroscopy.",
        "source": (
            "Agilent Cary, Shimadzu UVProbe, Thermo Evolution, PerkinElmer Lambda, "
            "Ocean Optics, Avantes, StellarNet, Malvern, Hitachi UV series, "
            "academic CSV/TXT exports, JCAMP‑DX UV‑Vis files."
        ),
        "confidence": 0.9,
        "last_updated": "2026-01-27",
        "tags": ["uvvis", "uv-vis", "uv-vis-nir", "spectroscopy", "optical", "absorbance", "transmittance"],
    },

    "version": "1.0.0",
})

TECHNIQUE_ANCHORS[Technique.UVVIS] = _uvvis


# ----------------------------------------------------------------------
# Other techniques (placeholders)
# ----------------------------------------------------------------------

for tech in [
    Technique.FLUORESCENCE,
    Technique.IR,
    Technique.RAMAN,
    Technique.NMR,
    Technique.EPR,
    Technique.CV,
    Technique.GCMS,
    Technique.LCMS,
    Technique.CHROMATOGRAPHY,
]:
    TECHNIQUE_ANCHORS[tech] = clone_template()


# ======================================================================
# Validate on import
# ======================================================================

validate_anchors(TECHNIQUE_ANCHORS)
