chemworkbenchv2/
└── chemworkbench/
    ├── __init__.py

    # ------------------------------------------------------------
    # Core system: models, pipeline, registry, routing, IO
    # ------------------------------------------------------------
    ├── core/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── pipeline.py
    │   ├── registry.py
    │   ├── routing.py
    │   ├── technique_anchors.py          # ← NEW (full anchor-term library)
    │   └── io/
    │       ├── __init__.py
    │       ├── json_loader.py
    │       ├── yaml_loader.py
    │       ├── serializer.py
    │       └── versioning.py

    # ------------------------------------------------------------
    # Processors: one folder per analytical technique
    # ------------------------------------------------------------
    ├── processors/
    │   ├── __init__.py
    │   ├── base_processor.py
    │   └── uvvis/
    │       ├── __init__.py
    │       ├── config.py
    │       └── processor.py
    │
    │   # Future processors:
    │   # ir/, nmr/, raman/, cv/, epr/, gcms/, lcms/

    # ------------------------------------------------------------
    # Utilities: math layer, helpers, shared logic
    # ------------------------------------------------------------
    ├── utils/
    │   ├── __init__.py
    │   ├── math_spectral.py
    │   ├── data_utils.py
    │   ├── io_utils.py
    │   ├── math_core.py
    │   ├── math_technique.py
    │   └── plotting_utils.py
            normalization.py

    │   # --------------------------------------------------------
    │   # File Detection System (NEW: DetectionEngine architecture)
    │   # --------------------------------------------------------
    │   ├── file_sniffer/
    │   │   ├── __init__.py
    │   │   ├── file_sniffer.py           # ← MODIFIED (calls DetectionEngine)
    │   │   ├── detection_engine.py       # ← NEW (multi-signal scoring engine)
    │   │   ├── signals.py                # ← NEW (scoring helpers)
    │   │   └── vendor/                   # (unchanged for now)
    │   │       ├── __init__.py
    │   │       ├── agilent_detectors.py
    │   │       ├── bruker_detectors.py
    │   │       ├── thermo_detectors.py
    │   │       ├── shimadzu_detectors.py
    │   │       ├── perkinelmer_detectors.py
    │   │       ├── waters_detectors.py
    │   │       ├── jeol_detectors.py
    │   │       └── varian_detectors.py

    │   # --------------------------------------------------------
    │   # Loaders (vendor-specific + universal + technique-specific)
    │   # --------------------------------------------------------
    │   ├── loaders/
    │   │   ├── __init__.py
    │   │   ├── base_loader.py            # ← MODIFIED (add TECHNIQUE attr)
    │   │   ├── registry.py               # ← MODIFIED (ensure class registry)

    │   │   # Universal loaders
    │   │   ├── csv_loader.py
    │   │   ├── xlsx_loader.py
    │   │   ├── jcamp_loader.py

    │   │   # Vendor-specific loaders
    │   │   ├── agilent/
    │   │   │   ├── __init__.py
    │   │   │   ├── agilent_uv_loader.py          # ← MODIFIED (TECHNIQUE)
    │   │   │   ├── agilent_sp_loader.py
    │   │   │   ├── agilent_d_uvvis_loader.py
    │   │   │   ├── agilent_d_chrom_loader.py     # ← MODIFIED
    │   │   │   └── agilent_d_ms_loader.py

    │   │   ├── bruker/
    │   │   │   ├── __init__.py
    │   │   │   ├── bruker_opus_loader.py
    │   │   │   ├── bruker_nmr_loader.py          # ← MODIFIED
    │   │   │   └── bruker_epr_loader.py

    │   │   ├── thermo/
    │   │   │   ├── __init__.py
    │   │   │   ├── thermo_spa_loader.py
    │   │   │   ├── thermo_spc_loader.py
    │   │   │   └── thermo_srs_loader.py

    │   │   ├── shimadzu/
    │   │   │   ├── __init__.py
    │   │   │   ├── shimadzu_spc_loader.py
    │   │   │   ├── shimadzu_irx_loader.py
    │   │   │   ├── shimadzu_uvs_loader.py
    │   │   │   └── shimadzu_lcd_loader.py

    │   │   ├── perkinelmer/
    │   │   │   ├── __init__.py
    │   │   │   ├── perkinelmer_sp_loader.py
    │   │   │   └── perkinelmer_spc_loader.py

    │   │   ├── waters/
    │   │   │   ├── __init__.py
    │   │   │   └── waters_raw_loader.py

    │   │   ├── jeol/
    │   │   │   ├── __init__.py
    │   │   │   └── jeol_jdf_loader.py

    │   │   ├── varian/
    │   │   │   ├── __init__.py
    │   │   │   └── varian_nmr_loader.py

    │   │   # Raman-specific loaders
    │   │   ├── raman/
    │   │   │   ├── __init__.py
    │   │   │   ├── dpt_loader.py
    │   │   │   ├── rruf_loader.py
    │   │   │   └── rruf_gz_loader.py

    │   │   # Fluorescence loaders
    │   │   ├── horiba/
    │   │   │   ├── __init__.py
    │   │   │   └── horiba_fluor_loader.py

    │   │   # Electrochemistry loaders
    │   │   ├── ch_instruments/
    │   │   │   ├── __init__.py
    │   │   │   └── chi_dta_loader.py

    # ------------------------------------------------------------
    # Plotting subsystem
    # ------------------------------------------------------------
    ├── plotting/
    │   ├── __init__.py
    │   ├── engine/
    │   ├── layer_types/
    │   ├── schema/
    │   ├── builder/
    │   └── registry/

    # ------------------------------------------------------------
    # Services layer
    # ------------------------------------------------------------
    ├── services/
    │   ├── __init__.py
    │   ├── plotting_service.py
    │   ├── processing_service.py
    │   ├── caching_service.py
    │   └── file_service.py

    # ------------------------------------------------------------
    # API layer
    # ------------------------------------------------------------
    ├── api/
    │   ├── __init__.py
    │   ├── run_plotting.py
    │   └── run_processing.py

    # ------------------------------------------------------------
    # CLI layer
    # ------------------------------------------------------------
    ├── cli/
    │   └── __init__.py

    # ------------------------------------------------------------
    # Config system
    # ------------------------------------------------------------
    ├── config/
    │   ├── __init__.py
    │   ├── schema.py
    │   ├── validators.py
    │   ├── defaults/
    │   └── templates/

    # ------------------------------------------------------------
    # Plugins
    # ------------------------------------------------------------
    ├── plugins/
    │   ├── __init__.py
    │   ├── processors/
    │   ├── plotting/
    │   └── math/

    # ------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------
    ├── runtime/
    │   ├── __init__.py
    │   ├── logging.py
    │   ├── environment.py
    │   └── errors.py

    # ------------------------------------------------------------
    # Examples
    # ------------------------------------------------------------
    ├── examples/
    │   ├── __init__.py
    │   └── test_uvvis_pipeline.py

    # ------------------------------------------------------------
    # Documentation
    # ------------------------------------------------------------
    └── docs/
        ├── architecture/
        ├── developer-guide/
        ├── user-guide/
        └── api/

# ------------------------------------------------------------
# Tests
# ------------------------------------------------------------
tests/
    ├── test_uvvis_processor.py
    ├── test_math_spectral.py
    ├── test_pipeline.py
    ├── test_plotting_engine.py
    ├── test_detection_engine.py      # ← NEW
    ├── test_file_sniffer.py          # ← MODIFIED
    └── plotting/
        ├── test_schema.py
        ├── test_builder.py
        ├── test_engine.py
        └── test_registry.py

# ------------------------------------------------------------
# Version file
# ------------------------------------------------------------
VERSION
