# Architecture: Three-Tier Plotting Engine

The plotting system is fully declarative and consists of three layers.

## Tier 1 — Plotting Engine (`plotting/engine.py`)

Responsible for:

- Reading `ProcessedData`
- Reading `plot_config`
- Applying templates
- Creating figure and axes
- Rendering layers in order

## Tier 2 — Layer Types (`plotting/layer_types.py`)

Defines schemas for:

- line
- scatter
- region
- peaks
- annotations
- heatmap (2D)
- contour (2D)

Each layer has:

- required fields
- optional style fields
- data source mapping

## Tier 3 — Plotting Utils (`utils/plotting_utils.py`)

Low-level Matplotlib helpers:

- draw_line
- draw_region
- draw_peaks
- apply_axis_style
- apply_theme

## Templates

Templates live in:

config/templates/<tech>_default_plot.json


Users can save and load templates.

