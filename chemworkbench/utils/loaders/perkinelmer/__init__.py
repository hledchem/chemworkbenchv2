"""
PerkinElmer vendor-specific loaders.

This package provides loaders for:
- SP spectral exports (legacy PerkinElmer format)
- SPC spectral exports (modern PerkinElmer format)

Each loader subclasses BaseVendorLoader and follows the canonical loader API.
"""

from .perkinelmer_sp_loader import PerkinElmerSPLoader
from .perkinelmer_spc_loader import PerkinElmerSPCLoader

__all__ = [
    "PerkinElmerSPLoader",
    "PerkinElmerSPCLoader",
]
