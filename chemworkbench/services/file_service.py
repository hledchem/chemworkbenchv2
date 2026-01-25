"""
services/file_service.py

Centralized file handling utilities for ChemWorkBench v2.

Responsibilities:
    - Normalize file paths
    - Validate file existence and readability
    - Provide safe byte-level access for detectors and loaders
    - Handle temporary files (future cloud integration)
    - Provide a clean abstraction for API/UI layers

This service does NOT parse scientific data.
It only handles filesystem-level concerns.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional, Union

from chemworkbench.runtime.logging import get_logger
from chemworkbench.runtime.errors import PipelineError


logger = get_logger(__name__)

PathLike = Union[str, Path]


class FileService:
    """
    High-level file access service.

    This is used by:
        - file sniffer
        - loaders
        - API endpoints
        - CLI commands
        - future cloud storage adapters
    """

    # ------------------------------------------------------------------
    # Path normalization
    # ------------------------------------------------------------------

    def normalize(self, path: PathLike) -> Path:
        """
        Convert input into a normalized Path object.
        """
        try:
            p = Path(path).expanduser().resolve()
            logger.debug(f"Normalized path: {p}")
            return p
        except Exception as exc:
            raise PipelineError(f"Invalid file path: {path}") from exc

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def ensure_exists(self, path: PathLike) -> Path:
        """
        Ensure the file exists and is readable.
        """
        p = self.normalize(path)

        if not p.exists():
            raise PipelineError(f"File not found: {p}")

        if not p.is_file():
            raise PipelineError(f"Path is not a file: {p}")

        return p

    # ------------------------------------------------------------------
    # Byte-level access
    # ------------------------------------------------------------------

    def read_bytes(self, path: PathLike) -> bytes:
        """
        Read raw bytes from a file.
        """
        p = self.ensure_exists(path)

        try:
            data = p.read_bytes()
            logger.debug(f"Read {len(data)} bytes from {p}")
            return data
        except Exception as exc:
            raise PipelineError(f"Failed to read bytes from {p}: {exc}") from exc

    # ------------------------------------------------------------------
    # Text access
    # ------------------------------------------------------------------

    def read_text(self, path: PathLike, encoding: str = "utf-8") -> str:
        """
        Read text from a file.
        """
        p = self.ensure_exists(path)

        try:
            text = p.read_text(encoding=encoding)
            logger.debug(f"Read text file: {p}")
            return text
        except Exception as exc:
            raise PipelineError(f"Failed to read text from {p}: {exc}") from exc

    # ------------------------------------------------------------------
    # Write utilities (for examples, tests, and UI export)
    # ------------------------------------------------------------------

    def write_bytes(self, path: PathLike, data: bytes) -> Path:
        """
        Write bytes to a file.
        """
        p = Path(path)

        try:
            p.write_bytes(data)
            logger.debug(f"Wrote {len(data)} bytes to {p}")
            return p
        except Exception as exc:
            raise PipelineError(f"Failed to write bytes to {p}: {exc}") from exc

    def write_text(self, path: PathLike, text: str, encoding: str = "utf-8") -> Path:
        """
        Write text to a file.
        """
        p = Path(path)

        try:
            p.write_text(text, encoding=encoding)
            logger.debug(f"Wrote text file: {p}")
            return p
        except Exception as exc:
            raise PipelineError(f"Failed to write text to {p}: {exc}") from exc


# ----------------------------------------------------------------------
# Singleton instance
# ----------------------------------------------------------------------

file_service = FileService()
