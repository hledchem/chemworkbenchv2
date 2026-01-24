"""
Raman-specific loaders.

This package provides loaders for:
- DPT Raman spectra
- RRUFF Raman spectra
- RRUFF.GZ compressed Raman spectra

Each loader subclasses BaseVendorLoader and follows the canonical loader API.
"""

from .dpt_loader import DPTLoader
from .rruf_loader import RRUFFLoader
from .rruf_gz_loader import RRUFFGZLoader

__all__ = [
    "DPTLoader",
    "RRUFFLoader",
    "RRUFFGZLoader",
]
