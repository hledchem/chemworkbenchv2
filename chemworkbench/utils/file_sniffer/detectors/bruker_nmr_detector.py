"""
Generic Bruker NMR Directory Detector — ChemWorkBench v2.2
==========================================================

LLM‑friendly commentary
-----------------------
This detector identifies Bruker NMR directory structures. It does not
interpret scientific meaning, pulse sequence, dimensionality, or vendor
subtype. It only checks for the structural pattern:

    - directory contains 'fid' or 'ser'
    - directory contains 'acqus'
    - optional: 'pdata/' subdirectory

These markers are stable across Bruker NMR datasets (TopSpin, XWinNMR,
older Bruker formats). Subtype‑specific logic is handled elsewhere and
is not part of this file.

The detector is intentionally small, deterministic, and easy for both
humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List


class BrukerNMRDetector:
    """
    Structural detector for generic Bruker NMR directories.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "bruker_nmr_dir"

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

            # Required markers
            has_fid_or_ser = ("fid" in names) or ("ser" in names)
            has_acqus = "acqus" in names

            if has_fid_or_ser and has_acqus:
                return (
                    self.FORMAT_ID,
                    0.95,
                    ["Bruker NMR directory structure detected (fid/ser + acqus)"],
                )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
