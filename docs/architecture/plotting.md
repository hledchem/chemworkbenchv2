
# Architecture: Plotting Layer

ChemWorkBench uses a backend-agnostic plotting system based on **plot configs** and **layers**.

Processors never draw figures directly.  
They return `PlotConfig` objects, which the plotting engine renders using a backend (Matplotlib for v2).

## Folder Structure


chemworkbench/plotting/ engine/ base_engine.py matplotlib_engine.py layer_types/ line.py scatter.py bar.py stem.py step.py errorbar.py heatmap.py contour.py image.py pie.py histogram.py line_3d.py scatter_3d.py surface_3d.py wireframe_3d.py style_presets/ default.py

## PlotConfig

`PlotConfig` describes a single figure:

- backend (e.g. `matplotlib`)
- title, labels, scales
- figure size
- 2D or 3D
- subplot grid (`nrows`, `ncols`, `sharex`, `sharey`)
- axis limits
- list of `PlotLayerConfig` objects

## PlotLayerConfig

Each layer describes:

- `plot_type` (line, scatter, bar, heatmap, contour, image, pie, histogram, 3D types)
- `panel` index (for multi-panel figures)
- data (`x`, `y`, `z`)
- styling (color, linewidth, linestyle, marker, alpha, cmap)
- error bars, bins, pie labels, etc.

## Multi-Panel Figures

Multi-panel plots are defined by:

- `PlotConfig.nrows`, `PlotConfig.ncols`
- `PlotLayerConfig.panel` (0-based index into the grid)

The Matplotlib engine:

- creates a subplot grid
- routes each layer to the correct axis
- optionally shares x/y axes

## Dashboards

A dashboard is a list of `PlotConfig` objects:

``python
figures = PlotEngine.render_all(result.plots)


The UI decides how to arrange these figures on screen.

---

#### `docs/developer-guide/adding-plot-templates.md`

``markdown
# Developer Guide: Adding Plot Templates

Plot templates are **reusable patterns** for building `PlotConfig` objects.

They live in:


chemworkbench/utils/plotting_utils.py

and are called by processors.

## Example: Single-Panel Line Plot

``python
def make_simple_line_plot(x, y, title: str, x_label: str, y_label: str) -> PlotConfig:
    return PlotConfig(
        id="simple_line",
        title=title,
        x_label=x_label,
        y_label=y_label,
        backend=PlotBackend.MATPLOTLIB,
        nrows=1,
        ncols=1,
        layers=[
            PlotLayerConfig(
                plot_type=PlotType.LINE,
                x=x,
                y=y,
                color="C0",
                label="signal",
            )
        ],
    )


Example: Multi-Panel UV-Vis Dashboard
def make_uvvis_dashboard(x, y_raw, y_processed, baseline) -> PlotConfig:
    return PlotConfig(
        id="uvvis_dashboard",
        title="UV-Vis Processing Overview",
        x_label="Wavelength (nm)",
        y_label="Intensity",
        backend=PlotBackend.MATPLOTLIB,
        nrows=2,
        ncols=2,
        sharex=True,
        layers=[
            # Panel 0: raw
            PlotLayerConfig(
                panel=0,
                plot_type=PlotType.LINE,
                x=x,
                y=y_raw,
                color="gray",
                label="raw",
            ),
            # Panel 1: baseline
            PlotLayerConfig(
                panel=1,
                plot_type=PlotType.LINE,
                x=x,
                y=baseline,
                color="red",
                linestyle="--",
                label="baseline",
            ),
            # Panel 2: corrected
            PlotLayerConfig(
                panel=2,
                plot_type=PlotType.LINE,
                x=x,
                y=y_processed,
                color="blue",
                label="processed",
            ),
        ],
    )


Best Practices
- Keep templates pure and stateless.
- Use PlotBackend.MATPLOTLIB for v2.
- Prefer PlotLayerConfig.panel over manual subplot logic.
- Let processors call templates instead of building plots inline.

---

#### `docs/user-guide/layers.md` (focused on users)

``markdown
# User Guide: Plot Layers and Dashboards

ChemWorkBench visualizes results using **plot layers** and **dashboards**.

## Layers

Each plot is built from one or more layers:

- line, scatter, bar, stem, step
- error bars
- heatmaps, contours, images
- histograms, pie charts
- 3D line, scatter, surface, wireframe

Layers can be toggled, recolored, or restyled by the UI.

## Multi-Panel Figures

Some plots use multiple panels (subplots) in a single figure:

- raw vs processed
- baseline vs corrected
- magnitude vs phase

Panels share the same x-axis when appropriate.

## Dashboards

A dashboard is a collection of plots:

- one figure per technique
- or multiple figures per sample
- or comparison across samples

Dashboards are driven by the same underlying `PlotConfig` objects, so they are fully reproducible and scriptable.




