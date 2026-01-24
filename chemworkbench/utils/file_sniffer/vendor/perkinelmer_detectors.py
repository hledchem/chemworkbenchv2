from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple, Callable, Union

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

PERKINELMER_DETECTORS: List[Tuple[str, DetectorFn]] = []


def _detector_perkinelmer_spc(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".spc"


def _detector_perkinelmer_sp(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".sp"


PERKINELMER_DETECTORS.extend(
    [
        ("perkinelmer_spc", _detector_perkinelmer_spc),
        ("perkinelmer_sp", _detector_perkinelmer_sp),
    ]
)
