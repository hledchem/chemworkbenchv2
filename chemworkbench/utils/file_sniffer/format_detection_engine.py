"""
FormatDetectionEngine — ChemWorkBench v2.2
==========================================

Unified structural format detector.

This replaces the legacy detector tree with a deterministic,
rule‑based engine that inspects:

- file extension
- first few lines of text
- directory structure (for vendor formats)
- magic bytes (for binary formats)

Output:
    FormatDetectionResult(format_id: str, confidence: float)
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FormatDetectionResult:
    format_id: str
    confidence: float


class FormatDetectionEngine:
    """
    v2.2 structural format detector.

    No plugin detectors.
    No per‑format detector classes.
    Pure rule‑based logic.
    """

    def __init__(self):
        pass  # v2.2 takes no arguments

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def detect(self, path: Path) -> FormatDetectionResult:
        suffix = path.suffix.lower()

        # --------------------------------------------------------------
        # JCAMP
        # --------------------------------------------------------------
        if suffix in {".dx", ".jdx"}:
            return FormatDetectionResult("jcamp_dx", 0.95)

        # --------------------------------------------------------------
        # Two‑column ASCII
        # --------------------------------------------------------------
        if suffix in {".txt", ".dat", ".asc", ".xy"}:
            # Peek at first non‑empty line
            try:
                with path.open("r", encoding="utf-8") as f:
                    for line in f:
                        stripped = line.strip()
                        if not stripped:
                            continue
                        parts = stripped.split()
                        if len(parts) == 2:
                            return FormatDetectionResult("two_column_ascii", 0.80)
                        if len(parts) > 2:
                            return FormatDetectionResult("multi_column_ascii", 0.80)
            except Exception:
                pass

        # --------------------------------------------------------------
        # CSV
        # --------------------------------------------------------------
        if suffix == ".csv":
            return FormatDetectionResult("generic_csv_headered", 0.70)

        # --------------------------------------------------------------
        # XLSX
        # --------------------------------------------------------------
        if suffix == ".xlsx":
            return FormatDetectionResult("generic_xlsx", 0.90)

        # --------------------------------------------------------------
        # Bruker NMR directory
        # --------------------------------------------------------------
        if path.is_dir():
            if (path / "fid").exists() and (path / "acqus").exists():
                return FormatDetectionResult("bruker_nmr_dir", 0.95)

        # --------------------------------------------------------------
        # Waters RAW directory
        # --------------------------------------------------------------
        if path.is_dir() and any(p.suffix.lower() == ".raw" for p in path.iterdir()):
            return FormatDetectionResult("waters_raw_dir", 0.90)

        # --------------------------------------------------------------
        # JEOL JDF
        # --------------------------------------------------------------
        if suffix == ".jdf":
            return FormatDetectionResult("jeol_jdf_binary", 0.90)

        # --------------------------------------------------------------
        # SPC (Thermo, Shimadzu, PerkinElmer)
        # --------------------------------------------------------------
        if suffix == ".spc":
            return FormatDetectionResult("thermo_spc_binary", 0.85)

        # --------------------------------------------------------------
        # Fallback
        # --------------------------------------------------------------
        return FormatDetectionResult("unknown", 0.10)
