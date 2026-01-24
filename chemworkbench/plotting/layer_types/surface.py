# chemworkbench/plotting/layer_types/surface.py
from __future__ import annotations

from typing import Optional, Union, List

import numpy as np
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from chemworkbench.core.models import PlotLayerConfig, PlotType


def _to_array_2d(values: Optional[Union[List[List[float]], List[float]]]) -> np.ndarray:
    if values is None:
        return np.zeros((0, 0), dtype=float)
    arr = np.asarray(values, dtype=float)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    return arr


def _ensure_3d_axes(ax: Axes) -> Axes:
    """
    Ensure the given axes is 3D. If it's 2D, replace it with a 3D axes
    in the same subplot position.
    """
    if hasattr(ax, "plot_surface"):
        return ax  # already 3D

    fig = ax.figure
    subplotspec = ax.get_subplotspec()
    ax.remove()
    new_ax = fig.add_subplot(subplotspec, projection="3d")
    return new_ax


def render(ax: Axes, layer: PlotLayerConfig) -> None:
    """
    Render 3D layers: line, scatter, surface, wireframe.

    This module is used by the engine for all 3D PlotTypes.
    """
    ax3d = _ensure_3d_axes(ax)

    if layer.plot_type in (PlotType.LINE_3D, PlotType.SCATTER_3D):
        x = np.asarray(layer.x if layer.x is not None else [], dtype=float).ravel()
        y = np.asarray(layer.y if layer.y is not None else [], dtype=float).ravel()
        z = np.asarray(layer.z if layer.z is not None else [], dtype=float).ravel()

        if x.size == 0 or y.size == 0 or z.size == 0:
            return

        if not (x.size == y.size == z.size):
            raise ValueError(
                f"3D line/scatter layer has mismatched x/y/z lengths: "
                f"{x.size}, {y.size}, {z.size}"
            )

        if layer.plot_type == PlotType.LINE_3D:
            ax3d.plot(
                x,
                y,
                z,
                label=layer.label,
                color=layer.color,
                linewidth=layer.linewidth,
                linestyle=layer.linestyle,
                alpha=layer.alpha,
                zorder=layer.zorder,
            )
        else:
            size = layer.markersize if layer.markersize is not None else 20.0
            ax3d.scatter(
                x,
                y,
                z,
                label=layer.label,
                color=layer.color,
                marker=layer.marker,
                s=size,
                alpha=layer.alpha,
                zorder=layer.zorder,
            )

    else:
        # Surface-like: z is 2D, x/y define grid if provided
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
                f"3D surface layer has mismatched x/y vs z shape: "
                f"x={x.size}, y={y.size}, z={z.shape}"
            )

        X, Y = np.meshgrid(x, y)

        if layer.plot_type == PlotType.SURFACE_3D:
            surf = ax3d.plot_surface(
                X,
                Y,
                z,
                cmap=layer.cmap or "viridis",
                alpha=layer.alpha,
            )
            if layer.label:
                surf.set_label(layer.label)
        elif layer.plot_type == PlotType.WIREFRAME_3D:
            wire = ax3d.plot_wireframe(
                X,
                Y,
                z,
                color=layer.color,
                alpha=layer.alpha,
            )
            if layer.label:
                wire.set_label(layer.label)
