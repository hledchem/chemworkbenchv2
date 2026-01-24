from __future__ import_annotations

from pathlib import Path
from typing import List, Optional, Tuple, Callable, Union

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

WATERS_DETECTORS: List[Tuple[str, DetectorFn]] = []


def _detector_waters_raw_dir(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    if p.suffix.lower() != ".raw" or not p.is_dir():
        return False
    # MassLynx RAW directory typically contains these files
    header = p / "_HEADER.TXT"
    func = p / "_FUNC001.DAT"
    return header.exists() or func.exists()


WATERS_DETECTORS.extend(
    [
        ("waters_raw_dir", _detector_waters_raw_dir),
    ]
)
