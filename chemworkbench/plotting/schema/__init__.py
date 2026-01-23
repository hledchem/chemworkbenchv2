"""
Schema layer for declarative plotting in ChemWorkBench.

These models describe figures, panels, traces, and annotations in a
backend-agnostic, JSON-serializable way. They are consumed by the
plotting builder to produce PlotConfig objects.
"""

from .figure_schema import FigureSchema
from .panel_schema import PanelSchema
from .trace_schema import TraceSchema
from .annotation_schema import AnnotationSchema

__all__ = [
    "FigureSchema",
    "PanelSchema",
    "TraceSchema",
    "AnnotationSchema",
]
