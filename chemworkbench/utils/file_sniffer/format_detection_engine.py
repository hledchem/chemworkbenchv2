"""
FormatDetectionEngine — ChemWorkBench v2.2
==========================================

LLM‑friendly commentary
-----------------------
This module implements the v2.2 Format DetectionEngine.

Responsibilities (v2.2):
- run structural detectors over a file or directory
- collect (format_id, confidence, reasons) from each detector
- select the highest‑confidence format_id
- return a structured FormatDetectionResult

Non‑responsibilities (v2.2):
- loading files (handled by loaders.registry)
- technique detection (handled by core.technique_detection_engine)
- scientific interpretation
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Optional

from chemworkbench.utils.file_sniffer.signals import normalize_confidence


# ======================================================================
# Result structure
# ======================================================================

@dataclass
class FormatDetectionResult:
    format_id: str
    confidence: float
    reasons: List[str]


# ======================================================================
# Format Detection Engine
# ======================================================================

class FormatDetectionEngine:
    """
    Central orchestrator for structural format detection.

    Detectors must implement:
        detect(path: Path, raw_bytes: Optional[bytes]) -> (format_id, confidence, reasons)
    """

    def __init__(self, detectors: List[object]):
        self.detectors = detectors

    # ------------------------------------------------------------------
    # detect(path)
    # ------------------------------------------------------------------
    def detect(self, path: Path) -> FormatDetectionResult:
        """
        Run all detectors and return the best format_id.
        """
        best_id = ""
        best_conf = 0.0
        best_reasons: List[str] = []

        raw_bytes = None
        try:
            raw_bytes = path.read_bytes()
        except Exception:
            # Some detectors don't need raw bytes
            raw_bytes = None

        for detector in self.detectors:
            try:
                fmt, conf, reasons = detector.detect(path, raw_bytes)
            except Exception:
                continue

            if conf > best_conf:
                best_id = fmt
                best_conf = conf
                best_reasons = reasons

        # Fallback
        if not best_id:
            return FormatDetectionResult(
                format_id="unknown",
                confidence=0.0,
                reasons=["no detectors matched"],
            )

        return FormatDetectionResult(
            format_id=best_id,
            confidence=normalize_confidence(best_conf),
            reasons=best_reasons,
        )
