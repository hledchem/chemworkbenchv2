"""
core/models.py

Shared data structures for ChemWorkBench v2.
These models define the contract between:
- file sniffer
- loader registry
- vendor loaders
- technique router
- processing pipeline
- processors
- plotting subsystem
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional


# ------------------------------------------------------------
# Technique Enumeration
# ------------------------------------------------------------

class Technique(Enum):
    UVVIS = auto()
    FLUORESCENCE = auto()
    IR = auto()
    RAMAN = auto()
    NMR = auto()
    EPR = auto()
    CV = auto()
    GCMS = auto()
    LCMS = auto()
    CHROMATOGRAPHY = auto()
    UNKNOWN = auto()


# ------------------------------------------------------------
# File Detection Result (output of file sniffer)
# ------------------------------------------------------------

@dataclass
class DetectedFormat:
    vendor: Optional[str]          # e.g., "Agilent", "Bruker", "Horiba"
    technique: Technique           # e.g., Technique.UVVIS
    subtype: Optional[str] = None  # e.g., "DAD", "OPUS", "SPA"
    confidence: float = 1.0        # sniffer confidence score (0–1)

    def is_confident(self) -> bool:
        return self.confidence >= 0.75


# ------------------------------------------------------------
# Raw Data Bundle (output of loaders)
# ------------------------------------------------------------

@dataclass
class RawDataBundle:
    technique: Technique
    data: Any                      # vendor-specific raw data structure
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_path: Optional[str] = None

    def require(self, key: str) -> Any:
        """Convenience accessor for required metadata fields."""
        if key not in self.metadata:
            raise KeyError(f"Missing required metadata field: {key}")
        return self.metadata[key]


# ------------------------------------------------------------
# Processed Data Bundle (output of processors)
# ------------------------------------------------------------

@dataclass
class ProcessedData:
    technique: Technique
    processed: Any                 # normalized, cleaned, structured data
    metadata: Dict[str, Any] = field(default_factory=dict)
    plots: List["PlotConfig"] = field(default_factory=list)


# ------------------------------------------------------------
# Plot Configuration (input to plotting engine)
# ------------------------------------------------------------

@dataclass
class PlotConfig:
    plot_type: str                 # e.g., "line", "scatter", "heatmap"
    title: Optional[str] = None
    x: Optional[List[float]] = None
    y: Optional[List[float]] = None
    z: Optional[List[List[float]]] = None  # for 2D maps
    style: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def require_xy(self):
        if self.x is None or self.y is None:
            raise ValueError("PlotConfig requires x and y arrays for this plot type.")


# ------------------------------------------------------------
# Pipeline Result (final output)
# ------------------------------------------------------------

@dataclass
class PipelineResult:
    raw: RawDataBundle
    processed: ProcessedData
    plots: List[PlotConfig]

    def summary(self) -> Dict[str, Any]:
        return {
            "technique": self.raw.technique.name,
            "num_plots": len(self.plots),
            "metadata": self.raw.metadata,
        }
