"""
Default values and helpers for plotting configuration.
"""

from typing import Dict, Any


def get_default_figure_kwargs() -> Dict[str, Any]:
    return {
        "backend": "matplotlib",
        "style_preset": "default",
        "n_rows": 1,
        "n_cols": 1,
    }


def get_default_panel_kwargs() -> Dict[str, Any]:
    return {
        "x_scale": "linear",
        "y_scale": "linear",
        "show_legend": True,
        "show_grid": True,
    }


def get_default_trace_kwargs() -> Dict[str, Any]:
    return {
        "plot_type": "line",
        "visible": True,
    }
