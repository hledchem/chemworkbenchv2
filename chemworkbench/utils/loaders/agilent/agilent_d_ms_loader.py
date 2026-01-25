# utils/loaders/agilent/agilent_d_ms_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, List, Dict

from chemworkbench.core.models import Technique

from ..base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class AgilentDMSLoader(BaseVendorLoader):
    """
    Agilent .D directory loader for MS data (LC-MS / GC-MS / MS/MS).

    This is a scaffold implementation. In real deployments, this would likely
    use vendor SDKs or intermediate exports. Here, we assume the presence of
    one or more CSV files with m/z vs intensity (possibly per scan or averaged).
    """

    VENDOR = "agilent"
    FORMAT = "d_ms"
    EXTENSIONS = (".d",)



    def sniff(self, path) -> bool:
        """
        Agilent .D directory sniffer.
        Accepts either a string or a Path.
        """
        path = Path(path)  # normalize input
        return path.is_dir() and path.suffix.lower() == ".d"

    def _find_ms_files(self, path: Path) -> List[Path]:
        # Heuristic: look for MS*.CSV or similar
        candidates = list(path.glob("MS*.CSV")) + list(path.glob("*MS*.CSV"))
        if candidates:
            return candidates
        return list(path.glob("*.csv"))

    def load_raw(self, path: Path) -> Any:
        try:
            ms_files = self._find_ms_files(path)
            if not ms_files:
                raise LoaderReadError(
                    f"No MS files found in Agilent .D directory '{path}'"
                )

            spectra: Dict[str, Dict[str, Any]] = {}

            for fpath in ms_files:
                mz = []
                intensity = []
                with fpath.open("r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        parts = line.replace(",", " ").split()
                        if len(parts) < 2:
                            continue
                        try:
                            mz.append(float(parts[0]))
                            intensity.append(float(parts[1]))
                        except ValueError:
                            continue

                spectra[fpath.name] = {
                    "mz": mz,
                    "intensity": intensity,
                }

            return {
                "spectra": spectra,
                "directory": str(path),
            }

        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read Agilent .D MS directory '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            specs = raw_data.get("spectra", {})
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_spectra": len(specs),
                "spectrum_names": list(specs.keys()),
                "directory": raw_data.get("directory"),
                "technique": Technique.MS,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from Agilent .D MS: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "spectra": raw_data["spectra"],
                "kind": "ms_spectrum_set",
                "axis_units": {"x": "m/z", "y": "intensity"},
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize Agilent .D MS data: {exc}"
            ) from exc
