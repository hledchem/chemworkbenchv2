"""
CH Instruments vendor-specific loaders.

Includes:
- CHIDTALoader (.DTA electrochemistry files)
"""

from .chi_dta_loader import CHIDTALoader

__all__ = [
    "CHIDTALoader",
]
