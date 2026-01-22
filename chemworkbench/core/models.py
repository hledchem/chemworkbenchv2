from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field


# ------------------------------------------------------------
# Core enums
# ------------------------------------------------------------

class Technique(str, Enum):
    UV_VIS = "uvvis"
    IR = "ir"
    NMR = "nmr"
    RAMAN = "raman"
    CV = "cv"
    EPR = "epr"
    GCMS = "gcms"
    LCMS = "lcms"


class PlotBackend(str, Enum):
    NONE = "none"
    MATPLOTLIB = "matplotlib"
    # PLOTLY = "plotly"  # future
    # BOKEH = "bokeh"    # future


class PlotType(str, Enum):
    # 2D
    LINE = "line"
    SCATTER = "scatter"
    BAR = "bar"
    STEM = "stem"
    STEP = "step"
    ERRORBAR = "errorbar"
    HEATMAP = "heatmap"
    CONTOUR = "contour"
    IMAGE = "image"
    PIE = "pie"
    HISTOGRAM = "histogram"

    # 3D
    LINE_3D = "line_3d"
    SCATTER_3D = "scatter_3d"
    SURFACE_3D = "surface_3d"
    WIREFRAME_3D = "wireframe_3d"


# ------------------------------------------------------------
# Base processor config
# ------------------------------------------------------------

class BaseProcessorConfig(BaseModel):
    """Base configuration shared by all processors."""

    name: str = Field(default="default", description="Human-readable name for this config.")
    version: str = Field(default="1.0.0", description="Config schema version.")

    # Pipeline toggles
    enable_load: bool = True
    enable_validate: bool = True
    enable_preprocess: bool = True
    enable_process: bool = True
    enable_postprocess: bool = True
    enable_plot: bool = True
    enable_export: bool = False

    # Extra technique-specific options
    extra: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "ignore"


# ------------------------------------------------------------
# QC metrics
# ------------------------------------------------------------

class QCMetric(BaseModel):
    """Quality control metric with description."""

    value: float
    description: str


# ------------------------------------------------------------
# Plot models
# ------------------------------------------------------------

class PlotLayerConfig(BaseModel):
    """Configuration for a single plot layer."""

    # Core
    plot_type: PlotType
    label: Optional[str] = None

    # Panel index (for multi-panel figures; 0-based)
    panel: int = 0

    # Data
    x: Optional[List[float]] = None
    y: Optional[List[float]] = None
    # For heatmaps / images / surfaces: z can be 1D or 2D
    z: Optional[Union[List[float], List[List[float]]]] = None

    # Error bars
    yerr: Optional[List[float]] = None
    xerr: Optional[List[float]] = None

    # Styling
    color: Optional[str] = None
    linewidth: float = 1.5
    linestyle: str = "-"
    marker: Optional[str] = None
    markersize: Optional[float] = None
    alpha: float = 1.0
    cmap: Optional[str] = "viridis"

    # Bar / histogram
    width: Optional[float] = None
    bins: Optional[int] = None
    stacked: bool = False

    # Pie
    labels: Optional[List[str]] = None
    explode: Optional[List[float]] = None
    normalize: bool = True

    # 3D
    is_3d: bool = False


class PlotConfig(BaseModel):
    """High-level plot configuration, backend-agnostic."""

    id: str
    title: str = ""
    x_label: str = ""
    y_label: str = ""
    z_label: str = ""

    backend: PlotBackend = PlotBackend.NONE

    # Figure layout
    figsize: Tuple[float, float] = (6.0, 4.0)
    is_3d: bool = False

    # Subplot grid (for multi-panel figures)
    nrows: int = 1
    ncols: int = 1
    sharex: bool = False
    sharey: bool = False

    # Axes options
    x_scale: str = "linear"
    y_scale: str = "linear"
    z_scale: str = "linear"

    x_limits: Optional[Tuple[float, float]] = None
    y_limits: Optional[Tuple[float, float]] = None
    z_limits: Optional[Tuple[float, float]] = None

    # Layers
    layers: List[PlotLayerConfig] = Field(default_factory=list)

    # Extra options for UI/backends
    extra: Dict[str, Any] = Field(default_factory=dict)


# ------------------------------------------------------------
# Processed data + pipeline result
# ------------------------------------------------------------

class ProcessedData(BaseModel):
    """
    Canonical container for processed numerical data.

    This is intentionally flexible and JSON-serializable.
    """

    # Core arrays
    x: Optional[List[float]] = None
    y: Optional[List[float]] = None

    # Raw data
    x_raw: Optional[List[float]] = None
    y_raw: Optional[List[float]] = None

    # Intermediate arrays (UV-Vis example)
    baseline: Optional[List[float]] = None
    y_corrected: Optional[List[float]] = None
    y_smooth: Optional[List[float]] = None

    # Analysis results
    peak_results: Optional[Dict[str, Any]] = None
    integration_results: Optional[Dict[str, Any]] = None

    # Technique-specific extras
    extra: Dict[str, Any] = Field(default_factory=dict)


class PipelineResult(BaseModel):
    """Unified result object returned by the universal pipeline."""

    processed_data: Union[ProcessedData, Dict[str, Any], None] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    qc: Dict[str, QCMetric] = Field(default_factory=dict)
    plots: List[PlotConfig] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
