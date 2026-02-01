"""
ChemWorkBench v2.2 — Pluggable Loader Registry
==============================================

Purpose
-------
This module defines the canonical registry for all loader classes used by
the v2.2 ingestion engine. It maps:

    loader_key  →  LoaderClass

Loader keys are referenced by FormatDescriptor objects in the
FormatRegistry. This decouples structural format detection from loader
resolution and enables a fully pluggable ingestion architecture.

Design Principles (v2.2)
------------------------
• Loaders are *structural-family based*, not technique-based.
• Technique detection is handled separately by the anchor engine.
• Registry is deterministic, explicit, and LLM-queryable.
• Plugins may register new loaders or override existing ones.
• Loader keys must remain stable across versions for reproducibility.

Future-Proofing Notes
---------------------
This registry is designed for:
• AI-driven loader generation (LLMs can safely register new loaders)
• Vendor-specific overrides (e.g., agilent_masshunter_loader_v2)
• Multi-loader families (e.g., ascii_2col vs ascii_multicol)
• Plugin ecosystems (third-party loaders, research formats)
• Deterministic ingestion (no ambiguity in loader resolution)

Public API
----------
- LoaderRegistry.register(key, cls)
- LoaderRegistry.register_plugin(key, cls)
- LoaderRegistry.get(key)
- LoaderRegistry.all_loader_keys()
- LoaderRegistry.all_loader_classes()
"""

from __future__ import annotations

from typing import Dict, Type, Iterable
from pathlib import Path

from chemworkbench.core.models import DetectedFormat, RawDataBundle


# ======================================================================
# Loader Protocol (duck-typed)
# ======================================================================

class BaseLoader:
    """
    Duck-typed protocol for all loaders.

    A loader must implement:

        load(path: Path, detected: DetectedFormat) -> RawDataBundle

    We intentionally avoid using typing.Protocol here to keep the system
    plugin-friendly and avoid forcing strict inheritance.
    """

    def load(self, path: Path, detected: DetectedFormat) -> RawDataBundle:
        raise NotImplementedError("Loader classes must implement .load()")


# ======================================================================
# Loader Registry
# ======================================================================

class LoaderRegistry:
    """
    Canonical v2.2 loader registry.

    Responsibilities
    ----------------
    • Map loader_key → LoaderClass.
    • Provide deterministic lookup for ingestion engine.
    • Support plugin overrides.
    • Provide introspection for LLMs and developer tools.

    Non-Responsibilities
    --------------------
    • Structural format detection (handled by FormatRegistry + sniffer).
    • Technique detection (handled by anchor engine).
    • File reading logic (handled by loader classes).

    Future-Proofing
    ---------------
    • Registry is intentionally simple and explicit.
    • Plugins may override built-in loaders.
    • LLMs can query registry contents for reasoning and debugging.
    """

    def __init__(self) -> None:
        self._loaders: Dict[str, Type[BaseLoader]] = {}
        self._plugins: Dict[str, Type[BaseLoader]] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, key: str, loader_cls: Type[BaseLoader]) -> None:
        """
        Register a built-in loader class.

        Built-in loaders should be deterministic and stable across versions.
        """
        self._loaders[key] = loader_cls

    def register_plugin(self, key: str, loader_cls: Type[BaseLoader]) -> None:
        """
        Register a plugin-provided loader class.

        Plugins may override built-in loaders if necessary.
        """
        self._plugins[key] = loader_cls

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, key: str) -> Type[BaseLoader]:
        """
        Retrieve a loader class by its loader_key.

        Plugin loaders override built-in loaders.
        """
        if key in self._plugins:
            return self._plugins[key]
        return self._loaders[key]

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def all_loader_keys(self) -> Iterable[str]:
        """Return all loader keys (built-in + plugins)."""
        return list(self._loaders.keys()) + list(self._plugins.keys())

    def all_loader_classes(self) -> Iterable[Type[BaseLoader]]:
        """Return all loader classes."""
        return list(self._loaders.values()) + list(self._plugins.values())

    def __contains__(self, key: str) -> bool:
        return key in self._loaders or key in self._plugins

    def __len__(self) -> int:
        return len(self._loaders) + len(self._plugins)

    def __repr__(self) -> str:
        return (
            f"<LoaderRegistry builtins={len(self._loaders)} "
            f"plugins={len(self._plugins)}>"
        )
