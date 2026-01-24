# utils/loaders/csv_loader.py

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, Mapping

from .base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class CSVLoader(BaseVendorLoader):
    """
    Universal CSV loader.

    This loader is intentionally technique-agnostic. It simply reads CSV files
    into a list-of-dicts structure and leaves interpretation to processors.
    """

    VENDOR = "universal"
    FORMAT = "csv"
    EXTENSIONS = (".csv",)

    def sniff(self, path: Path) -> bool:
        # Basic extension check; CSV is too generic for deeper sniffing
        return path.suffix.lower() == ".csv"

    def load_raw(self, path: Path) -> Any:
        try:
            with path.open("r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as exc:
            raise LoaderReadError(f"Failed to read CSV file '{path}': {exc}") from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "format": "csv",
                "num_rows": len(raw_data),
                "num_columns": len(raw_data[0]) if raw_data else 0,
            }
        except Exception as exc:
            raise LoaderMetadataError(f"Failed to extract CSV metadata: {exc}") from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        """
        Universal representation for CSV is simply the list-of-dicts structure.
        Processors will interpret this based on technique.
        """
        try:
            return raw_data
        except Exception as exc:
            raise LoaderNormalizationError(f"Failed to normalize CSV data: {exc}") from exc
