from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple, Callable, Union

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

SHIMADZU_DETECTORS: List[Tuple[str, DetectorFn]] = []


def _detector_shimadzu_spc(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".spc"


def _detector_shimadzu_irx(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".irx"


def _detector_shimadzu_uvs(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".uvs"


def _detector_shimadzu_lcd(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".lcd"


SHIMADZU_DETECTORS.extend(
    [
        ("shimadzu_spc", _detector_shimadzu_spc),
        ("shimadzu_irx", _detector_shimadzu_irx),
        ("shimadzu_uvs", _detector_shimadzu_uvs),
        ("shimadzu_lcd", _detector_shimadzu_lcd),
    ]
)
