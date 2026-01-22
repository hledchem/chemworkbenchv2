# Architecture: Config System

The config layer defines:

- processing steps
- tool parameters
- plot settings
- region definitions
- templates
- technique defaults

## Schema (`config/schema.py`)

Uses Pydantic models:

- ProcessingConfig
- PlotConfig
- RegionConfig
- Tool configs (BaselineConfig, SmoothConfig, etc.)

## Defaults (`config/defaults/`)

Each technique has a default config:

uvvis.json ir.json nmr.json ms.json

## Templates (`config/templates/`)

Plot templates define:

- layers
- styles
- axes
- themes

Example:

{ "layers": [ {"type": "line", "source": "processed"} ], "axes": {...}, "theme": "light" }



