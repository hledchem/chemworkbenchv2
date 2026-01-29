"""
Generic NetCDF / ANDI‑MS Detector — ChemWorkBench v2.2
======================================================

LLM‑friendly commentary
-----------------------
This detector identifies NetCDF (CDF) files used for chromatography and
mass spectrometry interchange formats (ANDI‑MS, ANDI‑Chrom). It does not
interpret scientific meaning, vendor information, or technique subtype.
It only checks for the structural pattern:

    - file extension is .cdf or .nc
    - NetCDF magic bytes:
        * 'CDF\\x01'
        * 'CDF\\x02'

These markers are stable across NetCDF exports from Agilent, Thermo,
Waters, Shimadzu, Bruker, LECO, and many OEM systems. Subtype‑specific
logic is handled elsewhere and is not part of this file.

The detector is intentionally small, deterministic, and easy for both
humans and LLMs to maintain.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List


class NetCDFDetector:
    """
    Structural detector for generic NetCDF / ANDI‑MS files.

    Returns:
        (format_id, confidence, reasons)
    """

    FORMAT_ID = "netcdf_andi_ms"

    VALID_EXTENSIONS = {".cdf", ".nc"}

    MAGIC_1 = b"CDF\x01"
    MAGIC_2 = b"CDF\x02"

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        # Only consider .cdf or .nc files
        if path.suffix.lower() not in self.VALID_EXTENSIONS:
            return ("", 0.0, [])

        if raw_bytes is None or len(raw_bytes) < 4:
            return ("", 0.0, [])

        try:
            header = raw_bytes[:4]

            if header == self.MAGIC_1 or header == self.MAGIC_2:
                return (
                    self.FORMAT_ID,
                    0.95,
                    ["NetCDF magic bytes detected ('CDF\\x01' or 'CDF\\x02')"],
                )

        except Exception:
            return ("", 0.0, [])

        return ("", 0.0, [])
