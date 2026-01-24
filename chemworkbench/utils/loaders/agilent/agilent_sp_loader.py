# utils/loaders/agilent/agilent_sp_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from ..base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class AgilentSPLoader(BaseVendorLoader):
    """
    Agilent generic spectral loader for .SP-like exports.

    This is a generic spectral loader for legacy Agilent formats that export
    simple x–y data (e.g., IR, UV-Vis, fluorescence).
    """

    VENDOR = "agilent"
    FORMAT = "sp_export"
    EXTENSIONS = (".sp",)

    def sniff(self, path: Path) -> bool:
        return path.suffix.lower() == ".sp"

    def load_raw(self, path: Path) -> Any:
        try:
            x_vals = []
            y_vals = []
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.replace(",", " ").split()
                    if len(parts) < 2:
                        continue
                    try:
                        x_vals.append(float(parts[0]))
                        y_vals.append(float(parts[1]))
                    except ValueError:
                        continue

            return {"x": x_vals, "y": y_vals}
        except Exception as exc:
            raise LoaderReadError(f"Failed to read Agilent SP file '{path}': {exc}") from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_points": len(raw_data.get("x", [])),
            }
        except Exception as exc:
            raise LoaderMetadataError(f"Failed to extract metadata from Agilent SP file: {exc}") from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "x": raw_data["x"],
                "y": raw_data["y"],
                "kind": "spectrum",
                "axis_units": {"x": None, "y": None},
            }
        except Exception as exc:
            raise LoaderNormalizationError(f"Failed to normalize Agilent SP data: {exc}") from exc
