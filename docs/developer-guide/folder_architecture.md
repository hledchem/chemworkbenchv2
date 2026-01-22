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
            base_engine.py        # render_plot(), backend selection, style merging
            matplotlib_engine.py  # Matplotlib backend implementation
            plotly_engine.py      # Plotly backend implementation (future)
            bokeh_engine.py       # Bokeh backend implementation (future)

 layer_types/
            __init__.py
            line.py               # Renderer for PlotType.LINE
            scatter.py            # Renderer for PlotType.SCATTER
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
            default.py            # Default theme
            dark.py               # Dark theme
            publication.py        # Publication-ready theme
            high_contrast.py      # Accessibility theme
            pastel.py             # Soft color theme
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
    # Architecture, naming conventions, developer guides
    naming_conventions.md
    developer_guide.md
    plotting_overview.md
    processor_development.md
    pipeline_overview.md

tests/
    # Unit tests for processors, math layer, pipeline, plotting
    test_uvvis_processor.py
    test_math_spectral.py
    test_pipeline.py
    test_plotting_engine.py
