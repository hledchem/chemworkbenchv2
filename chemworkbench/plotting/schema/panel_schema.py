from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .trace_schema import TraceSchema


@dataclass
class PanelSchema:
    """
    A single panel (axes) within a figure.

    Panels can be arranged in a grid via row/col indices and spans.
    """

    id: Optional[str] = None
    title: Optional[str] = None

    x_label: Optional[str] = None
    y_label: Optional[str] = None

    x_scale: str = "linear"  # "linear", "log"
    y_scale: str = "linear"

    show_legend: bool = True
    show_grid: bool = True

    # Layout within a grid
    row: int = 0
    col: int = 0
    row_span: int = 1
    col_span: int = 1

    # Axis sharing (by panel id)
    share_x_with: Optional[str] = None
    share_y_with: Optional[str] = None

    traces: List[TraceSchema] = field(default_factory=list)

    extra: Dict[str, Any] = field(default_factory=dict)
