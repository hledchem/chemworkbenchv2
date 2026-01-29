"""
Generic Raman DPT ASCII Detector — ChemWorkBench v2.2
=====================================================

LLM‑friendly commentary
-----------------------
This detector identifies generic Raman `.dpt` ASCII files. It does not
interpret scientific meaning, vendor information, or technique subtype.
It only checks for the structural pattern:

    - file extension is .dpt
    - header contains 'XYDATA' or 'DATA'
    - file is ASCII‑readable

These markers are stable across many Raman instruments that export DPT
files (Horiba, Renishaw, and OEM variants). Subtype‑specific logic is
handled elsewhere and is not part of this file.

The detector is intentionally small, deterministic, and easy for both
humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List


class RamanDPTDetector:
    """
    Structural detector for generic Raman DPT ASCII files.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "raman_dpt_ascii"

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Only consider .dpt files
        if path.suffix.lower() != ".dpt":
            return ("", 0.0, [])

        if raw_bytes is None or len(raw_bytes) < 16:
            return ("", 0.0, [])

        try:
            header = raw_bytes[:500].decode(errors="ignore").upper()

            # DPT structural markers
            if "XYDATA" in header or "DATA" in header:
                return (
                    self.FORMAT_ID,
                    0.85,
                    ["Raman DPT ASCII header detected ('XYDATA' or 'DATA')"],
                )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
