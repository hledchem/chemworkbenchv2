"""
spectral_detectors.py

Tier 2 technique inference for ChemWorkBench v2.
This layer is intentionally minimal because real technique
detection is handled by loaders and vendor logic.

This placeholder keeps the architecture intact.
"""

from chemworkbench.core.models import Technique, DetectedFormat


def infer_technique_from_data(path: str):
    """
    Placeholder technique inference.
    Always returns None so that loaders determine technique.
    """
    return None
