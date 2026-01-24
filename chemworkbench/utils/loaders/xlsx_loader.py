from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Union

import openpyxl  # XLSX reader

PathLike = Union[str, Path]


def load_xlsx(path_or_bytes: PathLike | bytes) -> Dict:
    """
    Load an XLSX file into a raw tabular structure.

    This loader:
        - reads the first non-empty sheet
        - extracts header row if present
        - handles mixed data types
        - returns a raw table for the cleaning layer

    Returns:
        {
            "columns": List[str],
            "data": List[List[float | str]],
            "metadata": Dict,
            "raw_format": "xlsx"
        }
    """
    # ------------------------------------------------------------------
    # Step 1 — Normalize input
    # ------------------------------------------------------------------
    if isinstance(path_or_bytes, (str, Path)):
        path = Path(path_or_bytes)
        wb = openpyxl.load_workbook(path, data_only=True)
    elif isinstance(path_or_bytes, bytes):
        from io import BytesIO
        wb = openpyxl.load_workbook(BytesIO(path_or_bytes), data_only=True)
        path = None
    else:
        raise TypeError(f"Unsupported input type: {type(path_or_bytes)}")

    # ------------------------------------------------------------------
    # Step 2 — Select the first non-empty sheet
    # ------------------------------------------------------------------
    sheet = None
    for ws in wb.worksheets:
        if ws.max_row > 1 and ws.max_column > 0:
            sheet = ws
            break

    if sheet is None:
        raise ValueError("XLSX file contains no non-empty sheets.")

    # ------------------------------------------------------------------
    # Step 3 — Extract rows
    # ------------------------------------------------------------------
    rows = []
    for row in sheet.iter_rows(values_only=True):
        if any(cell is not None and str(cell).strip() for cell in row):
            rows.append([_normalize_cell(cell) for cell in row])

    if not rows:
        raise ValueError("XLSX sheet appears to be empty.")

    # ------------------------------------------------------------------
    # Step 4 — Detect header row
    # ------------------------------------------------------------------
    header = rows[0]
    if _looks_like_header(header):
        columns = [str(c) for c in header]
        data_rows = rows[1:]
    else:
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
            "sheet_name": sheet.title,
            "source_path": str(path) if path else None,
        },
        "raw_format": "xlsx",
    }


# ======================================================================
# Helper functions
# ======================================================================

def _normalize_cell(cell):
    """Convert Excel cell values to clean Python types."""
    if cell is None:
        return ""
    if isinstance(cell, (int, float)):
        return cell
    return str(cell).strip()


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

    return numeric_count < len(row) / 2
