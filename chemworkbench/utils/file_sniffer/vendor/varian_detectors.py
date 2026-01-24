from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple, Callable, Union

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

VARIAN_DETECTORS: List[Tuple[str, DetectorFn]] = []


def _detector_varian_nmr_dir(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    if not p.is_dir():
        return False
    fid = p / "fid"
    procpar = p / "procpar"
    return fid.exists() and procpar.exists()


VARIAN_DETECTORS.extend(
    [
        ("varian_nmr", _detector_varian_nmr_dir),
    ]
)
