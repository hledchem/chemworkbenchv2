# utils/loaders/jeol/jeol_jdf_loader.py

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


class JEOLJDFLoader(BaseVendorLoader):
    """
    JEOL JDF loader.

    JDF is the JEOL Delta NMR format used for:
    - 1H, 13C
    - COSY, HSQC, HMBC
    - DEPT
    - ROESY, NOESY
    - VT NMR
    - Relaxation experiments

    This scaffold implementation handles ASCII JDF exports.
    """

    VENDOR = "jeol"
    FORMAT = "jdf"
    EXTENSIONS = (".jdf",)

    def sniff(self, path) -> bool:
        path = Path(path)  # normalize input (string or Path)
        return path.suffix.lower() == ".jdf"

    # -----------------------------
    # Helpers
    # -----------------------------

    def _parse_jdf(self, path: Path) -> Dict[str, Any]:
        """
        Minimal JDF parser for ASCII exports.
        JEOL Delta can export JDF as text with key-value metadata and data blocks.
        """
        metadata: Dict[str, Any] = {}
        spectrum: List[float] = []

        try:
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                in_data_block = False
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    # Detect start of data block
                    if line.startswith("##DATA"):
                        in_data_block = True
                        continue

                    if not in_data_block:
                        # Metadata lines: KEY = VALUE
                        if "=" in line:
                            key, val = line.split("=", 1)
                            metadata[key.strip()] = val.strip()
                        continue

                    # Data block: one intensity per line
                    try:
                        spectrum.append(float(line))
                    except ValueError:
                        continue

            return {"metadata": metadata, "spectrum": spectrum}
        except Exception as exc:
            raise LoaderReadError(
                f"Failed to parse JEOL JDF file '{path}': {exc}"
            ) from exc

    # -----------------------------
    # Loader API
    # -----------------------------

    def load_raw(self, path: Path) -> Any:
        return self._parse_jdf(path)

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            md = raw_data.get("metadata", {})
            nucleus = md.get("NUCLEUS", "unknown")
            num_points = len(raw_data.get("spectrum", []))

            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "nucleus": nucleus,
                "num_points": num_points,
                "technique": Technique.NMR,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from JEOL JDF: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "nmr_dataset",
                "spectrum": raw_data["spectrum"],
                "metadata": raw_data["metadata"],
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize JEOL JDF data: {exc}"
            ) from exc
