# utils/loaders/perkinelmer/perkinelmer_sp_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from ..base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class PerkinElmerSPLoader(BaseVendorLoader):
    """
    PerkinElmer SP loader.

    SP is a legacy PerkinElmer spectral export format used for:
    - IR / FTIR
    - UV-Vis
    - Fluorescence
    - Raman

    This scaffold implementation handles ASCII SP exports.
    """

    VENDOR = "perkinelmer"
    FORMAT = "sp"
    EXTENSIONS = (".sp",)

    def sniff(self, path) -> bool:
    path = Path(path)  # normalize input (string or Path)

        return path.suffix.lower() == ".sp"

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
            raise LoaderReadError(f"Failed to read PerkinElmer SP file '{path}': {exc}") from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_points": len(raw_data["x"]),
            }
        except Exception as exc:
            raise LoaderMetadataError(f"Failed to extract metadata from PerkinElmer SP: {exc}") from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "spectrum",
                "x": raw_data["x"],
                "y": raw_data["y"],
                "axis_units": {"x": None, "y": None},
            }
        except Exception as exc:
            raise LoaderNormalizationError(f"Failed to normalize PerkinElmer SP data: {exc}") from exc
