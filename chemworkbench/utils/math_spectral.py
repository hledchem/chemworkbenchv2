"""
math_spectral.py — Universal Spectral Math Layer (ChemWorkBench v2.2)
=====================================================================

LLM‑friendly commentary
-----------------------
This module implements the canonical, technique‑agnostic spectral math
utilities for ChemWorkBench v2.2. All functions are:

• pure (no mutation of inputs)
• stateless
• vectorized where possible
• processor‑agnostic
• technique‑agnostic
• reusable across UV‑Vis, IR, Raman, MS, NMR magnitude, etc.

Responsibilities:
- provide universal 1D spectral transforms (baseline, smoothing, normalization)
- provide peak detection and region integration
- ensure consistent behavior across all processors
- avoid duplication (each operation implemented once here)

Non‑responsibilities:
- file I/O
- processor orchestration
- technique‑specific interpretation
"""

from __future__ import annotations

from typing import Sequence, Tuple, Optional, Dict, Any

import numpy as np
from numpy import trapezoid   # NumPy 2.0‑safe trapezoidal integration

from scipy import sparse
from scipy.sparse.linalg import spsolve


# ============================================================================
# Baseline Correction
# ============================================================================

def baseline_polynomial(
    x: Sequence[float],
    y: Sequence[float],
    order: int = 3,
) -> Tuple[np.ndarray, np.ndarray]:
    """Polynomial baseline fitting."""
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)
    coeffs = np.polyfit(x_arr, y_arr, deg=order)
    baseline = np.polyval(coeffs, x_arr)
    return x_arr, baseline


def baseline_rolling_min(
    x: Sequence[float],
    y: Sequence[float],
    window: int = 51,
) -> Tuple[np.ndarray, np.ndarray]:
    """Rolling minimum baseline estimate."""
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    if window < 1:
        window = 1
    if window % 2 == 0:
        window += 1

    half = window // 2
    baseline = np.empty_like(y_arr)

    for i in range(len(y_arr)):
        start = max(0, i - half)
        end = min(len(y_arr), i + half + 1)
        baseline[i] = np.min(y_arr[start:end])

    return x_arr, baseline


def baseline_rolling_quantile(
    x: Sequence[float],
    y: Sequence[float],
    window: int = 51,
    quantile: float = 0.1,
) -> Tuple[np.ndarray, np.ndarray]:
    """Rolling quantile baseline (e.g., 10th percentile)."""
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    if window < 1:
        window = 1
    if window % 2 == 0:
        window += 1

    half = window // 2
    baseline = np.empty_like(y_arr)
    q = np.clip(quantile, 0.0, 1.0)

    for i in range(len(y_arr)):
        start = max(0, i - half)
        end = min(len(y_arr), i + half + 1)
        baseline[i] = np.quantile(y_arr[start:end], q)

    return x_arr, baseline


def baseline_asls(
    x: Sequence[float],
    y: Sequence[float],
    lam: float = 1e5,
    p: float = 0.001,
    n_iter: int = 10,
) -> Tuple[np.ndarray, np.ndarray]:
    """Asymmetric least squares baseline (Eilers & Boelens)."""
    x_arr = np.asarray(x)
    y_arr = np.asarray(y, dtype=float)

    L = len(y_arr)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
    DTD = lam * (D @ D.T)

    w = np.ones(L)
    for _ in range(n_iter):
        W = sparse.diags(w, 0)
        Z = W + DTD
        z = spsolve(Z, w * y_arr)
        w = p * (y_arr > z) + (1 - p) * (y_arr < z)

    return x_arr, z


def baseline(
    x: Sequence[float],
    y: Sequence[float],
    method: str = "polynomial",
    **kwargs,
) -> Tuple[np.ndarray, np.ndarray]:
    """Unified baseline correction wrapper."""
    method = method.lower()

    if method == "polynomial":
        return baseline_polynomial(x, y, **kwargs)
    elif method == "rolling_min":
        return baseline_rolling_min(x, y, **kwargs)
    elif method == "rolling_quantile":
        return baseline_rolling_quantile(x, y, **kwargs)
    elif method == "asls":
        return baseline_asls(x, y, **kwargs)
    else:
        raise ValueError(f"Unknown baseline method: {method}")


# ============================================================================
# Smoothing
# ============================================================================

def _ensure_odd(window: int) -> int:
    """Ensure window size is odd and >= 3."""
    if window < 3:
        return 3
    return window if window % 2 == 1 else window + 1


def smooth_moving_average(
    x: Sequence[float],
    y: Sequence[float],
    window: int = 11,
) -> Tuple[np.ndarray, np.ndarray]:
    """Moving average smoothing."""
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    w = _ensure_odd(window)
    if w > len(y_arr):
        w = len(y_arr) if len(y_arr) % 2 == 1 else len(y_arr) - 1
    if w < 3:
        return x_arr, y_arr

    kernel = np.ones(w) / w
    y_smooth = np.convolve(y_arr, kernel, mode="same")
    return x_arr, y_smooth


def smooth_gaussian(
    x: Sequence[float],
    y: Sequence[float],
    sigma: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """Gaussian smoothing using a discrete Gaussian kernel."""
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    if sigma <= 0:
        return x_arr, y_arr

    half_width = int(3 * sigma)
    idx = np.arange(-half_width, half_width + 1)
    kernel = np.exp(-0.5 * (idx / sigma) ** 2)
    kernel /= kernel.sum()

    y_smooth = np.convolve(y_arr, kernel, mode="same")
    return x_arr, y_smooth


def smooth_savitzky_golay(
    x: Sequence[float],
    y: Sequence[float],
    window: int = 11,
    polyorder: int = 3,
) -> Tuple[np.ndarray, np.ndarray]:
    """Savitzky–Golay smoothing using a sliding polynomial fit."""
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    w = _ensure_odd(window)
    if w <= polyorder:
        w = polyorder + 2 if (polyorder + 2) % 2 == 1 else polyorder + 3

    n = len(y_arr)
    if w > n:
        w = n if n % 2 == 1 else n - 1
    if w <= polyorder:
        return x_arr, y_arr

    half = w // 2
    y_smooth = np.empty_like(y_arr, dtype=float)

    for i in range(n):
        i_min = max(0, i - half)
        i_max = min(n, i + half + 1)
        x_win = x_arr[i_min:i_max]
        y_win = y_arr[i_min:i_max]

        if len(x_win) <= polyorder:
            y_smooth[i] = y_arr[i]
        else:
            coeffs = np.polyfit(x_win, y_win, polyorder)
            y_smooth[i] = np.polyval(coeffs, x_arr[i])

    return x_arr, y_smooth


def smooth(
    x: Sequence[float],
    y: Sequence[float],
    method: str = "moving_average",
    **kwargs,
) -> Tuple[np.ndarray, np.ndarray]:
    """Unified smoothing wrapper."""
    method = method.lower()

    if method == "moving_average":
        return smooth_moving_average(x, y, **kwargs)
    elif method == "gaussian":
        return smooth_gaussian(x, y, **kwargs)
    elif method == "savitzky_golay":
        return smooth_savitzky_golay(x, y, **kwargs)
    else:
        raise ValueError(f"Unknown smoothing method: {method}")


# ============================================================================
# Normalization
# ============================================================================

def normalize_max(
    x: Sequence[float],
    y: Sequence[float],
) -> Tuple[np.ndarray, np.ndarray]:
    """Normalize so that max(|y|) = 1."""
    x_arr = np.asarray(x)
    y_arr = np.asarray(y, dtype=float)

    max_val = np.max(np.abs(y_arr))
    if max_val == 0:
        return x_arr, y_arr

    return x_arr, y_arr / max_val


def normalize_min_max(
    x: Sequence[float],
    y: Sequence[float],
) -> Tuple[np.ndarray, np.ndarray]:
    """Normalize to the [0, 1] range."""
    x_arr = np.asarray(x)
    y_arr = np.asarray(y, dtype=float)

    y_min = np.min(y_arr)
    y_max = np.max(y_arr)

    if y_max == y_min:
        return x_arr, y_arr

    return x_arr, (y_arr - y_min) / (y_max - y_min)


def normalize_area(
    x: Sequence[float],
    y: Sequence[float],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Normalize so that the area under the curve is 1.
    NumPy‑2.0‑safe trapezoidal integration.
    """
    x_arr = np.asarray(x)
    y_arr = np.asarray(y, dtype=float)

    area = float(trapezoid(y_arr, x_arr))
    if area == 0:
        return x_arr, y_arr

    return x_arr, y_arr / area


def normalize(
    x: Sequence[float],
    y: Sequence[float],
    method: str = "max",
    **kwargs,
) -> Tuple[np.ndarray, np.ndarray]:
    """Unified normalization wrapper."""
    method = method.lower()

    if method == "max":
        return normalize_max(x, y, **kwargs)
    elif method == "min_max":
        return normalize_min_max(x, y, **kwargs)
    elif method == "area":
        return normalize_area(x, y, **kwargs)
    else:
        raise ValueError(f"Unknown normalization method: {method}")


# ============================================================================
# Region Integration
# ============================================================================

def integrate_region(
    x: Sequence[float],
    y: Sequence[float],
    x_min: Optional[float] = None,
    x_max: Optional[float] = None,
) -> float:
    """
    Integrate y over a specified x‑range using trapezoidal integration.
    NumPy‑2.0‑safe.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)

    if x_arr.size == 0:
        return 0.0

    if x_min is None:
        x_min = float(x_arr.min())
    if x_max is None:
        x_max = float(x_arr.max())
    if x_min >= x_max:
        return 0.0

    mask = (x_arr >= x_min) & (x_arr <= x_max)
    if not np.any(mask):
        return 0.0

    return float(trapezoid(y_arr[mask], x_arr[mask]))


def integrate_regions(
    x: Sequence[float],
    y: Sequence[float],
    regions: Sequence[Tuple[float, float]],
) -> np.ndarray:
    """Integrate y over multiple x‑ranges."""
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)

    areas = np.zeros(len(regions), dtype=float)
    for i, (x_min, x_max) in enumerate(regions):
        areas[i] = integrate_region(x_arr, y_arr, x_min=x_min, x_max=x_max)

    return areas


# ============================================================================
# Peak Detection
# ============================================================================

class PeakDetectionResult:
    """Container for peak detection results."""

    def __init__(
        self,
        indices: np.ndarray,
        x: np.ndarray,
        y: np.ndarray,
        prominence: Optional[np.ndarray] = None,
        width: Optional[np.ndarray] = None,
        refined_x: Optional[np.ndarray] = None,
        refined_y: Optional[np.ndarray] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.indices = indices
        self.x = x
        self.y = y
        self.prominence = prominence
        self.width = width
        self.refined_x = refined_x
        self.refined_y = refined_y
        self.metadata = metadata or {}
