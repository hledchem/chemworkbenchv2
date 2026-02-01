"""
UV‑Vis Processor (ChemWorkBench v2.2)
=====================================

High‑level role
---------------
This module implements the **UV‑Vis technique processor** for ChemWorkBench v2.2.

It is responsible for taking **already‑loaded, structurally normalized data**
(`RawDataBundle`) and performing **technique‑specific UV‑Vis operations** to
produce a `ProcessedData` object that is ready for:

- scientific interpretation
- plotting
- comparison between spectra
- downstream automation (e.g., reporting, batch analysis)

This processor is intentionally **narrow in scope but high in leverage**:
it focuses on the core UV‑Vis workflows that are widely supported in
publicly available UV‑Vis software (Agilent Cary, Shimadzu UVProbe,
Thermo Insight, OceanView, etc.):

    • Single‑scan spectrum processing
    • Overlay of multiple spectra
    • Simple comparison between spectra (λmax shift, ΔAbs)

It does **not** attempt to implement advanced analytics (PCA, kinetics
engines, chemometrics, spectral libraries, etc.). Those can be layered
on later as separate processors or higher‑level analysis modules.

LLM‑oriented description
------------------------
This module is designed to be **LLM‑friendly** and easy to reason about.

If you are an AI model trying to understand or extend this code, here is
how to think about it:

1. **Input object**: `RawDataBundle`
   - Contains one or more **scans**.
   - Each scan has:
       - `x`: wavelength array (nm)
       - `y`: absorbance array (AU)
       - `label`: optional human‑readable label (e.g., "t = 0 min")

2. **Output object**: `ProcessedData`
   - `payload`: machine‑readable flags and intermediate results
   - `metadata`: human‑interpretable metrics (e.g., λmax, Abs_max, shifts)
   - `qc`: quality control info (currently minimal, can be extended)
   - `plots`: list of `PlotConfig` objects describing how to visualize results

3. **Core behaviors**:
   - If there is **one scan**, the processor:
       - optionally baseline‑corrects
       - optionally smooths
       - optionally normalizes
       - optionally detects λmax
       - produces a **single line plot** of Abs vs wavelength
   - If there are **multiple scans**, the processor:
       - processes each scan as above
       - builds a **single overlay plot** with one layer per scan
       - optionally computes a **difference spectrum** (last − first)
       - optionally computes simple comparison metrics:
           - λmax shift between first and last
           - ΔAbs_max between first and last

4. **Configuration model**: `UVVisConfig`
   - Contains simple boolean toggles for:
       - `smoothing`
       - `baseline`
       - `detect_lmax`
       - `normalize`
       - `overlay` (user toggle)
       - `auto_overlay` (automatic mode based on number of scans)
       - `compute_difference`
       - `compute_metrics`
   - In this implementation, the config is instantiated with defaults
     inside the processor, but it is intentionally a dataclass so that
     future versions can:
       - load it from user preferences
       - expose it via a UI
       - be modified by an AI agent

5. **Design constraints**:
   - The processor **does not**:
       - read files
       - detect formats
       - detect techniques
       - manage loaders
   - It assumes:
       - data is already loaded and normalized into `RawDataBundle`
       - the technique has already been identified as UV‑Vis
   - It focuses purely on **UV‑Vis domain logic**.

6. **Extension points**:
   - You can safely add:
       - more metrics to `metadata`
       - more QC checks to `qc`
       - more plot types to `plots`
       - more toggles to `UVVisConfig`
   - As long as:
       - `process()` still returns a `ProcessedData`
       - the public behavior remains deterministic and documented

Public API
----------
- `UVVisConfig`: configuration dataclass for UV‑Vis processing toggles.
- `UVVisProcessor`: main processor class, used by `ProcessorRouter`.

Typical usage
-------------
The processor is not called directly by end‑users. Instead, it is
invoked by the **ProcessorRouter** after the ingestion engine has:

    1. Detected the structural format
    2. Loaded the data via the appropriate loader
    3. Identified the technique as UV‑Vis

Example (conceptual):

    router = ProcessorRouter()
    processor = router.resolve(Technique.UVVIS)
    processed = processor.process(raw_bundle)

This yields a `ProcessedData` object with plots and metadata ready for
visualization or further analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any

import numpy as np

from chemworkbench.core.models import (
    RawDataBundle,
    ProcessedData,
    PlotConfig,
)
from chemworkbench.processors.base_processor import BaseProcessor


# ======================================================================
# Configuration
# ======================================================================

@dataclass
class UVVisConfig:
    """
    Configuration for UV‑Vis processing.

    All fields are simple toggles or options that control which
    operations are applied. This is intentionally minimal and
    human‑readable so that:

    • Users can understand what the processor is doing.
    • UIs can expose these options directly.
    • LLMs can safely modify or reason about them.
    """

    # Core single‑scan operations
    smoothing: bool = True
    baseline: bool = True
    detect_lmax: bool = True
    normalize: bool = False

    # Overlay behavior
    overlay: bool = True          # user‑controlled toggle
    auto_overlay: bool = True     # automatic if multiple scans present

    # Comparison behavior (for multi‑scan cases)
    compute_difference: bool = False
    compute_metrics: bool = True  # λmax shift, ΔAbs_max, etc.


# ======================================================================
# Processor
# ======================================================================

class UVVisProcessor(BaseProcessor):
    """
    UV‑Vis processor supporting:
    • Single‑scan processing
    • Overlay of multiple spectra
    • Simple comparison metrics between spectra

    This class is designed to be:

    • Deterministic: same input → same output.
    • Introspectable: behavior is controlled by UVVisConfig.
    • Extensible: new metrics and plots can be added without breaking the API.
    """

    def process(self, raw: RawDataBundle) -> ProcessedData:
        """
        Main entry point for UV‑Vis processing.

        Behavior:
        ---------
        • If there is exactly one scan:
            → process as a single spectrum.
        • If there are multiple scans:
            → if auto_overlay or overlay is enabled:
                → process in overlay mode.
            → otherwise:
                → process only the first scan as a single spectrum.

        Notes for LLMs:
        ---------------
        • You can change the behavior by modifying UVVisConfig defaults
          or by wiring a user‑provided config into this method.
        • You should not change the return type: it must remain ProcessedData.
        """

        config = UVVisConfig()  # future: load from user or global config

        scans = raw.scans  # list of Scan objects
        n = len(scans)

        # --------------------------------------------------------------
        # Determine mode (single vs overlay)
        # --------------------------------------------------------------
        if n == 1:
            return self._process_single(scans[0], config)

        if config.auto_overlay or config.overlay:
            return self._process_overlay(scans, config)

        # Fallback: treat first scan as single
        return self._process_single(scans[0], config)

    # ==================================================================
    # Single Scan
    # ==================================================================

    def _process_single(self, scan, config: UVVisConfig) -> ProcessedData:
        """
        Process a single UV‑Vis spectrum.

        Input:
        ------
        • scan.x: wavelength array (nm)
        • scan.y: absorbance array (AU)

        Operations (controlled by config):
        ----------------------------------
        • Baseline correction (simple offset)
        • Smoothing (moving average)
        • Normalization (max = 1.0)
        • λmax detection (wavelength of max absorbance)

        Output:
        -------
        • payload: flags indicating which operations were applied
        • metadata: λmax and Abs_max (if enabled)
        • plots: one line plot of Abs vs wavelength
        """

        x = np.array(scan.x)
        y = np.array(scan.y)

        payload: Dict[str, Any] = {}
        metadata: Dict[str, Any] = {}
        qc: Dict[str, Any] = {}
        plots: List[PlotConfig] = []

        # --------------------------------------------------------------
        # Baseline correction
        # --------------------------------------------------------------
        if config.baseline:
            baseline = float(np.min(y))
            y = y - baseline
            payload["baseline_corrected"] = True
            metadata["baseline_offset"] = baseline

        # --------------------------------------------------------------
        # Smoothing
        # --------------------------------------------------------------
        if config.smoothing:
            y = self._smooth(y)
            payload["smoothed"] = True

        # --------------------------------------------------------------
        # Normalization
        # --------------------------------------------------------------
        if config.normalize:
            max_val = float(np.max(y)) or 1.0
            y = y / max_val
            payload["normalized"] = True
            metadata["normalization_factor"] = max_val

        # --------------------------------------------------------------
        # λmax detection
        # --------------------------------------------------------------
        if config.detect_lmax and len(y) > 0:
            idx = int(np.argmax(y))
            lambda_max = float(x[idx])
            abs_max = float(y[idx])
            metadata["lambda_max"] = lambda_max
            metadata["abs_max"] = abs_max

        # --------------------------------------------------------------
        # Plot
        # --------------------------------------------------------------
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
    # Overlay Mode
    # ==================================================================

    def _process_overlay(self, scans, config: UVVisConfig) -> ProcessedData:
        """
        Process multiple UV‑Vis spectra in overlay mode.

        Behavior:
        ---------
        • Each scan is processed using the single‑scan pipeline.
        • A single overlay plot is created with one layer per scan.
        • Optionally, a difference spectrum (last − first) is computed.
        • Optionally, simple comparison metrics are computed:
            - λmax shift between first and last
            - ΔAbs_max between first and last

        Notes:
        ------
        • This is designed for visual comparison and simple metrics,
          not for advanced chemometrics.
        """

        payload: Dict[str, Any] = {"mode": "overlay"}
        metadata: Dict[str, Any] = {}
        qc: Dict[str, Any] = {}
        plots: List[PlotConfig] = []

        overlay_plot = PlotConfig(
            title="UV‑Vis Overlay",
            xlabel="Wavelength (nm)",
            ylabel="Absorbance (AU)",
            style="line",
            layers=[],
        )

        # --------------------------------------------------------------
        # Process each scan individually
        # --------------------------------------------------------------
        processed_scans: List[ProcessedData] = []
        for idx, scan in enumerate(scans, start=1):
            single = self._process_single(scan, config)
            processed_scans.append(single)

            # Add to overlay plot as a new layer
            overlay_plot.layers.append({
                "x": single.plots[0].x,
                "y": single.plots[0].y,
                "label": scan.label or f"Scan {idx}",
            })

        # --------------------------------------------------------------
        # Optional difference spectrum (first vs last)
        # --------------------------------------------------------------
        if config.compute_difference and len(processed_scans) >= 2:
            x = np.array(processed_scans[0].plots[0].x)
            y1 = np.array(processed_scans[0].plots[0].y)
            y2 = np.array(processed_scans[-1].plots[0].y)
            diff = (y2 - y1).tolist()

            plots.append(
                PlotConfig(
                    title="Difference Spectrum (Last − First)",
                    x=x.tolist(),
                    y=diff,
                    xlabel="Wavelength (nm)",
                    ylabel="ΔAbsorbance (AU)",
                    style="line",
                )
            )

        # --------------------------------------------------------------
        # Optional comparison metrics
        # --------------------------------------------------------------
        if config.compute_metrics and len(processed_scans) >= 2:
            first_meta = processed_scans[0].metadata
            last_meta = processed_scans[-1].metadata

            if "lambda_max" in first_meta and "lambda_max" in last_meta:
                metadata["lambda_max_shift"] = (
                    last_meta["lambda_max"] - first_meta["lambda_max"]
                )

            if "abs_max" in first_meta and "abs_max" in last_meta:
                metadata["delta_abs_max"] = (
                    last_meta["abs_max"] - first_meta["abs_max"]
                )

        # Add the overlay plot last so it appears as the primary view
        plots.append(overlay_plot)

        return ProcessedData(
            payload=payload,
            metadata=metadata,
            qc=qc,
            plots=plots,
        )

    # ==================================================================
    # Helpers
    # ==================================================================

    def _smooth(self, y: np.ndarray, window: int = 5) -> np.ndarray:
        """
        Simple moving average smoothing.

        Notes:
        ------
        • This is intentionally simple and transparent.
        • For more advanced smoothing (Savitzky‑Golay, etc.), a future
          version can add additional methods or toggles.
        """
        if len(y) < window:
            return y
        kernel = np.ones(window) / window
        return np.convolve(y, kernel, mode="same")
