"""
Agilent vendor-specific loaders.

This package provides loaders for:
- Simple exported UV-Vis files (.UV, .CSV, .TXT)
- Generic Agilent spectral exports (.SP)
- Full Agilent .D directories for UV-Vis
- Full Agilent .D directories for chromatography (HPLC/GC/LC-MS)
- Full Agilent .D directories for MS (LC-MS / GC-MS / MS/MS)

Each loader subclasses BaseVendorLoader and follows the canonical loader API.
"""

from .agilent_uv_loader import AgilentUVLoader
from .agilent_sp_loader import AgilentSPLoader
from .agilent_d_uvvis_loader import AgilentDUVVisLoader
from .agilent_d_chrom_loader import AgilentDChromLoader
from .agilent_d_ms_loader import AgilentDMSLoader

__all__ = [
    "AgilentUVLoader",
    "AgilentSPLoader",
    "AgilentDUVVisLoader",
    "AgilentDChromLoader",
    "AgilentDMSLoader",
]
