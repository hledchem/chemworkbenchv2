# loaders/ch_instruments/chi_dta_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from ..base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class CHIDTALoader(BaseVendorLoader):
    """
    CH Instruments .DTA loader.

    Supports:
    - Cyclic voltammetry (CV)
    - DPV
    - SWV
    - Chronoamperometry
    - Chronopotentiometry

    This scaffold implementation reads ASCII-exported DTA files.
    """

    VENDOR = "ch_instruments"
    FORMAT = "dta"
    EXTENSIONS = (".dta",)

    def sniff(self, path: Path) -> bool:
        return path.suffix.lower() == ".dta"

    def load_raw(self, path: Path) -> Any:
        try:
            x_vals, y_vals = [], []
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("CH Instruments"):
                        continue
                    parts = line.replace(",", " ").split()
                    if len(parts) >= 2:
                        try:
                            x_vals.append(float(parts[0]))
                            y_vals.append(float(parts[1]))
                        except ValueError:
                            continue

            return {"x": x_vals, "y": y_vals, "path": str(path)}

        except Exception as exc:
            raise LoaderReadError(f"Failed to read CHI .DTA file '{path}': {exc}") from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "vendor": self.VENDOR,
                "format": self.FORMAT,
                "num_points": len(raw_data["x"]),
                "technique": "electrochemistry",
            }
        except Exception as exc:
            raise LoaderMetadataError(f"Failed to extract metadata from CHI .DTA: {exc}") from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "echem_trace",
                "x": raw_data["x"],
                "y": raw_data["y"],
                "axis_units": {"x": "V", "y": "A"},
            }
        except Exception as exc:
            raise LoaderNormalizationError(f"Failed to normalize CHI .DTA data: {exc}") from exc
