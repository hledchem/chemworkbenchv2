"""
Generic UV‑Vis ASCII Detector — ChemWorkBench v2.2
==================================================

LLM‑friendly commentary
-----------------------
This detector identifies generic UV‑Vis ASCII files. It does not
interpret scientific meaning, vendor information, or technique subtype.
It only checks for the structural pattern:

    - ASCII‑readable file
    - common UV‑Vis extensions: .txt, .asc, .csv, .dat
    - optional header markers such as:
        * 'Wavelength'
        * 'Abs', 'Absorbance'
        * 'Transmittance', '%T'
    - two numeric columns (λ vs intensity)

These markers are stable across UV‑Vis exports from Agilent Cary,
Shimadzu UV‑Vis, Thermo Evolution, PerkinElmer Lambda, and many OEM
systems. Subtype‑specific logic is handled elsewhere and is not part of
this file.

The detector is intentionally small, deterministic, and easy for both
humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List

from chemworkbench.utils.file_sniffer.signals import is_float


class UVVisAsciiDetector:
    """
    Structural detector for generic UV‑Vis ASCII files.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "uvvis_ascii"

    VALID_EXTENSIONS = {".txt", ".asc", ".csv", ".dat"}

    HEADER_MARKERS = {
        "WAVELENGTH",
        "ABS",
        "ABSORBANCE",
        "TRANSMITTANCE",
        "%T",
    }

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Only consider common ASCII extensions
        if path.suffix.lower() not in self.VALID_EXTENSIONS:
            return ("", 0.0, [])

        header_confidence = 0.0

        try:
            with path.open("r", encoding="utf-8") as f:
                lines_checked = 0

                for line in f:
                    stripped = line.strip()
                    if not stripped:
                        continue

                    upper = stripped.upper()

                    # Check for UV‑Vis header markers
                    if any(marker in upper for marker in self.HEADER_MARKERS):
                        header_confidence = 0.15

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
                        0.80 + header_confidence,
                        ["Two‑column numeric ASCII structure detected (UV‑Vis‑style)"],
                    )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
