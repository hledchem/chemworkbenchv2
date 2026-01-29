"""
signals.py — ChemWorkBench v2.2
===============================

LLM‑friendly commentary
-----------------------
This module provides shared scoring utilities for the v2.2
FormatDetectionEngine. These helpers keep detectors small and
deterministic by centralizing confidence normalization and simple
scoring math.

Responsibilities (v2.2):
- normalize confidence values to a stable [0.0, 1.0] range
- provide additive scoring helpers for detectors
- provide safe numeric checks for ASCII detectors

Non‑responsibilities:
- running detectors
- selecting loaders
- interpreting scientific meaning
- technique detection
"""

from __future__ import annotations

from typing import Iterable


# ======================================================================
# Confidence normalization
# ======================================================================

def normalize_confidence(value: float) -> float:
    """
    Clamp a confidence value into the [0.0, 1.0] range.

    Detectors may return values outside this range (e.g., 2.0 for
    strong matches). The FormatDetectionEngine always normalizes
    before returning a final FormatDetectionResult.
    """
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)


# ======================================================================
# Numeric helpers
# ======================================================================

def is_float(token: str) -> bool:
    """
    Return True if the token can be parsed as a float.

    Used by ASCII detectors to quickly validate numeric columns
    without raising exceptions.
    """
    try:
        float(token)
        return True
    except Exception:
        return False


def all_float(tokens: Iterable[str]) -> bool:
    """
    Return True if all tokens in the iterable are valid floats.
    """
    return all(is_float(t) for t in tokens)


# ======================================================================
# Scoring helpers
# ======================================================================

def weighted_add(base: float, weight: float) -> float:
    """
    Add a weighted score contribution. Detectors may use this to
    accumulate confidence based on structural signals.
    """
    return base + float(weight)


def boost_if(condition: bool, amount: float) -> float:
    """
    Return a confidence boost if the condition is True, otherwise 0.0.
    """
    return float(amount) if condition else 0.0


def penalty_if(condition: bool, amount: float) -> float:
    """
    Return a negative confidence penalty if the condition is True.
    """
    return -float(amount) if condition else 0.0
