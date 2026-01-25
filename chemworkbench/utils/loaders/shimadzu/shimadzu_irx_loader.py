# utils/loaders/shimadzu/shimadzu_irx_loader.py

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


class ShimadzuIRXLoader(BaseVendorLoader):
    """
    Shimadzu IRX loader.

    IRX is a Shimadzu IR/FTIR format used for:
    - IR
    - FTIR
    - ATR-FTIR
    """

    VENDOR = "shimadzu"
    FORMAT = "irx"
    EXTENSIONS = (".irx",)

    def sniff(self, path) -> bool:
    path = Path(path)  # normalize input (string or Path)

        return path.suffix.lower() == ".irx"

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
                f"Failed to read Shimadzu IRX file '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_points": len(raw_data["x"]),
                "technique": Technique.IR,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from Shimadzu IRX: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "spectrum",
                "x": raw_data["x"],
                "y": raw_data["y"],
                "axis_units": {"x": "cm^-1", "y": "absorbance"},
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize Shimadzu IRX data: {exc}"
            ) from exc
