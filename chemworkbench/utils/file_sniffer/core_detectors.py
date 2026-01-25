"""
core_detectors.py

Tier 1 detectors for ChemWorkBench v2.
These provide:
- extension-based detection (low confidence)
- minimal magic-byte detection

Vendor-specific logic is handled by loaders (Tier 3).
"""

from __future__ import annotations
from pathlib import Path
from chemworkbench.core.models import DetectedFormat, Technique


# ------------------------------------------------------------
# Extension-based detection (safe, unambiguous formats only)
# ------------------------------------------------------------

EXTENSION_MAP = {
    # Universal formats
    ".csv": ("universal", "csv"),
    ".jdx": ("universal", "jcamp"),
    ".dx": ("universal", "jcamp"),
    ".xlsx": ("universal", "xlsx"),

    # Raman formats (safe by extension)
    ".dpt": ("raman", "dpt"),
    ".rruf": ("raman", "rruf"),
    ".txt": ("raman", "rruf"),  # RRUFF often uses .txt

    # PerkinElmer (safe)
    ".sp": ("perkinelmer", "sp"),
    ".spc": ("perkinelmer", "spc"),

    # Bruker (safe)
    ".opus": ("bruker", "opus"),
    ".dta": ("bruker", "epr"),
    ".esp": ("bruker", "epr"),

    # JEOL (safe)
    ".jdf": ("jeol", "jdf"),

    # Waters (safe)
    ".raw": ("waters", "raw"),

    # Shimadzu (safe)
    ".irx": ("shimadzu", "irx"),
    ".lcd": ("shimadzu", "lcd"),
    ".uvs": ("shimadzu", "uvs"),
}


def detect_by_extension(path: str):
    ext = Path(path).suffix.lower()
    if ext in EXTENSION_MAP:
        vendor, subtype = EXTENSION_MAP[ext]
        return DetectedFormat(
            vendor=vendor,
            technique=Technique.UNKNOWN,
            subtype=subtype,
            confidence=0.40,
        )
    return None


# ------------------------------------------------------------
# Magic-byte detection (minimal placeholder)
# ------------------------------------------------------------

def detect_magic_bytes(path: str):
    """
    Placeholder for binary signature detection.
    Currently only detects Bruker OPUS-style '##' headers.
    """
    try:
        with open(path, "rb") as f:
            header = f.read(16)

        if header.startswith(b"##"):
            return DetectedFormat(
                vendor="bruker",
                technique=Technique.UNKNOWN,
                subtype="opus",
                confidence=0.50,
            )

    except Exception:
        pass

    return None
