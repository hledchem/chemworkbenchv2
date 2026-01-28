"""
Unified Data Models — ChemWorkBench v2.2
========================================

LLM‑friendly commentary
-----------------------
This module defines the canonical data structures used throughout the
ChemWorkBench v2.2 ingestion pipeline. These models form the contract
between:

    - file sniffer
    - loader registry
    - vendor loaders
    - technique router
    - processing pipeline
    - processors
    - plotting subsystem

Responsibilities:
- provide stable, deterministic data structures
- define the universal loader → processor interface
- define the processor → pipeline → plotting interface
- ensure compatibility with plugins and future extensions

Non‑responsibilities:
- file reading (handled by loaders)
- technique detection (handled by the anchor engine)
- scientific interpretation (handled by processors)
- plotting logic (handled by the plotting service)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


# ======================================================================
# Technique Enumeration (canonical, frozen)
# ======================================================================

class Technique(str, Enum):
    UVVIS = "uvvis"
    FLUORESCENCE = "fluorescence"
    IR = "ir"
    RAMAN = "raman"
    NMR = "nmr"
    EPR = "epr"
    CV = "cv"
    GCMS = "gcms"
    LCMS = "lcms"
    CHROMATOGRAPHY = "chromatography"
    UNKNOWN = "unknown"


# ======================================================================
# File Detection Result (output of file sniffer)
# ======================================================================

@dataclass
class DetectedFormat:
    """
    Output of the v2.2 file sniffer.

    - vendor: optional vendor hint from loader sniffing
    - technique: detected technique from anchor engine
    - subtype: loader-specific format identifier
    - confidence: technique confidence score
    """
    vendor: Optional[str]
    technique: Technique
    subtype: Optional[str] = None
    confidence: float = 1.0

    def is_confident(self) -> bool:
        return self.confidence >= 0.75


# ======================================================================
# Raw Data Bundle (output of loaders)
# ======================================================================

@dataclass
class RawDataBundle:
    """
    Raw loader output in v2.2.

    Loaders must return:
        - technique: Technique enum
        - data: universal list-of-dicts [{"x": float, "y": float}, ...]
        - metadata: loader-specific metadata
        - source_path: original file path
    """
    technique: Technique
    data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_path: Optional[str] = None

    def require(self, key: str) -> Any:
        if key not in self.metadata:
            raise KeyError(f"Missing required metadata field: {key}")
        return self.metadata[key]


# ======================================================================
# Processed Data Bundle (output of processors)
# ======================================================================

@dataclass
class ProcessedData:
    """
    Output of the v2.2 processor pipeline.

    Processors return a dict payload containing:
        - x, y arrays
        - intermediate arrays (baseline, corrected, smoothed)
        - peak_results
        - integration_results
        - plots (list of PlotConfig)
    """
    technique: Technique
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    qc: Dict[str, Any] = field(default_factory=dict)
    plots: List["PlotConfig"] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


# ======================================================================
# Plot Configuration (input to plotting engine)
# ======================================================================

@dataclass
class PlotConfig:
    """
    Canonical plot configuration for the v2.2 plotting engine.
    """
    plot_type: str
    title: Optional[str] = None
    x: Optional[List[float]] = None
    y: Optional[List[float]] = None
    z: Optional[List[List[float]]] = None
    style: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def require_xy(self):
        if self.x is None or self.y is None:
            raise ValueError("PlotConfig requires x and y arrays for this plot type.")


# ======================================================================
# Pipeline Result (final output)
# ======================================================================

@dataclass
class PipelineResult:
    """
    Final output of the v2.2 ingestion pipeline.

    Contains:
        - raw: RawDataBundle
        - processed: dict payload from processor
        - metadata: processor metadata
        - qc: processor QC metrics
        - plots: list of PlotConfig
    """
    raw: RawDataBundle
    processed: Dict[str, Any]
    metadata: Dict[str, Any]
    qc: Dict[str, Any]
    plots: List[PlotConfig]

    def summary(self) -> Dict[str, Any]:
        return {
            "technique": self.raw.technique.value,
            "num_points": len(self.processed.get("x", [])),
            "num_plots": len(self.plots),
            "metadata": self.metadata,
        }


# ======================================================================
# Base Processor Config (shared parent for all processors)
# ======================================================================

@dataclass
class BaseProcessorConfig:
    """
    Base class for all processor configuration objects.

    Technique-specific processors (UV‑Vis, IR, Raman, etc.)
    should define their own config classes inheriting from this.
    """
    pass
