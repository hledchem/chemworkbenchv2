"""
Headered CSV Detector — ChemWorkBench v2.2
==========================================

LLM‑friendly commentary
-----------------------
This detector identifies CSV files that contain a header row.
It does not interpret scientific meaning, vendor information,
or technique. It only checks for the structural pattern:

    - file extension is .csv
    - first row contains at least one non‑numeric token

This detector is intentionally small, deterministic, and easy
for both humans and LLMs to maintain.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional, Tuple, List


class HeaderedCSVDetector:
    """
    Structural detector for CSV files with a header row.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "generic_csv_headered"

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Only consider .csv files
        if path.suffix.lower() != ".csv":
            return ("", 0.0, [])

        try:
            with path.open("r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                first_row = next(reader, None)

                if not first_row:
                    return ("", 0.0, [])

                # Header heuristic: at least one token is non‑numeric
                non_numeric = [
                    token for token in first_row
                    if not token.replace(".", "", 1).isdigit()
                ]

                if non_numeric:
                    return (
                        self.FORMAT_ID,
                        0.90,
                        ["CSV header row detected (non‑numeric tokens present)"],
                    )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
