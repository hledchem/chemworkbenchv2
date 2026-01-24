from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple, Callable, Union

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

AGILENT_DETECTORS: List[Tuple[str, DetectorFn]] = []


def _detector_agilent_d(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    # Agilent .d is a directory, often with specific subfiles
    if p.suffix.lower() == ".d" and p.is_dir():
        return True
    return False


def _detector_agilent_dx(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".dx"


def _detector_agilent_uv(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".uv"


def _detector_agilent_sp(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".sp"


AGILENT_DETECTORS.extend(
    [
        ("agilent_d", _detector_agilent_d),
        ("agilent_dx", _detector_agilent_dx),
        ("agilent_uv", _detector_agilent_uv),
        ("agilent_sp", _detector_agilent_sp),
    ]
)
