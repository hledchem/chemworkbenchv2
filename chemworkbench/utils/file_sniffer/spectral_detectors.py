from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple, Callable, Union

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

SPECTRAL_DETECTORS: List[Tuple[str, DetectorFn]] = []


def _detector_jcamp_dx(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    if p.suffix.lower() in {".dx", ".jdx"}:
        return True
    if raw_bytes is None:
        return False
    head = raw_bytes[:4096].decode(errors="ignore").upper()
    return "##TITLE=" in head and "##XUNITS=" in head


def _detector_spc(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    if p.suffix.lower() == ".spc":
        return True
    # SPC has a specific binary header; for now, rely on extension.
    return False


def _detector_spa(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".spa"


def _detector_sp(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".sp"


def _detector_uv(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".uv"


def _detector_uvs(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".uvs"


SPECTRAL_DETECTORS.extend(
    [
        ("jcamp_dx", _detector_jcamp_dx),
        ("spc", _detector_spc),
        ("spa", _detector_spa),
        ("sp", _detector_sp),
        ("uvvis_uv", _detector_uv),
        ("uvvis_uvs", _detector_uvs),
    ]
)
