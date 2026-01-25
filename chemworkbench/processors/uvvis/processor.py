from __future__ import annotations

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


class UVVisProcessor:
    """UV-Vis processor implementing the universal processor protocol.

    Expects 1D spectral data (wavelength vs absorbance or similar).
    Integrates with the universal pipeline, math layer, and plotting engine.
    """

    name: str
    version: str
    technique: Technique = Technique.UV_VIS

    def __init__(self, name: str = "uvvis_processor", version: str = "1.0.0") -> None:
        self.name = name
        self.version = version

    # -------------------------------------------------------------------------
    # Required core method (called by the pipeline)
    # -------------------------------------------------------------------------
    def process(self, data: Any, config: BaseProcessorConfig) -> Any:
        """Core processing step.

        Assumes preprocessing has already produced a baseline-corrected,
        smoothed, normalized spectrum. Here we primarily compute peak-related
        outputs and integration results, and return a structured payload.
        """
        if not isinstance(config, UVVisConfig):
            raise TypeError("UVVisProcessor requires a UVVisConfig instance.")

        # Data at this stage should be the dict returned by preprocess()
        if not isinstance(data, dict):
            raise TypeError("UVVisProcessor.process expects a dict from preprocess().")

        x_arr = np.asarray(data["x"], dtype=float)
        y_arr = np.asarray(data["y"], dtype=float)

        # Peak detection (optional)
        peak_results_dict: Optional[Dict[str, Any]] = None
        if config.detect_peaks:
            peaks_result = detect_peaks(
                x_arr,
                y_arr,
                method=config.peak_method,
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

        # Integration (optional)
        integration_results: Dict[str, float] = {}
        if config.integration_regions:
            areas = integrate_regions(x_arr, y_arr, config.integration_regions)
            for (x_min, x_max), area in zip(config.integration_regions, areas, strict=False):
                key = f"region_{x_min:g}_{x_max:g}"
                integration_results[key] = float(area)

        # Merge with existing preprocessed payload so we keep baseline, etc.
        processed_payload: Dict[str, Any] = dict(data)
        processed_payload["peak_results"] = peak_results_dict
        processed_payload["integration_results"] = integration_results

        return processed_payload

    # -------------------------------------------------------------------------
    # Optional hooks used by the pipeline
    # -------------------------------------------------------------------------
    def load(self, data: Any, config: BaseProcessorConfig) -> Any:
        """Load step.

        For now, this is a simple pass-through. In the future, this could
        handle file paths, data frames, or other raw formats.
        """
        return data

    def validate(self, data: Any, config: BaseProcessorConfig) -> Any:
        """Validate the input data structure."""
        x_arr, y_arr = self._extract_xy(data)
        if x_arr.size == 0 or y_arr.size == 0:
            raise ValueError("UV-Vis data must contain non-empty x and y arrays.")
        if x_arr.shape != y_arr.shape:
            raise ValueError("UV-Vis x and y arrays must have the same shape.")
        # Preserve raw arrays in a dict for downstream steps
        return {"x_raw": x_arr, "y_raw": y_arr}

    def preprocess(self, data: Any, config: BaseProcessorConfig) -> Any:
        """Apply baseline correction, smoothing, and normalization."""
        if not isinstance(config, UVVisConfig):
            raise TypeError("UVVisProcessor requires a UVVisConfig instance.")

        if isinstance(data, dict) and "x_raw" in data and "y_raw" in data:
            x_arr = np.asarray(data["x_raw"], dtype=float)
            y_arr = np.asarray(data["y_raw"], dtype=float)
        else:
            x_arr, y_arr = self._extract_xy(data)

        # Keep a copy of the raw signal
        y_raw = y_arr.copy()

        # Baseline correction
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
        """Optional postprocessing step.

        For now, this is a pass-through. It could be used for
        additional filtering or feature engineering.
        """
        return data

    def build_metadata(self, data: Any, config: BaseProcessorConfig) -> Dict[str, Any]:
        """Build technique-specific metadata for ProcessedData.metadata."""
        if isinstance(data, dict) and "x" in data:
            x_arr = np.asarray(data["x"], dtype=float)
        else:
            x_arr, _ = self._extract_xy(data)

        meta: Dict[str, Any] = {
            "n_points": int(x_arr.size),
            "x_min": float(x_arr.min()) if x_arr.size > 0 else None,
            "x_max": float(x_arr.max()) if x_arr.size > 0 else None,
            "config": config.model_dump(),
        }

        integration = data.get("integration_results") if isinstance(data, dict) else None
        if isinstance(integration, dict) and integration:
            meta["integration_regions"] = list(integration.keys())

        return meta

    def compute_qc(self, data: Any, config: BaseProcessorConfig) -> Dict[str, QCMetric]:
        """Compute quality-control metrics for ProcessedData.qc."""
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
                description="Maximum absolute signal value after preprocessing.",
            )
            qc["rms_signal"] = QCMetric(
                name="rms_signal",
                value=rms,
                description="Root-mean-square of the processed signal.",
            )

        return qc

    def make_plots(
        self,
        data: Any,
        config: BaseProcessorConfig,
    ) -> List[PlotConfig]:
        """Generate PlotConfig objects for the processed UV-Vis data."""
        if isinstance(data, dict) and "x" in data and "y" in data:
            x_arr = np.asarray(data["x"], dtype=float)
            y_arr = np.asarray(data["y"], dtype=float)
            baseline_arr = (
                np.asarray(data["baseline"], dtype=float)
                if "baseline" in data
                else None
            )
            y_raw = (
                np.asarray(data["y_raw"], dtype=float)
                if "y_raw" in data
                else None
            )
        else:
            x_arr, y_arr = self._extract_xy(data)
            baseline_arr = None
            y_raw = None

        layers: List[PlotLayerConfig] = []

        # Raw layer (if available)
        if y_raw is not None:
            layers.append(
                PlotLayerConfig(
                    label="raw",
                    plot_type=PlotType.LINE,
                    x=x_arr.tolist(),
                    y=y_raw.tolist(),
                    color="gray",
                    linewidth=1.0,
                    alpha=0.5,
                )
            )

        # Processed layer
        layers.append(
            PlotLayerConfig(
                label="processed",
                plot_type=PlotType.LINE,
                x=x_arr.tolist(),
                y=y_arr.tolist(),
                color="blue",
                linewidth=1.5,
            )
        )

        # Baseline layer (if available)
        if baseline_arr is not None:
            layers.append(
                PlotLayerConfig(
                    label="baseline",
                    plot_type=PlotType.LINE,
                    x=x_arr.tolist(),
                    y=baseline_arr.tolist(),
                    color="red",
                    linewidth=1.0,
                    linestyle="--",
                )
            )

        plot = PlotConfig(
            id="uvvis_main",
            title="UV-Vis Spectrum",
            x_label="Wavelength",
            y_label="Intensity (normalized)",
            backend=PlotBackend.MATPLOTLIB,
            show_legend=True,
            show_grid=True,
            x_scale="linear",
            y_scale="linear",
            layers=layers,
            layout={},
        )

        return [plot]

    def export(self, data: Any, config: BaseProcessorConfig) -> None:
        """Optional export step.

        Placeholder for writing processed results to disk or other targets.
        """
        return None

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------
    @staticmethod
    def _extract_xy(data: Any) -> Tuple[np.ndarray, np.ndarray]:
        """Extract x and y arrays from various possible input formats.

        Supported formats:
        - dict with keys 'x' and 'y'
        - dict with keys 'wavelength' and 'absorbance'
        - tuple/list of (x, y)
        """
        if isinstance(data, dict):
            if "x" in data and "y" in data:
                x = data["x"]
                y = data["y"]
            elif "wavelength" in data and "absorbance" in data:
                x = data["wavelength"]
                y = data["absorbance"]
            else:
                raise ValueError("Unsupported dict format for UV-Vis data.")
        elif isinstance(data, (list, tuple)) and len(data) == 2:
            x, y = data
        else:
            raise TypeError("UV-Vis data must be a dict or (x, y) tuple.")

        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)
        return x_arr, y_arr

    @staticmethod
    def _peak_result_to_dict(result: Any) -> Optional[Dict[str, Any]]:
        """Convert PeakDetectionResult to a JSON-serializable dict."""
        if result is None:
            return None

        indices = result.indices.tolist()
        x = result.x.tolist()
        y = result.y.tolist()
        prominence = (
            result.prominence.tolist() if result.prominence is not None else None
        )
        width = result.width.tolist() if result.width is not None else None
        refined_x = (
            result.refined_x.tolist() if result.refined_x is not None else None
        )
        refined_y = (
            result.refined_y.tolist() if result.refined_y is not None else None
        )

        return {
            "indices": indices,
            "x": x,
            "y": y,
            "prominence": prominence,
            "width": width,
            "refined_x": refined_x,
            "refined_y": refined_y,
            "metadata": result.metadata,
        }
