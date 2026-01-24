# chemworkbench/plotting/layer_types/heatmap.py
from __future__ import annotations

from typing import Optional, Union, List

import numpy as np
from matplotlib.axes import Axes

from chemworkbench.core.models import PlotLayerConfig


def _to_array_2d(values: Optional[Union[List[List[float]], List[float]]]) -> np.ndarray:
    if values is None:
        return np.zeros((0, 0), dtype=float)
    arr = np.asarray(values, dtype=float)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    return arr


def render(ax: Axes, layer: PlotLayerConfig) -> None:
    """
    Render a heatmap layer.

    - Expects z as 2D array.
    - Uses x/y only for extent if provided.
    """
    z = _to_array_2d(layer.z)
    if z.size == 0:
        return

    cmap = layer.cmap or "viridis"

    extent = None
    if layer.x is not None and layer.y is not None:
        x = np.asarray(layer.x, dtype=float)
        y = np.asarray(layer.y, dtype=float)
        if x.size >= 2 and y.size >= 2:
            extent = (x.min(), x.max(), y.min(), y.max())

    im = ax.imshow(
        z,
        origin="lower",
        aspect="auto",
        cmap=cmap,
        extent=extent,
        alpha=layer.alpha,
        zorder=layer.zorder,
    )

    if layer.label:
        im.set_label(layer.label)
