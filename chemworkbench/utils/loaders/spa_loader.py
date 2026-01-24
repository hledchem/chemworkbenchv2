from __future__ import annotations

import struct
from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np

PathLike = Union[str, Path]


def load_spa(path_or_bytes: PathLike | bytes) -> Dict:
    """
    Minimal SPA loader for Thermo/PerkinElmer/Agilent FTIR .spa files.

    Supports:
        - Single-spectrum SPA files
        - Basic header parsing
        - X-axis start, end, and point count
        - Y-data extraction (float32)

    Does NOT support (yet):
        - Multi-block SPA files
        - Complex experiment types
        - Interferograms
        - Logarithmic axes

    Returns:
        {
            "columns": ["x", "y"],
            "data": [[x1, y1], ...],
            "metadata": {...},
            "raw_format": "spa"
        }
    """
    # ------------------------------------------------------------------
    # Step 1 — Normalize input
    # ------------------------------------------------------------------
    if isinstance(path_or_bytes, (str, Path)):
        path = Path(path_or_bytes)
        raw = path.read_bytes()
    elif isinstance(path_or_bytes, bytes):
        raw = path_or_bytes
        path = None
    else:
        raise TypeError(f"Unsupported input type: {type(path_or_bytes)}")

    # ------------------------------------------------------------------
    # Step 2 — Validate minimum size
    # ------------------------------------------------------------------
    if len(raw) < 512:
        raise ValueError("SPA file too small to contain valid header.")

    # ------------------------------------------------------------------
    # Step 3 — Parse SPA header (simplified)
    # ------------------------------------------------------------------
    # Common SPA header offsets (Thermo/PerkinElmer style):
    #  0x00: signature "PE"
    #  0x10: number of points (int32)
    #  0x14: X start (float32)
    #  0x18: X end (float32)
    #  0x1C: Y data offset (int32)
    #  0x20: Y data type (0 = float32)

    signature = raw[0:2].decode(errors="ignore")
    if signature not in {"PE", "SP"}:
        # Some vendors use "SP" or other variants
        pass

    n_points = struct.unpack("<I", raw[0x10:0x14])[0]
    x_start = struct.unpack("<f", raw[0x14:0x18])[0]
    x_end = struct.unpack("<f", raw[0x18:0x1C])[0]
    y_offset = struct.unpack("<I", raw[0x1C:0x20])[0]
    y_data_type = struct.unpack("<I", raw[0x20:0x24])[0]

    if y_data_type != 0:
        raise NotImplementedError(
            f"Unsupported Y-data type {y_data_type} (only float32 supported)."
        )

    # ------------------------------------------------------------------
    # Step 4 — Extract Y-data
    # ----------------------------------------------------------------
