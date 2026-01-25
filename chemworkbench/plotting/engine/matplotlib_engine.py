"""
chemworkbench/plotting/engine/matplotlib_engine.py

Matplotlib-based renderer for ChemWorkBench v2.
This implementation is intentionally minimal so that the pipeline
and tests can run without requiring a full plotting subsystem.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt

from chemworkbench.core.models import PlotConfig


class MatplotlibEngine:
    """
    Minimal Matplotlib renderer for PlotConfig objects.
    """

    @staticmethod
    def render(plot: PlotConfig) -> Dict[str, Any]:
        """
        Render a single PlotConfig using Matplotlib.

        Returns a dictionary containing the figure and axes so that
        tests and downstream code can inspect the result.
        """

        fig, ax = plt.subplots()

        # Basic XY plot
        if plot.x is not None and plot.y is not None:
            ax.plot(
                plot.x,
                plot.y,
                **plot.style,
            )

        # Apply title
        if plot.title:
            ax.set_title(plot.title)

        # Apply metadata-driven layers (optional)
        layers = plot.metadata.get("layers", [])
        for layer in layers:
            MatplotlibEngine._render_layer(ax, layer)

        return {
            "figure": fig,
            "axes": ax,
            "metadata": plot.metadata,
        }

    @staticmethod
    def _render_layer(ax, layer: Dict[str, Any]):
        """
        Render a single layer from metadata.
        """

        x = layer.get("x")
        y = layer.get("y")
        if x is None or y is None:
            return

        plot_type = layer.get("plot_type", "line")

        if plot_type == "line":
            ax.plot(
                x,
                y,
                color=layer.get("color"),
                linewidth=layer.get("linewidth", 1.0),
                alpha=layer.get("alpha", 1.0),
            )
        elif plot_type == "scatter":
            ax.scatter(
                x,
                y,
                color=layer.get("color"),
                alpha=layer.get("alpha", 1.0),
            )
        # Additional plot types can be added here

    @staticmethod
    def render_all(plots: List[PlotConfig]) -> List[Any]:
        """
        Render a list of PlotConfig objects.
        """
        return [MatplotlibEngine.render(p) for p in plots]
