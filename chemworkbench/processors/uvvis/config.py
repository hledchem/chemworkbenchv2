from pydantic import BaseModel, Field
from typing import List, Tuple, Optional


class UVVisConfig(BaseModel):
    # Peak detection
    detect_peaks: bool = Field(default=True)
    peak_method: str = Field(default="local_maxima")   # v2.1 correct
    peak_height: Optional[float] = Field(default=None)
    peak_rel_height: float = Field(default=0.05)
    peak_min_prominence: float = Field(default=0.01)
    peak_width_rel_height: float = Field(default=0.5)
    peak_refine: bool = Field(default=True)

    # Integration
    integration_regions: Optional[List[Tuple[float, float]]] = Field(default=None)

    # Baseline correction
    baseline_method: str = Field(default="polynomial")
    baseline_order: int = Field(default=3)
    baseline_window: int = Field(default=51)
    baseline_quantile: float = Field(default=0.1)
    baseline_lam: float = Field(default=1e5)
    baseline_p: float = Field(default=0.001)

    # Smoothing
    smoothing_method: str = Field(default="moving_average")
    smoothing_window: int = Field(default=11)
    smoothing_sigma: float = Field(default=1.0)
    smoothing_polyorder: int = Field(default=3)

    # Normalization
    normalization_method: str = Field(default="max")
