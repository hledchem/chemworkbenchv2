from __future__ import annotations

from typing import Any, Optional

from chemworkbench.core.models import (
    PipelineResult,
    ProcessedData,
)
from chemworkbench.processors.base_processor import BaseProcessor
from chemworkbench.plotting.builder.config_builder import PlotConfigBuilder
from chemworkbench.plotting.schema.figure_schema import FigureSchema


class Pipeline:
    """
    ChemWorkBench v2 Pipeline

    Executes a processor end-to-end using the standardized lifecycle:
    load → validate → preprocess → process → postprocess → metadata → qc → plot → export

    The pipeline is fully declarative, toggle-aware, and processor-agnostic.
    """

    def __init__(self, processor: BaseProcessor):
        self.processor = processor

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, raw_input: Any) -> PipelineResult:
        """
        Execute the full pipeline and return a PipelineResult.
        """
        result = PipelineResult()
        data = ProcessedData()

        try:
            # ------------------------------------------------------------
            # LOAD
            # ------------------------------------------------------------
            if self.processor.config.enable_load:
                loaded = self.processor.load(raw_input)
                data.raw_data = loaded if loaded is not None else raw_input
            else:
                data.raw_data = raw_input

            # ------------------------------------------------------------
            # VALIDATE
            # ------------------------------------------------------------
            if self.processor.config.enable_validate:
                self.processor.validate(data)

            # ------------------------------------------------------------
            # PREPROCESS
            # ------------------------------------------------------------
            if self.processor.config.enable_preprocess:
                self.processor.preprocess(data)

            # ------------------------------------------------------------
            # PROCESS (required)
            # ------------------------------------------------------------
            if self.processor.config.enable_process:
                self.processor.process(data)

            # ------------------------------------------------------------
            # POSTPROCESS
            # ------------------------------------------------------------
            if self.processor.config.enable_postprocess:
                self.processor.postprocess(data)

            # ------------------------------------------------------------
            # METADATA
            # ------------------------------------------------------------
            metadata = self.processor.build_metadata(data)
            if metadata:
                data.metadata.update(metadata)

            # ------------------------------------------------------------
            # QC METRICS
            # ------------------------------------------------------------
            qc = self.processor.compute_qc(data)
            if qc:
                data.qc.update(qc)

            # ------------------------------------------------------------
            # PLOTTING (NEW v2 architecture)
            # ------------------------------------------------------------
            if self.processor.config.enable_plot:
                figure_schema = self.processor.make_plots(data)

                if isinstance(figure_schema, FigureSchema):
                    builder = PlotConfigBuilder()
                    plot_configs = builder.build_from_figure(figure_schema)

                    # Attach PlotConfig objects to the pipeline result
                    result.plots = plot_configs

                    # Also attach the schema for UI / JSON export
                    result.figure_schema = figure_schema

            # ------------------------------------------------------------
            # EXPORT
            # ------------------------------------------------------------
            if self.processor.config.enable_export:
                exported = self.processor.export(data)
                if exported is not None:
                    result.exported = exported

            # Finalize
            result.processed_data = data

        except Exception as exc:
            result.errors.append(
                f"Error in pipeline for processor '{self.processor.__class__.__name__}': {exc}"
            )

        return result
