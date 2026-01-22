from __future__ import annotations

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from chemworkbench.core.models import PlotConfig, PlotLayerConfig, PlotType
from chemworkbench.plotting.style_presets.default import apply_default_style
from chemworkbench.plotting.layer_types import (
    render_line,
    render_scatter,
    render_bar,
    render_stem,
    render_step,
    render_errorbar,
    render_heatmap,
    render_contour,
    render_image,
    render_pie,
    render_histogram,
    render_3d_line,
    render_3d_scatter,
    render_3d_surface,
    render_3d_wireframe,
)


class MatplotlibEngine:
    """Matplotlib backend for rendering PlotConfig objects."""

    @staticmethod
    def render(plot: PlotConfig):
        apply_default_style()

        if plot.is_3d:
            fig = plt.figure(figsize=plot.figsize)
            ax = fig.add_subplot(111, projection="3d")
        else:
            fig, ax = plt.subplots(figsize=plot.figsize)

        ax.set_title(plot.title)
        ax.set_xlabel(plot.x_label)
        ax.set_ylabel(plot.y_label)

        for layer in plot.layers:
            MatplotlibEngine._render_layer(ax, layer)

        fig.tight_layout()
        return fig

    @staticmethod
    def _render_layer(ax, layer: PlotLayerConfig):
        if layer.plot_type == PlotType.LINE:
            return render_line(ax, layer)
        if layer.plot_type == PlotType.SCATTER:
            return render_scatter(ax, layer)
        if layer.plot_type == PlotType.BAR:
            return render_bar(ax, layer)
        if layer.plot_type == PlotType.STEM:
            return render_stem(ax, layer)
        if layer.plot_type == PlotType.STEP:
            return render_step(ax, layer)
        if layer.plot_type == PlotType.ERRORBAR:
            return render_errorbar(ax, layer)
        if layer.plot_type == PlotType.HEATMAP:
            return render_heatmap(ax, layer)
        if layer.plot_type == PlotType.CONTOUR:
            return render_contour(ax, layer)
        if layer.plot_type == PlotType.IMAGE:
            return render_image(ax, layer)
        if layer.plot_type == PlotType.PIE:
            return render_pie(ax, layer)
        if layer.plot_type == PlotType.HISTOGRAM:
            return render_histogram(ax, layer)
        if layer.plot_type == PlotType.LINE_3D:
            return render_3d_line(ax, layer)
        if layer.plot_type == PlotType.SCATTER_3D:
            return render_3d_scatter(ax, layer)
        if layer.plot_type == PlotType.SURFACE_3D:
            return render_3d_surface(ax, layer)
        if layer.plot_type == PlotType.WIREFRAME_3D:
            return render_3d_wireframe(ax, layer)

        raise ValueError(f"Unsupported plot type: {layer.plot_type}")
