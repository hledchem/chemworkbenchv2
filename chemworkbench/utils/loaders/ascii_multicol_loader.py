"""
Multi‑Column ASCII Loader — ChemWorkBench v2.2
==============================================

LLM‑friendly commentary
-----------------------
This loader implements the canonical v2.2 ingestion architecture for
multi‑column ASCII files. These appear across UV‑Vis, IR, Raman,
fluorescence, electrochemistry, and general scientific data exports.

Responsibilities:
- Read multi‑column ASCII files safely and deterministically
- Produce a universal structure: list‑of‑dicts with keys col_0, col_1, ...
- Extract minimal structural metadata
- Raise structured loader errors

Non‑responsibilities:
- Technique detection
- Vendor detection
- Scientific interpretation
- Token normalization
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Dict

from chemworkbench.utils.loaders.base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


# ======================================================================
# Multi‑Column ASCII Loader (v2.2)
# ======================================================================

class ASCIIMultiColLoader(BaseVendorLoader):
    """
    Universal multi‑column ASCII loader for ChemWorkBench v2.2.

    Expected structure:
        <float> <float> <float> ...
        <float> <float> <float> ...
        ...

    Columns are returned as:
        {"col_0": float, "col_1": float, ...}
    """

    VENDOR = "universal"
    FORMAT = "multi_column_ascii"
    EXTENSIONS = (".txt", ".dat", ".asc", ".csv")  # non‑authoritative

    # ------------------------------------------------------------------
    # sniff(path)
    # ------------------------------------------------------------------
    def sniff(self, path: Path) -> bool:
        return path.suffix.lower() in self.EXTENSIONS

    # ------------------------------------------------------------------
    # load_raw(path)
    # ------------------------------------------------------------------
    def load_raw(self, path: Path) -> Any:
        rows = []
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped:
                        continue

                    parts = stripped.split()
                    if len(parts) < 2:
                        raise LoaderReadError(
                            f"Expected ≥2 columns in '{path}', got {len(parts)}"
                        )

                    # Convert all columns to floats
                    try:
                        floats = list(map(float, parts))
                    except Exception as exc:
                        raise LoaderReadError(
                            f"Non‑numeric value in multi‑column ASCII file '{path}': {exc}"
                        ) from exc

                    row: Dict[str, float] = {
                        f"col_{i}": value for i, value in enumerate(floats)
                    }
                    rows.append(row)

            return rows

        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read multi‑column ASCII file '{path}': {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # extract_metadata(raw_data)
    # ------------------------------------------------------------------
    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            num_cols = len(raw_data[0]) if raw_data else 0
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_points": len(raw_data),
                "num_columns": num_cols,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from multi‑column ASCII: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # to_universal(raw_data, metadata)
    # ------------------------------------------------------------------
    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return raw_data
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize multi‑column ASCII data: {exc}"
            ) from exc
