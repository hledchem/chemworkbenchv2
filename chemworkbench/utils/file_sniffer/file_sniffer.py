from __future__ import annotations

import io
from pathlib import Path
from typing import Callable, List, Optional, Tuple, Union

from .core_detectors import CORE_DETECTORS
from .spectral_detectors import SPECTRAL_DETECTORS
from .vendor import (
    AGILENT_DETECTORS,
    BRUKER_DETECTORS,
    THERMO_DETECTORS,
    SHIMADZU_DETECTORS,
    PERKINELMER_DETECTORS,
    WATERS_DETECTORS,
    JEOL_DETECTORS,
    VARIAN_DETECTORS,
)

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

# ----------------------------------------------------------------------
# Registry
# ----------------------------------------------------------------------

DETECTORS: List[Tuple[str, DetectorFn]] = []

# Order: vendor-specific → spectral → core/generic
DETECTORS.extend(AGILENT_DETECTORS)
DETECTORS.extend(BRUKER_DETECTORS)
DETECTORS.extend(THERMO_DETECTORS)
DETECTORS.extend(SHIMADZU_DETECTORS)
DETECTORS.extend(PERKINELMER_DETECTORS)
DETECTORS.extend(WATERS_DETECTORS)
DETECTORS.extend(JEOL_DETECTORS)
DETECTORS.extend(VARIAN_DETECTORS)
DETECTORS.extend(SPECTRAL_DETECTORS)
DETECTORS.extend(CORE_DETECTORS)


def detect_file_type(path_or_bytes: PathLike | bytes | io.IOBase) -> str:
    """
    Detect the file type and return a canonical format string.

    Returns:
        A lower_snake_case string such as:
            "csv", "tsv", "xlsx", "json", "txt",
            "jcamp_dx", "spc", "spa", "sp",
            "uvvis_uv", "uvvis_uvs",
            "agilent_d", "bruker_opus", "bruker_nmr",
            "thermo_raw", "shimadzu_lcd", "waters_raw_dir",
            "jeol_jdf", "varian_nmr",
            or "unknown".

    Notes:
        - This function does NOT parse or clean the data.
        - It only inspects headers, extensions, and basic structure.
    """
    path: Optional[Path] = None
    raw_bytes: Optional[bytes] = None

    if isinstance(path_or_bytes, (str, Path)):
        path = Path(path_or_bytes)
        if path.is_file():
            raw_bytes = path.read_bytes()
    elif isinstance(path_or_bytes, bytes):
        raw_bytes = path_or_bytes
    elif isinstance(path_or_bytes, io.IOBase):
        pos = path_or_bytes.tell()
        raw_bytes = path_or_bytes.read()
        path_or_bytes.seek(pos)
    else:
        raise TypeError(f"Unsupported input type for detect_file_type: {type(path_or_bytes)}")

    # Run registered detectors in order
    for format_name, fn in DETECTORS:
        try:
            if fn(path or Path(""), raw_bytes):
                return format_name
        except Exception:
            # Detectors must be robust; failures should not break detection
            continue

    return "unknown"
