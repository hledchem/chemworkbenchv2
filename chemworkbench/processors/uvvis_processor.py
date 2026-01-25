"""
Compatibility shim for UV-Vis processor.

Keeps older imports working:
    from chemworkbench.processors.uvvis_processor import UVVisProcessor

while the real implementation lives in:
    chemworkbench/processors/uvvis/processor.py
"""

from .uvvis.processor import UVVisProcessor

__all__ = ["UVVisProcessor"]
