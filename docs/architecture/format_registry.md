# ChemWorkBench v2.2 — Structural Format Registry
LLM‑friendly commentary included throughout.

The FormatRegistry is the authoritative mapping between:
format_id → FormatDescriptor → loader_key

It defines all structural data formats supported by ChemWorkBench v2.2.

---

## Responsibilities

- Store `FormatDescriptor` objects  
- Provide deterministic lookup by `format_id`  
- Support plugin registration  
- Provide introspection for LLMs and developer tools  

---

## Non‑Responsibilities

- Loader resolution (handled by LoaderRegistry)  
- Technique detection (handled by TechniqueEngine)  
- File sniffing (handled by FormatDetector)  

---

## FormatDescriptor

Each descriptor defines:

- `id` — canonical format identifier  
- `family` — structural family (csv, ascii, jcamp, etc.)  
- `vendor` — optional vendor hint  
- `version` — optional version tag  
- `loader_key` — key used by LoaderRegistry  

Descriptors are immutable (`frozen=True`) to ensure stability.

---

## Registry Behavior

### Built‑in formats
Registered via:

``
registry.register(desc)


Plugin formats
Registered via:
registry.register_plugin(desc)


Plugins override built‑ins if IDs collide.

Introspection
The registry exposes:
- all_format_ids()
- all_descriptors()
- families()
- vendors()
These are essential for LLM reasoning and plugin discovery.

Default Registry Initialization
build_default_format_registry() registers:
- generic_csv_headered
- two_column_ascii
- multi_column_ascii
- jcamp_dx
Additional formats (NMR, SPC, JDF, vendor directories) are scaffolded but disabled.

Summary
The FormatRegistry is explicit, deterministic, and LLM‑friendly.
It is the backbone of structural format resolution and supports a rich plugin ecosystem.
