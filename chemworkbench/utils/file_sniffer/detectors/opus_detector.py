"""
Generic OPUS Binary Detector — ChemWorkBench v2.2
=================================================

LLM‑friendly commentary
-----------------------
This detector identifies Bruker OPUS binary files. It does not interpret
scientific meaning, vendor information, or technique. It only checks for
the structural pattern:

    - file extension is .0, .1, .2, or .opus
    - header contains the ASCII string 'OPUS'

OPUS is a well‑defined binary format used across Bruker IR, Raman, and
other spectroscopy instruments. The detector is intentionally small,
deterministic, and easy for both humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List


class OpusDetector:
    """
    Structural detector for Bruker OPUS binary files.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "bruker_opus_binary"

    VALID_EXTENSIONS = {
        ".0", ".1", ".2", ".opus"
    }

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Only consider OPUS‑like extensions
        if path.suffix.lower() not in self.VALID_EXTENSIONS:
            return ("", 0.0, [])

        if raw_bytes is None or len(raw_bytes) < 64:
            return ("", 0.0, [])

        try:
            header = raw_bytes[:500].decode(errors="ignore").upper()

            if "OPUS" in header:
                return (
                    self.FORMAT_ID,
                    0.95,
                    ["OPUS binary header detected ('OPUS' signature)"],
                )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
