from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .panel_schema import PanelSchema
from .annotation_schema import AnnotationSchema


@dataclass
class FigureSchema:
    """
    Top-level declarative description of a figure.

    This is the main entry point for the plotting builder.
    """

    id: Optional[str] = None
    title: Optional[str] = None

    backend: str = "matplotlib"
    style_preset: str = "default"

    # Overall layout
    n_rows: int = 1
    n_cols: int = 1

    width: Optional[float] = None  # inches
    height: Optional[float] = None  # inches
    dpi: Optional[int] = None

    panels: List[PanelSchema] = field(default_factory=list)
    annotations: List[AnnotationSchema] = field(default_factory=list)

    extra: Dict[str, Any] = field(default_factory=dict)
