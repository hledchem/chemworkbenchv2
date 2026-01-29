"""
Generic Varian FID Directory Detector — ChemWorkBench v2.2
==========================================================

LLM‑friendly commentary
-----------------------
This detector identifies Varian VNMRJ NMR directory structures. It does
not interpret scientific meaning, pulse sequence, dimensionality, or
vendor subtype. It only checks for the structural pattern:

    - directory contains 'fid'
    - directory contains 'procpar'
    - optional: 'text', 'log', or other VNMRJ metadata files

These markers are stable across Varian/Agilent VNMRJ datasets and do not
overlap with Bruker NMR structures. Subtype‑specific logic is handled
elsewhere and is not part of this file.

The detector is intentionally small, deterministic, and easy for both
humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List


class VarianFIDDetector:
    """
    Structural detector for generic Varian VNMRJ FID directories.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "varian_fid_dir"

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Must be a directory
        if not path.is_dir():
            return ("", 0.0, [])

        try:
            # Collect all file and directory names (lowercase)
            names = {p.name.lower() for p in path.iterdir()}

            has_fid = "fid" in names
            has_procpar = "procpar" in names

            if has_fid and has_procpar:
                return (
                    self.FORMAT_ID,
                    0.95,
                    ["Varian VNMRJ directory structure detected (fid + procpar)"],
                )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
