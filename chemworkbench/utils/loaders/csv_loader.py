from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np

PathLike = Union[str, Path]


def load_csv(path_or_bytes: PathLike | bytes) -> Dict:
    """
    Load a CSV file into a raw tabular structure.

    This loader:
        - detects delimiter automatically
        - handles Excel-style CSVs
        - handles UTF-8/UTF-16/BOM encodings
        - extracts header row if present
        - returns a raw table for the cleaning layer

    Returns:
        {
            "columns": List[str],
            "data": List[List[float | str]],
            "metadata": Dict,
            "raw_format": "csv"
        }
    """
    # ------------------------------------------------------------------
    # Step 1 — Normalize input
    # ------------------------------------------------------------------
    if isinstance(path_or_bytes, (str, Path)):
        path = Path(path_or_bytes)
        raw_bytes = path.read_bytes()
    elif isinstance(path_or_bytes, bytes):
        raw_bytes = path_or_bytes
        path = None
    else:
        raise TypeError(f"Unsupported input type: {type(path_or_bytes)}")

    # Try UTF-8 first, fallback to UTF-16, then latin-1
    text = None
    for encoding in ("utf-8-sig", "utf-16", "latin-1"):
        try:
            text = raw_bytes.decode(encoding)
            break
        except Exception:
            continue

    if text is None:
        raise ValueError("Unable to decode CSV file with common encodings.")

    # ------------------------------------------------------------------
    # Step 2 — Detect delimiter
    # ------------------------------------------------------------------
    sample = text.splitlines()[:5]
    delimiter = _detect_delimiter(sample)

    # ------------------------------------------------------------------
    # Step 3 — Parse CSV
    # ------------------------------------------------------------------
    reader = csv.reader(text.splitlines(), delimiter=delimiter)
    rows = [row for row in reader if any(cell.strip() for cell in row)]

    if not rows:
        raise ValueError("CSV file appears to be empty.")

    # ------------------------------------------------------------------
    # Step 4 — Detect header row
    # ------------------------------------------------------------------
    header = rows[0]
    if _looks_like_header(header):
        columns = header
        data_rows = rows[1:]
    else:
        # Auto-generate column names
        n_cols = len(header)
        columns = [f"col_{i+1}" for i in range(n_cols)]
        data_rows = rows

    # ------------------------------------------------------------------
    # Step 5 — Return raw structure
    # ------------------------------------------------------------------
    return {
        "columns": columns,
        "data": data_rows,
        "metadata": {
            "delimiter": delimiter,
            "encoding": encoding,
            "source_path": str(path) if path else None,
        },
        "raw_format": "csv",
    }


# ======================================================================
# Helper functions
# ======================================================================

def _detect_delimiter(sample_lines: List[str]) -> str:
    """
    Detect delimiter by counting occurrences in sample lines.
    """
    candidates = [",", "\t", ";", "|"]
    counts = {d: 0 for d in candidates}

    for line in sample_lines:
        for d in candidates:
            counts[d] += line.count(d)

    # Pick the delimiter with the highest count
    return max(counts, key=counts.get)


def _looks_like_header(row: List[str]) -> bool:
    """
    Heuristic: header rows contain mostly non-numeric strings.
    """
    numeric_count = 0
    for cell in row:
        try:
            float(cell)
            numeric_count += 1
        except Exception:
            pass

    # If most cells are numeric, it's not a header
    return numeric_count < len(row) / 2
