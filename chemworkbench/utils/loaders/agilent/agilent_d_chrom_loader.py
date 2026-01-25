# utils/loaders/agilent/agilent_d_chrom_loader.py

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


class AgilentDChromLoader(BaseVendorLoader):
    """
    Agilent .D directory loader for chromatography data (HPLC/GC/LC-MS chromatograms).

    This scaffold implementation looks for a chromatogram-like CSV inside the .D
    directory and parses time vs intensity.
    """

    VENDOR = "agilent"
    FORMAT = "d_chrom"
    EXTENSIONS = (".d",)


def sniff(self, path) -> bool:
    """
    Agilent .D directory sniffer.
    Accepts either a string or a Path.
    """
    path = Path(path)  # normalize input
    return path.is_dir() and path.suffix.lower() == ".d"

    def _find_chrom_files(self, path: Path) -> List[Path]:
        # Heuristic: look for CHROM*.CSV or similar
        candidates = list(path.glob("CHROM*.CSV")) + list(path.glob("*.CHROM.CSV"))
        if candidates:
            return candidates
        # Fallback: any CSV that looks like time,intensity
        return list(path.glob("*.csv"))

    def load_raw(self, path: Path) -> Any:
        try:
            chrom_files = self._find_chrom_files(path)
            if not chrom_files:
                raise LoaderReadError(
                    f"No chromatogram files found in Agilent .D directory '{path}'"
                )

            chromatograms: Dict[str, Dict[str, Any]] = {}

            for fpath in chrom_files:
                times = []
                intensities = []
                with fpath.open("r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        parts = line.replace(",", " ").split()
                        if len(parts) < 2:
                            continue
                        try:
                            times.append(float(parts[0]))
                            intensities.append(float(parts[1]))
                        except ValueError:
                            continue

                chromatograms[fpath.name] = {
                    "time": times,
                    "intensity": intensities,
                }

            return {
                "chromatograms": chromatograms,
                "directory": str(path),
            }

        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read Agilent .D chromatogram directory '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            chroms = raw_data.get("chromatograms", {})
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_traces": len(chroms),
                "trace_names": list(chroms.keys()),
                "directory": raw_data.get("directory"),
                "technique": Technique.CHROM,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from Agilent .D chromatograms: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            # Universal representation: dict of chromatograms
            return {
                "chromatograms": raw_data["chromatograms"],
                "kind": "chromatogram_set",
                "axis_units": {"x": "min", "y": "intensity"},
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize Agilent .D chromatogram data: {exc}"
            ) from exc
