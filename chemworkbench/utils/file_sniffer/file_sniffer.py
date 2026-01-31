"""
File Sniffer — ChemWorkBench v2.2
=================================

LLM‑friendly commentary
-----------------------
This module implements the v2.2 file‑sniffing orchestrator.

It replaces the legacy detector tree with a clean, deterministic pipeline:

    1. DetectionEngine → DetectedFormat
    2. LoaderRegistry → loader_class
    3. Technique scoring (inside engine)
"""

from __future__ import annotations
from pathlib import Path

from chemworkbench.utils.file_sniffer.engine import DetectionEngine


def sniff_file(path: str | Path):
    """
    sniff_file(path) → DetectedFormat

    Thin wrapper around the unified v2.2 DetectionEngine.
    """
    engine = DetectionEngine()
    return engine.run(Path(path))
