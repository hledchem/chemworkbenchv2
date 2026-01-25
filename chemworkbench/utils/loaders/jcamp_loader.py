# utils/loaders/jcamp_loader.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping

from .base_loader import (
    BaseVendorLoader,
    LoaderReadError,
    LoaderMetadataError,
    LoaderNormalizationError,
)


class JCAMPLoader(BaseVendorLoader):
    """
    Universal JCAMP-DX loader.

    Parses JCAMP files into:
        {
            "metadata": {...},
            "x": [...],
            "y": [...],
        }

    This loader is intentionally minimal and technique-agnostic.
    """

    VENDOR = "universal"
    FORMAT = "jcamp"
    EXTENSIONS = (".jdx", ".dx")

    def sniff(self, path: Path) -> bool:
        return path.suffix.lower() in {".jdx", ".dx"}

    def load_raw(self, path: Path) -> Any:
        try:
            metadata = {}
            x_vals = []
            y_vals = []

            with path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()

                    # Metadata lines: ##KEY=VALUE
                    if line.startswith("##") and "=" in line:
                        key, value = line[2:].split("=", 1)
                        metadata[key.strip().lower()] = value.strip()
                        continue

                    # Data lines: x y
                    if line and not line.startswith("##"):
                        parts = line.split()
                        if len(parts) == 2:
                            try:
                                x_vals.append(float(parts[0]))
                                y_vals.append(float(parts[1]))
                            except ValueError:
                                pass

            return {
                "metadata": metadata,
                "x": x_vals,
                "y": y_vals,
            }

        except Exception as exc:
            raise LoaderReadError(
                f"Failed to read JCAMP file '{path}': {exc}"
            ) from exc

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        try:
            md = raw_data.get("metadata", {})
            return {
                "format": self.FORMAT,
                "title": md.get("title"),
                "owner": md.get("owner"),
                "origin": md.get("origin"),
                "num_points": len(raw_data.get("x", [])),
            }
        except Exception as exc:
            raise LoaderMetadataError(
                f"Failed to extract JCAMP metadata: {exc}"
            ) from exc

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        try:
            return {
                "x": raw_data["x"],
                "y": raw_data["y"],
                "metadata": raw_data["metadata"],
            }
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to normalize JCAMP data: {exc}"
            ) from exc
