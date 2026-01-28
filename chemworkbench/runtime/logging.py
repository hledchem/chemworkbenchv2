"""
chemworkbench/runtime/logging.py

Unified logging utility for ChemWorkBench v2.2
----------------------------------------------

Design goals (v2.2):
- Minimal, deterministic, and dependency‑free
- Safe for plugin ecosystems and multiprocessing
- No global reconfiguration of Python's logging system
- Each module obtains its own logger via get_logger()
- Debug mode can be enabled cleanly by the CLI

This module intentionally avoids complex logging trees,
file handlers, or global overrides. The CLI is responsible
for enabling DEBUG level when requested.
"""

from __future__ import annotations

import logging


# ----------------------------------------------------------------------
# Logger factory
# ----------------------------------------------------------------------

def get_logger(name: str = "chemworkbench") -> logging.Logger:
    """
    Return a configured logger instance.

    v2.2 behavior:
    - Each logger is configured once (idempotent)
    - StreamHandler only (stdout)
    - INFO level by default
    - Format is compact and human‑readable
    """
    logger = logging.getLogger(name)

    # Only configure once
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Default level (CLI may override)
        logger.setLevel(logging.INFO)

    return logger


# ----------------------------------------------------------------------
# Debug mode helper (optional)
# ----------------------------------------------------------------------

def enable_debug_mode() -> None:
    """
    Enable DEBUG logging globally.

    This is intentionally simple: it raises the root logger level
    without altering handlers or formats. The CLI calls this when
    the user passes --debug.
    """
    logging.getLogger().setLevel(logging.DEBUG)
