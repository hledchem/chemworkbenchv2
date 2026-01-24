"""
Bruker vendor-specific loaders.

This package provides loaders for:
- Bruker OPUS spectral files (IR, FTIR, Raman, NIR)
- Bruker TopSpin NMR datasets (1H, 13C, COSY, HSQC, HMBC, etc.)

Each loader subclasses BaseVendorLoader and follows the canonical loader API.
"""

from .bruker_opus_loader import BrukerOPUSLoader
from .bruker_nmr_loader import BrukerNMRLoader

__all__ = [
    "BrukerOPUSLoader",
    "BrukerNMRLoader",
]
