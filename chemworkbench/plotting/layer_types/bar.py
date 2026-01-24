# chemworkbench/plotting/layer_types/bar.py
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
    Render a 2D bar layer.

    - Uses index as x if x is missing.
    - Validates x/y length match.
    - Applies width, color, alpha, zorder, label.
    """
    y = _to_array(layer.y)
    if y.size == 0:
        return

    x = _to_array(layer.x)
    if x.size == 0:
        x = np.arange(y.size, dtype=float)

    if x.size != y.size:
        raise ValueError(
            f"Bar layer has mismatched x/y lengths: {x.size} vs {y.size}"
        )

    width = layer.width if layer.width is not None else 0.8

    ax.bar(
        x,
        y,
        width=width,
        label=layer.label,
        color=layer.color,
        alpha=layer.alpha,
        zorder=layer.zorder,
    )
