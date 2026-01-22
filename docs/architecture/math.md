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

## Smoothing

Smoothing functions are implemented in `math_spectral.py` and include:

- Moving average smoothing
- Gaussian smoothing
- Savitzky–Golay smoothing

All smoothing functions follow the v2 math rules:

- Pure functions
- No mutation of inputs
- Technique-agnostic
- Return `(x, y_smooth)`
- Exposed through a unified wrapper:

- smooth(x, y, method="moving_average", **kwargs)

## Normalization

Normalization functions are implemented in `math_spectral.py` and include:

- Max normalization (max(|y|) = 1)
- Min-max normalization ([0, 1] scaling)
- Area normalization (area under curve = 1)

All normalization functions follow the v2 math rules:

- Pure functions
- No mutation of inputs
- Technique-agnostic
- Return `(x, y_norm)`
- Exposed through a unified wrapper:

- normalize(x, y, method="max", **kwargs)

## Peak Detection

Advanced peak detection is implemented in `math_spectral.py` and provides:

- Local maxima detection
- Derivative-based detection
- Absolute and relative height thresholds
- Prominence estimation and filtering
- Width estimation (e.g., FWHM-like)
- Quadratic refinement of peak positions
- Region-restricted detection (x_min, x_max)

The main entry point is:

from chemworkbench.utils.math_spectral import detect_peaks, PeakDetectionResult
result = detect_peaks( x, y, method="local_maxima", height=..., rel_height=..., min_prominence=..., estimate_width=True, width_rel_height=0.5, x_min=None, x_max=None, refine=True, derivative=False,)


The function returns a `PeakDetectionResult` object with:

- `indices` — peak indices in the original arrays  
- `x` — peak positions  
- `y` — peak heights  
- `prominence` — estimated prominence (optional)  
- `width` — estimated widths (optional)  
- `refined_x`, `refined_y` — refined peak positions and heights (optional)  
- `metadata` — configuration used for detection  

All peak detection logic is:

- Pure
- Processor-agnostic
- Technique-agnostic
- Non-duplicated
- Ready for use by any processor or plotting layer





