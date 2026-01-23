from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AnnotationSchema:
    """
    Text/arrow annotations attached to a panel or figure.
    """

    text: str
    x: float
    y: float

    panel_id: Optional[str] = None  # None = figure-level

    arrow: bool = False
    extra: Dict[str, Any] = field(default_factory=dict)
