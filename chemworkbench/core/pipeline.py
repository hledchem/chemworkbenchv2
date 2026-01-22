from __future__ import annotations

import logging
from typing import Any, Protocol, runtime_checkable

from pydantic import ValidationError

from .models import (
    BaseProcessorConfig,
    PipelineResult,
    ProcessedData,
    Technique,
)

logger = logging.getLogger(__name__)


# ------------------------------------------------------------
# Processor Protocol
# ------------------------------------------------------------

@runtime_checkable
class ProcessorProtocol(Protocol):
    """Protocol that all processors must follow."""

    name: str
    version: str
    technique: Technique

    def process(self, data: Any, config: BaseProcessorConfig) -> Any:
        ...


# ------------------------------------------------------------
# Safe step wrapper
# ------------------------------------------------------------

def _safe_call_step(
    step_name: str,
    enabled: bool,
    func: Any,
    data: Any,
    config: BaseProcessorConfig,
    result: PipelineResult,
) -> Any:
    """Call a pipeline step safely, capturing errors and warnings."""

    if not enabled or func is None:
        logger.debug("Skipping step '%s' (disabled or missing).", step_name)
        return data

    logger.info("Starting step '%s' for processor '%s'.", step_name, config.name)

    try:
        new_data = func(data, config)
        logger.info("Finished step '%s' for processor '%s'.", step_name, config.name)
        return new_data
    except Exception as exc:  # noqa: BLE001
        msg = f"Error in step '{step_name}': {exc!r}"
        logger.exception(msg)
        result.errors.append(msg)
        return data


# ------------------------------------------------------------
# Universal Pipeline
# ------------------------------------------------------------

def run_pipeline(
    processor: ProcessorProtocol,
    config: BaseProcessorConfig,
    data: Any,
) -> PipelineResult:
    """Run the universal pipeline for a given processor."""

    # --------------------------------------------------------
    # Validate config
    # --------------------------------------------------------
    try:
        config = config.__class__.model_validate(config)
    except ValidationError as exc:
        logger.exception("Configuration validation failed for '%s'.", config.name)
        return PipelineResult(
            processed_data=None,
            metadata={"config_validation_error": exc.errors()},
            qc={},
            plots=[],
            errors=[f"Configuration validation failed: {exc}"],
        )

    # --------------------------------------------------------
    # Initialize PipelineResult container
    # --------------------------------------------------------
    result = PipelineResult(
        processed_data=None,
        metadata={},
        qc={},
        plots=[],
        errors=[],
    )

    # --------------------------------------------------------
    # Resolve processor hooks
    # --------------------------------------------------------
    load_fn = getattr(processor, "load", None)
    validate_fn = getattr(processor, "validate", None)
    preprocess_fn = getattr(processor, "preprocess", None)
    process_fn = getattr(processor, "process", None)
    postprocess_fn = getattr(processor, "postprocess", None)
    plot_fn = getattr(processor, "make_plots", None)
    export_fn = getattr(processor, "export", None)
    metadata_fn = getattr(processor, "build_metadata", None)
    qc_fn = getattr(processor, "compute_qc", None)

    current_data = data

    # --------------------------------------------------------
    # 1. load
    # --------------------------------------------------------
    current_data = _safe_call_step(
        "load",
        config.enable_load,
        load_fn,
        current_data,
        config,
        result,
    )

    # --------------------------------------------------------
    # 2. validate
    # --------------------------------------------------------
    current_data = _safe_call_step(
        "validate",
        config.enable_validate,
        validate_fn,
        current_data,
        config,
        result,
    )

    # --------------------------------------------------------
    # 3. preprocess
    # --------------------------------------------------------
    current_data = _safe_call_step(
        "preprocess",
        config.enable_preprocess,
        preprocess_fn,
        current_data,
        config,
        result,
    )

    # --------------------------------------------------------
    # 4. process (core step)
    # --------------------------------------------------------
    current_data = _safe_call_step(
        "process",
        config.enable_process,
        process_fn,
        current_data,
        config,
        result,
    )

    # --------------------------------------------------------
    # 5. postprocess
    # --------------------------------------------------------
    current_data = _safe_call_step(
        "postprocess",
        config.enable_postprocess,
        postprocess_fn,
        current_data,
        config,
        result,
    )

    # --------------------------------------------------------
    # Final processed payload
    # --------------------------------------------------------
    result.processed_data = current_data

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------
    if metadata_fn is not None:
        logger.info("Building metadata for processor '%s'.", config.name)
        try:
            metadata = metadata_fn(current_data, config)
            if metadata is not None:
                result.metadata.update(metadata)
        except Exception as exc:  # noqa: BLE001
            msg = f"Error while building metadata: {exc!r}"
            logger.exception(msg)
            result.errors.append(msg)

    # --------------------------------------------------------
    # QC metrics
    # --------------------------------------------------------
    if qc_fn is not None:
        logger.info("Computing QC metrics for processor '%s'.", config.name)
        try:
            qc_metrics = qc_fn(current_data, config)
            if qc_metrics is not None:
                result.qc.update(qc_metrics)
        except Exception as exc:  # noqa: BLE001
            msg = f"Error while computing QC metrics: {exc!r}"
            logger.exception(msg)
            result.errors.append(msg)

    # --------------------------------------------------------
    # 6. plot
    # --------------------------------------------------------
    if plot_fn is not None and config.enable_plot:
        logger.info("Generating plots for processor '%s'.", config.name)
        try:
            plots = plot_fn(current_data, config)
            if plots:
                result.plots.extend(plots)
        except Exception as exc:  # noqa: BLE001
            msg = f"Error while generating plots: {exc!r}"
            logger.exception(msg)
            result.errors.append(msg)

    # --------------------------------------------------------
    # 7. export
    # --------------------------------------------------------
    if export_fn is not None and config.enable_export:
        logger.info("Exporting results for processor '%s'.", config.name)
        try:
            export_fn(current_data, config)
        except Exception as exc:  # noqa: BLE001
            msg = f"Error while exporting results: {exc!r}"
            logger.exception(msg)
            result.errors.append(msg)

    # --------------------------------------------------------
    # Final log
    # --------------------------------------------------------
    if result.errors:
        logger.warning(
            "Pipeline completed for '%s' with %d error(s).",
            config.name,
            len(result.errors),
        )
    else:
        logger.info("Pipeline completed successfully for '%s'.", config.name)

    return result
