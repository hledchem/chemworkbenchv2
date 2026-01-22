# ChemWorkBench v2

ChemWorkBench v2 is a modular, extensible, multi-technique scientific analysis platform designed for spectroscopy, spectrometry, and general analytical workflows. It provides:

- A universal math layer for all scientific transforms
- A thin, technique-specific processor layer
- A config-driven pipeline (linear now, DAG-ready for the future)
- A three-tier plotting engine with full customizability
- A canonical data model supporting 1D, 2D, and 3D datasets
- A plugin-ready architecture for adding new techniques, tools, and visualizations

ChemWorkBench is built for long-term maintainability, reproducibility, and LLM-assisted development.

## Features

- UV-Vis, IR, NMR, MS (extensible to any technique)
- Config-driven processing and plotting
- Pure-function math utilities
- Layer-based plotting engine
- Saveable and loadable plot templates
- Region-based analysis support
- Future-proof for DAG pipelines and advanced modalities (2D NMR, MS imaging)

## Repository Structure

chemworkbench/ core/ utils/ processors/ plotting/ config/ api/ cli/ docs/ tests

See `/docs/overview.md` for a full explanation.

## Quickstart

Quickstart instructions will be added once the first processor is implemented.

## Documentation

All documentation lives in `/docs/`.

- Architecture: `/docs/architecture/`
- Developer Guide: `/docs/developer-guide/`
- User Guide: `/docs/user-guide/`

## Contributing

See `CONTRIBUTING.md`.

## License

TBD.
