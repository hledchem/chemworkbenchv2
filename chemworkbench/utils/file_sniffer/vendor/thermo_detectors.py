from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple, Callable, Union

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

THERMO_DETECTORS: List[Tuple[str, DetectorFn]] = []


def _detector_thermo_spa(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".spa"


def _detector_thermo_spc(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".spc"


def _detector_thermo_srs(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    return p.suffix.lower() == ".srs"


def _detector_thermo_raw(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    # Thermo Xcalibur RAW is a single .raw file
    return p.suffix.lower() == ".raw" and p.is_file()


THERMO_DETECTORS.extend(
    [
        ("thermo_spa", _detector_thermo_spa),
        ("thermo_spc", _detector_thermo_spc),
        ("thermo_srs", _detector_thermo_srs),
        ("thermo_raw", _detector_thermo_raw),
    ]
)
