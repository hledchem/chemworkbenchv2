"""
Multi‑Column ASCII Loader — ChemWorkBench v2.2
==============================================

LLM‑friendly commentary
-----------------------
This loader implements the canonical v2.2 ingestion architecture for
multi‑column ASCII files. These files appear across many vendor exports
and generic lab workflows. The loader does *not* interpret meaning. It
simply reads N numeric columns into a universal structure.

Responsibilities:
- Read multi‑column ASCII files safely and deterministically
- Produce a universal structure: list‑of‑dicts with synthetic column names
- Extract minimal structural metadata
- Raise structured loader errors

Non‑responsibilities:
- Technique detection
- Vendor detection
- Scientific interpretation
- Token normalization
- Anchor scoring
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from chemworkbench.utils.loaders.base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


# ======================================================================
# Multi‑Column ASCII Loader (v2.2)
# ======================================================================

class MultiColumnASCIILoader(BaseVendorLoader):
    """
    Universal multi‑column ASCII loader for ChemWorkBench v2.2.

    Expected structure:
        <float> <float> <float> ...
        <float> <float> <float> ...
        ...

    The loader does not validate technique or units. It simply parses
    N numeric columns separated by whitespace.
    """

    VENDOR = "universal"
    FORMAT = "multi_column_ascii"
    EXTENSIONS = (".txt", ".dat", ".asc")  # non‑authoritative

    def sniff(self, path: Path) -> bool:
        return path.suffix.lower() in self.EXTENSIONS

    def load_raw(self, path: Path) -> Any:
        rows = []
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    parts = stripped.split()
                    try:
                        floats = list(map(float, parts))
                    except ValueError:
                        raise LoaderReadError(
                            f"Non‑numeric token encountered in '{path}'"
                        )
                    row = {f"col{i+1}": val for i, val in enumerate(floats)}
                    rows.append(row)
            return rows
        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read multi‑column ASCII file '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            num_cols = len(raw_data[0]) if raw_data else 0
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_rows": len(raw_data),
                "num_columns": num_cols,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from multi‑column ASCII: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return raw_data
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize multi‑column ASCII data: {exc}"
            ) from exc
