from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple, Callable, Union

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

JEOL_DETECTORS: List[Tuple[str, DetectorFn]] = []


def _detector_jeol_jdf(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".jdf"


def _detector_jeol_jdx(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".jdx"


JEOL_DETECTORS.extend(
    [
        ("jeol_jdf", _detector_jeol_jdf),
        ("jeol_jdx", _detector_jeol_jdx),
    ]
)
