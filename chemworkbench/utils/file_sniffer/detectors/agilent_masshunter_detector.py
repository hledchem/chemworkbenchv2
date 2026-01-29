"""
Generic Agilent MassHunter Directory Detector — ChemWorkBench v2.2
==================================================================

LLM‑friendly commentary
-----------------------
This detector identifies Agilent MassHunter `.D` directories. It does
not interpret scientific meaning, technique, or vendor subtype. It only
checks for the structural pattern:

    - path is a directory ending in .D
    - contains MassHunter‑specific internal files such as:
        * AcqData/
        * MSScan.bin
        * DAD*.ch
        * FID.MS
        * Chrom.MS

These markers are stable across MassHunter UV‑Vis, LCMS, and
chromatography exports. Subtype‑specific detection is handled by
separate detectors and is not part of this file.

The detector is intentionally small, deterministic, and easy for both
humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List


class AgilentMassHunterDetector:
    """
    Structural detector for generic Agilent MassHunter `.D` directories.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "agilent_masshunter_dir"

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Must be a directory ending in .D
        if not path.is_dir() or path.suffix.lower() != ".d":
            return ("", 0.0, [])

        try:
            # Collect all file names (lowercase) inside the directory
            files = {p.name.lower() for p in path.rglob("*")}

            # MassHunter structural markers
            markers = [
                "acqdata",
                "msscan.bin",
                "fid.ms",
                "chrom.ms",
            ]

            # DAD channels (e.g., DAD1A.ch, DAD2A.ch)
            dad_channels = any(name.endswith(".ch") and name.startswith("dad") for name in files)

            # Check for any MassHunter markers
            if any(marker in files for marker in markers) or dad_channels:
                return (
                    self.FORMAT_ID,
                    0.90,
                    ["Agilent MassHunter .D directory structure detected"],
                )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
