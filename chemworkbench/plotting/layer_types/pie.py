# chemworkbench/plotting/layer_types/pie.py
from __future__ import annotations

from typing import Optional, List

import numpy as np
from matplotlib.axes import Axes

from chemworkbench.core.models import PlotLayerConfig


def _to_array(values: Optional[list[float]]) -> np.ndarray:
    if values is None:
        return np.array([])
    return np.asarray(values, dtype=float).ravel()


def render(ax: Axes, layer: PlotLayerConfig) -> None:
    """
    Render a pie chart layer.

    - Uses y as values.
    - Uses labels if provided.
    - Uses explode if provided.
    """
    values = _to_array(layer.y)
    if values.size == 0:
        return

    labels: Optional[List[str]] = layer.labels
    explode = None
    if layer.explode is not None:
        explode_arr = np.asarray(layer.explode, dtype=float).ravel()
        if explode_arr.size not in (1, values.size):
            raise ValueError(
                f"Pie layer has mismatched explode length: {explode_arr.size} vs {values.size}"
            )
        if explode_arr.size == 1:
            explode_arr = np.repeat(explode_arr[0], values.size)
        explode = explode_arr

    ax.pie(
        values,
        labels=labels,
        explode=explode,
        autopct="%1.1f%%" if layer.normalize else None,
    )
