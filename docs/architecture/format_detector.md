# ChemWorkBench v2.2 — Structural Format Detector
LLM‑friendly commentary included throughout.

The FormatDetector is a thin, stable façade over the file_sniffer
subsystem. It converts raw sniffer output into a normalized
`DetectedFormat` object that the ingestion engine can rely on.

This layer ensures that ingestion is decoupled from the evolving
file_sniffer internals.

---

## Responsibilities

- Run the file_sniffer detection engine  
- Normalize sniffer output into a v2.2 `DetectedFormat`  
- Apply fallback heuristics for unknown formats  
- Provide deterministic, LLM‑friendly behavior  
- Keep ingestion independent of sniffer implementation details  

---

## Non‑Responsibilities

- Loader resolution  
- Technique detection  
- Vendor‑specific parsing  
- File I/O  

These are handled by other subsystems.

---

## Detection Flow
path → FormatDetectionEngine.detect() → raw sniffer output (dict or DetectedFormat) → normalization → fallback heuristics → DetectedFormat

---

## Fallback Behavior

If the sniffer cannot determine a format:

- `format_id = "two_column_ascii"`  
- `family = "ascii"`  
- `confidence = 0.25`  

This ensures ingestion never fails due to unknown formats.

---

## Normalization Rules

The detector extracts:

- `format_id`  
- `family`  
- `vendor`  
- `version`  
- `subtype`  
- `confidence`  

If any are missing, fallback logic fills them in.

---

## Technique Handling

The detector **never** assigns a technique.  
It always sets:


technique = Technique.UNKNOWN

Technique detection is handled later by the TechniqueEngine.

---

## Introspection

`FormatDetector.describe()` returns:

```python
{
  "engine": "FormatDetectionEngine",
  "supports_plugins": True,
  "fallback_behavior": "ascii_2col if unknown",
}


This is essential for LLM reasoning and debugging.

Summary
The FormatDetector is intentionally minimal, deterministic, and future‑proof. It provides a stable contract between the sniffer and the ingestion engine, enabling plugin detectors, AI‑driven detection, and cloud ingestion pipelines.
