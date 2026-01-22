from __future__ import annotations

import numpy as np
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

        # Multi-panel support
        if plot.nrows > 1 or plot.ncols > 1:
            fig, axes = plt.subplots(
                nrows=plot.nrows,
                ncols=plot.ncols,
                figsize=plot.figsize,
                sharex=plot.sharex,
                sharey=plot.sharey,
            )
            axes = np.array(axes).reshape(-1).tolist()
        else:
            if plot.is_3d:
                fig = plt.figure(figsize=plot.figsize)
                axes = [fig.add_subplot(111, projection="3d")]
            else:
                fig, ax = plt.subplots(figsize=plot.figsize)
                axes = [ax]

        # Apply global title only if single panel
        if plot.nrows == 1 and plot.ncols == 1:
            axes[0].set_title(plot.title)

        configured = set()

        for layer in plot.layers:
            idx = max(0, min(layer.panel, len(axes) - 1))
            ax = axes[idx]

            if idx not in configured:
                MatplotlibEngine._configure_axes(ax, plot, layer, is_main=(idx == 0))
                configured.add(idx)

            MatplotlibEngine._render_layer(ax, layer)

        # Add legends where appropriate
        for ax in axes:
            handles, labels = ax.get_legend_handles_labels()
            if handles:
                ax.legend()

        fig.tight_layout()
        return fig

    @staticmethod
    def _configure_axes(ax, plot: PlotConfig, layer: PlotLayerConfig, is_main: bool):
        # Only main panel gets labels if shared axes
        if is_main or not (plot.sharex or plot.sharey):
            ax.set_xlabel(plot.x_label)
            ax.set_ylabel(plot.y_label)
            if plot.is_3d and plot.z_label:
                ax.set_zlabel(plot.z_label)

        ax.set_xscale(plot.x_scale)
        ax.set_yscale(plot.y_scale)
        if plot.is_3d:
            ax.set_zscale(plot.z_scale)

        if plot.x_limits:
            ax.set_xlim(*plot.x_limits)
        if plot.y_limits:
            ax.set_ylim(*plot.y_limits)
        if plot.z_limits and plot.is_3d:
            ax.set_zlim(*plot.z_limits)

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
