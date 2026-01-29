"""
Generic SPC Binary Detector — ChemWorkBench v2.2
================================================

LLM‑friendly commentary
-----------------------
This detector identifies generic SPC binary files. It does not interpret
scientific meaning, vendor information, or technique. It only checks for
the universal SPC structural signature:

    - file extension is .spc
    - first two bytes match the SPC signature: 0x4B 0x02

This signature is shared across multiple vendor ecosystems, including
PerkinElmer, Thermo, Shimadzu, and Galactic SPC. Vendor‑specific SPC
detection is handled by separate detectors and is not part of this file.

The detector is intentionally small, deterministic, and easy for both
humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List


class SPCDetector:
    """
    Structural detector for generic SPC binary files.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "spc_binary"

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Only consider .spc files
        if path.suffix.lower() != ".spc":
            return ("", 0.0, [])

        # Need at least two bytes to check signature
        if raw_bytes is None or len(raw_bytes) < 2:
            return ("", 0.0, [])

        try:
            # Universal SPC signature: 0x4B 0x02
            if raw_bytes[0] == 0x4B and raw_bytes[1] == 0x02:
                return (
                    self.FORMAT_ID,
                    0.95,
                    ["Generic SPC binary signature detected (0x4B 0x02)"],
                )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
