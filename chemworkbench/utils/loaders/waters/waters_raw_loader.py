# utils/loaders/waters/waters_raw_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Dict, List

from ..base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class WatersRAWLoader(BaseVendorLoader):
    """
    Waters RAW loader.

    Waters RAW directories contain:
    - Chromatography traces (LC, LC-MS)
    - MS1 spectra
    - MS/MS spectra
    - Function metadata
    - Scan metadata

    This scaffold implementation avoids proprietary SDKs and instead looks for
    CSV/TXT exports inside the RAW directory.
    """

    VENDOR = "waters"
    FORMAT = "raw"
    EXTENSIONS = (".raw",)

    def sniff(self, path: Path) -> bool:
        return path.is_dir() and path.suffix.lower() == ".raw"

    # -----------------------------
    # Helpers
    # -----------------------------

    def _find_data_files(self, path: Path) -> List[Path]:
        # Waters often exports chromatograms and spectra as CSV/TXT
        return list(path.glob("*.csv")) + list(path.glob("*.txt"))

    # -----------------------------
    # Loader API
    # -----------------------------

    def load_raw(self, path: Path) -> Any:
        try:
            files = self._find_data_files(path)
            if not files:
                raise LoaderReadError(f"No CSV/TXT data files found in Waters RAW directory '{path}'")

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

                datasets[fpath.name] = {
                    "x": x_vals,
                    "y": y_vals,
                }

            return {
                "datasets": datasets,
                "directory": str(path),
            }
        except Exception as exc:
            raise LoaderReadError(f"Failed to read Waters RAW directory '{path}': {exc}") from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            datasets = raw_data.get("datasets", {})
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_datasets": len(datasets),
                "dataset_names": list(datasets.keys()),
                "technique": "ms",  # RAW is primarily MS/LC-MS
            }
        except Exception as exc:
            raise LoaderMetadataError(f"Failed to extract metadata from Waters RAW: {exc}") from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "ms_or_chrom_set",
                "datasets": raw_data["datasets"],
                "axis_units": {"x": None, "y": "intensity"},
            }
        except Exception as exc:
            raise LoaderNormalizationError(f"Failed to normalize Waters RAW data: {exc}") from exc
