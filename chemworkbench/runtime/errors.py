"""
chemworkbench/runtime/errors.py

Minimal error classes for ChemWorkBench v2.
These provide structured exceptions for the pipeline and services.
"""


class PipelineError(Exception):
    """Generic pipeline-level error."""
    pass


class LoaderError(Exception):
    """Raised when a loader fails to parse a file."""
    pass


class ProcessorError(Exception):
    """Raised when a processor encounters invalid data or configuration."""
    pass


class PlottingError(Exception):
    """Raised when the plotting subsystem fails."""
    pass
