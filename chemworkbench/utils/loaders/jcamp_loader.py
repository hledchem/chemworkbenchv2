"""
ChemWorkBench v2.2 — JCAMP-DX Loader
====================================

Purpose
-------
A minimal, technique‑agnostic JCAMP‑DX loader that extracts paired x/y
data from simple JCAMP files (.jdx, .dx). This loader is intentionally
lightweight and deterministic, producing a universal structure compatible
with the v2.2 ingestion engine.

Universal Output Structure
--------------------------
{
    "tabular": [...],   # list-of-dicts: {"x": float, "y": float}
    "scans": [Scan(...)],
    "metadata": {...}
}

This loader does *not* attempt to interpret multi-block JCAMP, derivative
tables, or vendor‑specific extensions. It is designed for robust ingestion
of simple UV‑Vis, IR, Raman, and general spectral JCAMP files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping, List

from chemworkbench.core.models import Scan
from .base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class JCAMPDXLoader(BaseVendorLoader):
    """
    Minimal JCAMP‑DX loader for ChemWorkBench v2.2.

    Responsibilities
    ----------------
    • Read raw JCAMP text
    • Extract minimal metadata (##TITLE, ##DATA TYPE)
    • Extract paired x/y data lines
    • Produce a universal structure for the ingestion engine

    Non‑Responsibilities
    --------------------
    • Technique inference
    • Multi‑block JCAMP parsing
    • Vendor‑specific JCAMP extensions
    """

    VENDOR = "universal"
    FORMAT = "jcamp"
    EXTENSIONS = (".jdx", ".dx")

    # ------------------------------------------------------------------
    # Sniff
    # ------------------------------------------------------------------
    def sniff(self, path: Path) -> bool:
        return path.suffix.lower() in self.EXTENSIONS

    # ------------------------------------------------------------------
    # Raw read
    # ------------------------------------------------------------------
    def load_raw(self, path: Path) -> str:
        try:
            return Path(path).read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            raise LoaderReadError(f"Failed to read JCAMP file '{path}': {exc}") from exc

    # ------------------------------------------------------------------
    # Metadata extraction
    # ------------------------------------------------------------------
    def extract_metadata(self, raw: str) -> Mapping[str, Any]:
        try:
            meta: Dict[str, Any] = {}
            for line in raw.splitlines():
                line = line.strip()
                if line.startswith("##TITLE="):
                    meta["title"] = line.split("=", 1)[1].strip()
                elif line.startswith("##DATA TYPE="):
                    meta["data_type"] = line.split("=", 1)[1].strip()
            return meta
        except Exception as exc:
            raise LoaderMetadataError(f"Failed to extract JCAMP metadata: {exc}") from exc

    # ------------------------------------------------------------------
    # Universal conversion (with structural scan inference)
    # ------------------------------------------------------------------
    def to_universal(self, raw: str, metadata: Mapping[str, Any]) -> Dict[str, Any]:
        try:
            x_vals: List[float] = []
            y_vals: List[float] = []
            tabular: List[Dict[str, float]] = []

            # Parse JCAMP lines
            for line in raw.splitlines():
                line = line.strip()
                if not line or line.startswith("##"):
                    continue

                # Replace commas with spaces, split into tokens
                parts = line.replace(",", " ").split()
                if len(parts) != 2:
                    continue

                try:
                    xv = float(parts[0])
                    yv = float(parts[1])
                except ValueError:
                    continue

                x_vals.append(xv)
                y_vals.append(yv)
                tabular.append({"x": xv, "y": yv})

            scans: List[Scan] = []

            # Structural rule: if x and y arrays are valid → one scan
            if len(x_vals) == len(y_vals) and len(x_vals) > 0:
                scans.append(
                    Scan(
                        x=x_vals,
                        y=y_vals,
                        label=metadata.get("title", "JCAMP Spectrum"),
                    )
                )

            return {
                "tabular": tabular,
                "scans": scans,
                "metadata": metadata,
            }

        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize JCAMP data: {exc}"
            ) from exc
