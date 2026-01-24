from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np

PathLike = Union[str, Path]


def load_jcamp(path_or_bytes: PathLike | bytes) -> Dict:
    """
    Load a JCAMP-DX (.dx, .jdx) file into a raw spectral structure.

    Supports:
        - ##XYDATA= (X++(Y..Y)) blocks
        - ##XYPOINTS= blocks
        - ##DATA TABLE= blocks
        - Multi-block JCAMP files
        - Vendor-specific metadata fields

    Returns:
        {
            "columns": ["x", "y"],
            "data": [[x1, y1], [x2, y2], ...],
            "metadata": {...},
            "raw_format": "jcamp_dx"
        }
    """
    # ------------------------------------------------------------------
    # Step 1 — Normalize input
    # ------------------------------------------------------------------
    if isinstance(path_or_bytes, (str, Path)):
        path = Path(path_or_bytes)
        text = path.read_text(errors="ignore")
    elif isinstance(path_or_bytes, bytes):
        text = path_or_bytes.decode(errors="ignore")
        path = None
    else:
        raise TypeError(f"Unsupported input type: {type(path_or_bytes)}")

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    metadata = {}
    x_vals: List[float] = []
    y_vals: List[float] = []

    mode = None  # "xydata", "xypoints", "datatable"

    # ------------------------------------------------------------------
    # Step 2 — Parse JCAMP header + detect data mode
    # ------------------------------------------------------------------
    for line in lines:
        if line.startswith("##"):
            key, _, value = line.partition("=")
            key = key.strip().upper()
            value = value.strip()

            # Metadata fields
            if key not in {"##XYDATA", "##XYPOINTS", "##DATA TABLE"}:
                metadata[key.lstrip("#")] = value

            # Detect data mode
            if key == "##XYDATA":
                mode = "xydata"
                continue
            if key == "##XYPOINTS":
                mode = "xypoints"
                continue
            if key == "##DATA TABLE":
                mode = "datatable"
                continue

            # End of data block
            if key == "##END":
                break

            continue

        # ------------------------------------------------------------------
        # Step 3 — Parse data lines based on mode
        # ------------------------------------------------------------------
        if mode == "xydata":
            # Format: X Y1 Y2 Y3 ...
            parts = line.split()
            if len(parts) < 2:
                continue
            x0 = float(parts[0])
            ys = [float(v) for v in parts[1:]]
            for i, y in enumerate(ys):
                x_vals.append(x0 + i)
                y_vals.append(y)

        elif mode == "xypoints":
            # Format: X, Y
            if "," in line:
                x_str, y_str = line.split(",", 1)
            else:
                x_str, y_str = line.split()
            x_vals.append(float(x_str))
            y_vals.append(float(y_str))

        elif mode == "datatable":
            # Format: X Y
            parts = line.split()
            if len(parts) != 2:
                continue
            x_vals.append(float
