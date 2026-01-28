# chemworkbench/core/technique_anchors.py

from chemworkbench.core.models import Technique
import copy

# ------------------------------------------------------------
# IMPORTANT: All anchor patterns must be written in canonical,
# normalized form. The DetectionEngine applies normalization
# (lowercasing, unicode normalization, punctuation stripping,
# separator normalization) BEFORE matching against anchors.
#
# Therefore:
# - Do NOT include punctuation variants (uv-vis, uv_vis, uv/vis)
# - Do NOT include capitalization variants (UVVis, UV-VIS)
# - Do NOT include vendor-specific quirks
# - Do NOT include whitespace variants
#
# Anchors must be written in their canonical normalized form:
#   "uvvis", "absorbance", "transmittance", "opticaldensity"
#
# This ensures:
# - LLM-safe extension
# - plugin-safe behavior
# - deterministic scoring
# - future ML integration
# ------------------------------------------------------------

# ------------------------------------------------------------
# Anchor Library Versioning
# ------------------------------------------------------------
ANCHOR_LIBRARY_VERSION = "1.0.0"

# ------------------------------------------------------------
# Base template for all technique anchor definitions
# ------------------------------------------------------------
BASE_TECHNIQUE_TEMPLATE = {
    "extensions": [],
    "directory_markers": [],
    "glob_patterns": [],
    "required_files": [],
    "header_keywords": [],
    "keywords": [],
    "numeric_ranges": {},
    "vendor_hints": [],
    "binary_patterns": {},
    "negative_markers": [],
    "metadata": {
        "description": "",
        "source": "",
        "confidence": 1.0,
        "last_updated": "2026-01-27",
        "tags": [],
    },
    "categories": {
        "structural": ["extensions", "directory_markers", "glob_patterns", "required_files"],
        "semantic": ["header_keywords", "keywords"],
        "numeric": ["numeric_ranges"],
        "vendor": ["vendor_hints"],
        "binary": ["binary_patterns"],
        "negative": ["negative_markers"],
    },
    "version": "1.0.0",
}

# ------------------------------------------------------------
# Template cloning
# ------------------------------------------------------------
def clone_template():
    return copy.deepcopy(BASE_TECHNIQUE_TEMPLATE)

# ------------------------------------------------------------
# Schema validation
# ------------------------------------------------------------
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

        for key in [
            "extensions", "directory_markers", "glob_patterns",
            "required_files", "header_keywords", "keywords",
            "vendor_hints", "negative_markers",
        ]:
            for item in block[key]:
                if isinstance(item, tuple):
                    if not isinstance(item[0], str) or not isinstance(item[1], (int, float)):
                        raise ValueError(f"Invalid weighted entry in {tech}.{key}: {item}")

        for axis, rng in block["numeric_ranges"].items():
            if not (isinstance(rng, tuple) and len(rng) == 2):
                raise ValueError(f"Invalid numeric range for {tech}.{axis}: {rng}")

        meta = block["metadata"]
        if not isinstance(meta.get("description", ""), str):
            raise ValueError(f"Invalid metadata.description for {tech}")
        if not isinstance(meta.get("source", ""), str):
            raise ValueError(f"Invalid metadata.source for {tech}")
        if not isinstance(meta.get("confidence", 1.0), (int, float)):
            raise ValueError(f"Invalid metadata.confidence for {tech}")
        if not isinstance(meta.get("tags", []), list):
            raise ValueError(f"Invalid metadata.tags for {tech}")

# ------------------------------------------------------------
# Technique Anchor Registry
# ------------------------------------------------------------
TECHNIQUE_ANCHORS = {
    Technique.UVVIS: {
        **clone_template(),

        "extensions": [
            (".uv", 6),
            (".spc", 5),
            (".jdx", 5),
            (".dx", 4),
            (".csv", 4),
            (".txt", 3),
            (".tsv", 3),
            (".dat", 3),
            (".asc", 3),
            (".xls", 2),
        ],

        "directory_markers": [
            ("uvsignal", 6),
            ("uvdata", 6),
            ("absorbance", 5),
            ("uvvis", 5),
            ("uv", 4),
            ("spectra", 4),
            ("scan", 3),
            ("signals", 3),
            ("data", 2),
            ("results", 2),
        ],

        "glob_patterns": [
            ("uv", 6),
            ("abs", 6),
            ("absorbance", 5),
            ("spectrum", 4),
            ("spectra", 4),
            ("scan", 4),
        ],

        "required_files": [],

        "header_keywords": [
            ("wavelength", 6),
            ("lambda", 5),
            ("nm", 5),
            ("nanometers", 4),
            ("absorbance", 6),
            ("absorb", 4),
            ("abs", 3),
            ("au", 4),
            ("baseline", 3),
            ("reference", 3),
            ("transmittance", 5),
            ("percenttransmittance", 4),
            ("opticaldensity", 5),
            ("spectrum", 3),
            ("spectra", 3),
            ("scan", 3),
        ],

        "keywords": [
            ("uvvis", 6),
            ("uvvisnir", 6),

            ("uv", 4),
            ("vis", 3),

            ("absorbance", 6),
            ("absorb", 4),
            ("abs", 3),
            ("au", 4),

            ("transmittance", 5),
            ("percenttransmittance", 4),

            ("wavelength", 6),
            ("lambda", 5),
            ("nm", 5),
            ("nanometers", 4),

            ("optical", 4),
            ("opticaldensity", 5),
            ("od", 3),

            ("spectrum", 3),
            ("spectra", 3),
            ("scan", 3),
        ],

        "numeric_ranges": {
            "x": (180.0, 1100.0),
        },

        "vendor_hints": [
            ("agilent", 4),
            ("cary", 5),
            ("shimadzu", 4),
            ("uvprobe", 4),
            ("thermo", 3),
            ("evolution", 3),
            ("perkinelmer", 4),
            ("lambda", 4),
            ("oceanoptics", 4),
            ("avantes", 4),
            ("stellarnet", 4),
            ("malvern", 3),
            ("hitachi", 3),
        ],

        "binary_patterns": {},

        "negative_markers": [
            ("fid", -8),
            ("acqus", -8),
            ("procs", -8),
            ("ppm", -6),
            ("cm1", -6),
            ("raman", -6),
            ("ms1", -6),
            ("ms2", -6),
            ("chrom", -4),
        ],

        "metadata": {
            "description": "Anchor terms and patterns for UV-Vis and UV-Vis-NIR absorbance/transmittance spectroscopy.",
            "source": (
                "Agilent Cary, Shimadzu UVProbe, Thermo Evolution, PerkinElmer Lambda, "
                "Ocean Optics, Avantes, StellarNet, Malvern, Hitachi UV series, "
                "academic CSV/TXT exports, JCAMP-DX UV-Vis files."
            ),
            "confidence": 0.9,
            "last_updated": "2026-01-27",
            "tags": ["uvvis", "uvvisnir", "spectroscopy", "optical", "absorbance", "transmittance"],
        },

        "version": "1.0.0",
    },

    Technique.FLUORESCENCE: clone_template(),
    Technique.IR: clone_template(),
    Technique.RAMAN: clone_template(),
    Technique.NMR: clone_template(),
    Technique.EPR: clone_template(),
    Technique.CV: clone_template(),
    Technique.GCMS: clone_template(),
    Technique.LCMS: clone_template(),
    Technique.CHROMATOGRAPHY: clone_template(),
}

# ------------------------------------------------------------
# Normalize anchors before validation
# ------------------------------------------------------------
from chemworkbench.utils.normalization import normalize_token

def _normalize_anchor_block(block: dict):
    for key in [
        "extensions", "directory_markers", "glob_patterns",
        "required_files", "header_keywords", "keywords",
        "vendor_hints", "negative_markers",
    ]:
        normalized_list = []
        for item in block[key]:
            if isinstance(item, tuple):
                pattern, weight = item
                normalized_list.append((normalize_token(pattern), weight))
            else:
                normalized_list.append(normalize_token(item))
        block[key] = normalized_list

for _tech, _block in TECHNIQUE_ANCHORS.items():
    _normalize_anchor_block(_block)

# ------------------------------------------------------------
# Validate on import
# ------------------------------------------------------------
validate_anchors(TECHNIQUE_ANCHORS)
