from __future__ import annotations

import struct
from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np

PathLike = Union[str, Path]


def load_sp(path_or_bytes: PathLike | bytes) -> Dict:
    """
    Minimal loader for PerkinElmer/Agilent .sp spectral files.

    Supports:
        - Single-spectrum SP files
        - Basic header parsing
        - X start, X end, and point count
        - Y-data extraction (float32)

    Does NOT support (yet):
        - Multi-block SP files
        - Complex experiment types
        - Logarithmic axes

    Returns:
        {
            "columns": ["x", "y"],
            "data": [[x1, y1], ...],
            "metadata": {...},
            "raw_format": "sp"
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
    if len(raw) < 256:
        raise ValueError(".sp file too small to contain valid header.")

    # ------------------------------------------------------------------
    # Step 3 — Parse SP header (simplified)
    # ------------------------------------------------------------------
    # Common SP header offsets (PerkinElmer/Agilent style):
    #   0x00: signature (2 bytes)
    #   0x10: number of points (int32)
    #   0x14: X start (float32)
    #   0x18: X end (float32)
    #   0x1C: Y data offset (int32)
    #   0x20: Y data type (0 = float32)

    signature = raw[0:2].decode(errors="ignore")

    n_points = struct.unpack("<I", raw[0x10:0x14])[0]
    x_start = struct.unpack("<f", raw[0x14:0x18])[0]
    x_end = struct.unpack("<f", raw[0x18:0x1C])[0]
    y_offset = struct
