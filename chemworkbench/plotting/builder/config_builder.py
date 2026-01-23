from typing import List

from chemworkbench.core.models import PlotConfig, PlotLayerConfig
from chemworkbench.plotting.schema import FigureSchema, PanelSchema, TraceSchema
from .validators import validate_figure_schema


class PlotConfigBuilder:
    """
    Convert a FigureSchema into one or more PlotConfig objects.

    Design choice:
    - Each PanelSchema becomes a separate PlotConfig.
    - Multi-panel figures are represented as a list of PlotConfig objects.
    - Panel layout information is stored in PlotConfig.layout["panel"].
    """

    def build_from_figure(self, figure: FigureSchema) -> List[PlotConfig]:
        validate_figure_schema(figure)

        plot_configs: List[PlotConfig] = []

        for panel in figure.panels:
            layers = [self._build_layer_from_trace(t) for t in panel.traces]

            layout = {
                "panel": {
                    "id": panel.id,
                    "row": panel.row,
                    "col": panel.col,
                    "row_span": panel.row_span,
                    "col_span": panel.col_span,
                    "share_x_with": panel.share_x_with,
                    "share_y_with": panel.share_y_with,
                },
                "figure": {
                    "id": figure.id,
                    "title": figure.title,
                    "n_rows": figure.n_rows,
                    "n_cols": figure.n_cols,
                    "style_preset": figure.style_preset,
                    "width": figure.width,
                    "height": figure.height,
                    "dpi": figure.dpi,
                },
            }

            plot_config = PlotConfig(
                id=panel.id or figure.id,
                title=panel.title or figure.title,
                x_label=panel.x_label,
                y_label=panel.y_label,
                z_label=None,
                backend=figure.backend,
                show_legend=panel.show_legend,
                show_grid=panel.show_grid,
                x_scale=panel.x_scale,
                y_scale=panel.y_scale,
                layers=layers,
                layout=layout,
            )
            plot_configs.append(plot_config)

        return plot_configs

    def _build_layer_from_trace(self, trace: TraceSchema) -> PlotLayerConfig:
        return PlotLayerConfig(
            label=trace.label,
            plot_type=trace.plot_type,
            x=trace.x,
            y=trace.y,
            z=trace.z,
            color=trace.color,
            linewidth=trace.linewidth,
            linestyle=trace.linestyle,
            marker=trace.marker,
            markersize=trace.markersize,
            alpha=trace.alpha,
            zorder=trace.zorder,
            visible=trace.visible,
            extra=trace.extra,
        )
