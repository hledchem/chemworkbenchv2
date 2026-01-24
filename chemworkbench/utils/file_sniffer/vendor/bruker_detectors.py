from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple, Callable, Union

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

BRUKER_DETECTORS: List[Tuple[str, DetectorFn]] = []


def _detector_bruker_opus(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    # OPUS often uses .0, .1, .2, .3; we treat any of these as OPUS
    if p.suffix.lower() in {".0", ".1", ".2", ".3"}:
        return True
    return False


def _detector_bruker_nmr_dir(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    # Bruker NMR: directory with 'fid' or 'ser' and 'acqus'
    if not p.is_dir():
        return False
    fid = p / "fid"
    ser = p / "ser"
    acqus = p / "acqus"
    return acqus.exists() and (fid.exists() or ser.exists())


BRUKER_DETECTORS.extend(
    [
        ("bruker_opus", _detector_bruker_opus),
        ("bruker_nmr", _detector_bruker_nmr_dir),
    ]
)
