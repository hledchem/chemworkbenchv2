# Math Layer Architecture (Spectral Math)

The math layer in ChemWorkBench v2 is divided into three tiers:

1. math_core.py  
   Universal numeric transforms (FFT, convolution, interpolation, derivatives)

2. math_spectral.py  
   Universal spectral transforms (baseline, smoothing, normalization, peaks)

3. math_technique.py  
   Technique-specific transforms (NMR phasing, MS calibration)

This document describes the spectral math layer.

## Baseline Correction

Baseline correction is implemented in:

chemworkbench/utils/math_spectral.py


Available methods:

- Polynomial baseline
- Rolling minimum baseline
- Rolling quantile baseline
- Asymmetric least squares (AsLS)

All functions are:

- Pure
- Stateless
- Vectorized where possible
- Technique-agnostic
- Pipeline-ready
- DAG-ready

## Unified Wrapper

The `baseline()` function provides a single entry point:
baseline(x, y, method="polynomial", **kwargs)


This allows processors and pipelines to call baseline correction without knowing the underlying implementation.

## Design Principles

- No mutation of inputs
- No global state
- No processor-specific logic
- No plotting logic
- No IO logic
- All functions return `(x, baseline)`

