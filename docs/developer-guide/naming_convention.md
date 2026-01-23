
# ChemWorkBench v2 — Naming Conventions (Authoritative Specification)

This document defines the official naming conventions for all code, configs, processors, math utilities, pipeline hooks, models, and documentation in ChemWorkBench v2.

These conventions are derived directly from the existing v2 codebase:

- `core/math_spectral.py`
- `core/pipeline.py`
- `core/models.py`

They are designed to be interpretable by both humans and LLMs, and to prevent naming drift as the platform grows.

---

# 1. File & Folder Naming

## 1.1 General Rules
- All filenames use **snake_case**.
- All folders use **snake_case**.
- Names must be descriptive and avoid unnecessary abbreviations.

### Examples


math_spectral.py pipeline.py models.py processor.py plotting_engine.py uvvis_processor.py

## 1.2 Math Modules
Math modules follow the pattern:


math_<domain>.py

Examples:


math_spectral.py math_baseline.py math_peaks.py math_smoothing.py math_normalization.py

This pattern is frozen for all future math modules.

## 1.3 Processor Modules
Processors live in:


processors/<technique>/processor.py processors/<technique>/config.py

Example:


processors/uvvis/processor.py processors/uvvis/config.py

---

# 2. Class Naming

## 2.1 Rules
- All classes use **PascalCase**.
- Class names must be nouns.
- Structured return objects must end with **Result**.

## 2.2 Canonical Examples
- `Technique`
- `PlotBackend`
- `PlotType`
- `PlotLayerConfig`
- `PlotConfig`
- `QCMetric`
- `ProcessedData`
- `BaseProcessorConfig`
- `PeakDetectionResult`
- `ProcessorProtocol`

---

# 3. Enum Naming

## 3.1 Rules
- Enum classes use **PascalCase**.
- Enum members use **UPPER_SNAKE_CASE**.
- Enum values (strings) use **lower_snake_case**.

### Example
python
class Technique(str, Enum):
    UV_VIS = "uv_vis"
    NMR = "nmr"



4. Function Naming
4.1 Public Functions
- Use snake_case.
- Must be verb-first.
- Must describe the operation clearly.
Examples from math_spectral.py:
- baseline_polynomial
- smooth_gaussian
- normalize_area
- integrate_region
- detect_peaks
4.2 Private/Internal Functions
- Must begin with _.
- Use snake_case.
- May return heterogeneous tuples.
Examples:
- _ensure_odd
- _apply_region
- _estimate_prominence

5. Processor Hook Naming
These names are frozen because the pipeline calls them dynamically.
5.1 Required Hook
- process
5.2 Optional Hooks
- load
- validate
- preprocess
- postprocess
- make_plots
- export
- build_metadata
- compute_qc
5.3 Step Names (internal to pipeline)
- "load"
- "validate"
- "preprocess"
- "process"
- "postprocess"
- "plot"
- "export"
Rule
Hook names are verbs; step names are nouns.


6. Config Naming
6.1 Config Classes
- Must inherit from BaseProcessorConfig.
- Must use PascalCase.
- Must end with Config.
Examples:
UVVisConfig
IRConfig
NMRConfig


6.2 Config Fields
Boolean toggles must follow:
enable_<step>


As defined in BaseProcessorConfig:
- enable_load
- enable_validate
- enable_preprocess
- enable_process
- enable_postprocess
- enable_plot
- enable_export
6.3 Additional Config Fields
- Must be JSON-serializable.
- Must use snake_case.
- Must be descriptive.

7. ProcessedData Naming
7.1 Required Fields
- technique
- raw_data
- processed_data
- metadata
- qc
- plots
- warnings
- errors
These names are frozen.
7.2 Rules
- All lowercase.
- Use snake_case.
- Plural fields must contain lists or dicts.

8. Plot Naming
8.1 PlotConfig Fields
- id
- title
- x_label
- y_label
- z_label
- backend
- show_legend
- show_grid
- x_scale
- y_scale
- layers
- layout
8.2 PlotLayerConfig Fields
- label
- plot_type
- x
- y
- z
- color
- linewidth
- linestyle
- marker
- markersize
- alpha
- zorder
- visible
- extra
Rule
All plot config fields must be JSON-serializable.


9. QC Metric Naming
9.1 QCMetric Fields
- name
- value
- description
- extra
9.2 QC Metric Keys
Stored in ProcessedData.qc as:
qc = {
    "snr": QCMetric(...),
    "baseline_rms": QCMetric(...),
}


Rule
QC metric keys must be lower_snake_case.


10. Variable Naming
10.1 General Rules
- Use snake_case.
- Prefer descriptive names (x_arr, y_smooth, baseline).
- Loop indices may use i, j, idx.
10.2 Math Layer Patterns
- Arrays end with _arr
- Smoothed arrays end with _smooth
- Baselines use baseline
- Masks use mask
- Regions use x_min, x_max
These patterns match math_spectral.py.

11. Error & Warning Naming
11.1 Error Strings
All error messages must begin with "Error".
Examples from pipeline:
- "Error in step 'process': ..."
- "Error while building metadata: ..."
11.2 Warning Strings
Stored in ProcessedData.warnings as plain strings.

12. Metadata Naming
12.1 Rules
- Keys must be JSON-serializable.
- Must use snake_case.
- Must be descriptive.
Example from peak detection:
metadata = {
    "method": "local_maxima",
    "derivative": False,
    "min_prominence": 0.05,
}



13. Technique Naming
13.1 Enum Members
- UV_VIS
- NMR
- IR
- RAMAN
- CV
- EPR
- GCMS
- LCMS
- GENERIC
13.2 Enum Values
- "uv_vis"
- "nmr"
- "ir"
- "raman"
- "cv"
- "epr"
- "gcms"
- "lcms"
- "generic"
Rule
Technique identifiers must always use lower_snake_case in serialized form.


14. Reserved Words
These names have special meaning and must not be reused:
- process
- load
- validate
- preprocess
- postprocess
- make_plots
- export
- build_metadata
- compute_qc
- ProcessedData
- PlotConfig
- PlotLayerConfig
- QCMetric
- Technique

15. Documentation Naming
15.1 Rules
- Docs must use snake_case filenames.
- Section headers use PascalCase.
- Terminology must match code exactly.
Examples:
naming_conventions.md
developer_guide.md
math_layer.md
pipeline_overview.md

16. Plotting Subsystem Naming
16.1 Schema Classes
- Must use PascalCase.
- Must end with Schema.
Examples:
- FigureSchema
- PanelSchema
- TraceSchema
- AnnotationSchema
16.2 Builder Classes
- Must use PascalCase.
- Must end with Builder or Validator.
Examples:
- PlotConfigBuilder
- PlotSchemaValidator
16.3 Registry Keys
- Must use lower_snake_case.
Examples:
- "uvvis_spectrum"
- "multi_panel_dashboard"
16.4 Template Files
- Must use lower_snake_case.json.
Examples:
- uvvis_spectrum.json
- chromatogram.json

17. Services Layer Naming
17.1 Service Files
- Must end with _service.py.
Examples:
- plotting_service.py
- processing_service.py
17.2 Service Classes
- Must end with Service.
Examples:
- PlottingService
- ProcessingService

18. Plugins Naming
18.1 Plugin Folder Structure
plugins/<domain>/<plugin_name>/


18.2 Plugin Metadata
- Must include plugin.json.
- Must define a PluginConfig class.

19. Runtime Layer Naming
19.1 Files
- logging.py
- environment.py
- errors.py
19.2 Classes
- RuntimeLogger
- RuntimeEnvironment
- ErrorHandler

20. Core IO Naming
20.1 Files
- json_loader.py
- yaml_loader.py
- serializer.py
- versioning.py
20.2 Classes
- JsonLoader
- YamlLoader
- Serializer
- VersionManager







