"""
CSV Loader — ChemWorkBench v2.2
===============================

LLM‑friendly commentary
-----------------------
This loader implements the canonical v2.2 ingestion architecture for CSV
files. In v2.2, loaders are *format readers only*. They do not:

    - detect technique
    - classify vendor
    - interpret scientific meaning
    - normalize tokens
    - perform anchor scoring

All detection and classification happens *before* loaders run.

The CSV loader reads a CSV file into a universal Python structure
(list‑of‑dicts) and performs *structural* scan inference when the table
represents one or more numeric spectra. This is technique‑agnostic and
purely structural.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping, List, Dict

from chemworkbench.core.models import Scan
from chemworkbench.utils.loaders.base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


# ======================================================================
# CSV Loader (v2.2)
# ======================================================================

class CSVLoader(BaseVendorLoader):
    """
    Universal CSV loader for ChemWorkBench v2.2.

    Responsibilities:
    - Read CSV files safely and deterministically
    - Produce a universal structure (list‑of‑dicts)
    - Infer *structural* scans when the table is numeric
    - Extract minimal structural metadata
    - Raise structured loader errors

    Non‑responsibilities:
    - Technique detection (anchor engine)
    - Vendor detection
    - Scientific interpretation
    - Token normalization
    """

    VENDOR = "universal"
    FORMAT = "csv"
    EXTENSIONS = (".csv",)

    # ------------------------------------------------------------------
    # sniff(path)
    # ------------------------------------------------------------------
    def sniff(self, path: Path) -> bool:
        path = Path(path)
        return path.suffix.lower() == ".csv"

    # ------------------------------------------------------------------
    # load_raw(path)
    # ------------------------------------------------------------------
    def load_raw(self, path: Path) -> Any:
        try:
            with path.open("r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read CSV file '{path}': {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # extract_metadata(raw_data)
    # ------------------------------------------------------------------
    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_rows": len(raw_data),
                "num_columns": len(raw_data[0]) if raw_data else 0,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract CSV metadata: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # to_universal(raw_data, metadata)
    # ------------------------------------------------------------------
    # Adds structural scan inference while preserving tabular output.
    # ------------------------------------------------------------------
    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            # Always preserve tabular rows
            tabular = raw_data

            scans: List[Scan] = []

            if not raw_data:
                return {"tabular": tabular, "scans": scans}

            # Extract headers
            headers = list(raw_data[0].keys())
            num_cols = len(headers)

            # Convert columns to numeric arrays when possible
            columns: List[List[float]] = []
            numeric_mask: List[bool] = []

            for h in headers:
                col = []
                is_numeric = True
                for row in raw_data:
                    val = row.get(h, "").strip()
                    try:
                        col.append(float(val))
                    except Exception:
                        is_numeric = False
                        break
                numeric_mask.append(is_numeric)
                columns.append(col if is_numeric else [])

            # If fewer than 2 numeric columns → no scans
            numeric_indices = [i for i, ok in enumerate(numeric_mask) if ok]
            if len(numeric_indices) < 2:
                return {"tabular": tabular, "scans": scans}

            # ------------------------------------------------------------------
            # Structural scan inference rules (v2.2)
            # ------------------------------------------------------------------

            # Case A: exactly 2 numeric columns → one scan
            if len(numeric_indices) == 2:
                xi, yi = numeric_indices
                x = columns[xi]
                y = columns[yi]
                if len(x) == len(y):
                    scans.append(
                        Scan(
                            x=x,
                            y=y,
                            label=f"{headers[yi]} vs {headers[xi]}",
                        )
                    )
                return {"tabular": tabular, "scans": scans}

            # Case B: even number of numeric columns → paired scans (x1,y1,x2,y2,...)
            if len(numeric_indices) % 2 == 0:
                for i in range(0, len(numeric_indices), 2):
                    xi = numeric_indices[i]
                    yi = numeric_indices[i + 1]
                    x = columns[xi]
                    y = columns[yi]
                    if len(x) == len(y):
                        scans.append(
                            Scan(
                                x=x,
                                y=y,
                                label=f"{headers[yi]} vs {headers[xi]}",
                            )
                        )
                return {"tabular": tabular, "scans": scans}

            # Case C: first numeric column is x, remaining are y-columns
            x_index = numeric_indices[0]
            x = columns[x_index]
            for yi in numeric_indices[1:]:
                y = columns[yi]
                if len(x) == len(y):
                    scans.append(
                        Scan(
                            x=x,
                            y=y,
                            label=f"{headers[yi]} vs {headers[x_index]}",
                        )
                    )

            return {"tabular": tabular, "scans": scans}

        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize CSV data: {exc}"
            ) from exc
