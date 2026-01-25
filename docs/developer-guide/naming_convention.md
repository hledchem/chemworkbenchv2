Absolutely, Hayden — here is the clean, corrected, unified, final v2.1 Naming Convention, incorporating every fix we discussed:
- uv_vis → uvvis everywhere
- clarified processor hooks vs pipeline steps
- added rule for plot layer type names
- added rule for technique config section names
- tightened language for consistency
This is now the authoritative, frozen naming specification for ChemWorkBench v2.

🧱 ChemWorkBench v2 — Naming Conventions (v2.1, Final & Frozen)
Version: 2.1
Status: Frozen
Scope: Entire codebase (core, processors, loaders, plotting, services, runtime, plugins, configs, tests, docs)
This document defines the canonical naming rules for ChemWorkBench v2.
All future development must follow this specification.

1. File & Folder Naming
1.1 General Rules
- All filenames use snake_case.
- All folders use snake_case.
- Names must be descriptive and avoid unnecessary abbreviations.
Examples
math_spectral.py
pipeline.py
models.py
processor.py
plotting_engine.py
uvvis_processor.py



1.2 Math Modules
Pattern:
math_<domain>.py


Examples:
math_spectral.py
math_baseline.py
math_peaks.py
math_smoothing.py
math_normalization.py


This pattern is frozen.

1.3 Processor Modules
Processors live in:
processors/<technique>/processor.py
processors/<technique>/config.py


Examples:
processors/uvvis/processor.py
processors/uvvis/config.py



2. Class Naming
2.1 Rules
- Classes use PascalCase.
- Class names must be nouns.
- Return objects end with Result.
- Schema classes end with Schema.
- Builder classes end with Builder.
- Service classes end with Service.
2.2 Canonical Examples
Technique
PlotBackend
PlotType
PlotLayerConfig
PlotConfig
QCMetric
ProcessedData
BaseProcessorConfig
PeakDetectionResult
FigureSchema
PanelSchema
TraceSchema
AnnotationSchema
PlotConfigBuilder
PlottingService
RuntimeEnvironment



3. Enum Naming
3.1 Rules
- Enum classes: PascalCase
- Enum members: UPPER_SNAKE_CASE
- Enum values: lower_snake_case
Example
class Technique(str, Enum):
    UVVIS = "uvvis"
    NMR = "nmr"



4. Function Naming
4.1 Public Functions
- snake_case
- verb‑first
- descriptive
Examples:
baseline_polynomial
smooth_gaussian
normalize_area
integrate_region
detect_peaks
build_plot_config
apply_style_preset


4.2 Private/Internal Functions
- _leading_underscore
- snake_case
Examples:
_ensure_odd
_apply_region
_estimate_prominence
_validate_schema



5. Processor Hook Naming
5.1 Required Hook
process


5.2 Optional Hooks (only run if implemented)
load
validate
preprocess
postprocess
make_plots
export
build_metadata
compute_qc


5.3 Pipeline Step Names (nouns)
"load"
"validate"
"preprocess"
"process"
"postprocess"
"plot"
"export"


Rule: Hook names are verbs; pipeline steps are nouns.

6. Config Naming
6.1 Config Classes
- PascalCase
- Must end with Config
- Must inherit from BaseProcessorConfig (for technique configs)
Examples:
UVVisConfig
IRConfig
NMRConfig


6.2 Config Fields
Boolean toggles follow:
enable_<step>


From BaseProcessorConfig:
enable_load
enable_validate
enable_preprocess
enable_process
enable_postprocess
enable_plot
enable_export


6.3 Additional Config Fields
- snake_case
- JSON‑serializable
- descriptive
6.4 Technique Config Section Names
Technique config sections must match enum values exactly:
{
  "uvvis": { ... },
  "raman": { ... },
  "nmr": { ... }
}



7. ProcessedData Naming
7.1 Required Fields
technique
raw_data
processed_data
metadata
qc
plots
warnings
errors


7.2 Rules
- snake_case
- plural fields contain lists or dicts

8. Plot Naming
8.1 PlotConfig Fields
id
title
x_label
y_label
z_label
backend
show_legend
show_grid
x_scale
y_scale
z_scale
layers
layout
figsize
nrows
ncols
sharex
sharey


8.2 PlotLayerConfig Fields
label
plot_type
panel
x
y
z
xerr
yerr
color
linewidth
linestyle
marker
markersize
alpha
zorder
visible
bins
width
cmap
explode
normalize
extra


8.3 Plot Layer Type Names
- lowercase
- no underscores
- no hyphens
Examples:
"line"
"scatter"
"heatmap"
"bar"
"histogram"



9. QC Metric Naming
9.1 QCMetric Fields
value
description
extra


9.2 QC Metric Keys
"snr"
"baseline_rms"
"peak_count"



10. Variable Naming
10.1 General Rules
- snake_case
- descriptive
- loop indices may use i, j, idx
10.2 Math Layer Patterns
x_arr, y_arr
y_smooth
baseline
mask
x_min, x_max



11. Error & Warning Naming
11.1 Error Strings
Must begin with "Error".
Examples:
"Error in step 'process': ..."
"Error while building metadata: ..."


11.2 Warning Strings
Stored as plain strings.

12. Metadata Naming
12.1 Rules
- snake_case
- JSON‑serializable
- descriptive
Example:
{
  "method": "local_maxima",
  "derivative": false,
  "min_prominence": 0.05
}



13. Technique Naming
13.1 Enum Members
UVVIS
NMR
IR
RAMAN
CV
EPR
GCMS
LCMS
GENERIC


13.2 Enum Values
"uvvis"
"nmr"
"ir"
"raman"
"cv"
"epr"
"gcms"
"lcms"
"generic"



14. Reserved Words
process
load
validate
preprocess
postprocess
make_plots
export
build_metadata
compute_qc
ProcessedData
PlotConfig
PlotLayerConfig
QCMetric
Technique



15. Documentation Naming
15.1 Rules
- snake_case filenames
- section headers use PascalCase
- terminology must match code exactly
Examples:
naming_conventions.md
developer_guide.md
pipeline_overview.md
math_layer.md



16. Plotting Subsystem Naming
16.1 Schema Classes
End with Schema.
16.2 Builder Classes
End with Builder or Validator.
16.3 Registry Keys
lower_snake_case
Examples:
"uvvis_spectrum"
"multi_panel_dashboard"


16.4 Template Files
lower_snake_case.json
Examples:
uvvis_spectrum.json
chromatogram.json



17. Services Layer Naming
17.1 Files
plotting_service.py
processing_service.py


17.2 Classes
PlottingService
ProcessingService



18. Plugins Naming
18.1 Folder Structure
plugins/<domain>/<plugin_name>/


18.2 Plugin Metadata
- must include plugin.json
- must define a PluginConfig class

19. Runtime Layer Naming
19.1 Files
logging.py
environment.py
errors.py


19.2 Classes
RuntimeLogger
RuntimeEnvironment
ErrorHandler



20. Core IO Naming
20.1 Files
json_loader.py
yaml_loader.py
serializer.py
versioning.py


20.2 Classes
JsonLoader
YamlLoader
Serializer
VersionManager



✅ End of Document
This naming convention is now frozen for ChemWorkBench v2.
