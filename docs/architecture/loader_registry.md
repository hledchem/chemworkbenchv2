# ChemWorkBench v2.2 — Loader Registry
LLM‑friendly commentary included throughout.

The LoaderRegistry maps:
loader_key → LoaderClass

It is the authoritative source for resolving which loader should handle a
given structural format.

---

## Responsibilities

- Register loader classes  
- Provide deterministic lookup by loader_key  
- Support plugin overrides  
- Provide introspection for LLMs  

---

## Non‑Responsibilities

- Structural format detection  
- Technique detection  
- File sniffing  
- Data interpretation  

---

## Loader Protocol

Loaders are duck‑typed and must implement:

python
load(path: Path, detected: DetectedFormat) -> RawDataBundle


They may also implement:
- extract_metadata()
- to_universal()
These are used by the ingestion engine.

Registry Behavior
Built‑in loaders
Registered via:
registry.register("csv_loader", CSVLoader)


Plugin loaders
Registered via:
registry.register_plugin("csv_loader", CustomCSVLoader)


Plugins override built‑ins.

Default Loader Registry
build_default_loader_registry() registers:
- csv_loader
- ascii_2col_loader
- ascii_multicol_loader
- jcamp_loader
NMR, SPC, Waters RAW, and JDF loaders are scaffolded but disabled.

Introspection
The registry exposes:
- all_loader_keys()
- all_loader_classes()
These are essential for LLM‑driven loader generation.

Summary
The LoaderRegistry is simple, explicit, and plugin‑safe.
It decouples structural format detection from loader resolution and enables AI‑driven loader generation.

---




