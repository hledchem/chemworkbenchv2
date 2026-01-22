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

## Example: Adding Baseline Correction

The baseline correction functions in `math_spectral.py` demonstrate the correct structure:

- Pure functions
- Clear docstrings
- No side effects
- Technique-agnostic
- Exposed through a unified wrapper (`baseline()`)

When adding new spectral math functions, follow the same pattern.

### Example: Adding Smoothing Functions

The smoothing functions in `math_spectral.py` demonstrate:

- How to implement multiple related transforms
- How to expose them through a unified wrapper (`smooth()`)
- How to keep functions pure and technique-agnostic
