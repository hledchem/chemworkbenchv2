from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from chemworkbench.core.models import (
    BaseProcessorConfig,
    PlotConfig,
    Technique,
)
from chemworkbench.utils.math_spectral import (
    baseline,
    detect_peaks,
    integrate_regions,
    normalize,
    smooth,
)
from .config import UVVisConfig


# -------------------------------------------------------------------------
# Minimal internal stubs for QC + Plot layers (v2.1 placeholder)
# -------------------------------------------------------------------------

@dataclass
class QCMetric:
    name: str
    value: float
    description: str = ""


@dataclass
class PlotLayerConfig:
    label: str
    plot_type: str
    x: Optional[List[float]] = None
    y: Optional[List[float]] = None
    color: Optional[str] = None
    linewidth: Optional[float] = None
    alpha: Optional[float] = None
    style: Dict[str, Any] = field(default_factory=dict)


class PlotType:
    LINE = "line"


# -------------------------------------------------------------------------
# UV-Vis Processor
# -------------------------------------------------------------------------

class UVVisProcessor:
    """UV-Vis processor implementing the universal processor protocol."""

    name: str
    version: str
    technique: Technique = Technique.UVVIS

    def __init__(self, name: str = "uvvis_processor", version: str = "1.0.0") -> None:
        self.name = name
        self.version = version

    # ---------------------------------------------------------------------
    # Core processing step
    # ---------------------------------------------------------------------
    def process(self, data: Any, config: BaseProcessorConfig) -> Any:
        if not isinstance(config, UVVisConfig):
            raise TypeError("UVVisProcessor requires a UVVisConfig instance.")

        if not isinstance(data, dict):
            raise TypeError("UVVisProcessor.process expects a dict from preprocess().")

        x_arr = np.asarray(data["x"], dtype=float)
        y_arr = np.asarray(data["y"], dtype=float)

        # Peak detection
        peak_results_dict: Optional[Dict[str, Any]] = None
        if config.detect_peaks:
            method = config.peak_method.lower()
            peaks_result = detect_peaks(
                x_arr,
                y_arr,
                method=method,
                height=config.peak_height,
                rel_height=config.peak_rel_height,
                min_prominence=config.peak_min_prominence,
                estimate_width=True,
                width_rel_height=config.peak_width_rel_height,
                x_min=None,
                x_max=None,
                refine=config.peak_refine,
                derivative=False,
            )
            peak_results_dict = self._peak_result_to_dict(peaks_result)

        # Integration
        integration_results: Dict[str, float] = {}
        if config.integration_regions:
            areas = integrate_regions(x_arr, y_arr, config.integration_regions)
            for (x_min, x_max), area in zip(config.integration_regions, areas, strict=False):
                key = f"region_{x_min:g}_{x_max:g}"
                integration_results[key] = float(area)

        processed_payload = dict(data)
        processed_payload["peak_results"] = peak_results_dict
        processed_payload["integration_results"] = integration_results

        return processed_payload

    # ---------------------------------------------------------------------
    # Pipeline hooks
    # ---------------------------------------------------------------------
    def load(self, data: Any, config: BaseProcessorConfig) -> Any:
        return data

    def validate(self, data: Any, config: BaseProcessorConfig) -> Any:
        x_arr, y_arr = self._extract_xy(data)
        if x_arr.size == 0 or y_arr.size == 0:
            raise ValueError("UV-Vis data must contain non-empty x and y arrays.")
        if x_arr.shape != y_arr.shape:
            raise ValueError("UV-Vis x and y arrays must have the same shape.")
        return {"x_raw": x_arr, "y_raw": y_arr}

    def preprocess(self, data: Any, config: BaseProcessorConfig) -> Any:
        if not isinstance(config, UVVisConfig):
            raise TypeError("UVVisProcessor requires a UVVisConfig instance.")

        if isinstance(data, dict) and "x_raw" in data:
            x_arr = np.asarray(data["x_raw"], dtype=float)
            y_arr = np.asarray(data["y_raw"], dtype=float)
        else:
            x_arr, y_arr = self._extract_xy(data)

        y_raw = y_arr.copy()

        # Baseline
        baseline_kwargs: Dict[str, Any] = {}
        if config.baseline_method == "polynomial":
            baseline_kwargs["order"] = config.baseline_order
        elif config.baseline_method in {"rolling_min", "rolling_quantile"}:
            baseline_kwargs["window"] = config.baseline_window
            if config.baseline_method == "rolling_quantile":
                baseline_kwargs["quantile"] = config.baseline_quantile
        elif config.baseline_method == "asls":
            baseline_kwargs["lam"] = config.baseline_lam
            baseline_kwargs["p"] = config.baseline_p

        _, baseline_arr = baseline(
            x_arr,
            y_arr,
            method=config.baseline_method,
            **baseline_kwargs,
        )
        y_corrected = y_arr - baseline_arr

        # Smoothing
        smooth_kwargs: Dict[str, Any] = {}
        if config.smoothing_method == "moving_average":
            smooth_kwargs["window"] = config.smoothing_window
        elif config.smoothing_method == "gaussian":
            smooth_kwargs["sigma"] = config.smoothing_sigma
        elif config.smoothing_method == "savitzky_golay":
            smooth_kwargs["window"] = config.smoothing_window
            smooth_kwargs["polyorder"] = config.smoothing_polyorder

        _, y_smooth = smooth(
            x_arr,
            y_corrected,
            method=config.smoothing_method,
            **smooth_kwargs,
        )

        # Normalization
        _, y_norm = normalize(
            x_arr,
            y_smooth,
            method=config.normalization_method,
        )

        return {
            "x": x_arr,
            "y": y_norm,
            "x_raw": x_arr,
            "y_raw": y_raw,
            "baseline": baseline_arr,
            "y_corrected": y_corrected,
            "y_smooth": y_smooth,
        }

    def postprocess(self, data: Any, config: BaseProcessorConfig) -> Any:
        return data

    def build_metadata(self, data: Any, config: BaseProcessorConfig) -> Dict[str, Any]:
        if isinstance(data, dict) and "x" in data:
            x_arr = np.asarray(data["x"], dtype=float)
        else:
            x_arr, _ = self._extract_xy(data)

        meta: Dict[str, Any] = {
            "n_points": int(x_arr.size),
            "x_min": float(x_arr.min()) if x_arr.size > 0 else None,
            "x_max": float(x_arr.max()) if x_arr.size > 0 else None,
            "config": config.model_dump() if hasattr(config, "model_dump") else dict(config),
        }

        integration = data.get("integration_results") if isinstance(data, dict) else None
        if isinstance(integration, dict) and integration:
            meta["integration_regions"] = list(integration.keys())

        return meta

    def compute_qc(self, data: Any, config: BaseProcessorConfig) -> Dict[str, QCMetric]:
        if isinstance(data, dict) and "y" in data:
            y_arr = np.asarray(data["y"], dtype=float)
        else:
            _, y_arr = self._extract_xy(data)

        qc: Dict[str, QCMetric] = {}

        if y_arr.size > 0:
            max_val = float(np.max(np.abs(y_arr)))
            rms = float(np.sqrt(np.mean(y_arr**2)))
            qc["max_abs_signal"] = QCMetric(
                name="max_abs_signal",
                value=max_val,
                description="Maximum absolute signal value.",
            )
            qc["rms_signal"] = QCMetric(
                name="rms_signal",
                value=rms,
                description="Root-mean-square of the signal.",
            )

        return qc

    # ---------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------
    def _extract_xy(self, data: Any) -> Tuple[np.ndarray, np.ndarray]:
        if isinstance(data, dict) and "x" in data and "y" in data:
            return np.asarray(data["x"], dtype=float), np.asarray(data["y"], dtype=float)
        raise TypeError("Data must contain 'x' and 'y' arrays.")

    def _peak_result_to_dict(self, peaks_result: Any) -> Dict[str, Any]:
        """
        Convert PeakDetectionResult into a simple dict for downstream use.
        This is v2.1-native: we just expose whatever attributes the result has.
        """
        if peaks_result is None:
            return {}

        out: Dict[str, Any] = {}
        for attr in ("indices", "x", "y", "prominence", "width", "refined_x", "refined_y"):
            if hasattr(peaks_result, attr):
                value = getattr(peaks_result, attr)
                out[attr] = value.tolist() if hasattr(value, "tolist") else value

        return out
