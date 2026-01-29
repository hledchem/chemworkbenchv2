"""
JCAMP‑DX Detector — ChemWorkBench v2.2
======================================

LLM‑friendly commentary
-----------------------
This detector identifies JCAMP‑DX spectroscopy files. It does not
interpret scientific meaning, vendor information, or technique. It only
checks for the structural pattern:

    - file extension is .jdx or .dx
    - header contains '##TITLE' or '##JCAMP'

JCAMP‑DX is a well‑defined ASCII format used across IR, Raman, UV‑Vis,
and NMR. The detector is intentionally small, deterministic, and easy
for both humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List


class JcampDetector:
    """
    Structural detector for JCAMP‑DX files.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "jcamp_dx"
    VALID_EXTENSIONS = {".jdx", ".dx"}

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Only consider JCAMP extensions
        if path.suffix.lower() not in self.VALID_EXTENSIONS:
            return ("", 0.0, [])

        if raw_bytes is None:
            return ("", 0.0, [])

        try:
            header = raw_bytes[:500].decode(errors="ignore").upper()

            if "##TITLE" in header or "##JCAMP" in header:
                return (
                    self.FORMAT_ID,
                    0.95,
                    ["JCAMP‑DX header detected"],
                )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
