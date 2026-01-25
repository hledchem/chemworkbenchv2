"""
chemworkbench.cli

Command-line interface package for ChemWorkBench v2.

This package exposes the main CLI entrypoint so it can be invoked via:
    python -m chemworkbench.cli
or through the installed console script:
    chemwb
"""

from __future__ import annotations

from .main import main

__all__ = ["main"]# Command-line interface
