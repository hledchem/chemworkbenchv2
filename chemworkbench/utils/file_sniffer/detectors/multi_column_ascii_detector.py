"""
Multi‑Column ASCII Detector — ChemWorkBench v2.2
================================================

LLM‑friendly commentary
-----------------------
This detector identifies whitespace‑delimited ASCII files that contain
three or more numeric columns. It does not interpret scientific meaning,
vendor information, or technique. It only checks for the structural
pattern:

    <float> <float> <float> ...
    <float> <float> <float> ...
    ...

This pattern appears across many vendor exports and generic lab data
tables. The detector is intentionally small, deterministic, and easy for
both humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List

from chemworkbench.utils.file_sniffer.signals import all_float


class MultiColumnAsciiDetector:
    """
    Structural detector for multi‑column numeric ASCII files.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "multi_column_ascii"

    VALID_EXTENSIONS = {".txt", ".dat", ".asc"}

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Only consider common ASCII extensions
        if path.suffix.lower() not in self.VALID_EXTENSIONS:
            return ("", 0.0, [])

        try:
            with path.open("r", encoding="utf-8") as f:
                lines_checked = 0

                for line in f:
                    stripped = line.strip()
                    if not stripped:
                        continue

                    parts = stripped.split()
                    lines_checked += 1

                    # Must be 3 or more columns
                    if len(parts) < 3:
                        return ("", 0.0, [])

                    # All must be numeric
                    if not all_float(parts):
                        return ("", 0.0, [])

                    # Check only first few lines for efficiency
                    if lines_checked >= 5:
                        break

                if lines_checked > 0:
                    return (
                        self.FORMAT_ID,
                        0.75,
                        ["Multi‑column numeric ASCII structure detected"],
                    )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
