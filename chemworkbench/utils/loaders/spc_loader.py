from __future__ import annotations

import struct
from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np

PathLike = Union[str, Path]


def load_spc(path_or_bytes: PathLike | bytes) -> Dict:
    """
    Minimal SPC loader for Galactic .spc files.

    Supports:
        - Single-spectrum SPC files
        - Basic header parsing
        - X-axis start, increment, and point count
        - Y-data extraction (float32)

    Does NOT support (yet):
        - Multi-subfile SPCs
        - Complex experiment types
        - XYXY mode
        - Logarithmic axes

    Returns:
        {
            "columns": ["x", "y"],
            "data": [[x1, y1], ...],
            "metadata": {...},
            "raw_format": "spc"
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
    # Step 2 — Parse SPC header (first 512 bytes)
    # ------------------------------------------------------------------
    if len(raw) < 512:
        raise ValueError("SPC file too small to contain valid header.")

    header = raw[:512]

    # SPC header structure (simplified)
    # Byte offsets from Galactic SPC spec:
    #  0: file version
    #  2: experiment type
    #  4: number of points (int32)
    # 10: X start (float32)
    # 14: X increment (float32)
    # 16: Y data type (0 = float32)
    # 20: number of subfiles (int16)

    version = header[0]
    experiment_type = header[2]
    n_points = struct.unpack("<I", header[4:8])[0]
    x_start = struct.unpack("<f", header[10:14])[0]
    x_increment = struct.unpack("<f", header[14:18])[0]
    y_data_type = header[16]
    n_subfiles = struct.unpack("<H", header[20:22])[0]

    # ------------------------------------------------------------------
    # Step 3 — Validate supported SPC type
    # ------------------------------------------------------------------
    if n_subfiles > 1:
        raise NotImplementedError(
            "Multi-subfile SPC not supported in v2 (can be added later)."
        )

    if y_data_type != 0:
        raise NotImplementedError(
            f"Unsupported Y-data type {y_data_type} (only float32 supported)."
        )

    # ------------------------------------------------------------------
    # Step 4 — Extract Y-data (float32 array)
    # ------------------------------------------------------------------
    y_offset = 512
    expected_bytes = n_points * 4

    if len(raw) < y_offset + expected_bytes:
        raise ValueError("SPC file truncated or invalid.")

    y_vals = np.frombuffer(raw[y_offset:y_offset + expected_bytes], dtype="<f4")

    # ------------------------------------------------------------------
    # Step 5 — Construct X-axis
    # ------------------------------------------------------------------
    x_vals = x_start + np.arange(n_points) * x_increment

    # ------------------------------------------------------------------
    # Step 6 — Build output structure
    # ------------------------------------------------------------------
    data = list(zip(x_vals.tolist(), y_vals.tolist()))

    metadata = {
        "version": version,
        "experiment_type": experiment_type,
        "n_points": n_points,
        "x_start": x_start,
        "x_increment": x_increment,
        "y_data_type": y_data_type,
        "n_subfiles": n_subfiles,
        "source_path": str(path) if path else None,
    }

    return {
        "columns": ["x", "y"],
        "data": data,
        "metadata": metadata,
        "raw_format": "spc",
    }
