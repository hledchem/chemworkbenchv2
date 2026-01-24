# utils/loaders/agilent/agilent_d_uvvis_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from ..base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class AgilentDUVVisLoader(BaseVendorLoader):
    """
    Agilent .D directory loader for UV-Vis data.

    This loader expects an Agilent .D directory containing UV-Vis spectra.
    Implementation here is a scaffold: it looks for a primary data file
    (e.g., 'DATA.CSV') and parses wavelength vs absorbance.
    """

    VENDOR = "agilent"
    FORMAT = "d_uvvis"
    EXTENSIONS = (".d",)

    def sniff(self, path: Path) -> bool:
        return path.is_dir() and path.suffix.lower() == ".d"

    def _find_data_file(self, path: Path) -> Path:
        # Simple heuristic: look for CSV-like data inside the .D directory
        candidates = ["DATA.CSV", "DATA.TXT", "UV.CSV"]
        for name in candidates:
            candidate = path / name
            if candidate.exists():
                return candidate
        # Fallback: first .csv in directory
        for p in path.glob("*.csv"):
            return p
        raise LoaderReadError(f"No UV-Vis data file found in Agilent .D directory '{path}'")

    def load_raw(self, path: Path) -> Any:
        try:
            data_file = self._find_data_file(path)
            x_vals = []
            y_vals = []
            with data_file.open("r", encoding="utf-8", errors="ignore") as f:
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

            return {
                "x": x_vals,
                "y": y_vals,
                "source_file": str(data_file),
            }
        except Exception as exc:
            raise LoaderReadError(f"Failed to read Agilent .D UV-Vis directory '{path}': {exc}") from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_points": len(raw_data.get("x", [])),
                "source_file": raw_data.get("source_file"),
                "technique": "uvvis",
            }
        except Exception as exc:
            raise LoaderMetadataError(f"Failed to extract metadata from Agilent .D UV-Vis: {exc}") from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "x": raw_data["x"],
                "y": raw_data["y"],
                "kind": "spectrum",
                "axis_units": {"x": "nm", "y": "absorbance"},
            }
        except Exception as exc:
            raise LoaderNormalizationError(f"Failed to normalize Agilent .D UV-Vis data: {exc}") from exc
