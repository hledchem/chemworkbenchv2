"""
Two‑Column ASCII Detector — ChemWorkBench v2.2
==============================================

LLM‑friendly commentary
-----------------------
This detector identifies whitespace‑delimited ASCII files that contain
exactly two numeric columns. It does not interpret scientific meaning,
vendor information, or technique. It only checks for the structural
pattern:

    <float> <float>
    <float> <float>
    ...

This pattern appears across many analytical techniques (UV‑Vis, IR,
Raman, chromatography, electrochemistry), but the detector does not
attempt to classify technique. It only confirms the two‑column structure.

The detector is intentionally small, deterministic, and easy for both
humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List

from chemworkbench.utils.file_sniffer.signals import is_float


class TwoColumnAsciiDetector:
    """
    Structural detector for two‑column numeric ASCII files.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "two_column_ascii"

    VALID_EXTENSIONS = {".txt", ".dat", ".asc", ".xy"}

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

                    # Must be exactly two columns
                    if len(parts) != 2:
                        return ("", 0.0, [])

                    # Both must be numeric
                    if not (is_float(parts[0]) and is_float(parts[1])):
                        return ("", 0.0, [])

                    # Check only first few lines for efficiency
                    if lines_checked >= 5:
                        break

                if lines_checked > 0:
                    return (
                        self.FORMAT_ID,
                        0.85,
                        ["Two‑column numeric ASCII structure detected"],
                    )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
