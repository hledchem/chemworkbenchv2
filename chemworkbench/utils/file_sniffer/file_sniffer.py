"""
File Sniffer — ChemWorkBench v2.2
=================================

LLM‑friendly commentary
-----------------------
This module implements the v2.2 file‑sniffing orchestrator.

It replaces the legacy 3‑tier detection system with a clean,
deterministic pipeline:

    1. FormatDetectionEngine → format_id
    2. Format Registry → loader_class
    3. TechniqueDetectionEngine → technique
    4. Construct DetectedFormat

Responsibilities:
- run structural format detection
- select the correct loader class via format registry
- run technique scoring
- return a DetectedFormat object

Non‑responsibilities:
- reading file contents (loaders do that)
- interpreting scientific meaning (processors do that)
- vendor/technique heuristics (anchors do that)
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from chemworkbench.core.models import Technique, DetectedFormat
from chemworkbench.core.technique_detection_engine import score as score_technique

from chemworkbench.utils.file_sniffer.format_detection_engine import FormatDetectionEngine
from chemworkbench.utils.file_sniffer.format_registry import FORMAT_REGISTRY

from chemworkbench.utils.file_sniffer.detectors.ascii.headered_csv_detector import HeaderedCSVDetector
from chemworkbench.utils.file_sniffer.detectors.ascii.no_header_csv_detector import NoHeaderCSVDetector
from chemworkbench.utils.file_sniffer.detectors.ascii.two_column_ascii_detector import TwoColumnAsciiDetector
from chemworkbench.utils.file_sniffer.detectors.ascii.multi_column_ascii_detector import MultiColumnAsciiDetector
from chemworkbench.utils.file_sniffer.detectors.spectroscopy.jcamp_detector import JcampDetector


# ======================================================================
# Build the FormatDetectionEngine with all detectors
# ======================================================================

FORMAT_ENGINE = FormatDetectionEngine(detectors=[
    HeaderedCSVDetector(),
    NoHeaderCSVDetector(),
    TwoColumnAsciiDetector(),
    MultiColumnAsciiDetector(),
    JcampDetector(),
    # future: SPCDetector(), OpusDetector(), vendor directory detectors, etc.
])


# ======================================================================
# Main sniffer entrypoint
# ======================================================================

def sniff_file(path: str | Path) -> DetectedFormat:
    """
    sniff_file(path) → DetectedFormat

    v2.2 file‑sniffing orchestrator.

    Steps:
    1. Run FormatDetectionEngine → format_id
    2. Lookup loader_class via FORMAT_REGISTRY
    3. Run TechniqueDetectionEngine → technique
    4. Return DetectedFormat(vendor, technique, subtype, confidence)
    """
    path = Path(path)

    if not path.exists():
        return DetectedFormat(
            vendor=None,
            technique=Technique.UNKNOWN,
            subtype=None,
            confidence=0.0,
        )

    # ------------------------------------------------------------
    # Step 1: Structural format detection
    # ------------------------------------------------------------
    fmt_result = FORMAT_ENGINE.detect(path)
    format_id = fmt_result.format_id
    format_conf = fmt_result.confidence

    # ------------------------------------------------------------
    # Step 2: Loader lookup
    # ------------------------------------------------------------
    loader_cls = FORMAT_REGISTRY.get(format_id)
    if loader_cls is None:
        # No loader found → technique may still be correct
        return DetectedFormat(
            vendor=None,
            technique=Technique.UNKNOWN,
            subtype=format_id,
            confidence=format_conf,
        )

    loader = loader_cls()

    # ------------------------------------------------------------
    # Step 3: Technique scoring (semantic)
    # ------------------------------------------------------------
    # NOTE: technique scoring uses normalized tokens, not raw bytes.
    # We normalize inside the technique engine.
    technique_score = score_technique(loader.normalize_for_technique(path))
    technique = technique_score.technique
    technique_conf = float(technique_score.score)

    # ------------------------------------------------------------
    # Step 4: Construct DetectedFormat
    # ------------------------------------------------------------
    return DetectedFormat(
        vendor=loader.VENDOR,
        technique=technique,
        subtype=loader.FORMAT,
        confidence=max(format_conf, technique_conf),
    )
