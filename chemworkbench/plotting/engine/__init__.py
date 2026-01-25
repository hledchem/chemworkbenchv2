"""
Plotting engine package for ChemWorkBench v2.

Exposes the default PlotEngine implementation and the base class.
"""

from .base_engine import BaseEngine
from .matplotlib_engine import MatplotlibEngine

# Default engine used by PlottingService and the pipeline
PlotEngine = MatplotlibEngine

__all__ = ["PlotEngine", "BaseEngine", "MatplotlibEngine"]
