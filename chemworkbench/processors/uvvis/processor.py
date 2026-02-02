"""
UV‑Vis Processor (ChemWorkBench v2.2, Block‑Based)
==================================================

High‑level purpose
------------------
This module implements a **block‑based, MNova‑style UV‑Vis processor**
for ChemWorkBench v2.2. It takes a `RawDataBundle` (one or more scans)
and produces a `ProcessedData` object with:

    • processed spectra
    • plots (single, overlay, difference)
    • metadata (λmax, areas, shifts, etc.)
    • QC hooks (currently minimal, extensible)

All scientific operations are organized into **processing blocks** that
are:

    • toggleable (via UVVisConfig)
    • ordered
    • modular
    • easy to extend

LLM‑oriented description
------------------------
If you are an AI model reading or modifying this file, here is how to
reason about it:

1. Input: `RawDataBundle`
   - `raw.scans` is a list of Scan objects.
   - Each Scan has:
       • `x`: wavelength array (nm)
       • `y`: absorbance array (AU)
       • `label`: optional string

2. Output: `ProcessedData`
   - `payload`: machine‑readable flags and intermediate results
   - `metadata`: human‑interpretable metrics (λmax, areas, shifts, etc.)
   - `qc`: quality control info (currently minimal)
   - `plots`: list of `PlotConfig` objects

3. Processing model:
   - For each scan, we run a **single‑scan pipeline**:
       1. Baseline correction
       2. Smoothing
       3. Normalization
       4. Peak detection
       5. Integration
       6. Single‑scan metrics
       7. Single‑scan plot
   - For multiple scans, we additionally run **multi‑scan blocks**:
       8. Overlay plot
       9. Difference spectrum (last − first)
       10. Multi‑scan metrics (λmax shift, ΔAbs)

4. Configuration:
   - All behavior is controlled by `UVVisConfig` (see config.py).
   - The processor reads:
       • baseline_method, baseline_order, baseline_window, baseline_quantile,
         baseline_lam, baseline_p
       • smoothing_method, smoothing_window, smoothing_sigma, smoothing_polyorder
       • normalization_method
       • detect_peaks, peak_* fields
       • integration_regions
   - The processor may ignore fields that are not relevant to a given
     workflow, but the schema is designed to be future‑proof.

5. Extension points:
   - You can safely:
       • add new blocks
       • add new methods to existing blocks
       • add new metadata fields
       • add new QC checks
   - As long as:
       • `process()` still returns `ProcessedData`
       • blocks remain deterministic and documented

Public API
----------
- `UVVisProcessor`: main processor class used by ProcessorRouter.
"""

from __future__ import annotations

from typing import List, Dict, Any, Tuple, Optional

import numpy as np
from scipy.signal import savgol_filter

from chemworkbench.core.models import (
    RawDataBundle,
    ProcessedData,
    PlotConfig,
)
from chemworkbench.processors.base_processor import BaseProcessor
from .config import UVVisConfig


class UVVisProcessor(BaseProcessor):
    """
    Block‑based UV‑Vis processor.

    Responsibilities
    ----------------
    • Run a configurable pipeline of processing blocks on each scan.
    • Support single‑scan and multi‑scan workflows.
    • Produce plots and metadata suitable for scientific interpretation.

    Non‑Responsibilities
    --------------------
    • File I/O
    • Structural format detection
    • Technique detection
    • Loader logic
    """

    # ==================================================================
    # Public entry point
    # ==================================================================

    def process(self, raw: RawDataBundle) -> ProcessedData:
        """
        Main entry point.

        Behavior:
        ---------
        • If there is exactly one scan:
            → run single‑scan pipeline and return its result.
        • If there are multiple scans:
            → run single‑scan pipeline on each scan
            → build overlay plot
            → optionally compute difference spectrum and multi‑scan metrics.
        """
        config = UVVisConfig()  # future: inject from user/session

        scans = raw.scans
        n = len(scans)

        if n == 0:
            return ProcessedData(payload={}, metadata={}, qc={}, plots=[])

        if n == 1:
            return self._process_single(scans[0], config)

        return self._process_multi(scans, config)

    # ==================================================================
    # Single‑scan pipeline
    # ==================================================================

    def _process_single(self, scan, config: UVVisConfig) -> ProcessedData:
        """
        Process a single UV‑Vis scan through the block pipeline.
        """
        x = np.array(scan.x, dtype=float)
        y = np.array(scan.y, dtype=float)

        metadata: Dict[str, Any] = {}
        payload: Dict[str, Any] = {}
        qc: Dict[str, Any] = {}
        plots: List[PlotConfig] = []

        # Define the ordered block pipeline
        blocks = [
            ("baseline", self._block_baseline),
            ("smoothing", self._block_smoothing),
            ("normalization", self._block_normalization),
            ("peak_detection", self._block_peak_detection),
            ("integration", self._block_integration),
            ("metrics", self._block_single_metrics),
        ]

        # Execute blocks in order
        for name, func in blocks:
            x, y, meta, pay = func(x, y, config)
            metadata.update(meta)
            payload.update(pay)

        # Final plot (processed spectrum)
        plots.append(
            PlotConfig(
                title=scan.label or "UV‑Vis Spectrum",
                x=x.tolist(),
                y=y.tolist(),
                xlabel="Wavelength (nm)",
                ylabel="Absorbance (AU)",
                style="line",
            )
        )

        return ProcessedData(
            payload=payload,
            metadata=metadata,
            qc=qc,
            plots=plots,
        )

    # ==================================================================
    # Multi‑scan pipeline
    # ==================================================================

    def _process_multi(self, scans, config: UVVisConfig) -> ProcessedData:
        """
        Process multiple scans:

        • Run single‑scan pipeline on each scan.
        • Build overlay plot.
        • Optionally compute difference spectrum (last − first).
        • Optionally compute multi‑scan metrics (λmax shift, ΔAbs).
        """
        payload: Dict[str, Any] = {"mode": "multi"}
        metadata: Dict[str, Any] = {}
        qc: Dict[str, Any] = {}
        plots: List[PlotConfig] = []

        processed_scans: List[ProcessedData] = []

        # Process each scan individually
        for scan in scans:
            processed = self._process_single(scan, config)
            processed_scans.append(processed)

        # Build overlay plot
        overlay = self._block_overlay(scans, processed_scans)
        plots.append(overlay)

        # Difference spectrum (last − first)
        diff_plot, diff_meta = self._block_difference(processed_scans)
        if diff_plot is not None:
            plots.append(diff_plot)
        metadata.update(diff_meta)

        # Multi‑scan metrics (λmax shift, ΔAbs)
        multi_meta = self._block_multi_metrics(processed_scans)
        metadata.update(multi_meta)

        return ProcessedData(
            payload=payload,
            metadata=metadata,
            qc=qc,
            plots=plots,
        )

    # ==================================================================
    # Blocks: Baseline
    # ==================================================================

    def _block_baseline(
        self, x: np.ndarray, y: np.ndarray, config: UVVisConfig
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any], Dict[str, Any]]:
        meta: Dict[str, Any] = {}
        payload: Dict[str, Any] = {}

        method = config.baseline_method.lower()
        if method in ("none", "", "off"):
            return x, y, meta, payload

        if method == "polynomial":
            order = max(1, config.baseline_order)
            coeffs = np.polyfit(x, y, order)
            baseline = np.polyval(coeffs, x)
            y = y - baseline
            meta["baseline_method"] = "polynomial"
            meta["baseline_order"] = order

        elif method == "quantile":
            window = max(3, config.baseline_window)
            q = config.baseline_quantile
            baseline = self._rolling_quantile(y, window, q)
            y = y - baseline
            meta["baseline_method"] = "quantile"
            meta["baseline_window"] = window
            meta["baseline_quantile"] = q

        elif method == "als":
            lam = config.baseline_lam
            p = config.baseline_p
            baseline = self._als_baseline(y, lam=lam, p=p)
            y = y - baseline
            meta["baseline_method"] = "als"
            meta["baseline_lam"] = lam
            meta["baseline_p"] = p

        # Future: rubberband, spline, etc.

        payload["baseline_applied"] = True
        return x, y, meta, payload

    # ==================================================================
    # Blocks: Smoothing
    # ==================================================================

    def _block_smoothing(
        self, x: np.ndarray, y: np.ndarray, config: UVVisConfig
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any], Dict[str, Any]]:
        meta: Dict[str, Any] = {}
        payload: Dict[str, Any] = {}

        method = config.smoothing_method.lower()
        if method in ("none", "", "off"):
            return x, y, meta, payload

        window = max(3, config.smoothing_window)
        if window % 2 == 0:
            window += 1  # ensure odd window for some methods

        if method == "moving_average":
            kernel = np.ones(window) / window
            y = np.convolve(y, kernel, mode="same")
            meta["smoothing_method"] = "moving_average"
            meta["smoothing_window"] = window

        elif method == "savgol":
            polyorder = min(config.smoothing_polyorder, window - 1)
            y = savgol_filter(y, window_length=window, polyorder=polyorder)
            meta["smoothing_method"] = "savgol"
            meta["smoothing_window"] = window
            meta["smoothing_polyorder"] = polyorder

        elif method == "gaussian":
            # simple Gaussian convolution
            sigma = max(1e-6, config.smoothing_sigma)
            # approximate kernel size as 6*sigma
            k = int(6 * sigma)
            if k % 2 == 0:
                k += 1
            xs = np.linspace(-3 * sigma, 3 * sigma, k)
            kernel = np.exp(-0.5 * (xs / sigma) ** 2)
            kernel /= kernel.sum()
            y = np.convolve(y, kernel, mode="same")
            meta["smoothing_method"] = "gaussian"
            meta["smoothing_sigma"] = sigma

        payload["smoothing_applied"] = True
        return x, y, meta, payload

    # ==================================================================
    # Blocks: Normalization
    # ==================================================================

    def _block_normalization(
        self, x: np.ndarray, y: np.ndarray, config: UVVisConfig
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any], Dict[str, Any]]:
        meta: Dict[str, Any] = {}
        payload: Dict[str, Any] = {}

        method = config.normalization_method.lower()
        if method in ("none", "", "off"):
            return x, y, meta, payload

        if method == "max":
            max_val = float(np.max(np.abs(y))) or 1.0
            y = y / max_val
            meta["normalization_method"] = "max"
            meta["normalization_factor"] = max_val

        elif method == "area":
            area = float(np.trapz(y, x)) or 1.0
            y = y / area
            meta["normalization_method"] = "area"
            meta["normalization_factor"] = area

        elif method == "vector":
            norm = float(np.linalg.norm(y)) or 1.0
            y = y / norm
            meta["normalization_method"] = "vector"
            meta["normalization_factor"] = norm

        payload["normalization_applied"] = True
        return x, y, meta, payload

    # ==================================================================
    # Blocks: Peak Detection
    # ==================================================================

    def _block_peak_detection(
        self, x: np.ndarray, y: np.ndarray, config: UVVisConfig
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any], Dict[str, Any]]:
        meta: Dict[str, Any] = {}
        payload: Dict[str, Any] = {}

        if not config.detect_peaks:
            return x, y, meta, payload

        # For now, implement a simple λmax + local maxima detection.
        # Future: use scipy.signal.find_peaks with full parameterization.
        idx_max = int(np.argmax(y))
        lambda_max = float(x[idx_max])
        abs_max = float(y[idx_max])

        meta["lambda_max"] = lambda_max
        meta["abs_max"] = abs_max
        meta["peak_method"] = config.peak_method

        payload["peaks_detected"] = True
        return x, y, meta, payload

    # ==================================================================
    # Blocks: Integration
    # ==================================================================

    def _block_integration(
        self, x: np.ndarray, y: np.ndarray, config: UVVisConfig
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any], Dict[str, Any]]:
        meta: Dict[str, Any] = {}
        payload: Dict[str, Any] = {}

        regions = config.integration_regions
        if not regions:
            return x, y, meta, payload

        areas: List[Dict[str, float]] = []
        for (start_nm, end_nm) in regions:
            mask = (x >= start_nm) & (x <= end_nm)
            if not np.any(mask):
                continue
            area = float(np.trapz(y[mask], x[mask]))
            areas.append(
                {"start_nm": float(start_nm), "end_nm": float(end_nm), "area": area}
            )

        if areas:
            meta["integration_regions"] = areas
            payload["integration_applied"] = True

        return x, y, meta, payload

    # ==================================================================
    # Blocks: Single‑scan Metrics
    # ==================================================================

    def _block_single_metrics(
        self, x: np.ndarray, y: np.ndarray, config: UVVisConfig
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any], Dict[str, Any]]:
        meta: Dict[str, Any] = {}
        payload: Dict[str, Any] = {}

        # Example: store basic stats
        meta["y_min"] = float(np.min(y))
        meta["y_max"] = float(np.max(y))
        meta["y_mean"] = float(np.mean(y))

        return x, y, meta, payload

    # ==================================================================
    # Blocks: Overlay (multi‑scan)
    # ==================================================================

    def _block_overlay(
        self,
        scans,
        processed_scans: List[ProcessedData],
    ) -> PlotConfig:
        overlay = PlotConfig(
            title="UV‑Vis Overlay",
            xlabel="Wavelength (nm)",
            ylabel="Absorbance (AU)",
            style="line",
            layers=[],
        )

        for idx, (scan, proc) in enumerate(zip(scans, processed_scans), start=1):
            if not proc.plots:
                continue
            p = proc.plots[0]
            overlay.layers.append(
                {
                    "x": p.x,
                    "y": p.y,
                    "label": scan.label or f"Scan {idx}",
                }
            )

        return overlay

    # ==================================================================
    # Blocks: Difference Spectrum (multi‑scan)
    # ==================================================================

    def _block_difference(
        self,
        processed_scans: List[ProcessedData],
    ) -> Tuple[Optional[PlotConfig], Dict[str, Any]]:
        meta: Dict[str, Any] = {}

        if len(processed_scans) < 2:
            return None, meta

        first = processed_scans[0].plots[0]
        last = processed_scans[-1].plots[0]

        x = np.array(first.x, dtype=float)
        y1 = np.array(first.y, dtype=float)
        y2 = np.array(last.y, dtype=float)

        if len(x) != len(y1) or len(y1) != len(y2):
            # For now, require same grid; future: interpolate.
            return None, meta

        diff = (y2 - y1).tolist()

        plot = PlotConfig(
            title="Difference Spectrum (Last − First)",
            x=x.tolist(),
            y=diff,
            xlabel="Wavelength (nm)",
            ylabel="ΔAbsorbance (AU)",
            style="line",
        )

        return plot, meta

    # ==================================================================
    # Blocks: Multi‑scan Metrics
    # ==================================================================

    def _block_multi_metrics(
        self,
        processed_scans: List[ProcessedData],
    ) -> Dict[str, Any]:
        meta: Dict[str, Any] = {}

        if len(processed_scans) < 2:
            return meta

        first_meta = processed_scans[0].metadata
        last_meta = processed_scans[-1].metadata

        if "lambda_max" in first_meta and "lambda_max" in last_meta:
            meta["lambda_max_shift"] = (
                last_meta["lambda_max"] - first_meta["lambda_max"]
            )

        if "abs_max" in first_meta and "abs_max" in last_meta:
            meta["delta_abs_max"] = (
                last_meta["abs_max"] - first_meta["abs_max"]
            )

        return meta

    # ==================================================================
    # Helper: Rolling Quantile Baseline
    # ==================================================================

    def _rolling_quantile(
        self, y: np.ndarray, window: int, q: float
    ) -> np.ndarray:
        """
        Simple rolling quantile baseline.

        Notes:
        ------
        • This is a straightforward implementation; for large datasets,
          a more efficient method may be desirable.
        """
        n = len(y)
        half = window // 2
        baseline = np.zeros_like(y)
        for i in range(n):
            start = max(0, i - half)
            end = min(n, i + half + 1)
            baseline[i] = np.quantile(y[start:end], q)
        return baseline

    # ==================================================================
    # Helper: ALS Baseline
    # ==================================================================

    def _als_baseline(
        self, y: np.ndarray, lam: float = 1e5, p: float = 0.001, niter: int = 10
    ) -> np.ndarray:
        """
        Asymmetric Least Squares (ALS) baseline correction.

        This is a standard algorithm used in spectroscopy for smooth
        baseline estimation.

        Parameters
        ----------
        y : np.ndarray
            Input signal.
        lam : float
            Smoothness parameter.
        p : float
            Asymmetry parameter.
        niter : int
            Number of iterations.

        Returns
        -------
        baseline : np.ndarray
        """
        L = len(y)
        D = np.diff(np.eye(L), 2)
        DTD = lam * (D.T @ D)
        w = np.ones(L)
        for _ in range(niter):
            W = np.diag(w)
            Z = W + DTD
            z = np.linalg.solve(Z, w * y)
            w = p * (y > z) + (1 - p) * (y < z)
        return z
