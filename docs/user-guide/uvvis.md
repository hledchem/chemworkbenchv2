# User Guide: UV-Vis

This guide explains how to load, process, and visualize UV-Vis spectra.

## Loading Data

Supported formats:

- CSV
- JCAMP-DX

Example:

from chemworkbench.api import run_processing
processed = run_processing("file.csv", technique="uvvis")


## Processing Tools

UV-Vis supports:

- baseline correction
- smoothing
- normalization
- peak detection
- region integration

Tools are configured in JSON or through the UI.

## Plotting

from chemworkbench.api import run_plotting
run_plotting(processed, "uvvis_default")


## Templates

UV-Vis includes:

uvvis_default_plot.json


Users can save custom templates.




