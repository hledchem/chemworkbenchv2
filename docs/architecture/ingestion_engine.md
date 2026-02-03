# ChemWorkBench v2.2 — Ingestion Engine
LLM‑friendly commentary included throughout.

The ingestion engine is the central orchestrator of the v2.2 pipeline.
It converts a file path into a fully processed `PipelineResult`.

---

## Responsibilities

1. Structural format detection  
2. Format resolution  
3. Loader resolution  
4. Raw file loading  
5. Universal → RawDataBundle conversion  
6. Technique inference  
7. Processor routing  
8. Processor execution  
9. PipelineResult assembly  

---

## High‑Level Flow

path → FormatDetector.detect() → FormatRegistry.get() → LoaderRegistry.get() → loader.load_raw() → loader.to_universal() → RawDataBundle → TechniqueEngine.detect() → ProcessorRouter.resolve() → processor.process() → PipelineResult

---

## Key Components

### **FormatDetector**
Runs the file sniffer and normalizes output into a `DetectedFormat`.

### **FormatRegistry**
Maps `format_id` → `FormatDescriptor`.

### **LoaderRegistry**
Maps `loader_key` → loader class.

### **Loader**
Reads raw file → universal structure.

### **TechniqueEngine**
Infers scientific technique.

### **ProcessorRouter**
Maps technique → processor.

### **Processor**
Runs block pipeline and produces:
- processed payload  
- metadata  
- QC  
- plots  

### **PipelineResult**
Unified output object.

---

## Universal → RawDataBundle Conversion

The ingestion engine supports three universal structures:

### 1. Legacy spectral dict
```python
{"x": [...], "y": [...], "label": "..."}


2. Legacy tabular list-of-dicts
[{"col1": ..., "col2": ...}, ...]


3. v2.2 universal structure
{
  "scans": [...],
  "tabular": [...],
  "metadata": {...}
}


All are normalized into a RawDataBundle.

Extensibility
The ingestion engine is designed for:
- plugin loaders
- plugin formats
- LLM‑generated loaders
- cloud ingestion pipelines
- multi‑detector ensembles

Introspection
IngestionEngine.describe() returns:
- registry sizes
- detector class
- technique engine class
- processor router class
This is essential for LLM reasoning and debugging.

Summary
The ingestion engine is the backbone of ChemWorkBench v2.2.
It is deterministic, explicit, and fully pluggable — ideal for both human developers and LLM‑driven extensions.

---

# 📄 `docs/math/math_spectral_reference.md`

```markdown
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




