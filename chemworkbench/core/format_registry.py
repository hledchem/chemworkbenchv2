"""
ChemWorkBench v2.2 — Structural Format Registry
===============================================

Purpose
-------
This module defines the canonical registry for *structural data formats*.
It is the authoritative mapping between:

    format_id  →  FormatDescriptor  →  loader_key

This registry is used by the v2.2 ingestion engine to resolve which loader
should be invoked after the file-sniffer determines the structural format.

Design Principles (v2.2)
------------------------
• Format IDs represent *structural families*, not vendors or techniques.
• Loaders are mapped by loader_key, not by vendor or technique.
• Technique detection is handled separately by the anchor engine.
• Registry is deterministic, explicit, and LLM-queryable.
• Plugins may register new formats without modifying core code.
• Format descriptors include:
      - id: canonical format identifier
      - family: structural family (csv, ascii, jcamp, vendor_dir, etc.)
      - vendor: optional vendor hint (agilent, bruker, thermo, etc.)
      - version: optional version tag
      - loader_key: key used by LoaderRegistry to resolve loader class

Future-Proofing Notes
---------------------
This registry is designed for:
• AI-driven format expansion (LLMs can safely add new formats)
• Vendor-specific variants (e.g., agilent_masshunter_dir_v2)
• Versioned formats (e.g., jcamp_dx_v5)
• Multi-loader families (e.g., ascii_2col vs ascii_multicol)
• Plugin ecosystems (third-party loaders, research formats)
• Deterministic ingestion (no ambiguity in loader resolution)

Public API
----------
- FormatDescriptor
- FormatRegistry
- build_default_format_registry()  (in format_registry_init.py)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Iterable


# ======================================================================
# Format Descriptor
# ======================================================================

@dataclass(frozen=True)
class FormatDescriptor:
    """
    Canonical description of a structural data format.

    Attributes
    ----------
    id : str
        Canonical format identifier (e.g., "generic_csv_headered").
    family : str
        Structural family ("csv", "ascii", "jcamp", "vendor_dir", etc.).
    vendor : Optional[str]
        Optional vendor hint ("agilent", "bruker", "thermo", etc.).
    version : Optional[str]
        Optional version tag ("1.0", "v2", etc.).
    loader_key : str
        Key used by LoaderRegistry to resolve the correct loader class.

    Notes
    -----
    • This object is intentionally immutable (frozen=True).
    • LLMs and plugins can safely construct new descriptors.
    • Format IDs must be globally unique.
    """

    id: str
    family: str
    vendor: Optional[str]
    version: Optional[str]
    loader_key: str


# ======================================================================
# Format Registry
# ======================================================================

class FormatRegistry:
    """
    Canonical v2.2 registry for structural data formats.

    Responsibilities
    ----------------
    • Store and retrieve FormatDescriptor objects.
    • Provide deterministic lookup by format_id.
    • Support plugin registration.
    • Provide introspection for LLMs and developer tools.

    Non-Responsibilities
    --------------------
    • Loader resolution (handled by LoaderRegistry).
    • Technique detection (handled by anchor engine).
    • File sniffing (handled by file_sniffer subsystem).

    Future-Proofing
    ---------------
    • Registry is intentionally simple and explicit.
    • Plugins may register new formats without modifying core code.
    • LLMs can query registry contents for reasoning and debugging.
    """

    def __init__(self) -> None:
        self._formats: Dict[str, FormatDescriptor] = {}
        self._plugins: Dict[str, FormatDescriptor] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, desc: FormatDescriptor) -> None:
        """
        Register a built-in format descriptor.

        Built-in formats should be deterministic and stable across versions.
        """
        self._formats[desc.id] = desc

    def register_plugin(self, desc: FormatDescriptor) -> None:
        """
        Register a plugin-provided format descriptor.

        Plugins may override built-in formats if necessary.
        """
        self._plugins[desc.id] = desc

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, format_id: str) -> FormatDescriptor:
        """
        Retrieve a FormatDescriptor by its canonical format_id.

        Plugin formats override built-in formats.
        """
        if format_id in self._plugins:
            return self._plugins[format_id]
        return self._formats[format_id]

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def all_format_ids(self) -> Iterable[str]:
        """Return all registered format IDs (built-in + plugins)."""
        return list(self._formats.keys()) + list(self._plugins.keys())

    def all_descriptors(self) -> Iterable[FormatDescriptor]:
        """Return all FormatDescriptor objects."""
        return list(self._formats.values()) + list(self._plugins.values())

    def families(self) -> Iterable[str]:
        """Return all structural families present in the registry."""
        return sorted({desc.family for desc in self.all_descriptors()})

    def vendors(self) -> Iterable[str]:
        """Return all vendors present in the registry."""
        return sorted({
            desc.vendor for desc in self.all_descriptors()
            if desc.vendor is not None
        })

    def __contains__(self, format_id: str) -> bool:
        return format_id in self._formats or format_id in self._plugins

    def __len__(self) -> int:
        return len(self._formats) + len(self._plugins)

    def __repr__(self) -> str:
        return (
            f"<FormatRegistry builtins={len(self._formats)} "
            f"plugins={len(self._plugins)}>"
        )
