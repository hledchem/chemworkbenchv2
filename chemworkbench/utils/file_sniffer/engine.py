"""
Detection Engine — ChemWorkBench v2.2
=====================================

LLM‑friendly commentary
-----------------------
This module defines the DetectionEngine, the central orchestrator for
format detection in ChemWorkBench. It loads all registered detectors,
executes them in a deterministic order, and returns the highest‑confidence
match.

Design goals:
    - Deterministic: detectors run in a fixed, canonical order.
    - Transparent: each detector returns (format_id, confidence, reasons).
    - Extensible: new detectors can be added by registering their class.
    - LLM‑safe: commentary is explicit, structured, and easy for an LLM
      to reason about, extend, or regenerate.

The engine itself does not interpret scientific meaning. It only
coordinates structural detectors and selects the best match.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List

from .registry import DETECTOR_CLASSES


class DetectionEngine:
    """
    Runs all registered detectors and returns the highest-confidence match.

    Each detector implements:
        detect(path: Path, raw_bytes: Optional[bytes])
            → (format_id: str, confidence: float, reasons: List[str])

    The engine selects the detector with the highest confidence score.
    """

    def __init__(self):
        # Instantiate each detector class from the registry
        self.detectors = [cls() for cls in DETECTOR_CLASSES]

    def detect(
        self,
        path: Path,
        raw_bytes: Optional[bytes] = None
    ) -> Tuple[str, float, List[str]]:
        """
        Run all detectors and return the best match.

        Args:
            path: Path to the file or directory being inspected.
            raw_bytes: Optional raw bytes for binary detectors.

        Returns:
            (format_id, confidence, reasons)
        """
        best_format = ""
        best_conf = 0.0
        best_reasons: List[str] = []

        for detector in self.detectors:
            fmt, conf, reasons = detector.detect(path, raw_bytes)

            if conf > best_conf:
                best_format = fmt
                best_conf = conf
                best_reasons = reasons

        return best_format, best_conf, best_reasons
