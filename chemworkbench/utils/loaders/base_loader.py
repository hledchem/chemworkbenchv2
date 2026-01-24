"""
Base loader protocol and common abstractions for all vendor and universal loaders.

All concrete loaders (e.g., Agilent, Bruker, Thermo, Waters, etc.) should inherit
from `BaseVendorLoader` and implement the abstract methods defined here.

This module is intentionally vendor- and technique-agnostic. It defines:
- The canonical loader interface (`BaseLoaderProtocol`)
- A concrete base class (`BaseVendorLoader`) with shared utilities
- A standard result container (`LoaderResult`)
- Common exceptions for loader failures
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class LoaderError(Exception):
    """Base exception for all loader-related errors."""


class LoaderSniffError(LoaderError):
    """Raised when a loader cannot confidently identify a file as its own."""


class LoaderReadError(LoaderError):
    """Raised when a loader fails while reading or parsing raw data."""


class LoaderMetadataError(LoaderError):
    """Raised when metadata extraction fails."""


class LoaderNormalizationError(LoaderError):
    """Raised when conversion to the universal data model fails."""


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------


@dataclass
class LoaderResult:
    """
    Canonical output of any loader.

    This is the handshake object between loaders and the rest of the system.
    It is intentionally generic so that:
    - Loaders can return whatever raw structures they need internally
    - Processors and the pipeline can rely on consistent keys and semantics
    """

    # Raw, vendor-specific data structure (e.g., parsed binary, dict, DataFrame, etc.)
    raw_data: Any

    # Normalized, universal representation (e.g., spectral arrays, chromatograms, etc.)
    universal_data: Any

    # Metadata as a simple mapping (instrument, acquisition, sample, etc.)
    metadata: Mapping[str, Any]

    # Optional hints for routing/processing (e.g., "uvvis", "ir", "nmr", "chrom", "ms")
    technique_hint: Optional[str] = None

    # Optional vendor/format identifiers (e.g., "agilent", "bruker_opus", "waters_raw")
    vendor: Optional[str] = None
    format_name: Optional[str] = None


# ---------------------------------------------------------------------------
# Protocol definition
# ---------------------------------------------------------------------------


@runtime_checkable
class BaseLoaderProtocol(Protocol):
    """
    Structural protocol for all loaders.

    Any loader (class or instance) that satisfies this protocol can be used
    by the pipeline, regardless of its concrete base class.
    """

    # Class-level identifiers (should be overridden by concrete loaders)
    VENDOR: str
    FORMAT: str  # e.g., "opus", "d_uvvis", "raw", "jcamp"
    EXTENSIONS: tuple[str, ...]  # file extensions this loader can handle

    def sniff(self, path: Path) -> bool:
        """
        Lightweight check: does this file *look like* something this loader can handle?

        This should be:
        - Fast (no heavy parsing)
        - Conservative (return False if unsure)
        - Deterministic

        Returns:
            True if the loader believes it can handle this file, False otherwise.
        """
        ...

    def load_raw(self, path: Path) -> Any:
        """
        Read and parse the vendor-specific file into a raw in-memory structure.

        This method is allowed to be relatively heavy (I/O, parsing, etc.).

        Raises:
            LoaderReadError on failure.
        """
        ...

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:
        """
        Extract metadata from the raw vendor-specific structure.

        This should return a simple mapping (dict-like) with stable keys such as:
        - "instrument"
        - "acquisition_datetime"
        - "operator"
        - "sample_id"
        - "method_name"
        - etc.

        Raises:
            LoaderMetadataError on failure.
        """
        ...

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:
        """
        Convert the raw vendor-specific structure into the universal data model.

        The exact type of the universal data is defined by the core models layer
        (e.g., spectral arrays, chromatograms, NMR datasets, etc.).

        Raises:
            LoaderNormalizationError on failure.
        """
        ...

    def load(self, path: Path) -> LoaderResult:
        """
        High-level convenience method: full load pipeline.

        Steps:
        1. load_raw(path)
        2. extract_metadata(raw_data)
        3. to_universal(raw_data, metadata)
        4. wrap into LoaderResult

        Raises:
            LoaderError subclasses on failure.
        """
        ...


# ---------------------------------------------------------------------------
# Concrete base class
# ---------------------------------------------------------------------------


class BaseVendorLoader(BaseLoaderProtocol):
    """
    Concrete base class implementing the common loader pipeline.

    Vendor-specific loaders should inherit from this and override:
    - VENDOR
    - FORMAT
    - EXTENSIONS
    - sniff()
    - load_raw()
    - extract_metadata()
    - to_universal()
    """

    # Sensible defaults; concrete loaders MUST override these.
    VENDOR: str = "generic"
    FORMAT: str = "generic"
    EXTENSIONS: tuple[str, ...] = ()

    def sniff(self, path: Path) -> bool:  # type: ignore[override]
        """
        Default sniff implementation: checks file extension only.

        Concrete loaders are encouraged to override this with more robust logic
        (e.g., magic bytes, header inspection, directory structure checks).
        """
        suffix = path.suffix.lower()
        return suffix in {ext.lower() for ext in self.EXTENSIONS}

    def load_raw(self, path: Path) -> Any:  # type: ignore[override]
        """
        Default implementation raises, forcing concrete loaders to implement.

        Concrete loaders must implement this method.
        """
        raise NotImplementedError("load_raw() must be implemented by concrete loaders.")

    def extract_metadata(self, raw_data: Any) -> Mapping[str, Any]:  # type: ignore[override]
        """
        Default implementation returns an empty dict.

        Concrete loaders are encouraged to override this to provide rich metadata.
        """
        return {}

    def to_universal(self, raw_data: Any, metadata: Mapping[str, Any]) -> Any:  # type: ignore[override]
        """
        Default implementation raises, forcing concrete loaders to implement.

        Concrete loaders must implement this method to produce the universal data model.
        """
        raise NotImplementedError("to_universal() must be implemented by concrete loaders.")

    def load(self, path: Path) -> LoaderResult:  # type: ignore[override]
        """
        Full load pipeline with standardized error handling.

        This method orchestrates:
        - sniff (optional, may be used by the caller instead)
        - load_raw
        - extract_metadata
        - to_universal
        - packaging into LoaderResult
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
                f"Failed to normalize data from '{path}' to universal model: {exc}"
            ) from exc

        # Ensure metadata is a plain dict for serialization friendliness
        if not isinstance(metadata, dict):
            metadata = dict(metadata)

        return LoaderResult(
            raw_data=raw,
            universal_data=universal,
            metadata=metadata,
            technique_hint=self._infer_technique_hint(metadata),
            vendor=self.VENDOR,
            format_name=self.FORMAT,
        )

    # ---------------------------------------------------------------------
    # Optional helpers
    # ---------------------------------------------------------------------

    def _infer_technique_hint(self, metadata: Mapping[str, Any]) -> Optional[str]:
        """
        Optional helper to infer a technique hint from metadata.

        Concrete loaders may override this to provide better hints, e.g.:
        - "uvvis"
        - "ir"
        - "raman"
        - "nmr"
        - "chrom"
        - "ms"
        """
        technique = metadata.get("technique") or metadata.get("measurement_type")
        if isinstance(technique, str):
            return technique.lower()
        return None
