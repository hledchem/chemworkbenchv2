from __future__ import annotations

from typing import Callable, Dict, Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from chemworkbench.core.models import (
    PlotBackend,
    PlotConfig,
    PlotLayerConfig,
    PlotType,
)
from chemworkbench.plotting.engine.base_engine import BasePlotEngine
from chemworkbench.plotting.layer_types import (
    line,
    scatter,
    bar,
    stem,
    step,
    errorbar,
    heatmap,
    contour,
    image,
    surface,
)


# --------------------------------------------------------------------
# Layer renderer registry
# --------------------------------------------------------------------

LayerRenderer = Callable[[Axes, PlotLayerConfig], None]


LAYER_RENDERERS: Dict[PlotType, LayerRenderer] = {
    PlotType.LINE: line.render,
    PlotType.SCATTER: scatter.render,
    PlotType.BAR: bar.render,
    PlotType.STEM: stem.render,
    PlotType.STEP: step.render,
    PlotType.ERRORBAR: errorbar.render,
    PlotType.HEATMAP: heatmap.render,
    PlotType.CONTOUR: contour.render,
    PlotType.IMAGE: image.render,
    # 3D / surface-like plots
    PlotType.SURFACE_3D: surface.render,
    PlotType.LINE_3D: surface.render,
    PlotType.SCATTER_3D: surface.render,
    PlotType.WIREFRAME_3D: surface.render,
    # These can be implemented later in dedicated modules:
    # PlotType.PIE: pie.render,
    # PlotType.HISTOGRAM: histogram.render,
}


# --------------------------------------------------------------------
# Matplotlib plotting engine
# --------------------------------------------------------------------

class MatplotlibEngine(BasePlotEngine):
    """
    Matplotlib-based plotting engine for ChemWorkBench.

    This engine consumes PlotConfig objects and renders them using
    Matplotlib, including support for multi-panel figures via the
    (nrows, ncols) grid and per-layer `panel` indices.
    """

    def render(self, plot_config: PlotConfig) -> Figure:
        """
        Render a PlotConfig into a Matplotlib Figure.

        Returns
        -------
        fig : matplotlib.figure.Figure
        """
        if plot_config.backend not in (PlotBackend.MATPLOTLIB, PlotBackend.NONE):
            raise ValueError(
                f"MatplotlibEngine cannot handle backend '{plot_config.backend.value}'"
            )

        fig, axes = self._create_figure_and_axes(plot_config)

        # Normalize axes to a 2D array for consistent indexing
        if isinstance(axes, Axes):
            axes_grid = [[axes]]
        else:
            axes_grid = axes

        # Render each layer on its assigned panel
        for layer in plot_config.layers:
            if not layer.visible:
                continue

            ax = self._select_axes_for_layer(
                axes_grid,
                layer.panel,
                plot_config.nrows,
                plot_config.ncols,
            )

            self._apply_axes_scales_and_limits(ax, plot_config)
            self._render_layer(ax, layer)

        # Apply labels and title to the first axes by default
        first_ax = axes_grid[0][0]
        self._apply_labels_and_title(first_ax, plot_config)

        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _create_figure_and_axes(
        self, plot_config: PlotConfig
    ) -> Tuple[Figure, Axes | list[list[Axes]]]:
        """
        Create a Matplotlib figure and axes grid based on PlotConfig.
        """
        nrows = max(1, plot_config.nrows)
        ncols = max(1, plot_config.ncols)

        fig, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=plot_config.figsize,
            sharex=plot_config.sharex,
            sharey=plot_config.sharey,
            squeeze=False,
        )

        return fig, axes

    def _select_axes_for_layer(
        self,
        axes_grid: list[list[Axes]],
        panel_index: int,
        nrows: int,
        ncols: int,
    ) -> Axes:
        """
        Map a layer's panel index to a specific Axes in the grid.
        """
        if panel_index < 0:
            panel_index = 0

        max_panels = nrows * ncols
        if panel_index >= max_panels:
            panel_index = max_panels - 1

        row = panel_index // ncols
        col = panel_index % ncols

        return axes_grid[row][col]

    def _apply_axes_scales_and_limits(self, ax: Axes, plot_config: PlotConfig) -> None:
        """
        Apply axis scales and limits from PlotConfig to a given Axes.
        """
        ax.set_xscale(plot_config.x_scale)
        ax.set_yscale(plot_config.y_scale)

        if plot_config.x_limits is not None:
            ax.set_xlim(*plot_config.x_limits)
        if plot_config.y_limits is not None:
            ax.set_ylim(*plot_config.y_limits)

    def _apply_labels_and_title(self, ax: Axes, plot_config: PlotConfig) -> None:
        """
        Apply axis labels and title to a given Axes.
        """
        if plot_config.x_label:
            ax.set_xlabel(plot_config.x_label)
        if plot_config.y_label:
            ax.set_ylabel(plot_config.y_label)
        if plot_config.title:
            ax.set_title(plot_config.title)

    def _render_layer(self, ax: Axes, layer: PlotLayerConfig) -> None:
        """
        Dispatch rendering of a single layer to the appropriate renderer.
        """
        renderer = LAYER_RENDERERS.get(layer.plot_type)
        if renderer is None:
            raise ValueError(f"No renderer registered for plot_type '{layer.plot_type.value}'")

        renderer(ax, layer)
