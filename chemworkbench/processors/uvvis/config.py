from __future__ import annotations

from typing import Dict, List, Tuple

from pydantic import Field

from chemworkbench.core.models import BaseProcessorConfig


class UVVisConfig(BaseProcessorConfig):
    """Configuration for the UV-Vis processor.

    Extends the universal BaseProcessorConfig with UV-Vis-specific
    preprocessing, normalization, and peak analysis options.
    """

    # ------------------------------------------------------------------
    # Baseline correction
    # ------------------------------------------------------------------
    baseline_method: str = Field(
        default="polynomial",
        description=(
            "Baseline method: 'polynomial', 'rolling_min', "
            "'rolling_quantile', or 'asls'."
        ),
    )
    baseline_order: int = Field(
        default=3,
        description="Polynomial order for 'polynomial' baseline.",
    )
    baseline_window: int = Field(
        default=51,
        description="Window size for rolling baseline methods.",
    )
    baseline_quantile: float = Field(
        default=0.1,
        description="Quantile for 'rolling_quantile' baseline (0–1).",
    )
    baseline_lam: float = Field(
        default=1e5,
        description="Smoothness parameter for 'asls' baseline.",
    )
    baseline_p: float = Field(
        default=0.001,
        description="Asymmetry parameter for 'asls' baseline.",
    )

    # ------------------------------------------------------------------
    # Smoothing
    # ------------------------------------------------------------------
    smoothing_method: str = Field(
        default="moving_average",
        description="Smoothing method: 'moving_average', 'gaussian', or 'savitzky_golay'.",
    )
    smoothing_window: int = Field(
        default=11,
        description="Window size for moving average / Savitzky–Golay.",
    )
    smoothing_sigma: float = Field(
        default=1.0,
        description="Sigma (points) for Gaussian smoothing.",
    )
    smoothing_polyorder: int = Field(
        default=3,
        description="Polynomial order for Savitzky–Golay smoothing.",
    )

    # ------------------------------------------------------------------
    # Normalization
    # ------------------------------------------------------------------
    normalization_method: str = Field(
        default="max",
        description="Normalization method: 'max', 'min_max', or 'area'.",
    )

    # ------------------------------------------------------------------
    # Peak detection
    # ------------------------------------------------------------------
    detect_peaks: bool = Field(
        default=True,
        description="Whether to perform peak detection.",
    )
    peak_method: str = Field(
        default="local_maxima",
        description="Peak detection method: currently 'local_maxima'.",
    )
    peak_height: float = Field(
        default=0.0,
        description="Absolute minimum peak height (in normalized units).",
    )
    peak_rel_height: float = Field(
        default=0.05,
        description="Relative minimum peak height (fraction of max).",
    )
    peak_min_prominence: float = Field(
        default=0.01,
        description="Minimum peak prominence.",
    )
    peak_width_rel_height: float = Field(
        default=0.5,
        description="Relative height for width estimation (e.g., 0.5 for FWHM).",
    )
    peak_refine: bool = Field(
        default=True,
        description="Whether to apply quadratic refinement to peak positions.",
    )

    # ------------------------------------------------------------------
    # Integration regions
    # ------------------------------------------------------------------
    integration_regions: List[Tuple[float, float]] = Field(
        default_factory=list,
        description="List of (x_min, x_max) regions for area integration.",
    )

    # ------------------------------------------------------------------
    # Extra metadata / options
    # ------------------------------------------------------------------
    extra_options: Dict[str, str] = Field(
        default_factory=dict,
        description="Additional UV-Vis-specific options (JSON-serializable).",
    )
