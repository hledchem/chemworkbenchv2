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
