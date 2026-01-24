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
            file_sniffer/
                core_detectors.py
                file_sniffer.py
                __init__.py
                vendor/
                    __init__.py
                    agilent_detectors.py
                    bruker_detectors.py
                    jeol_detectors.py
                    perkinelmer_detectors.py
                    shimadzu_detectors.py
                    thermo_detectors.py
                    varian_detectors.py
                    waters_detectors.py
            loaders/
                csv_loader.py
                xlsx_loader.py
                jcamp_loader.py
                    

    # ------------------------------------------------------------
    # Plotting subsystem: 6-tier architecture (final)
    # ------------------------------------------------------------
    ├── plotting/
    │   ├── __init__.py
    │
    │   # Rendering engines
    │   ├── engine/
    │   │   ├── __init__.py
    │   │   ├── base_engine.py
    │   │   └── matplotlib_engine.py
    │
    │   # Primitive layer types (traces)
    │   ├── layer_types/
    │   │   ├── __init__.py
    │   │   ├── line.py
    │   │   ├── scatter.py
    │   │   ├── bar.py
    │   │   ├── stem.py
    │   │   ├── step.py
    │   │   ├── errorbar.py
    │   │   ├── heatmap.py
    │   │   ├── contour.py
    │   │   ├── image.py
    │   │   └── surface.py
                histogram.py
                line_3d.py
                pie.py
                scatter_3d.py
                surface_3d.py
                wireframe_3d.py
                surface.py
    │
    │   # Declarative schema (NEW)
    │   ├── schema/
    │   │   ├── __init__.py
    │   │   ├── figure_schema.py
    │   │   ├── panel_schema.py
    │   │   ├── trace_schema.py
    │   │   └── annotation_schema.py
    │
    │   # Config builder (NEW)
    │   ├── builder/
    │   │   ├── __init__.py
    │   │   ├── config_builder.py
    │   │   ├── defaults.py
    │   │   └── validators.py
    │
    │   # Graph registry + templates (NEW)
    │   └── registry/
    │       ├── __init__.py
    │       ├── graph_registry.py
    │       └── templates/
    │           ├── uvvis_spectrum.json
    │           ├── multi_panel_dashboard.json
    │           └── chromatogram.json

    # ------------------------------------------------------------
    # Services layer (NEW)
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
    │   # main.py, commands/ (future)

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
    # Plugins (NEW)
    # ------------------------------------------------------------
    ├── plugins/
    │   ├── __init__.py
    │   ├── processors/
    │   ├── plotting/
    │   └── math/

    # ------------------------------------------------------------
    # Runtime (NEW)
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
        │   ├── config.md
        │   ├── layers.md
        │   ├── math.md
        │   ├── pipeline.md
        │   ├── plotting.md
        │   └── processors.md
        │
        ├── developer-guide/
        │   ├── adding-a-processor.md
        │   ├── adding-a-tool.md
        │   ├── adding-math-functions.md
        │   ├── adding-plot-templates.md
        │   ├── folder_architecture.md
        │   ├── naming_convention.md
        │   └── project-structure.md
        │
        ├── user-guide/
        │   ├── layers.md
        │   ├── overview.md
        │   └── pipeline.md
        │
        └── api/
            ├── plotting.md
            ├── processing.md
            └── config.md

# ------------------------------------------------------------
# Tests
# ------------------------------------------------------------
tests/
    ├── test_uvvis_processor.py
    ├── test_math_spectral.py
    ├── test_pipeline.py
    ├── test_plotting_engine.py
    └── plotting/
        ├── test_schema.py
        ├── test_builder.py
        ├── test_engine.py
        └── test_registry.py

# ------------------------------------------------------------
# Version file
# ------------------------------------------------------------
VERSION
