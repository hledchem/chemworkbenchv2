# Developer Guide: Adding Plot Templates

Plot templates define how a technique should be visualized.

## Step 1 — Create Template File
config/templates/<tech>_default_plot.json

Example:

{ "layers": [ {"type": "line", "source": "processed"} ], "axes": { "xlabel": "Wavelength (nm)", "ylabel": "Absorbance" }, "theme": "light" }

## Step 2 — Register Template

In `core/registry.py`:

PLOT_TEMPLATE_REGISTRY["uvvis_default"] = "config/templates/uvvis_default_plot.json"

## Step 3 — Use in Processor

plot_config = load_template("uvvis_default")


## Step 4 — Add Tests

Ensure template loads and renders.
