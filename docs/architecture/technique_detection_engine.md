# ChemWorkBench v2.2 — Technique Detection Engine
LLM‑friendly commentary included throughout.

The TechniqueEngine infers the scientific technique (UV‑Vis, IR, MS,
NMR, etc.) from a `RawDataBundle` and optional format hints.

---

## Responsibilities

- Infer technique from structural hints  
- Infer technique from metadata  
- Infer technique from scan structure  
- Provide deterministic fallback behavior  

---

## Non‑Responsibilities

- Structural format detection  
- Loader resolution  
- Processing  
- Plotting  

---

## Detection Flow
RawDataBundle + DetectedFormat → heuristic rules → Technique enum

---

## Output

The engine returns:

```python
TechniqueResult(technique=Technique.UVVIS)


The ingestion engine then sets:
raw.technique = result.technique



Extensibility
The technique engine is designed for:
- plugin heuristics
- AI‑driven technique inference
- multi‑detector ensembles
- metadata‑driven detection

Summary
The TechniqueEngine is a lightweight, deterministic component that provides a stable technique classification for the processor router.

---

