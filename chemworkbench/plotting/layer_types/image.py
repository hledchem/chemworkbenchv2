# chemworkbench/plotting/layer_types/image.py
from __future__ import annotations

from typing import Optional, Union, List

import numpy as np
from matplotlib.axes import Axes

from chemworkbench.core.models import PlotLayerConfig


def _to_array_image(values: Optional[Union[List[List[float]], List[float]]]) -> np.ndarray:
    if values is None:
        return np.zeros((0, 0), dtype=float)
    arr = np.asarray(values)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    return arr


def render(ax: Axes, layer: PlotLayerConfig) -> None:
    """
    Render an image layer.

    - Expects z as 2D or 3D array (grayscale or RGB).
    """
    z = _to_array_image(layer.z)
    if z.size == 0:
        return

    im = ax.imshow(
        z,
        origin="upper",
        aspect="equal",
        alpha=layer.alpha,
        zorder=layer.zorder,
        cmap=layer.cmap,
    )

    if layer.label:
        im.set_label(layer.label)
