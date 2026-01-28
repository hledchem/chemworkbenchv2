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

The CSV loader simply reads a CSV file into a universal Python structure
(list‑of‑dicts). Processors interpret the meaning of the data after the
anchor engine has selected the correct technique.

This file is intentionally small, deterministic, and easy for both humans
and LLMs to maintain.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping

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
    # v2.2 rule: sniffing is *format‑only*. Loaders do not sniff technique.
    # ------------------------------------------------------------------
    def sniff(self, path: Path) -> bool:
        path = Path(path)
        return path.suffix.lower() == ".csv"

    # ------------------------------------------------------------------
    # load_raw(path)
    # ------------------------------------------------------------------
    # Reads the CSV file and returns a list‑of‑dicts.
    # This is the only I/O‑heavy part of the loader.
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
    # Returns minimal structural metadata. No technique or vendor logic.
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
    # v2.2 rule: loaders output a universal structure that processors
    # can interpret. For CSV, this is simply the list‑of‑dicts.
    # ------------------------------------------------------------------
    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return raw_data
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize CSV data: {exc}"
            ) from exc
