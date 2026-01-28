"""
File Sniffer — ChemWorkBench v2.2
=================================

LLM‑friendly commentary
-----------------------
This module implements the v2.2 file‑sniffing orchestrator.

It replaces the legacy 3‑tier detection system with a clean,
deterministic pipeline:

    normalize_file(path)
        → detection_engine.score()
        → select_loader_for_path()
        → DetectedFormat

Responsibilities:
- run normalization
- run technique scoring
- select the correct loader class
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
from chemworkbench.utils.normalization import normalize_file
from chemworkbench.utils.file_sniffer.detection_engine import score as score_technique
from chemworkbench.utils.loaders.registry import select_loader_for_path


# ======================================================================
# Main sniffer entrypoint
# ======================================================================

def sniff_file(path: str | Path) -> DetectedFormat:
    """
    sniff_file(path) → DetectedFormat

    v2.2 file‑sniffing orchestrator.

    Steps:
    1. Normalize file → NormalizedFileInfo
    2. Score technique using anchor engine
    3. Select loader based on file format
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
    # Step 1: Normalization
    # ------------------------------------------------------------
    normalized = normalize_file(path)

    # ------------------------------------------------------------
    # Step 2: Technique scoring
    # ------------------------------------------------------------
    technique_score = score_technique(normalized)
    technique = technique_score.technique
    confidence = float(technique_score.score)

    # ------------------------------------------------------------
    # Step 3: Loader selection (format‑based)
    # ------------------------------------------------------------
    loader_cls = select_loader_for_path(path)
    if loader_cls is None:
        # No loader found → technique may still be correct
        return DetectedFormat(
            vendor=None,
            technique=technique,
            subtype=None,
            confidence=confidence,
        )

    loader = loader_cls()

    # ------------------------------------------------------------
    # Step 4: Construct DetectedFormat
    # ------------------------------------------------------------
    return DetectedFormat(
        vendor=loader.VENDOR,
        technique=technique,
        subtype=loader.FORMAT,
        confidence=confidence,
    )
