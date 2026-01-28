"""
Two‑Column ASCII Loader — ChemWorkBench v2.2
============================================

LLM‑friendly commentary
-----------------------
This loader implements the canonical v2.2 ingestion architecture for
two‑column ASCII files. These files appear across many scientific
techniques (UV‑Vis, IR, Raman, chromatography, electrochemistry), but
the loader does *not* interpret meaning. It simply reads two numeric
columns into a universal structure.

Responsibilities:
- Read two‑column ASCII files safely and deterministically
- Produce a universal structure: list‑of‑dicts with keys "x" and "y"
- Extract minimal structural metadata
- Raise structured loader errors

Non‑responsibilities:
- Technique detection
- Vendor detection
- Scientific interpretation
- Token normalization
- Anchor scoring
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from chemworkbench.utils.loaders.base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


# ======================================================================
# Two‑Column ASCII Loader (v2.2)
# ======================================================================

class TwoColumnASCIILoader(BaseVendorLoader):
    """
    Universal two‑column ASCII loader for ChemWorkBench v2.2.

    Expected structure:
        <float> <float>
        <float> <float>
        ...

    The loader does not validate technique or units. It simply parses
    two numeric columns separated by whitespace.
    """

    VENDOR = "universal"
    FORMAT = "two_column_ascii"
    EXTENSIONS = (".txt", ".dat", ".asc", ".xy")  # non‑authoritative

    # ------------------------------------------------------------------
    # sniff(path)
    # ------------------------------------------------------------------
    # v2.2 rule: sniffing is format‑only. Loaders do not sniff technique.
    # ------------------------------------------------------------------
    def sniff(self, path: Path) -> bool:
        # Very light sniff: check extension only.
        return path.suffix.lower() in self.EXTENSIONS

    # ------------------------------------------------------------------
    # load_raw(path)
    # ------------------------------------------------------------------
    # Reads the file and returns a list‑of‑dicts: [{"x": float, "y": float}, ...]
    # ------------------------------------------------------------------
    def load_raw(self, path: Path) -> Any:
        rows = []
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    parts = stripped.split()
                    if len(parts) != 2:
                        raise LoaderReadError(
                            f"Expected exactly 2 columns in '{path}', got {len(parts)}"
                        )
                    x, y = map(float, parts)
                    rows.append({"x": x, "y": y})
            return rows
        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read two‑column ASCII file '{path}': {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # extract_metadata(raw_data)
    # ------------------------------------------------------------------
    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            return {
                "format": self.FORMAT,
                "vendor": self.VENDOR,
                "num_points": len(raw_data),
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract metadata from two‑column ASCII: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # to_universal(raw_data, metadata)
    # ------------------------------------------------------------------
    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return raw_data
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize two‑column ASCII data: {exc}"
            ) from exc
