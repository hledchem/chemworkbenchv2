# chemworkbench/plotting/layer_types/step.py
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
    Render a 2D step layer.

    - Uses index as x if x is missing.
    - Validates x/y length match.
    - Applies styling, alpha, zorder, label.
    """
    y = _to_array(layer.y)
    if y.size == 0:
        return

    x = _to_array(layer.x)
    if x.size == 0:
        x = np.arange(y.size, dtype=float)

    if x.size != y.size:
        raise ValueError(
            f"Step layer has mismatched x/y lengths: {x.size} vs {y.size}"
        )

    ax.step(
        x,
        y,
        label=layer.label,
        color=layer.color,
        linewidth=layer.linewidth,
        linestyle=layer.linestyle,
        alpha=layer.alpha,
        where="mid",
        zorder=layer.zorder,
    )
