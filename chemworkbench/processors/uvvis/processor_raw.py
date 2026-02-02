"""
UV‑Vis Raw Plotting Processor (ChemWorkBench v2.2)
==================================================

High‑level purpose
------------------
This processor provides the **simplest possible UV‑Vis workflow**:
it takes one or more UV‑Vis scans (already loaded into a RawDataBundle)
and produces **raw, unprocessed plots**.

No smoothing.
No baseline correction.
No normalization.
No peak detection.
No integration.
No analytics.

This is the correct processor to use when:
• You want to validate that ingestion → loader → processor → plotting works.
• You want to visualize raw spectra exactly as they appear in the file.
• You want a stable foundation before enabling advanced UV‑Vis features.

LLM‑oriented description
------------------------
If you are an AI model reading or modifying this file, here is how to
reason about it:

1. **This processor is intentionally minimal.**
   It does not use UVVisConfig or any advanced processing toggles.

2. **Input:** RawDataBundle
   - Contains one or more Scan objects.
   - Each Scan has:
       • x: wavelength array (nm)
       • y: absorbance array (AU)
       • label: optional string

3. **Output:** ProcessedData
   - payload: empty or minimal
   - metadata: empty or minimal
   - qc: empty (future extension point)
   - plots: one or more PlotConfig objects

4. **Behavior:**
   - If there is one scan → produce one raw line plot.
   - If there are multiple scans → produce a single overlay plot with layers.

5. **Extension points:**
   - You may add:
       • axis scaling
       • color themes
       • legends
       • annotations
       • export options
   - You should NOT add scientific processing here. That belongs in the
     full UV‑Vis processor.

6. **Safety:**
   - This processor must remain deterministic.
   - It must not modify the raw data.
   - It must not apply smoothing, baseline correction, or any analytics.

This file is designed to be a stable, predictable foundation for raw
visualization and debugging of the ingestion pipeline.
"""

from __future__ import annotations

from typing import List, Dict, Any

import numpy as np

from chemworkbench.core.models import (
    RawDataBundle,
    ProcessedData,
    PlotConfig,
)
from chemworkbench.processors.base_processor import BaseProcessor


class UVVisRawProcessor(BaseProcessor):
    """
    Minimal UV‑Vis processor that produces raw plots only.

    Responsibilities
    ----------------
    • Plot raw x/y data for a single scan.
    • Overlay multiple scans if present.
    • Produce PlotConfig objects for visualization.

    Non‑Responsibilities
    --------------------
    • Smoothing
    • Baseline correction
    • Normalization
    • Peak detection
    • Integration
    • Any scientific processing
    """

    def process(self, raw: RawDataBundle) -> ProcessedData:
        scans = raw.scans
        n = len(scans)

        # Single scan → simple raw plot
        if n == 1:
            return self._plot_single(scans[0])

        # Multiple scans → overlay plot
        return self._plot_overlay(scans)

    # ------------------------------------------------------------------
    # Single Scan Plot
    # ------------------------------------------------------------------

    def _plot_single(self, scan) -> ProcessedData:
        x = np.array(scan.x)
        y = np.array(scan.y)

        plot = PlotConfig(
            title=scan.label or "UV‑Vis Raw Spectrum",
            x=x.tolist(),
            y=y.tolist(),
            xlabel="Wavelength (nm)",
            ylabel="Absorbance (AU)",
            style="line",
        )

        return ProcessedData(
            payload={"mode": "single_raw"},
            metadata={},
            qc={},
            plots=[plot],
        )

    # ------------------------------------------------------------------
    # Overlay Plot
    # ------------------------------------------------------------------

    def _plot_overlay(self, scans) -> ProcessedData:
        overlay = PlotConfig(
            title="UV‑Vis Raw Overlay",
            xlabel="Wavelength (nm)",
            ylabel="Absorbance (AU)",
            style="line",
            layers=[],
        )

        for idx, scan in enumerate(scans, start=1):
            x = np.array(scan.x)
            y = np.array(scan.y)

            overlay.layers.append({
                "x": x.tolist(),
                "y": y.tolist(),
                "label": scan.label or f"Scan {idx}",
            })

        return ProcessedData(
            payload={"mode": "overlay_raw"},
            metadata={},
            qc={},
            plots=[overlay],
        )
