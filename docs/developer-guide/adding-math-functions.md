# Developer Guide: Adding Math Functions

This guide explains how to add a new calculation to the math layer.

## Step 1 — Choose the Correct Module

| Module | Purpose |
|--------|---------|
| math_core.py | FFT, convolution, interpolation, derivatives |
| math_spectral.py | baseline, smoothing, normalization, peaks |
| math_technique.py | NMR phasing, MS calibration |

## Step 2 — Implement a Pure Function

Rules:

- No side effects
- No mutation of inputs
- Return new arrays
- Use NumPy vectorization

Example:

def derivative(y, x=None): return np.gradient(y) if x is None else np.gradient(y, x)

## Step 3 — Expose Through `data_utils.py`

Processors always import from `data_utils`.

## Step 4 — Add Tests

Add tests in:
tests/test_utils/


## Step 5 — Document

Update:

- `docs/architecture/math.md`
- Any relevant developer guides

## Example: Baseline Correction

Baseline correction functions in `math_spectral.py` demonstrate:

- Multiple methods (polynomial, rolling, AsLS)
- A unified wrapper (`baseline()`)
- Technique-agnostic design

## Example: Smoothing Functions

Smoothing functions in `math_spectral.py` demonstrate:

- Multiple methods (moving average, Gaussian, Savitzky–Golay)
- A unified wrapper (`smooth()`)
- Pure, processor-agnostic implementation

## Example: Normalization Functions

Normalization functions in `math_spectral.py` demonstrate:

- Multiple normalization strategies
- A unified wrapper (`normalize()`)
- No mutation of inputs

## Example: Peak Detection

Peak detection in `math_spectral.py` demonstrates:

- Advanced logic (local maxima, derivative-based, prominence, width, refinement)
- A structured result object (`PeakDetectionResult`)
- A unified wrapper (`detect_peaks()`)
- Processor-agnostic, technique-agnostic design

When adding new spectral math functions, follow these patterns.
