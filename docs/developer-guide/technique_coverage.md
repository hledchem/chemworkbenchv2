# ChemWorkBench v2 — Analytical Technique Coverage
Comprehensive, industry‑grade coverage of spectroscopy, spectrometry, chromatography, electrochemistry, and magnetic resonance techniques.  
This document defines the canonical technique universe for loaders, processors, classifiers, and pipeline routing.

---

# 1. Spectroscopy

## 1.1 UV‑Vis Spectroscopy
**Description:** Absorbance/reflectance spectra across UV–Visible wavelengths.  
**Common Vendors:** Agilent, Shimadzu, PerkinElmer, OceanOptics.  
**Typical Formats:** CSV, TXT, JCAMP, Agilent `.D`, Shimadzu `.UVS`.

### Sub‑modes:
- Single‑scan UV‑Vis
- Multi‑scan / kinetics
- Temperature‑dependent UV‑Vis

---

## 1.2 Fluorescence Spectroscopy
**Description:** Emission/excitation spectra and 2D fluorescence maps.  
**Common Vendors:** Agilent Cary Eclipse, Horiba, Edinburgh Instruments.  
**Typical Formats:** CSV, XLSX, vendor‑specific binary.

### Sub‑modes:
- Steady‑state fluorescence
- Excitation–Emission Matrices (EEM)
- Time‑resolved fluorescence (TCSPC)

---

## 1.3 Infrared Spectroscopy (IR / FTIR)
**Description:** Mid‑IR and near‑IR spectra, typically FTIR.  
**Common Vendors:** Bruker, Thermo, Shimadzu, PerkinElmer.  
**Typical Formats:** OPUS, SPC, SPA, SRS, JCAMP.

### Sub‑modes:
- FTIR
- ATR‑FTIR
- NIR

---

## 1.4 Raman Spectroscopy
**Description:** Raman scattering spectra, including resonance Raman and SERS.  
**Common Vendors:** Bruker, Horiba, Renishaw.  
**Typical Formats:** OPUS, DPT, RRUFF, RRUFF‑GZ.

### Sub‑modes:
- Raman
- Resonance Raman
- SERS

---

# 2. Nuclear Magnetic Resonance (NMR)

## 2.1 1D NMR
- **1H NMR**
- **13C NMR**
- **DEPT** (45/90/135)

## 2.2 2D NMR
- **COSY**
- **NOESY**
- **ROESY**
- **HSQC**
- **HMBC**

## 2.3 Advanced NMR Modes
- Variable Temperature (VT) NMR
- Relaxation (T1/T2)
- J‑resolved spectra

**Common Vendors:** Bruker (TopSpin), JEOL, Varian.  
**Typical Formats:** Bruker directory structure, JEOL JDF, Varian FID.

---

# 3. Mass Spectrometry (MS)

## 3.1 Ionization Techniques
- **ESI‑MS**
- **MALDI‑TOF**
- **APCI**
- **EI (Electron Ionization)**

## 3.2 Mass Analyzer Types
- **TOF‑MS**
- **Quadrupole**
- **Orbitrap**
- **Ion Trap**

## 3.3 MS Workflows
- **MS1 (full scan)**
- **MS/MS (tandem MS)**
- **HRMS (high‑resolution MS)**

**Common Vendors:** Agilent, Thermo, Waters, Shimadzu.  
**Typical Formats:** Agilent `.D`, Thermo RAW/SPC/SRS, Waters RAW, Shimadzu LCD.

---

# 4. Chromatography

## 4.1 Liquid Chromatography
- **HPLC**
- **UHPLC**
- **LC‑MS** (hybrid technique)

## 4.2 Gas Chromatography
- **GC**
- **GC‑MS** (hybrid technique)

## 4.3 Ion Chromatography (IC)

**Common Vendors:** Agilent, Waters, Thermo, Shimadzu.  
**Typical Formats:** Agilent `.D`, Waters RAW, Shimadzu LCD.

---

# 5. Electrochemistry

## 5.1 Voltammetry
- **Cyclic Voltammetry (CV)**
- **Differential Pulse Voltammetry (DPV)**
- **Square Wave Voltammetry (SWV)**

## 5.2 Time‑domain Electrochemistry
- **Chronoamperometry**
- **Chronopotentiometry**

**Common Vendors:** CH Instruments, Metrohm, Gamry.  
**Typical Formats:** CSV, TXT, vendor‑specific binary.

---

# 6. Magnetic Resonance (Non‑NMR)

## 6.1 Electron Paramagnetic Resonance (EPR)
- Continuous Wave (CW‑EPR)
- Pulse EPR

**Common Vendors:** Bruker EMX/EleXsys.  
**Typical Formats:** Bruker BES3T, ESP, proprietary binary.

---

# 7. Summary Table

| Category            | Techniques Included                                                                 |
|---------------------|--------------------------------------------------------------------------------------|
| UV‑Vis              | Single‑scan, multi‑scan, kinetics, temperature‑dependent                             |
| Fluorescence        | Steady‑state, EEM, TCSPC                                                             |
| IR / FTIR           | FTIR, ATR‑FTIR, NIR                                                                  |
| Raman               | Raman, resonance Raman, SERS                                                         |
| NMR                 | 1H, 13C, DEPT, COSY, NOESY, ROESY, HSQC, HMBC, VT, T1/T2                             |
| Mass Spectrometry   | ESI‑MS, MALDI‑TOF, TOF‑MS, MS/MS, HRMS                                               |
| Chromatography      | HPLC, UHPLC, GC, IC, LC‑MS, GC‑MS                                                    |
| Electrochemistry    | CV, DPV, SWV, chronoamperometry, chronopotentiometry                                 |
| Magnetic Resonance  | CW‑EPR, Pulse EPR                                                                    |

---

# 8. Loader & Processor Mapping (High‑Level)

Loaders are **vendor‑format‑specific**.  
Processors are **technique‑specific**.

Example:

- Bruker OPUS → IR / Raman processors  
- Agilent `.D` → UV‑Vis, Chrom, MS processors  
- Bruker NMR → NMR processors  
- Waters RAW → Chrom + MS processors  
- JCAMP → UV‑Vis / IR / Raman processors  
- CSV/XLSX → Any processor depending on metadata or classifier  

---

# 9. Versioning

This document defines the **canonical technique universe for ChemWorkBench v2**.  
Future versions (v3+) may add:

- XRD  
- XRF  
- ICP‑MS  
- Imaging modalities (AFM, SEM, TEM)  
- Hyphenated techniques (LC‑NMR, LC‑IR)  
