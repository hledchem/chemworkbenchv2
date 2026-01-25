from __future__ import annotations

from typing import List
import matplotlib.pyplot as plt

from chemworkbench.core.models import PipelineResult, PlotConfig
from chemworkbench.plotting.engine import PlotEngine


def show_dashboard(figures):
    """
    Convenience helper for local testing.
    Shows each Matplotlib figure and keeps the window open.
    """
    for fig in figures:
        if fig is not None:
            fig.show()

    # Ensures all figures remain visible until the user closes them
    plt.show()


def render_dashboard(result: PipelineResult):
    """
    Processor-agnostic dashboard renderer.

    Takes a PipelineResult and returns a list of Matplotlib figures
    rendered by the universal PlotEngine.
    """
    if not result.plots:
        raise ValueError("No plots found in PipelineResult.")

    # Render all PlotConfig objects using the universal engine
    figures = PlotEngine.render_all(result.plots)
    return figures
