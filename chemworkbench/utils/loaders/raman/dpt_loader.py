# utils/loaders/raman/dpt_loader.py

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


class DPTLoader(BaseVendorLoader):
    """
    DPT Raman loader.

    DPT is a common Raman export format used by several vendors.
    Typically contains:
    - Raman shift (cm^-1)
    - Intensity
    """

    VENDOR = "raman"
    FORMAT = "dpt"
    EXTENSIONS = (".dpt",)

    def sniff(self, path) -> bool:
        path = Path(path)  # normalize input (string or Path)

        return path.suffix.lower() == ".dpt"

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
            raise LoaderReadError(
                f"Failed to read DPT Raman file '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_points": len(raw_data["x"]),
                "technique": Technique.RAMAN,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from DPT Raman: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "spectrum",
                "x": raw_data["x"],
                "y": raw_data["y"],
                "axis_units": {"x": "cm^-1", "y": "intensity"},
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize DPT Raman data: {exc}"
            ) from exc
