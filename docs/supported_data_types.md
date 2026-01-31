# Supported Data Formats (v2.2)

ChemWorkBench v2.2 uses a **structural‑family ingestion architecture**.  
Each supported format belongs to a **format family**, and each family is handled by a **single loader class**.  
This design keeps the system minimal, scalable, and future‑proof.

Format detection, loading, and technique detection are **fully decoupled**:

- **Format Detection** identifies the structural family (`format_id`).
- **Loader** parses the file into normalized `universal_data` + metadata.
- **Technique Engine** determines the scientific meaning (UV‑Vis, IR, Raman, MS, NMR, etc.).

This document lists all supported format families, their `format_id`s, their loader keys, and their loader classes.

---

## 1. CSV Family

**Loader Key:** `csv_loader`  
**Loader Class:** `CSVLoader`  
**Family:** `csv`  
**Structure:** Comma‑separated values (headered or headerless)

### Format IDs

| Format ID               | Description            |
|-------------------------|------------------------|
| `generic_csv_headered`  | CSV with header row    |
| `generic_csv_no_header` | CSV without header     |

---

## 2. ASCII Family (Numeric)

**Family:** `ascii`  
**Structure:** Plain‑text numeric tables

### Loaders

| Loader Key             | Loader Class        | Description                 |
|------------------------|---------------------|-----------------------------|
| `ascii_2col_loader`    | ASCII2ColLoader     | Two‑column numeric ASCII    |
| `ascii_multicol_loader`| ASCIIMultiColLoader | Multi‑column numeric ASCII  |

### Format IDs

| Format ID            | Description                        |
|----------------------|------------------------------------|
| `two_column_ascii`   | `<float> <float>`                  |
| `multi_column_ascii` | `<float> <float> <float> ...`      |

---

## 3. JCAMP‑DX Family

**Loader Key:** `jcamp_loader`  
**Loader Class:** `JCampLoader`  
**Family:** `jcamp`  
**Structure:** JCAMP‑DX text format (`##TITLE=`, `##XYDATA=`)

### Format IDs

| Format ID   | Description            |
|-------------|------------------------|
| `jcamp_dx`  | JCAMP‑DX spectroscopy  |

---

## 4. NMR Directory Families

Directory‑based formats containing raw FID blocks + acquisition metadata.

### Loaders

| Loader Key          | Loader Class       |
|---------------------|--------------------|
| `bruker_nmr_loader` | BrukerNMRLoader    |
| `varian_nmr_loader` | VarianNMRLoader    |

### Format IDs

| Format ID        | Vendor         | Description                         |
|------------------|----------------|-------------------------------------|
| `bruker_nmr_dir` | Bruker         | TopSpin directory (`fid`, `acqus`)  |
| `varian_fid_dir` | Varian/Agilent | VNMRJ FID directory                 |

---

## 5. Thermo Spectroscopy Family (SPC/SPA/SRS)

Thermo’s legacy spectroscopy formats.

### Loaders

| Loader Key          | Loader Class       |
|---------------------|--------------------|
| `thermo_spc_loader` | ThermoSPCLoader    |
| `thermo_spa_loader` | ThermoSPALoader    |
| `thermo_srs_loader` | ThermoSRSLoader    |

### Format IDs

| Format ID            | Description        |
|----------------------|--------------------|
| `thermo_spc_binary`  | Binary SPC format  |
| `thermo_spa_ascii`   | ASCII SPA format   |
| `thermo_srs_ascii`   | ASCII SRS format   |

---

## 6. Waters RAW Directory Family

**Loader Key:** `waters_raw_loader`  
**Loader Class:** `WatersRAWLoader`  
**Family:** `vendor_dir`

### Format IDs

| Format ID        | Description                  |
|------------------|------------------------------|
| `waters_raw_dir` | Waters MassLynx RAW directory |

---

## 7. JEOL JDF Family

**Loader Key:** `jeol_jdf_loader`  
**Loader Class:** `JeolJDFLoader`  
**Family:** `jdf`

### Format IDs

| Format ID          | Description           |
|--------------------|-----------------------|
| `jeol_jdf_binary`  | JEOL JDF binary file  |

---

## 8. Agilent MassHunter Directory Family (.D)

**Loader Key:** `agilent_masshunter_loader`  
**Loader Class:** `AgilentMassHunterLoader`  
**Family:** `vendor_dir`

### Format IDs

| Format ID                | Description            |
|--------------------------|------------------------|
| `agilent_masshunter_dir` | Agilent `.D` directory |

---

## 9. Raman Special Formats

Formats with unique header structures.

### Loaders

| Loader Key       | Loader Class   |
|------------------|----------------|
| `rruf_loader`    | RRUFLoader     |
| `rruf_gz_loader` | RRUFGZLoader   |

### Format IDs

| Format ID            | Description          |
|----------------------|----------------------|
| `raman_rruf_ascii`   | RRUF ASCII           |
| `raman_rruf_gzip`    | RRUF.GZ compressed   |

---

## 10. Electrochemistry Special Formats

**Loader Key:** `chi_dta_loader`  
**Loader Class:** `CHIDTALoader`  
**Family:** `echem`

### Format IDs

| Format ID        | Description                  |
|------------------|------------------------------|
| `chi_dta_ascii`  | CH Instruments `.dta` ASCII  |

---

# Summary Table (All Format IDs → Loaders)

| Format ID               | Loader Key               | Loader Class          |
|-------------------------|--------------------------|------------------------|
| generic_csv_headered    | csv_loader               | CSVLoader              |
| generic_csv_no_header   | csv_loader               | CSVLoader              |
| two_column_ascii        | ascii_2col_loader        | ASCII2ColLoader        |
| multi_column_ascii      | ascii_multicol_loader    | ASCIIMultiColLoader    |
| jcamp_dx                | jcamp_loader             | JCampLoader            |
| bruker_nmr_dir          | bruker_nmr_loader        | BrukerNMRLoader        |
| varian_fid_dir          | varian_nmr_loader        | VarianNMRLoader        |
| thermo_spc_binary       | thermo_spc_loader        | ThermoSPCLoader        |
| thermo_spa_ascii        | thermo_spa_loader        | ThermoSPALoader        |
| thermo_srs_ascii        | thermo_srs_loader        | ThermoSRSLoader        |
| waters_raw_dir          | waters_raw_loader        | WatersRAWLoader        |
| jeol_jdf_binary         | jeol_jdf_loader          | JeolJDFLoader          |
| agilent_masshunter_dir  | agilent_masshunter_loader| AgilentMassHunterLoader|
| raman_rruf_ascii        | raman_rruf_loader        | RRUFLoader             |
| raman_rruf_gzip         | raman_rruf_gz_loader     | RRUFGZLoader           |
| chi_dta_ascii           | chi_dta_loader           | CHIDTALoader           |

---

# Technique Coverage (All Families)

The following scientific techniques are supported across the full set of format families:

UV‑Vis spectroscopy, IR spectroscopy, Raman spectroscopy, Fluorescence spectroscopy, NMR spectroscopy, Mass spectrometry (LC‑MS, GC‑MS, MS/MS), Chromatography (LC, GC), Electrochemistry (CV, CA, CP, EIS when ASCII), diode‑array UV‑Vis (PDA/DAD), general XY spectroscopy, multi‑channel spectroscopy, and vendor‑specific directory‑based acquisitions.
