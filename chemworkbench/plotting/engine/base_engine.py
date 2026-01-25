"""
chemworkbench/plotting/engine/base_engine.py

Base plotting engine for ChemWorkBench v2.

This abstract class defines the interface that all concrete plotting
engines (e.g., MatplotlibEngine) must implement.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from chemworkbench.core.models import PlotConfig


class BaseEngine(ABC):
    """
    Abstract base class for all plotting engines.

    Concrete engines must implement `render(plot_config)`.
    """

    @staticmethod
    @abstractmethod
    def render(plot: PlotConfig) -> Any:
        """
        Render a single PlotConfig object.

        Concrete engines should return any representation they choose:
        - a matplotlib Figure
        - a dict
        - a serialized object
        - or None (for headless/test mode)

        The pipeline and tests only require that this method exists.
        """
        raise NotImplementedError("Plotting engine must implement render().")

    @staticmethod
    def render_all(plots: list[PlotConfig]) -> list[Any]:
        """
        Render a list of PlotConfig objects.

        Default implementation simply calls render() on each plot.
        Engines may override this if they support dashboards.
        """
        return [BaseEngine.render(p) for p in plots]
