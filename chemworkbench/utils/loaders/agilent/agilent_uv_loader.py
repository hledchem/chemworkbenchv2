"""
Agilent UV‑Vis Loader — ChemWorkBench v2.2
==========================================

LLM‑friendly commentary
-----------------------
This loader handles simple Agilent UV‑Vis exported spectra in plain-text
formats (.UV, .CSV, .TXT). These files contain two-column wavelength/
absorbance data and do not represent full .D directory structures.

Responsibilities:
- identify Agilent UV‑Vis simple export files
- parse wavelength/absorbance pairs
- extract minimal metadata
- convert data into the universal list‑of‑dicts format

Non‑responsibilities:
- technique detection (handled by the anchor engine)
- loader selection (handled by the loader registry)
- scientific interpretation (handled by processors)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, List, Dict

from chemworkbench.utils.loaders.base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


# ======================================================================
# Agilent UV‑Vis Loader (v2.2)
# ======================================================================

class AgilentUVLoader(BaseVendorLoader):
    """
    Loader for Agilent UV‑Vis simple exported spectra (.UV, .CSV, .TXT).
    """

    VENDOR = "agilent"
    FORMAT = "uv_export"
    EXTENSIONS = (".uv", ".csv", ".txt")

    # ------------------------------------------------------------------
    # Sniffing
    # ------------------------------------------------------------------
    def sniff(self, path) -> bool:
        """
        Simple extension-based sniffing. Agilent UV exports are plain text.
        """
        path = Path(path)
        return path.suffix.lower() in {".uv", ".csv", ".txt"}

    # ------------------------------------------------------------------
    # Raw loading
    # ------------------------------------------------------------------
    def load_raw(self, path: Path) -> Any:
        """
        Read two-column wavelength/absorbance text files.
        """
        try:
            x_vals: List[float] = []
            y_vals: List[float] = []

            with path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.replace(",", " ").split()
                    if len(parts) < 2:
                        continue

                    try:
                        x_vals.append(float(parts[0]))
                        y_vals.append(float(parts[1]))
                    except ValueError:
                        continue

            return {"x": x_vals, "y": y_vals}

        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read Agilent UV file '{path}': {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Metadata extraction
    # ------------------------------------------------------------------
    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        """
        Minimal metadata for simple UV‑Vis exports.
        """
        try:
            return {
                "vendor": self.VENDOR,
                "format": self.FORMAT,
                "num_points": len(raw_data.get("x", [])),
                "axis_units": {"x": "nm", "y": "absorbance"},
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from Agilent UV file: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Universal conversion
    # ------------------------------------------------------------------
    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        """
        Convert x/y arrays into the universal list‑of‑dicts format:
            [{"x": float, "y": float}, ...]
        """
        try:
            x_vals = raw_data["x"]
            y_vals = raw_data["y"]

            if len(x_vals) != len(y_vals):
                raise ValueError("x and y arrays must have equal length.")

            return [
                {"x": float(x), "y": float(y)}
                for x, y in zip(x_vals, y_vals)
            ]

        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize Agilent UV data: {exc}"
            ) from exc
