"""
math_spectral.py

Universal spectral-domain math utilities for ChemWorkBench v2.
This module contains pure, vectorized functions that apply to any 1D
spectroscopy technique (UV-Vis, IR, Raman, NMR magnitude, MS, etc.).

Design rules:
- Pure (no side effects)
- Stateless
- Technique-agnostic
- Processor-agnostic
- Non-duplicated (each operation implemented once here)
- Return new arrays or structured results, never mutate inputs
"""

from __future__ import annotations
from typing import Sequence, Tuple, Optional, Dict, Any
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


# ---------------------------------------------------------------------------
# Baseline Correction
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
# Smoothing
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


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def normalize_max(
    x: Sequence[float],
    y: Sequence[float],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Normalize so that max(|y|) = 1.

    Parameters
    ----------
    x : array-like
    y : array-like

    Returns
    -------
    x_arr, y_norm
    """
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
    """
    Normalize to the [0, 1] range.

    Parameters
    ----------
    x : array-like
    y : array-like

    Returns
    -------
    x_arr, y_norm
    """
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
    Uses trapezoidal integration.

    Parameters
    ----------
    x : array-like
    y : array-like

    Returns
    -------
    x_arr, y_norm
    """
    x_arr = np.asarray(x)
    y_arr = np.asarray(y, dtype=float)

    area = np.trapz(y_arr, x_arr)
    if area == 0:
        return x_arr, y_arr

    return x_arr, y_arr / area


def normalize(
    x: Sequence[float],
    y: Sequence[float],
    method: str = "max",
    **kwargs,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Unified normalization wrapper.

    Parameters
    ----------
    x : array-like
    y : array-like
    method : str
        One of: "max", "min_max", "area"
    kwargs : dict
        Additional parameters passed to the underlying method.

    Returns
    -------
    x_arr, y_norm
    """
    method = method.lower()

    if method == "max":
        return normalize_max(x, y, **kwargs)
    elif method == "min_max":
        return normalize_min_max(x, y, **kwargs)
    elif method == "area":
        return normalize_area(x, y, **kwargs)
    else:
        raise ValueError(f"Unknown normalization method: {method}")


# ---------------------------------------------------------------------------
# Region Integration
# ---------------------------------------------------------------------------

def integrate_region(
    x: Sequence[float],
    y: Sequence[float],
    x_min: Optional[float] = None,
    x_max: Optional[float] = None,
) -> float:
    """
    Integrate y over a specified x-range using trapezoidal integration.

    Parameters
    ----------
    x : array-like
        X-axis values.
    y : array-like
        Y-axis values.
    x_min : float, optional
        Lower bound of integration range. If None, use min(x).
    x_max : float, optional
        Upper bound of integration range. If None, use max(x).

    Returns
    -------
    area : float
        Integrated area under the curve in the specified region.
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

    return float(np.trapz(y_arr[mask], x_arr[mask]))


def integrate_regions(
    x: Sequence[float],
    y: Sequence[float],
    regions: Sequence[Tuple[float, float]],
) -> np.ndarray:
    """
    Integrate y over multiple x-ranges.

    Parameters
    ----------
    x : array-like
        X-axis values.
    y : array-like
        Y-axis values.
    regions : sequence of (x_min, x_max)
        List of integration regions.

    Returns
    -------
    areas : np.ndarray
        Array of integrated areas, one per region.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)

    areas = np.zeros(len(regions), dtype=float)
    for i, (x_min, x_max) in enumerate(regions):
        areas[i] = integrate_region(x_arr, y_arr, x_min=x_min, x_max=x_max)
    return areas


# ---------------------------------------------------------------------------
# Peak Detection
# ---------------------------------------------------------------------------

class PeakDetectionResult:
    """
    Container for peak detection results.

    Attributes
    ----------
    indices : np.ndarray
        Indices of detected peaks in the original arrays.
    x : np.ndarray
        X positions of peaks.
    y : np.ndarray
        Y values at peak positions.
    prominence : np.ndarray or None
        Estimated prominence for each peak.
    width : np.ndarray or None
        Estimated width for each peak (in x units).
    refined_x : np.ndarray or None
        Refined peak positions (e.g., quadratic fit), if computed.
    refined_y : np.ndarray or None
        Refined peak heights, if computed.
    metadata : dict
        Additional information (e.g., method, thresholds).
    """

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


def _apply_region(
    x: np.ndarray,
    y: np.ndarray,
    x_min: Optional[float],
    x_max: Optional[float],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Apply an optional x-range restriction and return:
    - mask into original arrays
    - x_region, y_region
    """
    if x_min is None and x_max is None:
        mask = np.ones_like(x, dtype=bool)
        return mask, x, y

    mask = np.ones_like(x, dtype=bool)
    if x_min is not None:
        mask &= x >= x_min
    if x_max is not None:
        mask &= x <= x_max

    return mask, x[mask], y[mask]


def _find_local_maxima_indices(y: np.ndarray) -> np.ndarray:
    """
    Find indices of simple local maxima: y[i] > y[i-1] and y[i] > y[i+1].
    """
    if len(y) < 3:
        return np.array([], dtype=int)

    left = y[1:-1] > y[:-2]
    right = y[1:-1] > y[2:]
    mask = left & right
    return np.where(mask)[0] + 1


def _filter_by_height(
    indices: np.ndarray,
    y: np.ndarray,
    height: Optional[float],
    rel_height: Optional[float],
) -> np.ndarray:
    """
    Filter peaks by absolute and/or relative height.
    """
    if indices.size == 0:
        return indices

    y_peaks = y[indices]
    mask = np.ones_like(indices, dtype=bool)

    if height is not None:
        mask &= y_peaks >= height

    if rel_height is not None:
        max_val = np.max(y)
        mask &= y_peaks >= rel_height * max_val

    return indices[mask]


def _estimate_prominence(
    indices: np.ndarray,
    y: np.ndarray,
) -> np.ndarray:
    """
    Simple prominence estimate: difference between peak height and
    minimum of neighboring valleys.
    """
    if indices.size == 0:
        return np.array([], dtype=float)

    n = len(y)
    prominence = np.zeros_like(indices, dtype=float)

    for i, idx in enumerate(indices):
        left_min = y[idx]
        j = idx
        while j > 0 and y[j] <= y[j - 1]:
            left_min = min(left_min, y[j - 1])
            j -= 1

        right_min = y[idx]
        j = idx
        while j < n - 1 and y[j] <= y[j + 1]:
            right_min = min(right_min, y[j + 1])
            j += 1

        baseline_level = min(left_min, right_min)
        prominence[i] = y[idx] - baseline_level

    return prominence


def _filter_by_prominence(
    indices: np.ndarray,
    y: np.ndarray,
    min_prominence: Optional[float],
) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Filter peaks by minimum prominence.
    """
    if indices.size == 0:
        return indices, None

    prominence = _estimate_prominence(indices, y)

    if min_prominence is None:
        return indices, prominence

    mask = prominence >= min_prominence
    return indices[mask], prominence[mask]


def _estimate_widths(
    indices: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    rel_height: float = 0.5,
) -> np.ndarray:
    """
    Estimate peak widths at a relative height (e.g., half-height).

    Parameters
    ----------
    indices : np.ndarray
        Peak indices.
    x : np.ndarray
    y : np.ndarray
    rel_height : float
        Relative height (0–1) at which to estimate width.

    Returns
    -------
    widths : np.ndarray
        Estimated widths in x units.
    """
    if indices.size == 0:
        return np.array([], dtype=float)

    n = len(y)
    widths = np.zeros_like(indices, dtype=float)

    for i, idx in enumerate(indices):
        peak_y = y[idx]
        target = peak_y * rel_height

        j = idx
        while j > 0 and y[j] > target:
            j -= 1
        x_left = x[j]

        j = idx
        while j < n - 1 and y[j] > target:
            j += 1
        x_right = x[j]

        widths[i] = x_right - x_left

    return widths


def _quadratic_refine(
    indices: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Quadratic refinement of peak positions using a 3-point fit
    around each peak index.

    Returns
    -------
    refined_x, refined_y
    """
    if indices.size == 0:
        return np.array([], dtype=float), np.array([], dtype=float)

    refined_x = np.zeros_like(indices, dtype=float)
    refined_y = np.zeros_like(indices, dtype=float)

    n = len(y)
    for i, idx in enumerate(indices):
        if idx == 0 or idx == n - 1:
            refined_x[i] = x[idx]
            refined_y[i] = y[idx]
            continue

        x0, x1, x2 = x[idx - 1], x[idx], x[idx + 1]
        y0, y1, y2 = y[idx - 1], y[idx], y[idx + 1]

        X = np.array([[x0**2, x0, 1.0],
                      [x1**2, x1, 1.0],
                      [x2**2, x2, 1.0]])
        Y = np.array([y0, y1, y2])
        try:
            a, b, c = np.linalg.lstsq(X, Y, rcond=None)[0]
            if a == 0:
                refined_x[i] = x1
                refined_y[i] = y1
            else:
                x_peak = -b / (2 * a)
                y_peak = a * x_peak**2 + b * x_peak + c
                refined_x[i] = x_peak
                refined_y[i] = y_peak
        except np.linalg.LinAlgError:
            refined_x[i] = x1
            refined_y[i] = y1

    return refined_x, refined_y


def _derivative_peaks(
    x: np.ndarray,
    y: np.ndarray,
) -> np.ndarray:
    """
    Derivative-based peak detection: peaks correspond to zero-crossings
    of the first derivative with negative second derivative.

    Returns
    -------
    indices : np.ndarray
        Estimated peak indices.
    """
    if len(y) < 3:
        return np.array([], dtype=int)

    dy = np.gradient(y, x)
    d2y = np.gradient(dy, x)

    sign = np.sign(dy)
    zero_cross = (sign[:-1] > 0) & (sign[1:] < 0)
    candidate_indices = np.where(zero_cross)[0] + 1

    candidate_indices = candidate_indices[d2y[candidate_indices] < 0]

    return candidate_indices


def detect_peaks(
    x: Sequence[float],
    y: Sequence[float],
    method: str = "local_maxima",
    height: Optional[float] = None,
    rel_height: Optional[float] = None,
    min_prominence: Optional[float] = None,
    estimate_width: bool = True,
    width_rel_height: float = 0.5,
    x_min: Optional[float] = None,
    x_max: Optional[float] = None,
    refine: bool = True,
    derivative: bool = False,
) -> PeakDetectionResult:
    """
    Advanced peak detection for 1D spectra.

    Parameters
    ----------
    x : array-like
    y : array-like
    method : str
        Currently "local_maxima" or "derivative".
    height : float, optional
        Absolute minimum peak height.
    rel_height : float, optional
        Relative minimum peak height (fraction of max(y)).
    min_prominence : float, optional
        Minimum prominence threshold.
    estimate_width : bool
        Whether to estimate peak widths.
    width_rel_height : float
        Relative height at which to estimate width (e.g., 0.5 for FWHM).
    x_min : float, optional
        Minimum x for region-restricted detection.
    x_max : float, optional
        Maximum x for region-restricted detection.
    refine : bool
        Whether to apply quadratic refinement to peak positions.
    derivative : bool
        If True, use derivative-based detection instead of simple local maxima.

    Returns
    -------
    PeakDetectionResult
        Structured peak detection result.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)

    region_mask, x_reg, y_reg = _apply_region(x_arr, y_arr, x_min, x_max)

    method = method.lower()
    if derivative:
        core_indices_reg = _derivative_peaks(x_reg, y_reg)
    else:
        if method == "local_maxima":
            core_indices_reg = _find_local_maxima_indices(y_reg)
        else:
            raise ValueError(f"Unknown peak detection method: {method}")

    region_indices = np.where(region_mask)[0]
    core_indices = region_indices[core_indices_reg]

    core_indices = _filter_by_height(core_indices, y_arr, height, rel_height)

    core_indices, prominence = _filter_by_prominence(core_indices, y_arr, min_prominence)

    widths = None
    if estimate_width and core_indices.size > 0:
        widths = _estimate_widths(core_indices, x_arr, y_arr, rel_height=width_rel_height)

    refined_x = None
    refined_y = None
    if refine and core_indices.size > 0:
        refined_x, refined_y = _quadratic_refine(core_indices, x_arr, y_arr)

    result = PeakDetectionResult(
        indices=core_indices,
        x=x_arr[core_indices],
        y=y_arr[core_indices],
        prominence=prominence,
        width=widths,
        refined_x=refined_x,
        refined_y=refined_y,
        metadata={
            "method": method,
            "derivative": derivative,
            "height": height,
            "rel_height": rel_height,
            "min_prominence": min_prominence,
            "estimate_width": estimate_width,
            "width_rel_height": width_rel_height,
            "x_min": x_min,
            "x_max": x_max,
            "refine": refine,
        },
    )
    return result
