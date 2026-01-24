from __future__ import annotations

from pathlib import Path

from .registry import LoaderRegistry
from .routing import TechniqueRouter
from chemworkbench.services.processing_service import ProcessingService
from chemworkbench.services.plotting_service import PlottingService


class Pipeline:
    """
    Full backend pipeline:
    file → loader → universal → processor → plot
    """

    def __init__(self):
        self.loader_registry = LoaderRegistry()
        self.router = TechniqueRouter()
        self.processor_service = ProcessingService()
        self.plotting_service = PlottingService()

    def run(self, path: Path, config: dict | None = None):
        # 1. Pick loader
        loader = self.loader_registry.sniff_loader(path)

        # 2. Load raw
        raw = loader.load_raw(path)

        # 3. Extract metadata
        metadata = loader.extract_metadata(raw)

        # 4. Normalize to universal model
        universal = loader.to_universal(raw, metadata)

        # 5. Route to processor
        processor = self.router.route(metadata)

        # 6. Process
        processed = self.processor_service.run(processor, universal, config)

        # 7. Plot
        figure = self.plotting_service.run(processed)

        return {
            "metadata": metadata,
            "universal": universal,
            "processed": processed,
            "figure": figure,
        }
