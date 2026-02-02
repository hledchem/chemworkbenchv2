"""
UV‑Vis Configuration (ChemWorkBench v2.2)
=========================================

High‑level purpose
------------------
This module defines the configuration model for the UV‑Vis processor.
It uses Pydantic for validation and UI‑friendliness, and is designed to
be **future‑proof**, **LLM‑friendly**, and **extensible**.

The configuration describes *what scientific operations are allowed*,
not *how they are implemented*. The processor decides how to interpret
these toggles.

LLM‑oriented description
------------------------
If you are an AI model reading or modifying this configuration, here is
how to reason about it:

1. **This config does not perform any processing itself.**
   It only declares user‑controllable options that the UV‑Vis processor
   *may* use.

2. **Every field is optional for the processor.**
   The processor may ignore fields that are not relevant to the current
   workflow (e.g., raw plotting).

3. **Fields are grouped by scientific purpose:**
   - Peak detection
   - Integration
   - Baseline correction
   - Smoothing
   - Normalization

4. **The config is intentionally verbose and future‑proof.**
   Even if the processor currently performs only raw plotting, these
   fields allow future versions to enable advanced UV‑Vis workflows
   without changing the config schema.

5. **Safe for UI exposure.**
   A UI can directly expose these fields as toggles, dropdowns, or
   numeric inputs.

6. **Safe for LLM modification.**
   An AI agent can:
       - enable/disable features
       - change methods (e.g., smoothing_method="savitzky_golay")
       - adjust parameters
   without breaking the processor.

7. **No field is required for basic operation.**
   The processor can run with all defaults and simply plot raw data.

Public API
----------
- `UVVisConfig`: Pydantic model containing all UV‑Vis processing options.

Usage
-----
The processor typically loads this config as:

    from .config import UVVisConfig
    config = UVVisConfig()

The processor may choose to use only a subset of fields depending on
the workflow (single scan, overlay, comparison, etc.).
"""

from pydantic import BaseModel, Field
from typing import List, Tuple, Optional


class UVVisConfig(BaseModel):
    """
    Full UV‑Vis configuration model for ChemWorkBench v2.2.

    This model is intentionally comprehensive and future‑proof. The
    processor may ignore fields that are not relevant to the current
    workflow (e.g., raw plotting).
    """

    # ================================================================
    # Peak Detection
    # ================================================================
    detect_peaks: bool = Field(
        default=True,
        description="Enable peak detection (λmax, local maxima, etc.)."
    )
    peak_method: str = Field(
        default="local_maxima",
        description="Peak detection algorithm (e.g., local_maxima, scipy_find_peaks)."
    )
    peak_height: Optional[float] = Field(
        default=None,
        description="Absolute minimum peak height required to count as a peak."
    )
    peak_rel_height: float = Field(
        default=0.05,
        description="Relative height threshold (fraction of max absorbance)."
    )
    peak_min_prominence: float = Field(
        default=0.01,
        description="Minimum prominence for peak detection."
    )
    peak_width_rel_height: float = Field(
        default=0.5,
        description="Relative width threshold for peak detection."
    )
    peak_refine: bool = Field(
        default=True,
        description="Enable sub‑pixel refinement of peak positions."
    )

    # ================================================================
    # Integration
    # ================================================================
    integration_regions: Optional[List[Tuple[float, float]]] = Field(
        default=None,
        description="List of (start_nm, end_nm) wavelength regions to integrate."
    )

    # ================================================================
    # Baseline Correction
    # ================================================================
    baseline_method: str = Field(
        default="polynomial",
        description="Baseline correction method (polynomial, als, quantile, none)."
    )
    baseline_order: int = Field(
        default=3,
        description="Polynomial order for baseline fitting."
    )
    baseline_window: int = Field(
        default=51,
        description="Window size for rolling/quantile baseline methods."
    )
    baseline_quantile: float = Field(
        default=0.1,
        description="Quantile used for quantile baseline estimation."
    )
    baseline_lam: float = Field(
        default=1e5,
        description="Lambda parameter for ALS baseline correction."
    )
    baseline_p: float = Field(
        default=0.001,
        description="Asymmetry parameter for ALS baseline correction."
    )

    # ================================================================
    # Smoothing
    # ================================================================
    smoothing_method: str = Field(
        default="moving_average",
        description="Smoothing method (moving_average, savgol, gaussian)."
    )
    smoothing_window: int = Field(
        default=11,
        description="Window size for smoothing operations."
    )
    smoothing_sigma: float = Field(
        default=1.0,
        description="Sigma for Gaussian smoothing."
    )
    smoothing_polyorder: int = Field(
        default=3,
        description="Polynomial order for Savitzky‑Golay smoothing."
    )

    # ================================================================
    # Normalization
    # ================================================================
    normalization_method: str = Field(
        default="max",
        description="Normalization method (max, area, vector, none)."
    )
