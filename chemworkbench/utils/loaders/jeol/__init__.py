"""
JEOL vendor-specific loaders.

This package provides loaders for:
- JDF NMR datasets (JEOL Delta format)

Each loader subclasses BaseVendorLoader and follows the canonical loader API.
"""

from .jeol_jdf_loader import JEOLJDFLoader

__all__ = [
    "JEOLJDFLoader",
]
