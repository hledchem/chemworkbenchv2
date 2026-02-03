# ChemWorkBench v2.2 — Unified Data Models
LLM‑friendly commentary included throughout.

The unified data models define the canonical structures used throughout
the ingestion and processing pipeline.

These models form the contract between loaders, processors, and the
plotting subsystem.

---

## Core Models

### **DetectedFormat**
Structural format identity.

### **RawDataBundle**
Unified representation of raw data.

Contains:
- `scans`  
- `tabular`  
- `metadata`  
- `technique`  
- `source_path`  

### **Scan**
Represents a single x/y spectral scan.

### **PipelineResult**
Unified output of the ingestion engine.

Contains:
- `raw`  
- `processed`  
- `metadata`  
- `qc`  
- `plots`  

---

## Universal Structure

Loaders convert raw files into one of three universal structures:

1. Legacy spectral dict  
2. Legacy tabular list-of-dicts  
3. v2.2 universal structure (scans + tabular + metadata)

The ingestion engine normalizes all of them into a `RawDataBundle`.

---

## Extensibility

The data model layer is designed for:

- multi‑technique workflows  
- molecule‑centric linking (future)  
- external database annotations  
- plugin processors  
- LLM‑generated loaders  

---

## Summary

The unified data models provide a stable, deterministic foundation for
the entire ChemWorkBench v2.2 pipeline.
