# chemworkbench/core/technique_anchors.py

from chemworkbench.core.models import Technique

# ------------------------------------------------------------
# Base template for all technique anchor definitions
# ------------------------------------------------------------

BASE_TECHNIQUE_TEMPLATE = {
    "extensions": [],          # list[str]
    "directory_markers": [],   # list[str]
    "glob_patterns": [],       # list[str]
    "required_files": [],      # list[str]
    "header_keywords": [],     # list[str]
    "keywords": [],            # list[str]
    "numeric_ranges": {},      # dict[str, tuple[float, float]]
    "vendor_hints": [],        # list[str]
    "binary_patterns": {},     # dict[str, Any] (only for NMR/EPR)
}
