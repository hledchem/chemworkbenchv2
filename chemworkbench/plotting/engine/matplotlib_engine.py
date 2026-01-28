"""
Matplotlib Plotting Engine — ChemWorkBench v2.2
===============================================

LLM‑friendly commentary
-----------------------
This module implements the canonical Matplotlib-based rendering engine
for ChemWorkBench v2.2. It consumes PlotConfig objects produced by
processors and returns backend-rendered figure payloads suitable for
tests, UI layers, or downstream services.

Responsibilities:
- render a single PlotConfig deterministically
- support universal x/y plotting
- support optional multi-layer rendering
- return a backend-agnostic figure payload

Non‑responsibilities:
- constructing PlotConfig objects (handled by processors)
- orchestrating plot rendering (handled by PlottingService)
- scientific interpretation (handled by processors)
"""

from __future__ import annotations

from typing import Any, Dict, List

import matplotlib.pyplot as plt

from chemworkbench.core.models import PlotConfig


# ======================================================================
# Matplotlib Rendering Engine (v2.2)
# ======================================================================

class MatplotlibEngine:
    """
    Minimal, deterministic Matplotlib renderer for PlotConfig objects.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @staticmethod
    def render(plot: PlotConfig) -> Dict[str, Any]:
        """
        Render a single PlotConfig using Matplotlib.

        Returns:
            A dictionary containing:
                - "figure": Matplotlib Figure
                - "axes": Matplotlib Axes
                - "metadata": plot metadata (unchanged)
        """
        fig, ax = plt.subplots()

        # --------------------------------------------------------------
        # Primary XY plot
        # --------------------------------------------------------------
        if plot.x is not None and plot.y is not None:
            ax.plot(
                plot.x,
                plot.y,
                **plot.style,
            )

        # --------------------------------------------------------------
        # Title
        # --------------------------------------------------------------
        if plot.title:
            ax.set_title(plot.title)

        # --------------------------------------------------------------
        # Optional multi-layer rendering
        # --------------------------------------------------------------
        layers = plot.metadata.get("layers", [])
        for layer in layers:
            MatplotlibEngine._render_layer(ax, layer)

        return {
            "figure": fig,
            "axes": ax,
            "metadata": plot.metadata,
        }

    # ------------------------------------------------------------------
    # Internal layer renderer
    # ------------------------------------------------------------------
    @staticmethod
    def _render_layer(ax, layer: Dict[str, Any]):
        """
        Render a single layer from metadata.

        Expected layer structure:
            {
                "plot_type": "line" | "scatter",
                "x": [...],
                "y": [...],
                "color": "...",
                "linewidth": float,
                "alpha": float,
            }
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

        # Additional plot types can be added here as needed.

    # ------------------------------------------------------------------
    # Convenience: render multiple plots
    # ------------------------------------------------------------------
    @staticmethod
    def render_all(plots: List[PlotConfig]) -> List[Any]:
        """
        Render a list of PlotConfig objects.
        """
        return [MatplotlibEngine.render(p) for p in plots]
