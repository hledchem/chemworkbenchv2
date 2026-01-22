from __future__ import annotations

from typing import List

from chemworkbench.core.models import PlotConfig, PlotLayerConfig, PlotBackend
from chemworkbench.plotting.engine.matplotlib_engine import MatplotlibEngine


class PlotEngine:
    """Universal entry point for rendering PlotConfig objects."""

    @staticmethod
    def render(plot: PlotConfig):
        if plot.backend == PlotBackend.NONE:
            return None

        if plot.backend == PlotBackend.MATPLOTLIB:
            return MatplotlibEngine.render(plot)

        raise ValueError(f"Unsupported backend: {plot.backend}")

    @staticmethod
    def render_all(plots: List[PlotConfig]):
        return [PlotEngine.render(p) for p in plots]
