# ChemWorkBench v2 — Analytical Technique Coverage

ChemWorkBench v2 is designed as a universal, vendor‑agnostic scientific data platform capable of ingesting, normalizing, processing, and visualizing data across the major analytical techniques used in chemistry, materials science, and life sciences.

This document defines the **official technique coverage** for v2, including spectroscopy, separations, mass spectrometry, NMR, electrochemistry, and spin‑based methods.  
It also outlines **recommended v3+ expansions** for long‑term growth.

---

# 1. Nuclear Magnetic Resonance (NMR)

ChemWorkBench v2 supports the core 1D and 2D NMR experiments used in structural elucidation.

## 1D NMR
- ¹H NMR  
- ¹³C NMR  
- DEPT‑45 / DEPT‑90 / DEPT‑135 *(recommended addition)*  

## 2D NMR
- COSY  
- HSQC  
- HMBC  
- NOESY *(recommended addition)*  
- ROESY *(recommended addition)*  

## Supported Vendors
- Bruker (fid/ser/acqus/pdata)  
- JEOL (.jdf)  
- Varian/Agilent (fid/procpar)  

---

# 2. Mass Spectrometry (MS)

ChemWorkBench v2 supports the major MS modalities used in organic chemistry, pharma, and analytical labs.

## Core MS Techniques
- LC‑MS  
- GC‑MS  
- ESI‑MS  
- TOF‑MS  
- HRMS (Orbitrap/QTOF/FTICR) *(mode, not a separate technique)*  

## Tandem MS
- MS/MS *(recommended addition)*  
  - CID  
  - HCD  
  - ETD  

## Supported Vendors
- Agilent (.d)  
- Thermo (.raw)  
- Waters (MassLynx .raw directory)  
- Shimadzu (.lcd)  

---

# 3. Chromatography & Separations

## Chromatography
- HPLC  
- UHPLC  
- GC  
- DAD/PDA spectral detectors (Agilent .UV, .CSV, .TXT)  

## Electrophoresis *(optional v3)*
- Capillary electrophoresis (CE)  

---

# 4. Optical & Electronic Spectroscopy

## UV‑Vis
- Single‑scan  
- Multi‑scan  
- DAD/PDA spectral series  

## Fluorescence / Photoluminescence (PL) *(recommended addition)*  

## Circular Dichroism (CD) *(optional v3)*  

---

# 5. Vibrational Spectroscopy

## Infrared
- IR  
- FTIR  

## Raman
- Single‑scan Raman  
- Multi‑scan Raman  
- Supported formats:  
  - SPC  
  - JCAMP‑DX  
  - DPT  
  - RRUF / RRUF.GZ  

---

# 6. Electron Paramagnetic Resonance (EPR)

## Continuous‑Wave EPR (CW‑EPR)
- Standard first‑derivative EPR spectra  
- JCAMP‑DX and SPC support  

## **Pulse EPR (NEW)**
- Echo‑detected EPR  
- Hahn echo  
- Rabi oscillations  
- Relaxation measurements (T₁, T₂)  
- Basic time‑domain → frequency‑domain transforms  

Pulse EPR is included because it shares data structures with NMR FID processing and can be supported with similar loaders and processors.

---

# 7. Electrochemistry

## Core Techniques
- Cyclic Voltammetry (CV)  
- Differential Pulse Voltammetry (DPV) *(recommended addition)*  
- Square Wave Voltammetry (SWV) *(recommended addition)*  

These are widely used in:
- battery research  
- catalysis  
- redox chemistry  
- materials science  

---

# 8. Recommended v3+ Techniques (Not Required for v2)

These are high‑value but outside the scope of v2 loaders and processors.

## Materials Characterization
- XRD  
- XPS  
- XRF  
- TGA / DSC  

## Imaging
- MALDI Imaging  
- MS Imaging  
- Hyperspectral imaging  

## Biophysics
- SPR  
- CD (Circular Dichroism)  

---

# 9. Technique → File Format Coverage Map

| Technique | Formats |
|----------|---------|
| NMR | Bruker (fid/ser/acqus), JEOL (.jdf), Varian (fid/procpar), JCAMP |
| LC‑MS / GC‑MS | Agilent .d, Thermo .raw, Waters .raw directory, Shimadzu .lcd |
| UV‑Vis | CSV, XLSX, JCAMP, SPC, SP, UV, UVS, Agilent .UV |
| IR / FTIR | JCAMP, SPC, SPA, SP, OPUS |
| Raman | JCAMP, SPC, DPT, RRUF, RRUF.GZ |
| EPR / Pulse EPR | JCAMP, SPC, time‑domain binary formats |
| Electrochemistry | CSV, TXT, XLSX |

---

# 10. Integration Into the Architecture

## File Sniffer
Detects vendor + format → returns canonical format string.

## Loaders
Vendor‑specific loaders convert raw files → `{columns, data, metadata}`.

## Cleaning Layer
Normalizes all loader outputs into:
- x array  
- y array  
- metadata  

## Technique Classifier
Maps cleaned data → technique (UV‑Vis, IR, Raman, NMR, MS, etc.)

## Processors
Technique‑specific processing:
- peak detection  
- baseline correction  
- smoothing  
- integration  
- spectral math  
- NMR FID → spectrum  
- MS centroiding (optional v3)  
- Pulse EPR time‑domain → frequency‑domain  

---

# Summary

Your updated technique universe now includes:

- NMR (1D, 2D, DEPT, NOESY/ROESY)  
- MS (LC‑MS, GC‑MS, ESI‑MS, TOF‑MS, HRMS, MS/MS)  
- Chromatography (HPLC, GC, UHPLC)  
- UV‑Vis + Fluorescence  
- IR + FTIR  
- Raman (including DPT, RRUF)  
- **CW‑EPR + Pulse EPR**  
- Electrochemistry (CV, DPV, SWV)  

This is **industry‑grade coverage** for a v2 scientific SaaS platform.
