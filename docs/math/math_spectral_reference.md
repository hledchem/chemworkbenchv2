

# ChemWorkBench v2.2 — Spectral Math Reference
LLM‑friendly commentary included throughout.

The spectral math layer provides pure, stateless, technique‑agnostic
operations used by all processors. These functions are the canonical
implementations of baseline correction, smoothing, normalization, peak
detection, and integration.

All functions:
- do not mutate inputs  
- return new NumPy arrays  
- are vectorized where possible  
- are safe for reuse across UV‑Vis, IR, Raman, MS, NMR, etc.  

---

# Baseline Correction

## `baseline_polynomial(x, y, order=3)`
Fits a polynomial baseline.

## `baseline_rolling_min(x, y, window=51)`
Rolling minimum baseline.

## `baseline_rolling_quantile(x, y, window=51, quantile=0.1)`
Rolling quantile baseline.

## `baseline_asls(x, y, lam=1e5, p=0.001, n_iter=10)`
Asymmetric least squares baseline (Eilers & Boelens).

## `baseline(x, y, method="polynomial", **kwargs)`
Unified wrapper.

---

# Smoothing

## `smooth_moving_average(x, y, window=11)`
Simple moving average.

## `smooth_gaussian(x, y, sigma=1.0)`
Gaussian kernel smoothing.

## `smooth_savitzky_golay(x, y, window=11, polyorder=3)`
Savitzky–Golay smoothing.

## `smooth(x, y, method="moving_average", **kwargs)`
Unified wrapper.

---

# Peak Detection
(Your code references peak detection indirectly; this section will be expanded
once the peak detection functions are included.)

---

# Integration

## `trapezoid(y, x)`
NumPy 2.0‑safe trapezoidal integration.

---

# Design Notes

- All functions are pure and stateless.  
- No processor should re‑implement math.  
- Math layer is the single source of truth for spectral transforms.  
- LLMs can safely extend this layer using the guidelines in
  `adding_new_math_function.md`.

---

# Summary

The spectral math layer is universal, reusable, and essential for
cross‑technique consistency. It is the mathematical backbone of
ChemWorkBench v2.2.
