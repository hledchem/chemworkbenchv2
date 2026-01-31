"""
DetectionEngine — ChemWorkBench v2.2
====================================

Unified detection engine combining:

1. FormatDetectionEngine → structural format_id
2. FORMAT_REGISTRY → loader class
3. Technique scoring → semantic technique
4. DetectedFormat → unified result object
"""

from __future__ import annotations
from pathlib import Path

from chemworkbench.core.models import DetectedFormat, Technique
from chemworkbench.core.technique_detection_engine import score as score_technique

from chemworkbench.utils.file_sniffer.format_detection_engine import FormatDetectionEngine
from chemworkbench.utils.file_sniffer.format_registry import FORMAT_REGISTRY


class DetectionEngine:
    """
    Unified v2.2 detection engine.
    """

    def __init__(self):
        self.format_engine = FormatDetectionEngine()

    def run(self, path: Path) -> DetectedFormat:
        if not path.exists():
            return DetectedFormat(
                vendor=None,
                technique=Technique.UNKNOWN,
                subtype=None,
                confidence=0.0,
            )

        # Step 1 — structural format detection
        fmt_result = self.format_engine.detect(path)
        format_id = fmt_result.format_id
        format_conf = fmt_result.confidence

        # Step 2 — loader lookup
        loader_cls = FORMAT_REGISTRY.get(format_id)
        if loader_cls is None:
            return DetectedFormat(
                vendor=None,
                technique=Technique.UNKNOWN,
                subtype=format_id,
                confidence=format_conf,
            )

        loader = loader_cls()

        # Step 3 — technique scoring
        technique_score = score_technique(loader.normalize_for_technique(path))
        technique = technique_score.technique
        technique_conf = float(technique_score.score)

        # Step 4 — construct result
        return DetectedFormat(
            vendor=loader.VENDOR,
            technique=technique,
            subtype=loader.FORMAT,
            confidence=max(format_conf, technique_conf),
        )
