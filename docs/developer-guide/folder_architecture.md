chemworkbenchv2/
└── chemworkbench/
    ├── __init__.py

    # ============================================================
    # Core system: models, pipeline, routing, registries, ingestion
    # ============================================================
    ├── core/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── pipeline.py
    │   ├── routing.py
    │   ├── technique_anchors.py
    │   ├── technique_detection_engine.py
    │   │
    │   ├── ingestion_engine.py              # ← NEW (v2.2 orchestrator)
    │   ├── format_registry.py               # ← NEW (structural format registry)
    │   ├── format_registry_init.py          # ← NEW (register 16 format IDs)
    │   ├── loader_registry.py               # ← NEW (pluggable loader registry)
    │   ├── loader_registry_init.py          # ← NEW (register 12 loaders)
    │   │
    │   └── detection_engine_legacy.py       # (kept for reference; optional)

    # ============================================================
    # Processors: technique-specific processing pipelines
    # ============================================================
    ├── processors/
    │   ├── __init__.py
    │   ├── base_processor.py
    │   ├── uvvis_processor.py
    │   │
    │   └── uvvis/
    │       ├── __init__.py
    │       ├── config.py
    │       └── processor.py
    │
    │   # Future processors:
    │   # ir/, nmr/, raman/, cv/, epr/, gcms/, lcms/

    # ============================================================
    # Utilities: math, IO, normalization, helpers
    # ============================================================
    ├── utils/
    │   ├── __init__.py
    │   ├── math_spectral.py
    │   ├── data_utils.py
    │   ├── io_utils.py
    │   ├── math_core.py
    │   ├── math_technique.py
    │   ├── plotting_utils.py
    │   └── normalization.py

    # ============================================================
    # File Detection System (v2.2)
    # ============================================================
    ├── file_sniffer/
    │   ├── __init__.py
    │   ├── file_sniffer.py
    │   ├── format_detection_engine.py
    │   ├── signals.py
    │   ├── engine.py
    │   ├── core_detectors.py
    │   ├── spectral_detectors.py
    │   ├── registry.py                     # (sniffer registry, not loader registry)
    │   ├── format_registry.py              # (sniffer-specific; OK to keep)
    │   │
    │   ├── detectors/
    │   │   ├── agilent_masshunter_detector.py
    │   │   ├── bruker_nmr_detector.py
    │   │   ├── fluorescence_ascii_detector.py
    │   │   ├── headered_csv_detector.py
    │   │   ├── ir_ascii_detector.py
    │   │   ├── jcamp_detector.py
    │   │   ├── jeol_jdf_detector.py
    │   │   ├── multi_column_ascii_detector.py
    │   │   ├── netcdf_detector.py
    │   │   ├── no_header_csv_detector.py
    │   │   ├── opus_detector.py
    │   │   ├── raman_dpt_detector.py
    │   │   ├── spc_detector.py
    │   │   ├── two_column_ascii_detector.py
    │   │   ├── uvvis_ascii_detector.py
    │   │   └── varian_fid_detector.py
    │   │
    │   └── vendor/
    │       ├── __init__.py
    │       ├── agilent_detectors.py
    │       ├── bruker_detectors.py
    │       ├── thermo_detectors.py
    │       ├── shimadzu_detectors.py
    │       ├── perkinelmer_detectors.py
    │       ├── waters_detectors.py
    │       ├── jeol_detectors.py
    │       └── varian_detectors.py

    # ============================================================
    # Loaders (universal + vendor-specific)
    # ============================================================
    ├── loaders/
    │   ├── __init__.py
    │   ├── base_loader.py
    │   │
    │   ├── csv_loader.py
    │   ├── xlsx_loader.py
    │   ├── jcamp_loader.py
    │   ├── 2col_ascii_loader.py
    │   ├── multicol_ascii_loader.py
    │   │
    │   ├── agilent/
    │   │   ├── __init__.py
    │   │   ├── agilent_uv_loader.py
    │   │   ├── agilent_sp_loader.py
    │   │   ├── agilent_d_uvvis_loader.py
    │   │   ├── agilent_d_chrom_loader.py
    │   │   └── agilent_d_ms_loader.py
    │   │
    │   ├── bruker/
    │   │   ├── __init__.py
    │   │   ├── bruker_opus_loader.py
    │   │   ├── bruker_nmr_loader.py
    │   │   └── bruker_epr_loader.py
    │   │
    │   ├── thermo/
    │   │   ├── __init__.py
    │   │   ├── thermo_spa_loader.py
    │   │   ├── thermo_spc_loader.py
    │   │   └── thermo_srs_loader.py
    │   │
    │   ├── shimadzu/
    │   │   ├── __init__.py
    │   │   ├── shimadzu_spc_loader.py
    │   │   ├── shimadzu_irx_loader.py
    │   │   ├── shimadzu_uvs_loader.py
    │   │   └── shimadzu_lcd_loader.py
    │   │
    │   ├── perkinelmer/
    │   │   ├── __init__.py
    │   │   ├── perkinelmer_sp_loader.py
    │   │   └── perkinelmer_spc_loader.py
    │   │
    │   ├── waters/
    │   │   ├── __init__.py
    │   │   └── waters_raw_loader.py
    │   │
    │   ├── jeol/
    │   │   ├── __init__.py
    │   │   └── jeol_jdf_loader.py
    │   │
    │   ├── varian/
    │   │   ├── __init__.py
    │   │   └── varian_nmr_loader.py
    │   │
    │   ├
