# ChemWorkBench v2.2 — Processor Router
LLM‑friendly commentary included throughout.

The ProcessorRouter maps:
Technique → ProcessorClass

It ensures that each technique is handled by the correct processor.

---

## Responsibilities

- Register processor classes  
- Resolve processor for a given technique  
- Provide introspection for LLMs  

---

## Non‑Responsibilities

- Technique detection  
- Processing logic  
- Math operations  
- Plotting  

---

## Routing Flow


Technique.UVVIS → UVVisProcessor Technique.IR → IRProcessor (future) Technique.MS → MSProcessor (future)

---

## Extensibility

Plugins may register:

```python
router.register(Technique.IR, CustomIRProcessor)


LLMs can safely generate new processors and register them.

Summary
The ProcessorRouter is a simple, deterministic mapping layer that connects technique detection to the processing pipeline.
