chemworkbenchv2/
chemworkbench/
    __init__.py
  # ------------------------------------------------------------
  # Core system: models, pipeline, registry, routing
   # ------------------------------------------------------------
   core/
        __init__.py
        models.py            # ProcessedData, PlotConfig, QCMetric, Technique, etc.
        pipeline.py          # Universal pipeline orchestrator
        registry.py          # Processor registry (future)
        routing.py           # Technique → processor routing (future)

  # ------------------------------------------------------------
   # Processors: one folder per analytical technique
   # ------------------------------------------------------------
  processors/
        __init__.py
        base_processor.py

   uvvis/
            __init__.py
            config.py        # UVVisConfig (inherits BaseProcessorConfig)
            processor.py     # UVVisProcessor (implements ProcessorProtocol)

  # Future processors:
  # ir/
   # nmr/
   # raman/
   # cv/
  # epr/
   # gcms/
 # lcms/
# ------------------------------------------------------------
# Utilities: math layer, helpers, shared logic
 # ------------------------------------------------------------
utils/
        __init__.py
        math_spectral.py     # Baseline, smoothing, normalization, peaks, integration
        data_utils.py
        io_utils.py
        math_core.py
        math_technique.py
        plotting_utils.py
        # array_utils.py

# ------------------------------------------------------------
# Plotting subsystem: 3-tier architecture
 # ------------------------------------------------------------
 plotting/
 
    __init__.py

    engine/
        __init__.py
        base_engine.py
        matplotlib_engine.py

    layer_types/
        __init__.py
        line.py
        scatter.py
        bar.py
        stem.py
        step.py
        errorbar.py
        heatmap.py
        contour.py
        image.py
        surface.py

    style_presets/
        __init__.py
        default.py
        dark.py
        publication.py
        high_contrast.py
        pastel.py

  # ------------------------------------------------------------ 
  # API layer: REST, RPC, or WebSocket endpoints (future)
  # ------------------------------------------------------------
   api/
        __init__.py
        run_plotting.py
        run_processing.py

 # ------------------------------------------------------------
# CLI layer: command-line interface (future)
 # ------------------------------------------------------------
  cli/
        __init__.py
        # main.py
        # commands/

# ------------------------------------------------------------
# Config: global settings, YAML/JSON loaders, environment
# ------------------------------------------------------------
  config/
      __init__.py
      schema.py
      defaults/
      templates/

 # ------------------------------------------------------------
 # Examples: runnable scripts for testing processors & pipeline
 # ------------------------------------------------------------
examples/
     __init__.py
     test_uvvis_pipeline.py   # End-to-end test script

docs/
   architecture/
       config.md
       layers.md
       math.md
       pipeline.md
       plotting.md
       processors.md
   developer-guide/
       adding-a-processor.md
       adding-a-tool.md
       adding-math-functions.md
       adding-plot-templates.md
       folder_architecture.md
       naming_convenction.md
       project-structure.md
   user-guide/
       layers.md
       overview.md
       pipeline.md

tests/
    # Unit tests for processors, math layer, pipeline, plotting
    test_uvvis_processor.py
    test_math_spectral.py
    test_pipeline.py
    test_plotting_engine.py
