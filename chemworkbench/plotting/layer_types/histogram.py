# chemworkbench/plotting/layer_types/histogram.py
from __future__ import annotations

from typing import Optional

import numpy as np
from matplotlib.axes import Axes

from chemworkbench.core.models import PlotLayerConfig


def _to_array(values: Optional[list[float]]) -> np.ndarray:
    if values is None:
        return np.array([])
    return np.asarray(values, dtype=float).ravel()


def render(ax: Axes, layer: PlotLayerConfig) -> None:
    """
    Render a histogram layer.

    - Uses y as data; x is ignored (histogram of y).
    - Applies bins, stacked (ignored for single layer), color, alpha, zorder, label.
    """
    data = _to_array(layer.y)
    if data.size == 0:
        return

    bins = layer.bins if layer.bins is not None else "auto"

    ax.hist(
        data,
        bins=bins,
        label=layer.label,
        color=layer.color,
        alpha=layer.alpha,
        zorder=layer.zorder,
    )
