from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Tuple, Callable, Union

PathLike = Union[str, Path]
DetectorFn = Callable[[PathLike, Optional[bytes]], bool]

CORE_DETECTORS: List[Tuple[str, DetectorFn]] = []


def _looks_like_text(raw_bytes: bytes, sample_size: int = 2048) -> bool:
    sample = raw_bytes[:sample_size]
    if not sample:
        return False
    non_printable = sum(
        1 for b in sample
        if b < 9 or (13 < b < 32) or b == 127
    )
    ratio = non_printable / len(sample)
    return ratio < 0.1


def _detector_csv(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    if p.suffix.lower() == ".csv":
        return True
    if raw_bytes is None or not _looks_like_text(raw_bytes):
        return False
    head = raw_bytes[:4096].decode(errors="ignore")
    lines = head.splitlines()
    if not lines:
        return False
    sample = lines[:5]
    comma_counts = [line.count(",") for line in sample if line.strip()]
    return any(c >= 1 for c in comma_counts)


def _detector_tsv(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    if p.suffix.lower() == ".tsv":
        return True
    if raw_bytes is None or not _looks_like_text(raw_bytes):
        return False
    head = raw_bytes[:4096].decode(errors="ignore")
    lines = head.splitlines()
    if not lines:
        return False
    sample = lines[:5]
    tab_counts = [line.count("\t") for line in sample if line.strip()]
    return any(c >= 1 for c in tab_counts)


def _detector_xlsx(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    if p.suffix.lower() == ".xlsx":
        return True
    if raw_bytes is None:
        return False
    # XLSX is a ZIP container: PK\x03\x04
    return raw_bytes.startswith(b"PK\x03\x04")


def _detector_json(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    if p.suffix.lower() == ".json":
        return True
    if raw_bytes is None or not _looks_like_text(raw_bytes):
        return False
    head = raw_bytes.strip()
    if not head:
        return False
    if not (head.startswith(b"{") or head.startswith(b"[")):
        return False
    try:
        json.loads(head.decode(errors="ignore"))
        return True
    except Exception:
        return False


def _detector_txt(path: PathLike, raw_bytes: Optional[bytes]) -> bool:
    p = Path(path)
    if p.suffix.lower() == ".txt":
        return True
    if raw_bytes is None:
        return False
    return _looks_like_text(raw_bytes)


CORE_DETECTORS.extend(
    [
        ("csv", _detector_csv),
        ("tsv", _detector_tsv),
        ("xlsx", _detector_xlsx),
        ("json", _detector_json),
        ("txt", _detector_txt),
    ]
)
