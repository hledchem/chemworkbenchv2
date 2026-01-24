# loaders/horiba/horiba_fluor_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from ..base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class HoribaFluorescenceLoader(BaseVendorLoader):
    """
    Horiba fluorescence loader.

    Supports ASCII exports:
    - .txt
    - .dat
    - .csv

    Handles:
    - Emission spectra
    - Excitation spectra
    - Simple EEM slices (2-column)
    """

    VENDOR = "horiba"
    FORMAT = "fluor"
    EXTENSIONS = (".txt", ".dat", ".csv")

    def sniff(self, path: Path) -> bool:
        return path.suffix.lower() in self.EXTENSIONS

    def load_raw(self, path: Path) -> Any:
        try:
            x_vals, y_vals = [], []
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
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
            raise LoaderReadError(f"Failed to read Horiba fluorescence file '{path}': {exc}") from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "vendor": self.VENDOR,
                "format": self.FORMAT,
                "num_points": len(raw_data["x"]),
                "technique": "fluorescence",
            }
        except Exception as exc:
            raise LoaderMetadataError(f"Failed to extract metadata from Horiba fluorescence: {exc}") from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "spectrum",
                "x": raw_data["x"],
                "y": raw_data["y"],
                "axis_units": {"x": "nm", "y": "intensity"},
            }
        except Exception as exc:
            raise LoaderNormalizationError(f"Failed to normalize Horiba fluorescence data: {exc}") from exc
