"""
api/run_plotting.py

API entrypoint for rendering plots from PlotConfig objects.

This module provides a clean interface for:
    - UI components requesting plot rendering
    - Notebook workflows
    - HTTP API endpoints
    - CLI commands

It delegates actual rendering to:
    - PlottingService
"""

from __future__ import annotations
from typing import List, Any

from chemworkbench.core.models import PlotConfig
from chemworkbench.services.plotting_service import PlottingService
from chemworkbench.runtime.errors import PipelineError
from chemworkbench.runtime.logging import get_logger


logger = get_logger(__name__)

plotting_service = PlottingService()


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------

def run_plotting(plot_configs: List[PlotConfig]) -> List[Any]:
    """
    Render a list of PlotConfig objects using the plotting service.

    Returns:
        A list of backend-rendered figure objects or UI payloads.
    """

    if not isinstance(plot_configs, list):
        raise PipelineError("run_plotting expected a list of PlotConfig objects")

    logger.info(f"API: Rendering {len(plot_configs)} plot(s)")

    try:
        return plotting_service.render(plot_configs)
    except Exception as exc:
        raise PipelineError(f"Plotting failed: {exc}") from exc
