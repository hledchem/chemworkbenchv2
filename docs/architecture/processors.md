docs/architecture/processors.md
# Processor Architecture

ChemWorkBench processors live under:


chemworkbench/processors/<technique>/

Each processor is a self-contained module implementing the universal processing pipeline:

1. `load()`
2. `validate()`
3. `preprocess()`
4. `process()`
5. `postprocess()`
6. `make_plots()`
7. `export()`

Processors must return:

- processed numerical data (dict)
- metadata (dict)
- QC metrics (dict of `QCMetric`)
- plot definitions (`List[PlotConfig]`)

## Folder Structure

Example for UV-Vis:


chemworkbench/processors/uvvis/ init.py config.py processor.py

## Config Models

Each processor defines a Pydantic config model inheriting from:


chemworkbench/core/models.BaseProcessorConfig

This ensures:

- validation
- serialization
- compatibility with the universal pipeline

## Plot Output

Processors do not render figures directly.  
They return `PlotConfig` objects, which the plotting engine later renders.

Each `PlotConfig` contains:

- title, labels, scales
- backend selection
- a list of `PlotLayerConfig` objects




