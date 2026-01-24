# chemworkbench/plotting/layer_types/scatter_3d.py
from __future__ import annotations

from matplotlib.axes import Axes

from chemworkbench.core.models import PlotLayerConfig
from .surface import render as _render_surface


def render(ax: Axes, layer: PlotLayerConfig) -> None:
    """
    3D scatter layer.

    Delegates to the shared 3D surface module, which handles PlotType.SCATTER_3D.
    """
    _render_surface(ax, layer)
