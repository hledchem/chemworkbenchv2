from __future__ import annotations

import numpy as np

from chemworkbench.core.pipeline import run_pipeline
from chemworkbench.processors.uvvis import UVVisProcessor, UVVisConfig


def main() -> None:
    # ------------------------------------------------------------
    # 1. Create synthetic UV-Vis data
    # ------------------------------------------------------------
    x = np.linspace(200, 800, 1000)
    y = np.exp(-0.5 * ((x - 450) / 20) ** 2)  # Gaussian peak at 450 nm

    data = {"x": x, "y": y}

    # ------------------------------------------------------------
    # 2. Build a UVVisConfig
    # ------------------------------------------------------------
    config = UVVisConfig(
        name="uvvis_test",
        baseline_method="polynomial",
        baseline_order=3,
        smoothing_method="moving_average",
        smoothing_window=11,
        normalization_method="max",
        detect_peaks=True,
        peak_min_prominence=0.01,
        integration_regions=[(430.0, 470.0)],
    )

    # ------------------------------------------------------------
    # 3. Instantiate the processor
    # ------------------------------------------------------------
    processor = UVVisProcessor()

    # ------------------------------------------------------------
    # 4. Run the universal pipeline
    # ------------------------------------------------------------
    result = run_pipeline(processor, config, data)

    # ------------------------------------------------------------
    # 5. Print results
    # ------------------------------------------------------------
    print("\n=== ERRORS ===")
    print(result.errors)

    print("\n=== METADATA ===")
    print(result.metadata)

    print("\n=== QC METRICS ===")
    for name, metric in result.qc.items():
        print(f"{name}: {metric.value} ({metric.description})")

    print("\n=== PROCESSED DATA KEYS ===")
    if isinstance(result.processed_data, dict):
        print(list(result.processed_data.keys()))
    else:
        print(type(result.processed_data))

    print("\n=== PLOTS ===")
    for plot in result.plots:
        print(f"Plot id={plot.id}, title={plot.title}, layers={len(plot.layers)}")


if __name__ == "__main__":
    main()
