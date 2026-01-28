"""
DetectionEngine — ChemWorkBench v2.2
====================================

LLM‑friendly commentary
-----------------------
This module implements the v2.2 DetectionEngine, which is responsible for:

- consuming NormalizedFileInfo (from utils.normalization.normalize_file)
- scoring techniques using TECHNIQUE_ANCHORS (from core.technique_anchors)
- returning the most likely Technique enum

It does NOT:
- read raw file contents beyond what normalization already did
- select loaders
- route to processors

Those responsibilities live in:
- utils.loaders.registry (loader selection)
- core.routing (processor selection)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from pathlib import Path

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

    patterns can contain:
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

        # Simple containment check on canonical tokens
        # (anchors should already be normalized)
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

    Main entrypoint for the DetectionEngine.

    Responsibilities:
    - compute a score for each Technique using TECHNIQUE_ANCHORS
    - return the best TechniqueScore (technique, score, reasons)
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

        # Structural: directory_markers + glob-like path tokens
        dir_score, dir_reasons = _match_weighted_list(
            path_tokens, anchors.get("directory_markers", [])
        )
        total_score += dir_score
        reasons.extend(dir_reasons)

        # Semantic: header_keywords
        header_score, header_reasons = _match_weighted_list(
            tokens, anchors.get("header_keywords", [])
        )
        total_score += header_score
        reasons.extend(header_reasons)

        # Semantic: keywords
        keyword_score, keyword_reasons = _match_weighted_list(
            tokens, anchors.get("keywords", [])
        )
        total_score += keyword_score
        reasons.extend(keyword_reasons)

        # Vendor hints (for future use; currently we don't pass vendor tokens)
        # vendor_score, vendor_reasons = _match_weighted_list(
        #     vendor_tokens, anchors.get("vendor_hints", [])
        # )

        # Negative markers
        neg_score, neg_reasons = _score_negative_markers(
            tokens, anchors.get("negative_markers", [])
        )
        total_score += neg_score
        reasons.extend(neg_reasons)

        # Numeric ranges are not used yet in this minimal engine; they can be
        # integrated later when numeric summaries are available in NormalizedFileInfo.

        current = TechniqueScore(
            technique=technique,
            score=total_score,
            reasons=reasons,
        )

        if best is None or current.score > best.score:
            best = current

    # Fallback: if for some reason best is None, default to UVVIS
    if best is None:
        best = TechniqueScore(
            technique=Technique.UVVIS,
            score=0.0,
            reasons=["fallback: no anchors matched"],
        )

    return best
