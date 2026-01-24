# loaders/bruker/bruker_epr_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Dict, List

from ..base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class BrukerEPRLoader(BaseVendorLoader):
    """
    Bruker EPR loader.

    Supports:
    - ESP (ASCII)
    - DTA + DSC (paired files, metadata only)

    This is a scaffold implementation.
    """

    VENDOR = "bruker"
    FORMAT = "epr"
    EXTENSIONS = (".esp", ".dta")

    def sniff(self, path: Path) -> bool:
        return path.suffix.lower() in {".esp", ".dta"}

    def _load_esp(self, path: Path) -> Dict[str, Any]:
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
        return {"x": x_vals, "y": y_vals}

    def _load_dta_dsc(self, path: Path) -> Dict[str, Any]:
        dsc_path = path.with_suffix(".dsc")
        metadata = {}

        if dsc_path.exists():
            with dsc_path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "=" in line:
                        key, val = line.split("=", 1)
                        metadata[key.strip()] = val.strip()

        # Binary DTA parsing deferred to v3
        return {"x": [], "y": [], "metadata": metadata}

    def load_raw(self, path: Path) -> Any:
        try:
            if path.suffix.lower() == ".esp":
                return self._load_esp(path)
            return self._load_dta_dsc(path)
        except Exception as exc:
            raise LoaderReadError(f"Failed to read Bruker EPR file '{path}': {exc}") from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "vendor": self.VENDOR,
                "format": self.FORMAT,
                "num_points": len(raw_data.get("x", [])),
                "technique": "epr",
            }
        except Exception as exc:
            raise LoaderMetadataError(f"Failed to extract metadata from Bruker EPR: {exc}") from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "spectrum",
                "x": raw_data.get("x", []),
                "y": raw_data.get("y", []),
                "axis_units": {"x": "mT", "y": "intensity"},
                "metadata": raw_data.get("metadata", {}),
            }
        except Exception as exc:
            raise LoaderNormalizationError(f"Failed to normalize Bruker EPR data: {exc}") from exc
