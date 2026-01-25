# utils/loaders/shimadzu/shimadzu_lcd_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Dict, List

from chemworkbench.core.models import Technique

from ..base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class ShimadzuLCDLoader(BaseVendorLoader):
    """
    Shimadzu LCD loader.

    LCD directories contain:
    - Chromatography traces (HPLC, UHPLC, GC)
    - MS spectra (LC-MS, GC-MS)
    - PDA/DAD spectral data

    This scaffold implementation looks for CSV-like files inside the LCD directory.
    """

    VENDOR = "shimadzu"
    FORMAT = "lcd"
    EXTENSIONS = (".lcd",)

    def sniff(self, path) -> bool:
    path = Path(path)  # normalize input (string or Path)

        return path.is_dir() and path.suffix.lower() == ".lcd"

    def _find_data_files(self, path: Path) -> List[Path]:
        return list(path.glob("*.csv")) + list(path.glob("*.txt"))

    def load_raw(self, path: Path) -> Any:
        try:
            files = self._find_data_files(path)
            if not files:
                raise LoaderReadError(
                    f"No data files found in Shimadzu LCD directory '{path}'"
                )

            datasets: Dict[str, Dict[str, Any]] = {}

            for fpath in files:
                x_vals, y_vals = [], []
                with fpath.open("r", encoding="utf-8", errors="ignore") as f:
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

                datasets[fpath.name] = {"x": x_vals, "y": y_vals}

            return {"datasets": datasets, "directory": str(path)}

        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read Shimadzu LCD directory '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            datasets = raw_data.get("datasets", {})
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_datasets": len(datasets),
                "dataset_names": list(datasets.keys()),
                "technique": Technique.CHROM,  # LCD is primarily chromatography
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from Shimadzu LCD: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "chromatogram_set",
                "datasets": raw_data["datasets"],
                "axis_units": {"x": "min", "y": "intensity"},
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize Shimadzu LCD data: {exc}"
            ) from exc
