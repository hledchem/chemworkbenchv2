# utils/loaders/agilent/agilent_uv_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from chemworkbench.core.models import Technique

from ..base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class AgilentUVLoader(BaseVendorLoader):
    """
    Agilent UV-Vis loader for simple exported spectra (.UV, .CSV, .TXT).

    This loader targets single-file exports, not full .D directories.
    """

    VENDOR = "agilent"
    FORMAT = "uv_export"
    EXTENSIONS = (".uv", ".csv", ".txt")

    def sniff(self, path) -> bool:
        path = Path(path)  # normalize input (string or Path)
        return path.suffix.lower() in {".uv", ".csv", ".txt"}


    def load_raw(self, path: Path) -> Any:
        try:
            # Minimal CSV/TXT reader: wavelength, absorbance
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
            raise LoaderReadError(
                f"Failed to read Agilent UV file '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_points": len(raw_data.get("x", [])),
                "technique": Technique.UVVIS,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from Agilent UV file: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "x": raw_data["x"],
                "y": raw_data["y"],
                "kind": "spectrum",
                "axis_units": {"x": "nm", "y": "absorbance"},
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize Agilent UV data: {exc}"
            ) from exc
