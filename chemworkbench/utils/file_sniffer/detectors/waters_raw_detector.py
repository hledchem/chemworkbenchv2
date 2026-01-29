"""
Generic Waters RAW Directory Detector — ChemWorkBench v2.2
==========================================================

LLM‑friendly commentary
-----------------------
This detector identifies Waters MassLynx `.RAW` directory structures.
It does not interpret scientific meaning, technique, or vendor subtype.
It only checks for the structural pattern:

    - directory ends with .RAW
    - contains MassLynx function data files such as:
        * _FUNC001.DAT
        * _FUNC002.DAT
        * _HEADER.TXT
        * SAMPLE.INF

These markers are stable across Waters LCMS, QToF, and chromatographic
exports. Subtype‑specific logic is handled elsewhere and is not part of
this file.

The detector is intentionally small, deterministic, and easy for both
humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List


class WatersRAWDetector:
    """
    Structural detector for generic Waters MassLynx `.RAW` directories.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "waters_raw_dir"

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Must be a directory ending in .RAW
        if not path.is_dir() or path.suffix.lower() != ".raw":
            return ("", 0.0, [])

        try:
            # Collect all file names (lowercase) inside the directory
            names = {p.name.lower() for p in path.iterdir()}

            # Waters MassLynx structural markers
            function_files = any(
                name.startswith("_func") and name.endswith(".dat")
                for name in names
            )

            header_present = "_header.txt" in names
            sample_info_present = "sample.inf" in names

            if function_files or header_present or sample_info_present:
                return (
                    self.FORMAT_ID,
                    0.95,
                    ["Waters MassLynx .RAW directory structure detected"],
                )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
