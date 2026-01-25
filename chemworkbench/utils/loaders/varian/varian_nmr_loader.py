# utils/loaders/varian/varian_nmr_loader.py

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


class VarianNMRLoader(BaseVendorLoader):
    """
    Varian VNMR/VNMRJ NMR loader.

    Varian NMR datasets typically contain:
    - fid (binary time-domain data)
    - procpar (acquisition/processing parameters)
    - text (optional notes)
    - log (optional acquisition log)

    This scaffold implementation reads:
    - FID as signed 32-bit integers
    - procpar as key-value metadata
    """

    VENDOR = "varian"
    FORMAT = "nmr"
    EXTENSIONS = ("",)  # directories have no suffix

    def sniff(self, path) -> bool:
    path = Path(path)  # normalize input (string or Path)

    # Varian datasets are directories containing 'fid' and 'procpar'
    if not path.is_dir():
        return False

    return (path / "fid").exists() and (path / "procpar").exists()
    # -----------------------------
    # Helpers
    # -----------------------------

    def _read_procpar(self, path: Path) -> Dict[str, Any]:
        """
        Minimal parser for Varian procpar files.
        Format is key-value pairs with type annotations.
        """
        params = {}
        try:
            with path.open("r", encoding="latin-1", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split()
                    if len(parts) >= 2:
                        key = parts[0]
                        val = " ".join(parts[1:])
                        params[key] = val
        except Exception:
            pass
        return params

    def _read_fid(self, path: Path) -> List[int]:
        """
        Read Varian FID as big-endian 32-bit integers.
        """
        if not path.exists():
            return []
        try:
            with path.open("rb") as f:
                data = f.read()
            import struct
            count = len(data) // 4
            return list(struct.unpack(f">{count}i", data[: count * 4]))
        except Exception:
            return []

    # -----------------------------
    # Loader API
    # -----------------------------

    def load_raw(self, path: Path) -> Any:
        try:
            fid = self._read_fid(path / "fid")
            procpar = self._read_procpar(path / "procpar")

            return {
                "fid": fid,
                "procpar": procpar,
                "path": str(path),
            }
        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read Varian NMR directory '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            procpar = raw_data.get("procpar", {})
            nucleus = procpar.get("tn", "unknown")  # Varian uses 'tn' for nucleus

            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "nucleus": nucleus,
                "num_fid_points": len(raw_data.get("fid", [])),
                "technique": Technique.NMR,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from Varian NMR: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "nmr_dataset",
                "fid": raw_data["fid"],
                "spectrum": [],  # Varian does not store processed spectrum by default
                "metadata": {
                    "procpar": raw_data["procpar"],
                },
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize Varian NMR data: {exc}"
            ) from exc
