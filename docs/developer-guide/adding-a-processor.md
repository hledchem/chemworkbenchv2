# Developer Guide: Adding a Processor

Processors are thin, technique-specific modules.

## Step 1 — Create Folder
processors/<tech>/


## Step 2 — Implement Processor Class

Extend `BaseProcessor`:

- load_raw
- process
- build_layers
- metadata fields

## Step 3 — Register Processor

In `core/registry.py`:

PROCESSOR_REGISTRY["uvvis"] = UVVisProcessor


## Step 4 — Add Defaults and Templates

config/defaults/<tech>.json config/templates/<tech>_default_plot.json


## Step 5 — Add Tests

tests/test_processors/test_<tech>.py



