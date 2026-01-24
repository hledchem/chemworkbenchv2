"""
Shimadzu vendor-specific loaders.

This package provides loaders for:
- SPC spectral exports (IR, Raman, UV-Vis)
- IRX (Shimadzu IR/FTIR)
- UVS (Shimadzu UV-Vis)
- LCD (Shimadzu chromatography and MS)

Each loader subclasses BaseVendorLoader and follows the canonical loader API.
"""

from .shimadzu_spc_loader import ShimadzuSPCLoader
from .shimadzu_irx_loader import ShimadzuIRXLoader
from .shimadzu_uvs_loader import ShimadzuUVSLoader
from .shimadzu_lcd_loader import ShimadzuLCDLoader

__all__ = [
    "ShimadzuSPCLoader",
    "ShimadzuIRXLoader",
    "ShimadzuUVSLoader",
    "ShimadzuLCDLoader",
]
