"""
Plotting Service — ChemWorkBench v2.2
=====================================

LLM‑friendly commentary
-----------------------
This module provides the canonical high‑level plotting service for
ChemWorkBench v2.2. It acts as a thin orchestration layer between the
pipeline and the backend‑agnostic PlotEngine.

Responsibilities:
- accept a list of PlotConfig objects from processors
- validate plot configuration objects
- delegate rendering to the PlotEngine
- return backend‑rendered figures or UI‑ready payloads

Non‑responsibilities:
- constructing PlotConfig objects (handled by processors)
- scientific interpretation (handled by processors)
- backend‑specific rendering logic (handled by PlotEngine)
"""

from __future__ import annotations

from typing import List, Any

from chemworkbench.core.models import PlotConfig
from chemworkbench.plotting.engine import PlotEngine
from chemworkbench.runtime.logging import get_logger
from chemworkbench.runtime.errors import PipelineError


logger = get_logger(__name__)


# ======================================================================
# Plotting Service (v2.2)
# ======================================================================

class PlottingService:
    """
    High‑level wrapper around the backend‑agnostic PlotEngine.

    This service:
        - validates PlotConfig objects
        - delegates rendering to PlotEngine
        - returns backend‑specific figure objects or UI‑ready payloads
    """

    def __init__(self):
        self.engine = PlotEngine()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def render(self, plots: List[Any]) -> List[Any]:
    """
    Render a list of plot payloads or PlotConfig objects.

    Processors emit raw dicts.
    UI/CLI may emit PlotConfig objects.
    This method normalizes both into PlotConfig.
    """
    if not isinstance(plots, list):
        raise PipelineError("PlottingService.render expected a list")

    logger.debug(f"Rendering {len(plots)} plot(s)")

    rendered = []

    for idx, plot in enumerate(plots):
        # Accept raw dicts from processors
        if isinstance(plot, dict):
            try:
                plot_cfg = PlotConfig(**plot)
            except Exception as exc:
                raise PipelineError(
                    f"Invalid plot payload at index {idx}: {exc}"
                ) from exc

        # Accept PlotConfig objects from UI/CLI
        elif isinstance(plot, PlotConfig):
            plot_cfg = plot

        else:
            raise PipelineError(
                f"Invalid plot config at index {idx}: {plot}"
            )

        try:
            fig = self.engine.render(plot_cfg)
            rendered.append(fig)
        except Exception as exc:
            raise PipelineError(
                f"Plot rendering failed for plot {idx}: {exc}"
            ) from exc

    logger.debug("PlottingService completed rendering")
    return rendered
