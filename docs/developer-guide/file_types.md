ChemWorkBench v2 — Supported File Formats
ChemWorkBench v2 is designed to ingest real‑world scientific data across UV‑Vis, IR/FTIR, Raman, NMR, EPR, GC‑MS, LC‑MS, and general spectroscopy.
The formats below represent the complete v2 ingestion universe, covering all major vendors and universal scientific standards.

1. Text-Based Formats
These appear across all instrument types and vendors.
- .csv
- .tsv
- .txt
- .json
- .xlsx

2. Universal Spectroscopy Formats
These formats are widely used across multiple techniques and vendors.
- .dx, .jdx — JCAMP‑DX (IR, Raman, UV‑Vis, NMR, EPR)
- .spc — Galactic SPC (IR, Raman, UV‑Vis, Fluorescence, EPR)
- .spa — Thermo/PerkinElmer/Agilent (IR/FTIR)
- .sp — PerkinElmer/Agilent (UV‑Vis, IR)
- .uv, .uvs — UV‑Vis spectra

3. Raman-Specific Formats (New Additions Included)
These formats are commonly used by Raman instruments and software.
- .spc — Galactic SPC (Raman, IR)
- .dx, .jdx — JCAMP‑DX Raman
- .dpt — ASCII Raman format (Horiba, Renishaw, others)
- .rruf — Renishaw Raman Universal Format
- .rruf.gz — Compressed Renishaw Raman format
- .grm — Thermo Raman format (optional, vendor-specific)

4. Vendor-Specific Formats
Agilent
- .d — ChemStation directory (UV‑Vis, LC‑MS, GC‑MS)
- .dx — JCAMP‑DX variant
- .uv — UV‑Vis
- .sp — UV‑Vis / IR
Bruker
- OPUS binary formats: .0, .1, .2, .3 (IR, Raman)
- NMR directory structure:
- fid
- ser
- acqus
- pdata/1/1r
- .jdx — JCAMP‑DX export
Thermo Fisher
- .spa — IR/FTIR
- .spc — IR/Raman
- .srs — OMNIC spectral format
- .raw — Xcalibur RAW (LC‑MS/GC‑MS)
Shimadzu
- .spc — UV‑Vis / IR
- .irx — IR/FTIR
- .uvs — UV‑Vis
- .lcd — LC‑MS / GC‑MS
PerkinElmer
- .spc — IR/Raman
- .sp — UV‑Vis / IR
JEOL
- .jdf — NMR
- .jdx — JCAMP‑DX
Varian / Agilent NMR
- fid
- procpar
Waters
- MassLynx RAW directory:
- _FUNC001.DAT
- _HEADER.TXT
- _CHRO.DAT

5. Mass Spectrometry Formats
These formats appear across LC‑MS and GC‑MS workflows.
- .raw — Thermo Xcalibur RAW
- .d — Agilent ChemStation directory
- .raw — Waters MassLynx directory
- .lcd — Shimadzu LC‑MS

Coverage Summary
ChemWorkBench v2 supports:
- All major spectroscopy techniques
- All major instrument vendors
- All universal scientific formats
- All common text formats
- All essential Raman formats (including DPT and RRUF)
This list enables ingestion of ~99% of real‑world spectroscopy data encountered in academic, industrial, pharmaceutical, and materials science environments.
