# chemworkbench/plotting/layer_types/contour.py
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
    Render a contour layer.

    - Expects z as 2D array.
    - Uses x/y as coordinates if provided.
    """
    z = _to_array_2d(layer.z)
    if z.size == 0:
        return

    ny, nx = z.shape

    if layer.x is not None:
        x = np.asarray(layer.x, dtype=float)
    else:
        x = np.arange(nx, dtype=float)

    if layer.y is not None:
        y = np.asarray(layer.y, dtype=float)
    else:
        y = np.arange(ny, dtype=float)

    if x.size != nx or y.size != ny:
        raise ValueError(
            f"Contour layer has mismatched x/y vs z shape: "
            f"x={x.size}, y={y.size}, z={z.shape}"
        )

    X, Y = np.meshgrid(x, y)

    cs = ax.contourf(
        X,
        Y,
        z,
        cmap=layer.cmap or "viridis",
        alpha=layer.alpha,
        zorder=layer.zorder,
    )

    if layer.label and cs.collections:
        cs.collections[0].set_label(layer.label)
