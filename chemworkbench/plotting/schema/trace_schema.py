from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TraceSchema:
    """
    Declarative description of a single plot layer/trace.

    This maps closely onto PlotLayerConfig but is higher-level and
    backend-agnostic. It is intended to be JSON-serializable.
    """

    label: Optional[str] = None
    plot_type: str = "line"  # e.g. "line", "scatter", "bar", etc.

    x: List[float] = field(default_factory=list)
    y: List[float] = field(default_factory=list)
    z: Optional[List[float]] = None

    color: Optional[str] = None
    linewidth: Optional[float] = None
    linestyle: Optional[str] = None
    marker: Optional[str] = None
    markersize: Optional[float] = None
    alpha: Optional[float] = None
    zorder: Optional[int] = None
    visible: bool = True

    extra: Dict[str, Any] = field(default_factory=dict)
