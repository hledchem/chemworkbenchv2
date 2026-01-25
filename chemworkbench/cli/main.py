"""
chemworkbench.cli.main

Primary command-line interface for ChemWorkBench v2.

Supports:
    chemwb run <file>
    chemwb process <file>
    chemwb plot <plot_config.json>

This CLI is designed to work cleanly in PowerShell, CMD, Bash, and zsh.
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path

from chemworkbench.api.run_processing import run_processing_from_file
from chemworkbench.api.run_plotting import run_plotting
from chemworkbench.core.pipeline import pipeline
from chemworkbench.core.models import PlotConfig
from chemworkbench.runtime.logging import enable_debug_logging, get_logger
from chemworkbench.runtime.errors import PipelineError


logger = get_logger(__name__)


# ----------------------------------------------------------------------
# Command implementations
# ----------------------------------------------------------------------

def cmd_run(args):
    """Run the full pipeline on a file."""
    try:
        result = run_processing_from_file(args.file)
        print(f"Technique: {result.raw.technique.name}")
        print(f"Plots generated: {len(result.plots)}")
    except PipelineError as exc:
        print(f"Error: {exc}")


def cmd_process(args):
    """Run processing only (no plotting)."""
    try:
        result = pipeline.run(args.file)
        print(f"Technique: {result.raw.technique.name}")
        print(f"Processed metadata: {result.processed.metadata}")
    except PipelineError as exc:
        print(f"Error: {exc}")


def cmd_plot(args):
    """Render plots from a PlotConfig JSON file."""
    try:
        with open(args.json, "r") as f:
            cfgs = json.load(f)

        plot_configs = [PlotConfig(**cfg) for cfg in cfgs]
        figs = run_plotting(plot_configs)
        print(f"Rendered {len(figs)} plot(s)")
    except Exception as exc:
        print(f"Error: {exc}")


# ----------------------------------------------------------------------
# CLI entrypoint
# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="chemwb",
        description="ChemWorkBench v2 Command-Line Interface",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose debug logging",
    )

    subparsers = parser.add_subparsers(dest="command")

    # Full pipeline
    p_run = subparsers.add_parser("run", help="Run full pipeline on a file")
    p_run.add_argument("file", type=str)
    p_run.set_defaults(func=cmd_run)

    # Processing only
    p_process = subparsers.add_parser("process", help="Run processing only")
    p_process.add_argument("file", type=str)
    p_process.set_defaults(func=cmd_process)

    # Plotting only
    p_plot = subparsers.add_parser("plot", help="Render plots from PlotConfig JSON")
    p_plot.add_argument("json", type=str)
    p_plot.set_defaults(func=cmd_plot)

    args = parser.parse_args()

    if args.debug:
        enable_debug_logging()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
