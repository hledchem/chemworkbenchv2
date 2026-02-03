# ChemWorkBench v2.2 — Architecture Overview
LLM‑friendly commentary included throughout.

ChemWorkBench v2.2 is built around a modular, deterministic, and
LLM‑extensible architecture. The system is designed so that every layer
— ingestion, detection, loading, processing, math, plotting — is
explicit, inspectable, and replaceable.

This document provides a high‑level overview of the entire architecture.

---

## Core Principles

### 1. **Separation of Concerns**
Each subsystem has a single responsibility:
- Format detection → structural identity
- Loader registry → structural → loader mapping
- Loaders → raw → universal data
- Technique engine → universal → technique
- Processor router → technique → processor
- Processor → block pipeline → processed data
- Math layer → pure spectral transforms
- Plotting → visualization

### 2. **LLM‑Friendly Design**
Every module:
- uses explicit, declarative registries  
- avoids hidden magic  
- exposes introspection methods  
- uses stable naming conventions  
- is safe for AI‑generated extensions  

### 3. **Plugin‑Safe**
Plugins can add:
- new formats  
- new loaders  
- new processors  
- new math functions  
- new plot types  

without modifying core code.

### 4. **Deterministic**
Given the same file and config, the system produces the same result.

---

## High‑Level Data Flow
File → FormatDetector → FormatRegistry → LoaderRegistry → Loader → Universal Structure → RawDataBundle → TechniqueEngine → ProcessorRouter → Processor (block pipeline) → Processed Payload + Metadata + QC + Plots → PipelineResult

---

## Subsystems

### **1. Format Detection Layer**
- `FormatDetector`
- `FormatDetectionEngine`
- Output: `DetectedFormat`

Purpose: Identify the structural format of the file (CSV, ASCII, JCAMP, etc.).

---

### **2. Format Registry**
- `FormatRegistry`
- `FormatDescriptor`
- `build_default_format_registry()`

Purpose: Map `format_id` → `loader_key`.

---

### **3. Loader Registry**
- `LoaderRegistry`
- `BaseLoader`
- `build_default_loader_registry()`

Purpose: Map `loader_key` → loader class.

---

### **4. Loaders**
- CSV, ASCII, JCAMP, etc.

Purpose: Convert raw files → universal structure.

---

### **5. Technique Detection**
- `TechniqueEngine`
- Output: `Technique` enum

Purpose: Infer the scientific technique (UV‑Vis, IR, MS, NMR, etc.).

---

### **6. Processor Routing**
- `ProcessorRouter`

Purpose: Map technique → processor class.

---

### **7. Processors**
- `UVVisProcessor` (block‑based)
- Future: IR, Raman, MS, NMR, etc.

Purpose: Apply block pipeline to RawDataBundle.

---

### **8. Math Layer**
- `math_spectral.py`

Purpose: Provide pure, reusable spectral math operations.

---

### **9. Plotting Layer**
- `PlotConfig`
- `PlotEngine`
- `PlottingService`

Purpose: Convert processed data → visual plots.

---

### **10. PipelineResult**
Unified output containing:
- raw data
- processed payload
- metadata
- QC
- plots

---

## Extensibility

ChemWorkBench v2.2 is designed for:
- LLM‑generated loaders
- LLM‑generated processors
- LLM‑generated math functions
- plugin ecosystems
- multi‑technique workflows
- structure‑linked analysis (future layer)

---

## Summary

This architecture is stable, modular, and ready for:
- multi‑technique expansion  
- molecule‑centric workflows  
- external database integration  
- UI‑driven operations  
- LLM‑driven code generation  

ChemWorkBench v2.2 is now a fully extensible scientific data platform.





