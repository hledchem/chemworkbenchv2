"""
TechniqueDetectionEngine — ChemWorkBench v2.2
=============================================

LLM‑friendly commentary
-----------------------
This module implements the v2.2 Technique DetectionEngine.

Responsibilities (v2.2):
- consume NormalizedFileInfo (from utils.normalization.normalize_file)
- score techniques using TECHNIQUE_ANCHORS (from core.technique_anchors)
- return the most likely Technique enum with a structured score report

Non‑responsibilities (v2.2):
- selecting loaders (handled by format_detection_engine + loaders.registry)
- selecting format_id (handled by structural detectors)
- routing to processors (handled by core.routing)
- interpreting scientific meaning beyond anchor scoring

This module is intentionally small, deterministic, and easy to maintain.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from chemworkbench.core.models import Technique
from chemworkbench.core.technique_anchors import TECHNIQUE_ANCHORS
from chemworkbench.utils.normalization import NormalizedFileInfo


# ======================================================================
# Scoring result structure
# ======================================================================

@dataclass
class TechniqueScore:
    technique: Technique
    score: float
    reasons: List[str]


# ======================================================================
# Helper functions
# ======================================================================

def _match_weighted_list(tokens: List[str], patterns) -> Tuple[float, List[str]]:
    """
    Generic matcher for weighted lists in anchor blocks.

    patterns may contain:
    - "string" (implicit weight 1.0)
    - ("string", weight)
    """
    total = 0.0
    reasons: List[str] = []

    token_set = set(tokens)

    for entry in patterns:
        if isinstance(entry, tuple):
            pattern, weight = entry
        else:
            pattern, weight = entry, 1.0

        if pattern.lower() in token_set:
            total += float(weight)
            reasons.append(f"+{weight} match '{pattern}'")

    return total, reasons


def _score_negative_markers(tokens: List[str], patterns) -> Tuple[float, List[str]]:
    """
    Apply negative markers to reduce the score when conflicting
    technique signals are present.
    """
    total = 0.0
    reasons: List[str] = []

    token_set = set(tokens)

    for entry in patterns:
        if isinstance(entry, tuple):
            pattern, weight = entry
        else:
            pattern, weight = entry, -1.0

        if pattern.lower() in token_set:
            total += float(weight)
            reasons.append(f"{weight} negative '{pattern}'")

    return total, reasons


def _tokens_from_path(path: Path) -> List[str]:
    """
    Derive simple path tokens (directory names, stem) for structural anchors.
    These are NOT the same as canonical header tokens, but are still
    normalized to lowercase for matching against anchor patterns.
    """
    parts: List[str] = []

    # Directories
    for part in path.parent.parts:
        parts.append(part.lower())

    # Filename stem
    parts.append(path.stem.lower())

    return parts


# ======================================================================
# Core scoring function
# ======================================================================

def score(normalized: NormalizedFileInfo) -> TechniqueScore:
    """
    score(normalized) → TechniqueScore

    Main entrypoint for the Technique DetectionEngine.

    Responsibilities:
    - compute a score for each Technique using TECHNIQUE_ANCHORS
    - return the best TechniqueScore (technique, score, reasons)

    Notes:
    - This engine does NOT select loaders or formats.
    - This engine does NOT inspect raw bytes.
    - This engine does NOT interpret scientific meaning beyond anchors.
    """
    tokens = normalized.tokens
    path_tokens = _tokens_from_path(normalized.path)

    best: TechniqueScore | None = None

    for technique, anchors in TECHNIQUE_ANCHORS.items():
        total_score = 0.0
        reasons: List[str] = []

        # Structural: extensions
        ext = normalized.path.suffix.lower()
        ext_score, ext_reasons = _match_weighted_list(
            [ext], anchors.get("extensions", [])
        )
        total_score += ext_score
        reasons.extend(ext_reasons)

        # Structural: directory markers
        dir_score, dir_reasons = _match_weighted_list(
            path_tokens, anchors.get("directory_markers", [])
        )
        total_score += dir_score
        reasons.extend(dir_reasons)

        # Semantic: header keywords
        header_score, header_reasons = _match_weighted_list(
            tokens, anchors.get("header_keywords", [])
        )
        total_score += header_score
        reasons.extend(header_reasons)

        # Semantic: general keywords
        keyword_score, keyword_reasons = _match_weighted_list(
            tokens, anchors.get("keywords", [])
        )
        total_score += keyword_score
        reasons.extend(keyword_reasons)

        # Negative markers
        neg_score, neg_reasons = _score_negative_markers(
            tokens, anchors.get("negative_markers", [])
        )
        total_score += neg_score
        reasons.extend(neg_reasons)

        current = TechniqueScore(
            technique=technique,
            score=total_score,
            reasons=reasons,
        )

        if best is None or current.score > best.score:
            best = current

    # Fallback
    if best is None:
        best = TechniqueScore(
            technique=Technique.UVVIS,
            score=0.0,
            reasons=["fallback: no anchors matched"],
        )

    return best
