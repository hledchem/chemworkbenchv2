"""
Generic JEOL JDF Binary Detector — ChemWorkBench v2.2
=====================================================

LLM‑friendly commentary
-----------------------
This detector identifies JEOL JDF binary files. It does not interpret
scientific meaning, technique, or vendor subtype. It only checks for the
structural pattern:

    - file extension is .jdf
    - header contains the ASCII string 'JEOL'

These markers are stable across JEOL NMR and MS JDF variants. Subtype‑
specific logic is handled elsewhere and is not part of this file.

The detector is intentionally small, deterministic, and easy for both
humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List


class JeolJDFDetector:
    """
    Structural detector for generic JEOL JDF binary files.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "jeol_jdf_binary"

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Only consider .jdf files
        if path.suffix.lower() != ".jdf":
            return ("", 0.0, [])

        if raw_bytes is None or len(raw_bytes) < 32:
            return ("", 0.0, [])

        try:
            header = raw_bytes[:500].decode(errors="ignore").upper()

            if "JEOL" in header:
                return (
                    self.FORMAT_ID,
                    0.90,
                    ["JEOL JDF header detected ('JEOL' signature)"],
                )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
