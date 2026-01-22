# Contributing to ChemWorkBench v2

Thank you for contributing to ChemWorkBench. This project is designed to be modular, extensible, and easy to maintain.

This guide explains:

- Code style
- How to add math functions
- How to add tools
- How to add processors
- How to add plot templates
- How to run tests

# Code Style

- Use Python 3.10+
- Use type hints everywhere
- Use docstrings for all public functions and classes
- Keep functions pure (no side effects)
- Keep processors thin
- Keep math centralized in `utils/`
- Keep plotting declarative and layer-based

# Adding New Features

See `/docs/developer-guide/` for detailed instructions:

- adding-math-functions.md
- adding-a-tool.md
- adding-a-processor.md
- adding-plot-templates.md

# Running Tests

Tests live in `/tests/`.

Run:

pytest

# Pull Requests

- Keep PRs small and focused
- Include tests for new math functions and processors
- Update documentation when adding new features
- Follow the architecture rules in `/docs/architecture/`

# Questions

Open an issue or discussion on GitHub.
