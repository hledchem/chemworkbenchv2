"""
Plotting Utilities — ChemWorkBench v2.2
=======================================

LLM‑friendly commentary
-----------------------
This module provides lightweight developer‑facing helpers for rendering
plots during local testing or exploratory debugging.

These utilities sit *above* the v2.2 PlotEngine and PlottingService:

    - `render_dashboard` converts a PipelineResult into backend-rendered
      figures using the universal PlotEngine.

    - `show_dashboard` displays Matplotlib figures in a blocking window,
      useful for manual inspection during development.

Responsibilities:
- provide convenience wrappers for local debugging
- support quick visualization of PipelineResult objects
- remain processor‑agnostic and technique‑agnostic

Non‑responsibilities:
- constructing PlotConfig objects (processors do this)
- orchestrating multi‑plot layouts (PlottingService handles this)
- backend‑specific rendering logic (PlotEngine handles this)
"""

from __future__ import annotations

from typing import List, Any
import matplotlib.pyplot as plt

from chemworkbench.core.models import PipelineResult, PlotConfig
from chemworkbench.plotting.engine import PlotEngine


def show_dashboard(figures: List[Any]) -> None:
    """
    Developer convenience helper.

    Displays each Matplotlib figure and keeps the window open until closed.
    Intended for local debugging, not production use.
    """
    for fig in figures:
        if fig is not None:
            fig.show()

    # Ensures all figures remain visible until the user closes them
    plt.show()


def render_dashboard(result: PipelineResult) -> List[Any]:
    """
    Processor‑agnostic dashboard renderer.

    Parameters
    ----------
    result : PipelineResult
        The final output of the ingestion + processing pipeline.

    Returns
    -------
    List[Any]
        A list of backend‑rendered figure objects produced by PlotEngine.

    Notes
    -----
    - This function is intentionally thin: it delegates all normalization
      and rendering logic to PlotEngine.
    - It accepts only PipelineResult, not raw PlotConfig lists, to ensure
      consistency with the v2.2 pipeline contract.
    """
    if not result.plots:
        raise ValueError("No plots found in PipelineResult.")

    # Render all PlotConfig objects using the universal engine
    figures = PlotEngine.render_all(result.plots)
    return figures
