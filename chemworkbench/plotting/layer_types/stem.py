# chemworkbench/plotting/layer_types/stem.py
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
    Render a 2D stem layer.

    - Uses index as x if x is missing.
    - Validates x/y length match.
    - Applies color, alpha, zorder, label.
    """
    y = _to_array(layer.y)
    if y.size == 0:
        return

    x = _to_array(layer.x)
    if x.size == 0:
        x = np.arange(y.size, dtype=float)

    if x.size != y.size:
        raise ValueError(
            f"Stem layer has mismatched x/y lengths: {x.size} vs {y.size}"
        )

    markerfmt = layer.marker if layer.marker is not None else "o"
    linefmt = layer.linestyle if layer.linestyle is not None else "-"

    markerline, stemlines, baseline = ax.stem(x, y, linefmt=linefmt, markerfmt=markerfmt)
    if layer.color is not None:
        markerline.set_color(layer.color)
        stemlines.set_color(layer.color)
    markerline.set_alpha(layer.alpha)
    stemlines.set_alpha(layer.alpha)
    if layer.zorder is not None:
        markerline.set_zorder(layer.zorder)
        stemlines.set_zorder(layer.zorder)

    if layer.label:
        markerline.set_label(layer.label)
