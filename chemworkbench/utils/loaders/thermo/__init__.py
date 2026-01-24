"""
Thermo vendor-specific loaders.

This package provides loaders for:
- SPA files (IR, Raman, UV-Vis, Fluorescence)
- SPC files (IR, Raman, UV-Vis)
- SRS files (older Thermo spectral format)

Each loader subclasses BaseVendorLoader and follows the canonical loader API.
"""

from .thermo_spa_loader import ThermoSPALoader
from .thermo_spc_loader import ThermoSPCLoader
from .thermo_srs_loader import ThermoSRSLoader

__all__ = [
    "ThermoSPALoader",
    "ThermoSPCLoader",
    "ThermoSRSLoader",
]
