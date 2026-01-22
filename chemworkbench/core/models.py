from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Sequence

from pydantic import BaseModel, Field


class Technique(str, Enum):
    """Universal enumeration of analytical techniques.

    This is intentionally broad and future-proof; processors can
    use this for metadata, routing, or registry purposes.
    """

    UV_VIS = "uv_vis"
    NMR = "nmr"
    IR = "ir"
    RAMAN = "raman"
    CV = "cv"
    EPR = "epr"
    GCMS = "gcms"
    LCMS = "lcms"
    GENERIC = "generic"


class PlotBackend(str, Enum):
    """Backends supported by the universal plotting engine."""

    NONE = "none"
    MATPLOTLIB = "matplotlib"
    PLOTLY = "plotly"
    BOKEH = "bokeh"


class PlotType(str, Enum):
    """Universal plot types supported across all modalities."""

    LINE = "line"
    SCATTER = "scatter"
    BAR = "bar"
    STEM = "stem"
    STEP = "step"
    ERRORBAR = "errorbar"
    HEATMAP = "heatmap"
    CONTOUR = "contour"
    IMAGE = "image"
    SURFACE = "surface"


class PlotLayerConfig(BaseModel):
    """Configuration for a single visual layer within a plot.

    This is the atomic unit of plotting—each layer can be a line,
    scatter, bar, etc., with full Excel-level customization.
    """

    label: Optional[str] = Field(
        default=None,
        description="Legend label for this layer.",
    )
    plot_type: PlotType = Field(
        default=PlotType.LINE,
        description="Type of plot for this layer.",
    )

    # Data payload: always JSON-serializable sequences
    x: Optional[Sequence[float]] = Field(
        default=None,
        description="X-axis data for this layer.",
    )
    y: Optional[Sequence[float]] = Field(
        default=None,
        description="Y-axis data for this layer.",
    )
    z: Optional[Sequence[Sequence[float]]] = Field(
        default=None,
        description="Z data for 2D/3D plots (heatmap, contour, surface).",
    )

    # Visual styling (Excel-level customization)
    color: Optional[str] = Field(
        default=None,
        description="Color spec (hex, named color, etc.).",
    )
    linewidth: Optional[float] = Field(
        default=None,
        description="Line width for line-like plots.",
    )
    linestyle: Optional[str] = Field(
        default=None,
        description="Line style (e.g., '-', '--', ':', 'dashdot').",
    )
    marker: Optional[str] = Field(
        default=None,
        description="Marker style for scatter-like plots.",
    )
    markersize: Optional[float] = Field(
        default=None,
        description="Marker size for scatter-like plots.",
    )
    alpha: Optional[float] = Field(
        default=None,
        description="Transparency (0–1).",
    )
    zorder: Optional[int] = Field(
        default=None,
        description="Drawing order for overlapping layers.",
    )
    visible: bool = Field(
        default=True,
        description="Whether this layer is visible by default.",
    )

    # Arbitrary backend-specific options
    extra: Dict[str, Any] = Field(
        default_factory=dict,
        description="Backend-specific options (JSON-serializable).",
    )


class PlotConfig(BaseModel):
    """Universal plot configuration, independent of backend.

    The pipeline and processors only ever deal with this model.
    The plotting engine is responsible for turning this into
    actual figures for the chosen backend.
    """

    id: str = Field(
        ...,
        description="Unique identifier for this plot within a ProcessedData object.",
    )
    title: Optional[str] = Field(
        default=None,
        description="Plot title.",
    )
    x_label: Optional[str] = Field(
        default=None,
        description="X-axis label.",
    )
    y_label: Optional[str] = Field(
        default=None,
        description="Y-axis label.",
    )
    z_label: Optional[str] = Field(
        default=None,
        description="Z-axis label (for 3D plots).",
    )

    backend: PlotBackend = Field(
        default=PlotBackend.NONE,
        description="Preferred plotting backend.",
    )

    # Layout and global options
    show_legend: bool = Field(
        default=True,
        description="Whether to show a legend.",
    )
    show_grid: bool = Field(
        default=True,
        description="Whether to show grid lines.",
    )
    x_scale: Literal["linear", "log"] = Field(
        default="linear",
        description="Scale for the X-axis.",
    )
    y_scale: Literal["linear", "log"] = Field(
        default="linear",
        description="Scale for the Y-axis.",
    )

    # Multiple layers per plot
    layers: List[PlotLayerConfig] = Field(
        default_factory=list,
        description="List of visual layers composing this plot.",
    )

    # Arbitrary layout options (margins, fonts, etc.)
    layout: Dict[str, Any] = Field(
        default_factory=dict,
        description="Backend-agnostic layout options (JSON-serializable).",
    )


class QCMetric(BaseModel):
    """Single quality-control metric."""

    name: str = Field(
        ...,
        description="Name of the QC metric (e.g., 'snr', 'baseline_rms').",
    )
    value: float = Field(
        ...,
        description="Numeric value of the metric.",
    )
    description: Optional[str] = Field(
        default=None,
        description="Human-readable description of the metric.",
    )
    extra: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for this metric.",
    )


class ProcessedData(BaseModel):
    """Canonical processed data model returned by all processors.

    This is the contract between processors, the pipeline, and the UI.
    Every technique must conform to this schema so the rest of the
    system can remain stable and generic.
    """

    technique: Technique = Field(
        default=Technique.GENERIC,
        description="Analytical technique associated with this data.",
    )

    # Raw and processed payloads
    raw_data: Any = Field(
        ...,
        description="Unmodified input data as received by the processor.",
    )
    processed_data: Any = Field(
        ...,
        description="Final processed data (arrays, tables, etc.).",
    )

    # Metadata and QC
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Technique-specific metadata (JSON-serializable).",
    )
    qc: Dict[str, QCMetric] = Field(
        default_factory=dict,
        description="Quality-control metrics keyed by metric name.",
    )

    # Plotting
    plots: List[PlotConfig] = Field(
        default_factory=list,
        description="List of plot configurations for this dataset.",
    )

    # Diagnostics
    warnings: List[str] = Field(
        default_factory=list,
        description="Non-fatal issues encountered during processing.",
    )
    errors: List[str] = Field(
        default_factory=list,
        description="Fatal or near-fatal issues encountered during processing.",
    )


class BaseProcessorConfig(BaseModel):
    """Universal base configuration for all processors.

    Technique-specific configs must inherit from this class and
    add their own fields. All fields must be JSON-serializable
    and Pydantic-validated so they can be surfaced in the UI.
    """

    name: str = Field(
        ...,
        description="Human-readable name of the processor instance.",
    )
    version: str = Field(
        default="1.0.0",
        description="Version of the processor implementation.",
    )

    # Pipeline toggles
    enable_load: bool = Field(
        default=True,
        description="Enable the load step in the pipeline.",
    )
    enable_validate: bool = Field(
        default=True,
        description="Enable the validate step in the pipeline.",
    )
    enable_preprocess: bool = Field(
        default=True,
        description="Enable the preprocess step in the pipeline.",
    )
    enable_process: bool = Field(
        default=True,
        description="Enable the main process step in the pipeline.",
    )
    enable_postprocess: bool = Field(
        default=True,
        description="Enable the postprocess step in the pipeline.",
    )
    enable_plot: bool = Field(
        default=True,
        description="Enable plot generation in the pipeline.",
    )
    enable_export: bool = Field(
        default=False,
        description="Enable export step in the pipeline.",
    )

    # Arbitrary extra config for future-proofing
    extra: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional processor-specific configuration.",
    )
