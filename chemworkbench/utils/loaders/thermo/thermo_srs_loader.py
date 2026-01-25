# utils/loaders/thermo/thermo_srs_loader.py

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


class ThermoSRSLoader(BaseVendorLoader):
    """
    Thermo SRS loader.

    SRS is an older Thermo spectral format used for:
    - IR
    - Raman

    This scaffold implementation handles ASCII SRS exports.
    """

    VENDOR = "thermo"
    FORMAT = "srs"
    EXTENSIONS = (".srs",)

    def sniff(self, path) -> bool:
        path = Path(path)  # normalize input (string or Path)

        return path.suffix.lower() == ".srs"

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

            return {"x": x_vals, "y": y_vals, "path": str(path)}
        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read Thermo SRS file '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_points": len(raw_data.get("x", [])),
                "technique": Technique.IR,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from SRS file: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "spectrum",
                "x": raw_data["x"],
                "y": raw_data["y"],
                "axis_units": {"x": None, "y": None},
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize SRS data: {exc}"
            ) from exc
