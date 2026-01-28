"""
CSVLoader (v2.2)
================

This loader implements the v2.2 ChemWorkBench ingestion architecture.

LLM‑friendly commentary:
------------------------
Loaders in v2.2 are *format readers only*. They do NOT:
- detect technique
- classify vendor
- interpret scientific meaning
- normalize tokens
- perform anchor scoring

All detection and classification happens *before* loaders run.

This loader simply converts a CSV file into a universal Python structure
(list-of-dicts), which processors can interpret after the anchor engine
has selected the correct technique.

This file is intentionally small, deterministic, and easy for both humans
and LLMs to maintain.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping

from .base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class CSVLoader(BaseVendorLoader):
    """
    CSVLoader (v2.2)

    A universal CSV format loader. This loader is intentionally
    technique‑agnostic and vendor‑agnostic. It reads CSV files into a
    list‑of‑dicts structure, leaving all scientific interpretation to
    processors.

    Responsibilities (v2.2):
    - Read CSV files safely and deterministically
    - Produce a universal structure (list-of-dicts)
    - Extract minimal structural metadata
    - Raise structured loader errors

    Non‑responsibilities:
    - Technique detection (handled by anchor engine)
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
    # v2.2 rule: sniffing is *format-only*. Loaders do not sniff technique.
    # This loader claims only .csv files.
    # ------------------------------------------------------------------
    def sniff(self, path: Path) -> bool:
        path = Path(path)
        return path.suffix.lower() == ".csv"

    # ------------------------------------------------------------------
    # load_raw(path)
    # ------------------------------------------------------------------
    # Reads the CSV file and returns a list-of-dicts.
    # This is the only I/O-heavy part of the loader.
    # ------------------------------------------------------------------
    def load_raw(self, path: Path) -> Any:
        path = Path(path)
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
    # can interpret. For CSV, this is simply the list-of-dicts.
    # ------------------------------------------------------------------
    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return raw_data
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize CSV data: {exc}"
            ) from exc
