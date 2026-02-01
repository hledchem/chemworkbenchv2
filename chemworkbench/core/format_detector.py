"""
ChemWorkBench v2.2 — Structural Format Detector
===============================================

Purpose
-------
This module provides a stable, ingestion-facing wrapper around the
file_sniffer subsystem. It converts raw sniffer output into a normalized
v2.2 DetectedFormat object with:

    - format_id
    - family
    - vendor
    - version
    - technique (optional)
    - subtype
    - confidence

This detector is intentionally minimal, deterministic, and LLM-friendly.
It ensures that ingestion always receives a clean structural format
descriptor, regardless of which detectors or plugins are active.

Design Principles (v2.2)
------------------------
• Structural detection is separate from technique detection.
• Vendor hints are optional and never required.
• Fallback heuristics ensure ingestion never fails on unknown formats.
• Plugins may override or extend detection behavior.
• The detector is stable even if the file_sniffer subsystem evolves.

Future-Proofing Notes
---------------------
This detector is designed for:
• AI-driven format detection
• Plugin-based detectors
• Multi-detector ensembles
• Cloud ingestion pipelines
• Graceful degradation on unknown formats

Public API
----------
- FormatDetector.detect(path: Path) → DetectedFormat
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from chemworkbench.core.models import DetectedFormat, Technique
from chemworkbench.file_sniffer.format_detection_engine import FormatDetectionEngine


# ======================================================================
# Format Detector (v2.2 façade)
# ======================================================================

class FormatDetector:
    """
    Thin, stable façade over the file_sniffer subsystem.

    Responsibilities
    ----------------
    • Run the file_sniffer detection engine.
    • Normalize output into a v2.2 DetectedFormat.
    • Provide deterministic fallback behavior.
    • Keep ingestion decoupled from sniffer internals.

    Non-Responsibilities
    --------------------
    • Loader resolution (handled by LoaderRegistry)
    • Technique detection (handled by TechniqueEngine)
    • Vendor-specific parsing (handled by loaders)
    """

    def __init__(self, engine: Optional[FormatDetectionEngine] = None) -> None:
        self.engine = engine or FormatDetectionEngine()

    # ------------------------------------------------------------------
    # Main API
    # ------------------------------------------------------------------

    def detect(self, path: Path) -> DetectedFormat:
        """
        Detect the structural format of a file and return a normalized
        DetectedFormat object.

        Steps:
        1. Run file_sniffer engine
        2. Normalize sniffer output
        3. Apply fallback heuristics if needed
        """

        # --------------------------------------------------------------
        # 1. Run the file_sniffer engine
        # --------------------------------------------------------------
        sniff = self.engine.detect(path)

        # If the sniffer returns a fully-formed DetectedFormat, use it.
        if isinstance(sniff, DetectedFormat):
            return sniff

        # --------------------------------------------------------------
        # 2. Normalize sniffer output (dict-like)
        # --------------------------------------------------------------
        fmt_id = sniff.get("format_id")
        family = sniff.get("family")
        vendor = sniff.get("vendor")
        version = sniff.get("version")
        subtype = sniff.get("subtype")
        confidence = sniff.get("confidence", 0.5)

        # --------------------------------------------------------------
        # 3. Fallback heuristics (robustness)
        # --------------------------------------------------------------

        # If sniffer failed to identify a format, fall back to ASCII.
        if fmt_id is None:
            fmt_id = "two_column_ascii"
            family = family or "ascii"
            vendor = vendor or None
            version = version or None
            subtype = subtype or None
            confidence = 0.25  # low confidence fallback

        # If family is missing, infer from format_id.
        if family is None:
            if "csv" in fmt_id:
                family = "csv"
            elif "ascii" in fmt_id:
                family = "ascii"
            elif "jcamp" in fmt_id:
                family = "jcamp"
            elif "nmr" in fmt_id or "fid" in fmt_id:
                family = "nmr_dir"
            elif "raw" in fmt_id:
                family = "vendor_dir"
            else:
                family = "unknown"

        # --------------------------------------------------------------
        # 4. Construct normalized DetectedFormat
        # --------------------------------------------------------------
        return DetectedFormat(
            format_id=fmt_id,
            family=family,
            vendor=vendor,
            version=version,
            technique=Technique.UNKNOWN,  # technique engine will fill this in
            subtype=subtype,
            confidence=confidence,
        )

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def describe(self) -> dict:
        """
        Return a structured description of the detector for debugging,
        UI, or LLM reasoning.
        """
        return {
            "engine": self.engine.__class__.__name__,
            "supports_plugins": True,
            "fallback_behavior": "ascii_2col if unknown",
        }
