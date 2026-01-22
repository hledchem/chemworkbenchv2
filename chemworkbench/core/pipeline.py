from __future__ import annotations

import logging
from typing import Any, Protocol, runtime_checkable

from pydantic import ValidationError

from .models import BaseProcessorConfig, ProcessedData, Technique

logger = logging.getLogger(__name__)


@runtime_checkable
class ProcessorProtocol(Protocol):
    """Protocol that all processors are expected to follow.

    Only `process` is strictly required; all other methods are
    optional hooks that the pipeline will call if present.
    """

    name: str
    version: str
    technique: Technique

    def process(self, data: Any, config: BaseProcessorConfig) -> Any:
        ...


def _safe_call_step(
    step_name: str,
    enabled: bool,
    func: Any,
    data: Any,
    config: BaseProcessorConfig,
    processed: ProcessedData,
) -> Any:
    """Call a pipeline step safely, capturing errors and warnings.

    This function:
    - respects the `enabled` toggle
    - logs start/end of the step
    - catches exceptions and records them in ProcessedData.errors
    - never mutates the input data in place (returns a new object)
    """
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
        processed.errors.append(msg)
        return data


def run_pipeline(
    processor: ProcessorProtocol,
    config: BaseProcessorConfig,
    data: Any,
) -> ProcessedData:
    """Run the universal pipeline for a given processor.

    Steps:
        1. load        (optional)
        2. validate    (optional)
        3. preprocess  (optional)
        4. process     (required, but guarded)
        5. postprocess (optional)
        6. plot        (optional)
        7. export      (optional)

    All steps are:
        - toggled by config
        - called only if the corresponding method exists on the processor
        - wrapped in error handling so the pipeline never crashes

    Returns:
        ProcessedData: canonical processed data object.
    """
    # Validate config early to surface issues clearly
    try:
        config = config.__class__.model_validate(config)
    except ValidationError as exc:
        logger.exception("Configuration validation failed for '%s'.", config.name)
        # Even config validation errors are captured in a ProcessedData object
        processed = ProcessedData(
            technique=getattr(processor, "technique", Technique.GENERIC),
            raw_data=data,
            processed_data=data,
            metadata={"config_validation_error": exc.errors()},
            qc={},
            plots=[],
            warnings=[],
            errors=[f"Configuration validation failed: {exc}"],
        )
        return processed

    # Initialize canonical ProcessedData container
    processed = ProcessedData(
        technique=getattr(processor, "technique", Technique.GENERIC),
        raw_data=data,
        processed_data=data,
        metadata={},
        qc={},
        plots=[],
        warnings=[],
        errors=[],
    )

    # Resolve optional hooks on the processor
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

    # 1. load
    current_data = _safe_call_step(
        step_name="load",
        enabled=config.enable_load,
        func=load_fn,
        data=current_data,
        config=config,
        processed=processed,
    )

    # 2. validate
    current_data = _safe_call_step(
        step_name="validate",
        enabled=config.enable_validate,
        func=validate_fn,
        data=current_data,
        config=config,
        processed=processed,
    )

    # 3. preprocess
    current_data = _safe_call_step(
        step_name="preprocess",
        enabled=config.enable_preprocess,
        func=preprocess_fn,
        data=current_data,
        config=config,
        processed=processed,
    )

    # 4. process (core step; still guarded)
    current_data = _safe_call_step(
        step_name="process",
        enabled=config.enable_process,
        func=process_fn,
        data=current_data,
        config=config,
        processed=processed,
    )

    # 5. postprocess
    current_data = _safe_call_step(
        step_name="postprocess",
        enabled=config.enable_postprocess,
        func=postprocess_fn,
        data=current_data,
        config=config,
        processed=processed,
    )

    # At this point, current_data is the final processed payload
    processed.processed_data = current_data

    # Metadata
    if metadata_fn is not None:
        logger.info("Building metadata for processor '%s'.", config.name)
        try:
            metadata = metadata_fn(current_data, config)
            if metadata is not None:
                processed.metadata.update(metadata)
        except Exception as exc:  # noqa: BLE001
            msg = f"Error while building metadata: {exc!r}"
            logger.exception(msg)
            processed.errors.append(msg)

    # QC metrics
    if qc_fn is not None:
        logger.info("Computing QC metrics for processor '%s'.", config.name)
        try:
            qc_metrics = qc_fn(current_data, config)
            if qc_metrics is not None:
                processed.qc.update(qc_metrics)
        except Exception as exc:  # noqa: BLE001
            msg = f"Error while computing QC metrics: {exc!r}"
            logger.exception(msg)
            processed.errors.append(msg)

    # 6. plot
    if plot_fn is not None and config.enable_plot:
        logger.info("Generating plots for processor '%s'.", config.name)
        try:
            plots = plot_fn(current_data, config)
            if plots:
                processed.plots.extend(plots)
        except Exception as exc:  # noqa: BLE001
            msg = f"Error while generating plots: {exc!r}"
            logger.exception(msg)
            processed.errors.append(msg)

    # 7. export
    if export_fn is not None and config.enable_export:
        logger.info("Exporting results for processor '%s'.", config.name)
        try:
            export_fn(current_data, config)
        except Exception as exc:  # noqa: BLE001
            msg = f"Error while exporting results: {exc!r}"
            logger.exception(msg)
            processed.errors.append(msg)

    # Final log
    if processed.errors:
        logger.warning(
            "Pipeline completed for '%s' with %d error(s).",
            config.name,
            len(processed.errors),
        )
    else:
        logger.info("Pipeline completed successfully for '%s'.", config.name)

    return processed
