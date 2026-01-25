"""
services/plotting_service.py

High-level plotting service for ChemWorkBench v2.

This service:
    - Accepts a list of PlotConfig objects
    - Delegates rendering to the plotting engine
    - Returns backend-rendered figures or UI-ready payloads

The pipeline calls:
    plotting_service.render(processed.plots)
"""

from __future__ import annotations
from typing import List, Any

from chemworkbench.core.models import PlotConfig
from chemworkbench.plotting.engine import PlotEngine
from chemworkbench.runtime.logging import get_logger
from chemworkbench.runtime.errors import PipelineError


logger = get_logger(__name__)


class PlottingService:
    """
    High-level wrapper around the plotting engine.

    Responsibilities:
        - Validate PlotConfig objects
        - Call the backend-agnostic PlotEngine
        - Return rendered figures or UI payloads
    """

    def __init__(self):
        self.engine = PlotEngine()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self, plots: List[PlotConfig]) -> List[Any]:
        """
        Render a list of PlotConfig objects using the plotting engine.

        Returns:
            A list of backend-rendered figure objects or UI payloads.
        """

        if not isinstance(plots, list):
            raise PipelineError("PlottingService.render expected a list of PlotConfig objects")

        logger.debug(f"Rendering {len(plots)} plot(s)")

        rendered = []

        for idx, plot_cfg in enumerate(plots):
            if not isinstance(plot_cfg, PlotConfig):
                raise PipelineError(f"Invalid plot config at index {idx}: {plot_cfg}")

            try:
                fig = self.engine.render(plot_cfg)
                rendered.append(fig)
            except Exception as exc:
                raise PipelineError(f"Plot rendering failed for plot {idx}: {exc}") from exc

        logger.debug("PlottingService completed rendering")

        return rendered
