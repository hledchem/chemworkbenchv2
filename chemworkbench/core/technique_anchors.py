# chemworkbench/core/technique_anchors.py

from chemworkbench.core.models import Technique
import copy

# ------------------------------------------------------------
# Anchor Library Versioning
# ------------------------------------------------------------
ANCHOR_LIBRARY_VERSION = "1.0.0"

# ------------------------------------------------------------
# Base template for all technique anchor definitions
# ------------------------------------------------------------
# Each field supports:
# - simple strings
# - weighted tuples: (pattern, weight)
# - negative markers: (pattern, negative_weight)
#
# This structure is designed for:
# - LLM interpretability
# - plugin extension
# - future ML integration
# - deterministic scoring
# - explainability
# ------------------------------------------------------------

BASE_TECHNIQUE_TEMPLATE = {
    # Structural signals
    "extensions": [],            # list[str] or list[(str, weight)]
    "directory_markers": [],     # list[str] or list[(str, weight)]
    "glob_patterns": [],         # list[str] or list[(str, weight)]
    "required_files": [],        # list[str] or list[(str, weight)]

    # Semantic signals
    "header_keywords": [],       # list[str] or list[(str, weight)]
    "keywords": [],              # list[str] or list[(str, weight)]

    # Numeric signals
    "numeric_ranges": {},        # dict[str, tuple[min, max]]

    # Vendor signals
    "vendor_hints": [],          # list[str] or list[(str, weight)]

    # Binary signals (NMR/EPR only)
    "binary_patterns": {},       # dict[str, Any]

    # Negative signals (reduce score)
    "negative_markers": [],      # list[str] or list[(str, negative_weight)]

    # Metadata for LLMs, documentation, provenance
    "metadata": {
        "description": "",
        "source": "",
        "confidence": 1.0,
        "last_updated": "2026-01-27",
        "tags": [],
    },

    # Optional categories for LLM reasoning
    "categories": {
        "structural": ["extensions", "directory_markers", "glob_patterns", "required_files"],
        "semantic": ["header_keywords", "keywords"],
        "numeric": ["numeric_ranges"],
        "vendor": ["vendor_hints"],
        "binary": ["binary_patterns"],
        "negative": ["negative_markers"],
    },

    # Versioning for reproducibility
    "version": "1.0.0",
}

# ------------------------------------------------------------
# Template cloning (deep copy to avoid shared mutable state)
# ------------------------------------------------------------

def clone_template():
    """Return a deep copy of the base technique template."""
    return copy.deepcopy(BASE_TECHNIQUE_TEMPLATE)

# ------------------------------------------------------------
# Schema validation for anchor definitions
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

        # Validate weighted lists
        for key in [
            "extensions", "directory_markers", "glob_patterns",
            "required_files", "header_keywords", "keywords",
            "vendor_hints", "negative_markers"
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

# ------------------------------------------------------------
# Technique Anchor Registry (empty templates for now)
# ------------------------------------------------------------

TECHNIQUE_ANCHORS = {
    Technique.UVVIS: clone_template(),
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
# Validate on import
# ------------------------------------------------------------
validate_anchors(TECHNIQUE_ANCHORS)
