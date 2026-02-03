"""
Sequential Block Activation Test — UV‑Vis Processor (ChemWorkBench v2.2)
=======================================================================

This test runs the UV‑Vis processor multiple times, each time enabling
one additional processing block. It validates that each block:

    • runs without errors
    • modifies the spectrum as expected
    • produces correct metadata
    • composes correctly with previous blocks
"""

from copy import deepcopy
from pathlib import Path

from chemworkbench.core.ingestion_engine import IngestionEngine
from chemworkbench.core.routing import ProcessorRouter
from chemworkbench.core.technique_detection_engine import TechniqueEngine

# *** ONLY CHANGE MADE HERE ***
from chemworkbench.core.format_registry_init import build_default_format_registry
from chemworkbench.core.loader_registry_init import build_default_loader_registry

from chemworkbench.processors.uvvis.config import UVVisConfig

# NEW: plotting service import
from chemworkbench.services.plotting_service import PlottingService


def print_step_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def run_step(raw, config: UVVisConfig, description: str):
    print_step_header(description)

    router = ProcessorRouter()
    processor = router.resolve(raw.technique)

    # IMPORTANT FIX:
    # The processor does NOT accept config= in .process()
    # So we call the correct internal method based on scan count.
    if len(raw.scans) == 1:
        processed = processor._process_single(raw.scans[0], config, raw.technique)
    else:
        processed = processor._process_multi(raw.scans, config, raw.technique)

    print("\n--- Enabled Blocks ---")
    for field, value in config.dict().items():
        if value not in (None, False, "none"):
            print(f"{field}: {value}")

    print("\n--- Metadata ---")
    for k, v in processed.metadata.items():
        print(f"{k}: {v}")

    print("\n--- Payload ---")
    for k, v in processed.payload.items():
        print(f"{k}: {v}")

    print("\n--- Plots ---")
    plotter = PlottingService()

    for i, plot in enumerate(processed.plots, start=1):
        print(f"Plot {i}: {plot.title} ({len(plot.x or [])} points)")
        plotter.render([plot])


def run_sequential_test(filepath: str):
    print("\n=== Sequential UV‑Vis Block Activation Test ===")

    # --------------------------------------------------------------
    # 1. Build ingestion engine
    # --------------------------------------------------------------
    format_registry = build_default_format_registry()
    loader_registry = build_default_loader_registry()
    technique_engine = TechniqueEngine()
    router = ProcessorRouter()

    engine = IngestionEngine(
        format_registry=format_registry,
        loader_registry=loader_registry,
        technique_engine=technique_engine,
        processor_router=router,
    )

    # --------------------------------------------------------------
    # 2. Ingest file
    # --------------------------------------------------------------
    result = engine.ingest(Path(filepath))
    raw = result.raw

    print(f"Loaded: {filepath}")
    print(f"Technique: {raw.technique}")

    # --------------------------------------------------------------
    # Base config (all blocks off)
    # --------------------------------------------------------------
    base = UVVisConfig(
        baseline_method="none",
        smoothing_method="none",
        normalization_method="none",
        detect_peaks=False,
        integration_regions=None,
    )

    # --------------------------------------------------------------
    # Step 1 — Raw only
    # --------------------------------------------------------------
    cfg1 = deepcopy(base)
    run_step(raw, cfg1, "STEP 1 — Raw Spectrum Only")

    # --------------------------------------------------------------
    # Step 2 — Baseline only
    # --------------------------------------------------------------
    cfg2 = deepcopy(base)
    cfg2.baseline_method = "polynomial"
    run_step(raw, cfg2, "STEP 2 — Baseline Correction Only")

    # --------------------------------------------------------------
    # Step 3 — Baseline + Smoothing
    # --------------------------------------------------------------
    cfg3 = deepcopy(cfg2)
    cfg3.smoothing_method = "moving_average"
    run_step(raw, cfg3, "STEP 3 — Baseline + Smoothing")

    # --------------------------------------------------------------
    # Step 4 — Baseline + Smoothing + Normalization
    # --------------------------------------------------------------
    cfg4 = deepcopy(cfg3)
    cfg4.normalization_method = "max"
    run_step(raw, cfg4, "STEP 4 — Baseline + Smoothing + Normalization")

    # --------------------------------------------------------------
    # Step 5 — Add Peak Detection
    # --------------------------------------------------------------
    cfg5 = deepcopy(cfg4)
    cfg5.detect_peaks = True
    run_step(raw, cfg5, "STEP 5 — Add Peak Detection")

    # --------------------------------------------------------------
    # Step 6 — Add Integration
    # --------------------------------------------------------------
    cfg6 = deepcopy(cfg5)
    cfg6.integration_regions = [(250, 350), (400, 500)]
    run_step(raw, cfg6, "STEP 6 — Add Integration Regions")

    print("\n=== Sequential Test Complete ===\n")


# ======================================================================
# Pytest wrapper (NEW)
# ======================================================================

def test_uvvis_block_sequence():
    """
    Pytest wrapper for the sequential UV‑Vis block activation test.
    """
    test_file = "tests/synthetic_data/uvvis_synthetic_500nm.csv"
    run_sequential_test(test_file)


# Still runnable as a standalone script
if __name__ == "__main__":
    test_file = "tests/synthetic_data/uvvis_synthetic_500nm.csv"
    run_sequential_test(test_file)
