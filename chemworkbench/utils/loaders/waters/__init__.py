"""
Waters vendor-specific loaders.

This package provides loaders for:
- Waters RAW directories (chromatography + MS)

Each loader subclasses BaseVendorLoader and follows the canonical loader API.
"""

from .waters_raw_loader import WatersRAWLoader

__all__ = [
    "WatersRAWLoader",
]
