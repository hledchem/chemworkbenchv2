"""
Varian (Agilent/Varian VNMR) vendor-specific loaders.

This package provides loaders for:
- Varian NMR datasets (VNMR/VNMRJ directory format)

Each loader subclasses BaseVendorLoader and follows the canonical loader API.
"""

from .varian_nmr_loader import VarianNMRLoader

__all__ = [
    "VarianNMRLoader",
]
