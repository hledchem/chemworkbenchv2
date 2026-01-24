from __future__ import annotations

from typing import Any, Dict, Optional

from chemworkbench.core.models import (
    BaseProcessorConfig,
    ProcessedData,
    PipelineResult,
)
from chemworkbench.plotting.schema.figure_schema import FigureSchema


class BaseProcessor:
    """
    Base class for all ChemWorkBench v2 processors.

    This class defines the full processor lifecycle and provides
    extension hooks for each step. Subclasses override only what
    they need, and the pipeline dynamically calls the enabled steps.

    The processor is fully declarative, toggleable, and UI-friendly.
    """

    config_class = BaseProcessorConfig  # overridden by subclasses

    def __init__(self, config: Optional[BaseProcessorConfig] = None):
        self.config: BaseProcessorConfig = config or self.config_class()

    # ------------------------------------------------------------------
    # Public API: called by the pipeline
    # ------------------------------------------------------------------

    def run(self, raw_input: Any) -> PipelineResult:
        """
        Execute the full processor lifecycle and return a PipelineResult.
        The pipeline orchestrates this, but processors may call it directly.
        """
        result = PipelineResult()

        try:
            data = ProcessedData()
            data.raw_data = raw_input

            # -----------------------------
            # LOAD
            # -----------------------------
            if self.config.enable_load:
                loaded = self.load(raw_input)
                if loaded is not None:
                    data.raw_data = loaded

            # -----------------------------
            # VALIDATE
            # -----------------------------
            if self.config.enable_validate:
                self.validate(data)

            # -----------------------------
            # PREPROCESS
            # -----------------------------
            if self.config.enable_preprocess:
                self.preprocess(data)

            # -----------------------------
            # PROCESS (required)
            # -----------------------------
            if self.config.enable_process:
                self.process(data)

            # -----------------------------
            # POSTPROCESS
            # -----------------------------
            if self.config.enable_postprocess:
                self.postprocess(data)

            # -----------------------------
            # METADATA
            # -----------------------------
            metadata = self.build_metadata(data)
            if metadata:
                data.metadata.update(metadata)

            # -----------------------------
            # QC METRICS
            # -----------------------------
            qc = self.compute_qc(data)
            if qc:
                data.qc.update(qc)

            # -----------------------------
            # PLOTTING (schema → builder → PlotConfig)
            # -----------------------------
            if self.config.enable_plot:
                figure_schema = self.make_plots(data)
                if figure_schema is not None:
                    result.figure_schema = figure_schema  # pipeline converts it

            # -----------------------------
            # EXPORT
            # -----------------------------
            if self.config.enable_export:
                exported = self.export(data)
                if exported is not None:
                    result.exported = exported

            # Finalize
            result.processed_data = data

        except Exception as exc:
            result.errors.append(f"Error in processor '{self.__class__.__name__}': {exc}")

        return result

    # ------------------------------------------------------------------
    # Lifecycle hooks (subclasses override as needed)
    # ------------------------------------------------------------------

    def load(self, raw_input: Any) -> Any:
        """Load or parse raw input. Optional."""
        return raw_input

    def validate(self, data: ProcessedData) -> None:
        """Validate raw or intermediate data. Optional."""
        return None

    def preprocess(self, data: ProcessedData) -> None:
        """Preprocess data before main processing. Optional."""
        return None

    def process(self, data: ProcessedData) -> None:
        """
        Main processing step. REQUIRED.
        Subclasses must override this.
        """
        raise NotImplementedError("Processor must implement process()")

    def postprocess(self, data: ProcessedData) -> None:
        """Optional postprocessing step."""
        return None

    def build_metadata(self, data: ProcessedData) -> Dict[str, Any]:
        """Return metadata dict. Optional."""
        return {}

    def compute_qc(self, data: ProcessedData) -> Dict[str, Any]:
        """Return QC metrics dict. Optional."""
        return {}

    # ------------------------------------------------------------------
    # Plotting (NEW v2 architecture)
    # ------------------------------------------------------------------

    def make_plots(self, data: ProcessedData) -> Optional[FigureSchema]:
        """
        Return a FigureSchema describing the desired plots.

        Subclasses override this to declare plots using the
        declarative schema system. The pipeline will convert
        the schema → PlotConfig → rendered figure.

        Returning None means no plots.
        """
        return None

    # ------------------------------------------------------------------
    # Exporting
    # ------------------------------------------------------------------

    def export(self, data: ProcessedData) -> Any:
        """Optional export step (e.g., CSV, JSON, PDF)."""
        return None
