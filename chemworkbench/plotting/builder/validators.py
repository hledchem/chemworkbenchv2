"""
Lightweight validation helpers for plotting schemas.

These are intentionally simple and do not introduce external dependencies.
"""

from typing import List

from chemworkbench.plotting.schema import FigureSchema, PanelSchema, TraceSchema


def validate_trace_schema(trace: TraceSchema) -> None:
    if trace.plot_type not in {
        "line",
        "scatter",
        "bar",
        "stem",
        "step",
        "errorbar",
        "heatmap",
        "contour",
        "image",
        "surface",
    }:
        raise ValueError(f"Unsupported plot_type: {trace.plot_type}")

    if len(trace.x) != len(trace.y):
        raise ValueError("TraceSchema.x and TraceSchema.y must have the same length")


def validate_panel_schema(panel: PanelSchema) -> None:
    if panel.row < 0 or panel.col < 0:
        raise ValueError("PanelSchema.row and col must be non-negative")

    if panel.row_span <= 0 or panel.col_span <= 0:
        raise ValueError("PanelSchema.row_span and col_span must be positive")

    for trace in panel.traces:
        validate_trace_schema(trace)


def validate_figure_schema(figure: FigureSchema) -> None:
    if figure.n_rows <= 0 or figure.n_cols <= 0:
        raise ValueError("FigureSchema.n_rows and n_cols must be positive")

    for panel in figure.panels:
        validate_panel_schema(panel)
