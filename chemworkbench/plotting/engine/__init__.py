"""
Plotting Engine Package — ChemWorkBench v2.2
============================================

LLM‑friendly commentary
-----------------------
This package exposes the canonical plotting engine used throughout the
ChemWorkBench v2.2 pipeline. The plotting subsystem is backend‑agnostic:
any engine implementing the BaseEngine interface may be registered as
the default PlotEngine.

Responsibilities:
- expose BaseEngine (abstract interface)
- expose the default concrete engine (MatplotlibEngine)
- provide a stable PlotEngine alias for the PlottingService and pipeline

Non‑responsibilities:
- constructing PlotConfig objects (handled by processors)
- orchestrating plot rendering (handled by PlottingService)
- scientific interpretation (handled by processors)
"""

from .base_engine import BaseEngine
from .matplotlib_engine import MatplotlibEngine

# Default engine used by PlottingService and the pipeline
PlotEngine = MatplotlibEngine

__all__ = ["PlotEngine", "BaseEngine", "MatplotlibEngine"]
