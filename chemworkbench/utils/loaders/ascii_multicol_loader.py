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
- Infer structural Scan objects (technique‑agnostic)
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
from typing import Any, Mapping, Dict, List

from chemworkbench.core.models import Scan
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
    # Adds structural scan inference while preserving tabular rows.
    # ------------------------------------------------------------------
    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            tabular = raw_data
            scans: List[Scan] = []

            if not raw_data:
                return {"tabular": tabular, "scans": scans}

            # Determine number of columns
            num_cols = len(raw_data[0])
            if num_cols < 2:
                return {"tabular": tabular, "scans": scans}

            # Convert columns to numeric arrays
            columns: List[List[float]] = []
            for col_index in range(num_cols):
                col = [row[f"col_{col_index}"] for row in raw_data]
                columns.append(col)

            # ------------------------------------------------------------------
            # Structural scan inference rules (v2.2)
            # ------------------------------------------------------------------

            # Case A: exactly 2 columns → one scan
            if num_cols == 2:
                x = columns[0]
                y = columns[1]
                if len(x) == len(y):
                    scans.append(
                        Scan(
                            x=x,
                            y=y,
                            label="scan_1",
                        )
                    )
                return {"tabular": tabular, "scans": scans}

            # Case B: even number of columns → paired scans (x1,y1,x2,y2,...)
            if num_cols % 2 == 0:
                for i in range(0, num_cols, 2):
                    x = columns[i]
                    y = columns[i + 1]
                    if len(x) == len(y):
                        scans.append(
                            Scan(
                                x=x,
                                y=y,
                                label=f"scan_{(i // 2) + 1}",
                            )
                        )
                return {"tabular": tabular, "scans": scans}

            # Case C: first column is x, remaining are y-columns
            x = columns[0]
            for yi in range(1, num_cols):
                y = columns[yi]
                if len(x) == len(y):
                    scans.append(
                        Scan(
                            x=x,
                            y=y,
                            label=f"scan_{yi}",
                        )
                    )

            return {"tabular": tabular, "scans": scans}

        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize multi‑column ASCII data: {exc}"
            ) from exc
