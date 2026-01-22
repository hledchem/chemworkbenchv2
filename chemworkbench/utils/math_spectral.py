"""
math_spectral.py

Universal spectral-domain math utilities for ChemWorkBench v2.
This module contains pure, vectorized baseline correction functions
that apply to any 1D spectroscopy technique (UV-Vis, IR, Raman, NMR magnitude,
MS drift correction, etc.).

All functions follow these rules:
- Pure (no side effects)
- Stateless
- Vectorized where possible
- Return new arrays, never mutate inputs
- Accept numpy arrays or array-like sequences
- Return (x, baseline) pairs
"""

from __future__ import annotations
from typing import Sequence, Tuple
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


# ---------------------------------------------------------------------------
# Polynomial Baseline
# ---------------------------------------------------------------------------

def baseline_polynomial(
    x: Sequence[float],
    y: Sequence[float],
    order: int = 3,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Polynomial baseline fitting.

    Parameters
    ----------
    x : array-like
        X-axis values.
    y : array-like
        Y-axis values.
    order : int
        Polynomial degree (1–7 typical).

    Returns
    -------
    x_arr : np.ndarray
    baseline : np.ndarray
    """
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    coeffs = np.polyfit(x_arr, y_arr, deg=order)
    baseline = np.polyval(coeffs, x_arr)
    return x_arr, baseline


# ---------------------------------------------------------------------------
# Rolling Minimum Baseline
# ---------------------------------------------------------------------------

def baseline_rolling_min(
    x: Sequence[float],
    y: Sequence[float],
    window: int = 51,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Rolling minimum baseline estimate.

    Parameters
    ----------
    x : array-like
    y : array-like
    window : int
        Window size (odd preferred).

    Returns
    -------
    x_arr, baseline
    """
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


# ---------------------------------------------------------------------------
# Rolling Quantile Baseline
# ---------------------------------------------------------------------------

def baseline_rolling_quantile(
    x: Sequence[float],
    y: Sequence[float],
    window: int = 51,
    quantile: float = 0.1,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Rolling quantile baseline (e.g., 10th percentile).

    Parameters
    ----------
    x : array-like
    y : array-like
    window : int
    quantile : float
        Between 0 and 1.

    Returns
    -------
    x_arr, baseline
    """
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


# ---------------------------------------------------------------------------
# Asymmetric Least Squares Baseline (AsLS)
# ---------------------------------------------------------------------------

def baseline_asls(
    x: Sequence[float],
    y: Sequence[float],
    lam: float = 1e5,
    p: float = 0.001,
    n_iter: int = 10,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Asymmetric least squares baseline (Eilers & Boelens).

    Parameters
    ----------
    x : array-like
    y : array-like
    lam : float
        Smoothness parameter (higher = smoother baseline).
    p : float
        Asymmetry parameter (0–1). Small values favor baseline under peaks.
    n_iter : int
        Number of iterations.

    Returns
    -------
    x_arr, baseline
    """
    x_arr = np.asarray(x)
    y_arr = np.asarray(y, dtype=float)
    L = len(y_arr)

    # Second difference matrix
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
    DTD = lam * (D @ D.T)

    w = np.ones(L)
    for _ in range(n_iter):
        W = sparse.diags(w, 0)
        Z = W + DTD
        z = spsolve(Z, w * y_arr)
        w = p * (y_arr > z) + (1 - p) * (y_arr < z)

    baseline = z
    return x_arr, baseline


# ---------------------------------------------------------------------------
# Unified Baseline Wrapper
# ---------------------------------------------------------------------------

def baseline(
    x: Sequence[float],
    y: Sequence[float],
    method: str = "polynomial",
    **kwargs,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Unified baseline correction wrapper.

    Parameters
    ----------
    x : array-like
    y : array-like
    method : str
        One of: "polynomial", "rolling_min", "rolling_quantile", "asls"
    kwargs : dict
        Additional parameters passed to the underlying method.

    Returns
    -------
    x_arr, baseline
    """
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


# ---------------------------------------------------------------------------
# Smoothing Functions
# ---------------------------------------------------------------------------

def _ensure_odd(window: int) -> int:
    """
    Ensure window size is odd and >= 3.
    """
    if window < 3:
        return 3
    if window % 2 == 0:
        return window + 1
    return window


def smooth_moving_average(
    x: Sequence[float],
    y: Sequence[float],
    window: int = 11,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Moving average smoothing.

    Parameters
    ----------
    x : array-like
    y : array-like
    window : int
        Window size (odd, >= 3).

    Returns
    -------
    x_arr, y_smooth
    """
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
    """
    Gaussian smoothing using a discrete Gaussian kernel.

    Parameters
    ----------
    x : array-like
    y : array-like
    sigma : float
        Standard deviation in points.

    Returns
    -------
    x_arr, y_smooth
    """
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    if sigma <= 0:
        return x_arr, y_arr

    half_width = int(3 * sigma)
    size = 2 * half_width + 1
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
    """
    Savitzky–Golay smoothing using a sliding polynomial fit.

    Parameters
    ----------
    x : array-like
    y : array-like
    window : int
        Window size (odd, >= polyorder + 2).
    polyorder : int
        Polynomial order.

    Returns
    -------
    x_arr, y_smooth
    """
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


# ---------------------------------------------------------------------------
# Unified Smoothing Wrapper
# ---------------------------------------------------------------------------

def smooth(
    x: Sequence[float],
    y: Sequence[float],
    method: str = "moving_average",
    **kwargs,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Unified smoothing wrapper.

    Parameters
    ----------
    x : array-like
    y : array-like
    method : str
        One of: "moving_average", "gaussian", "savitzky_golay"
    kwargs : dict
        Additional parameters passed to the underlying method.

    Returns
    -------
    x_arr, y_smooth
    """
    method = method.lower()

    if method == "moving_average":
        return smooth_moving_average(x, y, **kwargs)
    elif method == "gaussian":
        return smooth_gaussian(x, y, **kwargs)
    elif method == "savitzky_golay":
        return smooth_savitzky_golay(x, y, **kwargs)
    else:
        raise ValueError(f"Unknown smoothing method: {method}")
