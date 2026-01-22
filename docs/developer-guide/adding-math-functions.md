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

Add docstring and update architecture docs if needed.
