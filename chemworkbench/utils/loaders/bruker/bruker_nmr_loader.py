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


class BrukerNMRLoader(BaseVendorLoader):
    """
    Bruker TopSpin NMR loader.

    Supports directory-based Bruker datasets containing:
    - fid (time-domain)
    - acqus (acquisition parameters)
    - procs (processing parameters)
    - pdata/1/1r (processed spectrum)

    This is a scaffold implementation that reads text metadata and raw binary
    arrays without performing full NMR processing.
    """

    VENDOR = "bruker"
    FORMAT = "nmr"
    EXTENSIONS = (".fid", "")  # directories have no suffix

    def sniff(self, path) -> bool:
        path = Path(path)  # normalize input (string or Path)

        # Bruker NMR datasets are directories containing 'fid' and 'acqus'
        if not path.is_dir():
            return False

        return (path / "fid").exists() and (path / "acqus").exists()

    # -----------------------------
    # Helpers
    # -----------------------------

    def _read_param_file(self, path: Path) -> Dict[str, Any]:
        params = {}
        if not path.exists():
            return params
        try:
            with path.open("r", encoding="latin-1", errors="ignore") as f:
                for line in f:
                    if "=" in line:
                        key, val = line.split("=", 1)
                        params[key.strip()] = val.strip()
        except Exception:
            pass
        return params

    def _read_binary_array(self, path: Path) -> List[int]:
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
            fid = self._read_binary_array(path / "fid")
            acqus = self._read_param_file(path / "acqus")
            procs = self._read_param_file(path / "procs")

            # Processed spectrum (optional)
            pdata_dir = path / "pdata" / "1"
            spectrum = self._read_binary_array(pdata_dir / "1r")

            return {
                "fid": fid,
                "acqus": acqus,
                "procs": procs,
                "spectrum": spectrum,
                "path": str(path),
            }
        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read Bruker NMR directory '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            acqus = raw_data.get("acqus", {})
            nucleus = acqus.get("NUC1", "unknown")
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "nucleus": nucleus,
                "num_fid_points": len(raw_data.get("fid", [])),
                "num_spectrum_points": len(raw_data.get("spectrum", [])),
                "technique": Technique.NMR,
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from Bruker NMR: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "kind": "nmr_dataset",
                "fid": raw_data["fid"],
                "spectrum": raw_data["spectrum"],
                "metadata": {
                    "acqus": raw_data["acqus"],
                    "procs": raw_data["procs"],
                },
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize Bruker NMR data: {exc}"
            ) from exc
