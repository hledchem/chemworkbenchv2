# chemworkbench/plotting/layer_types/errorbar.py
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
    Render a 2D errorbar layer.

    - Uses index as x if x is missing.
    - Validates x/y length match.
    - Validates error lengths if provided.
    """
    y = _to_array(layer.y)
    if y.size == 0:
        return

    x = _to_array(layer.x)
    if x.size == 0:
        x = np.arange(y.size, dtype=float)

    if x.size != y.size:
        raise ValueError(
            f"Errorbar layer has mismatched x/y lengths: {x.size} vs {y.size}"
        )

    yerr = _to_array(layer.yerr) if layer.yerr is not None else None
    xerr = _to_array(layer.xerr) if layer.xerr is not None else None

    if yerr is not None and yerr.size not in (1, y.size):
        raise ValueError(
            f"Errorbar layer has mismatched yerr length: {yerr.size} vs {y.size}"
        )
    if xerr is not None and xerr.size not in (1, x.size):
        raise ValueError(
            f"Errorbar layer has mismatched xerr length: {xerr.size} vs {x.size}"
        )

    ax.errorbar(
        x,
        y,
        yerr=yerr,
        xerr=xerr,
        label=layer.label,
        color=layer.color,
        linewidth=layer.linewidth,
        linestyle=layer.linestyle,
        marker=layer.marker,
        markersize=layer.markersize,
        alpha=layer.alpha,
        zorder=layer.zorder,
        capsize=2.0,
    )
