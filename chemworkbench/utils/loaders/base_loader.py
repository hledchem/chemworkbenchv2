"""
Base Loader Framework — ChemWorkBench v2.2
==========================================

LLM‑friendly commentary
-----------------------
This module defines the canonical loader interface for ChemWorkBench v2.2.
Loaders are responsible only for:

    - identifying whether they can handle a file (sniff)
    - reading vendor‑specific raw data (load_raw)
    - extracting metadata (extract_metadata)
    - converting raw data into the universal list‑of‑dicts format (to_universal)

Responsibilities:
- provide a deterministic, plugin‑safe loader interface
- return RawDataBundle objects for the pipeline
- isolate vendor‑specific parsing logic
- ensure universal output is stable and consistent

Non‑responsibilities:
- technique detection (handled by the anchor engine)
- loader selection (handled by the loader registry)
- scientific interpretation (handled by processors)
- plotting or visualization
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Protocol, runtime_checkable

from chemworkbench.core.models import RawDataBundle
from chemworkbench.core.models import Technique


# ======================================================================
# Exceptions
# ======================================================================

class LoaderError(Exception):
    """Base exception for all loader‑related errors."""


class LoaderSniffError(LoaderError):
    """Raised when a loader cannot confidently identify a file."""


class LoaderReadError(LoaderError):
    """Raised when a loader fails while reading or parsing raw data."""


class LoaderMetadataError(LoaderError):
    """Raised when metadata extraction fails."""


class LoaderNormalizationError(LoaderError):
    """Raised when conversion to the universal data model fails."""


# ======================================================================
# Loader Protocol (structural)
# ======================================================================

@runtime_checkable
class BaseLoaderProtocol(Protocol):
    """
    Structural protocol for all loaders.

    Any class implementing this protocol can be used by the loader registry
    and pipeline, regardless of inheritance.
    """

    # Class‑level identifiers
    VENDOR: str
    FORMAT: str
    EXTENSIONS: tuple[str, ...]

    def sniff(self, path: Path) -> bool:
        """Return True if this loader can handle the file."""
        ...

    def load_raw(self, path: Path) -> Any:
        """Read vendor‑specific raw data."""
        ...

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        """Extract metadata from raw vendor‑specific structure."""
        ...

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        """Convert raw data to universal list‑of‑dicts format."""
        ...

    def load(self, path: Path) -> RawDataBundle:
        """Full load pipeline returning a RawDataBundle."""
        ...


# ======================================================================
# Concrete Base Class (v2.2)
# ======================================================================

class BaseVendorLoader(BaseLoaderProtocol):
    """
    Concrete base class implementing the v2.2 loader pipeline.

    Vendor‑specific loaders should override:
        - VENDOR
        - FORMAT
        - EXTENSIONS
        - sniff()
        - load_raw()
        - extract_metadata()
        - to_universal()
    """

    VENDOR: str = "generic"
    FORMAT: str = "generic"
    EXTENSIONS: tuple[str, ...] = ()

    # ------------------------------------------------------------------
    # Sniffing
    # ------------------------------------------------------------------
    def sniff(self, path: Path) -> bool:  # type: ignore[override]
        """
        Default sniff implementation: extension check only.

        Concrete loaders are encouraged to override this with:
            - magic byte checks
            - directory structure checks
            - header inspection
        """
        suffix = path.suffix.lower()
        return suffix in {ext.lower() for ext in self.EXTENSIONS}

    # ------------------------------------------------------------------
    # Raw loading
    # ------------------------------------------------------------------
    def load_raw(self, path: Path) -> Any:  # type: ignore[override]
        raise NotImplementedError("load_raw() must be implemented by concrete loaders.")

    # ------------------------------------------------------------------
    # Metadata extraction
    # ------------------------------------------------------------------
    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:  # type: ignore[override]
        return {}

    # ------------------------------------------------------------------
    # Universal conversion
    # ------------------------------------------------------------------
    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:  # type: ignore[override]
        raise NotImplementedError("to_universal() must be implemented by concrete loaders.")

    # ------------------------------------------------------------------
    # Full load pipeline
    # ------------------------------------------------------------------
    def load(self, path: Path) -> RawDataBundle:  # type: ignore[override]
        """
        Full v2.2 loader pipeline:

            1. load_raw()
            2. extract_metadata()
            3. to_universal()
            4. wrap into RawDataBundle

        Loaders do NOT determine technique. That is handled by the
        detection engine and routing layer.
        """
        try:
            raw = self.load_raw(path)
        except Exception as exc:
            raise LoaderReadError(f"Failed to read file '{path}': {exc}") from exc

        try:
            metadata = self.extract_metadata(raw)
        except Exception as exc:
            raise LoaderMetadataError(f"Failed to extract metadata from '{path}': {exc}") from exc

        try:
            universal = self.to_universal(raw, metadata)
        except Exception as exc:
            raise LoaderNormalizationError(
                f"Failed to convert '{path}' to universal format: {exc}"
            ) from exc

        # Ensure metadata is a plain dict
        if not isinstance(metadata, dict):
            metadata = dict(metadata)

        return RawDataBundle(
            technique=Technique.UNKNOWN,  # technique is determined upstream
            data=universal,
            metadata=metadata,
            source_path=str(path),
        )
