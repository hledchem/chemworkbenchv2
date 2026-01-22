# Architecture: Layer Overview

ChemWorkBench v2 is built on a clean separation of concerns:

IO → Math → Pipeline → Processor → Canonical Model → Plotting → UI/API

Each layer has a single responsibility.

## IO Layer (`utils/io_utils.py`)

- Detect file type
- Load raw data
- Save processed data
- No math
- No plotting

## Math Layer (`utils/math_*`)

Tiered structure:

- `math_core.py` — FFT, convolution, interpolation, derivatives
- `math_spectral.py` — baseline, smoothing, normalization, peaks, regions
- `math_technique.py` — NMR phasing, MS calibration, IR band math
- `data_utils.py` — public API

All functions are pure and vectorized.

## Pipeline Layer (`core/pipeline.py`)

- Linear executor (DAG-ready)
- Reads config
- Applies math functions
- Calls processor transforms
- Produces `ProcessedData`

## Processor Layer (`processors/<tech>/processor.py`)

- Thin, technique-specific logic
- Maps config to math
- Builds plot layers
- Loads raw data
- Defines metadata for UI

## Canonical Data Model (`core/models.py`)

Supports:

- 1D spectra
- 2D matrices
- 3D cubes (MS imaging)

## Plotting Layer (`plotting/`)

Three tiers:

1. Engine — what to draw  
2. Layer Types — schemas for line, region, peaks, heatmap  
3. Plotting Utils — low-level Matplotlib helpers

## Config Layer (`config/`)

- Pydantic schema
- Technique defaults
- Plot templates
- Region definitions

## API Layer (`api/`)

- Stable interface for UI, CLI, and LLMs
