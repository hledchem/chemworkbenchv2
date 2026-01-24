from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional

from chemworkbench.plotting.schema.figure_schema import FigureSchema


class GraphRegistry:
    """
    Registry for declarative graph templates.

    Templates are stored as JSON files in:
        chemworkbench/plotting/registry/templates/

    Keys are lower_snake_case identifiers, e.g.:
        "uvvis_spectrum"
        "multi_panel_dashboard"
        "chromatogram"

    The registry loads templates lazily and caches them.
    """

    def __init__(self, template_dir: Optional[Path] = None):
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"

        self.template_dir: Path = template_dir
        self._cache: Dict[str, FigureSchema] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def list_templates(self) -> Dict[str, Path]:
        """
        Return a mapping of template keys → file paths.
        """
        templates = {}
        for file in self.template_dir.glob("*.json"):
            key = file.stem  # lower_snake_case
            templates[key] = file
        return templates

    def get(self, key: str) -> FigureSchema:
        """
        Load a template by key and return a FigureSchema.

        Templates are cached after first load.
        """
        key = key.lower()

        if key in self._cache:
            return self._cache[key]

        file_path = self.template_dir / f"{key}.json"
        if not file_path.exists():
            raise KeyError(f"Graph template '{key}' not found in registry.")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        schema = FigureSchema.from_dict(data)
        self._cache[key] = schema
        return schema

    def reload(self) -> None:
        """
        Clear the cache and reload templates on next access.
        """
        self._cache.clear()


# ----------------------------------------------------------------------
# Global registry instance
# ----------------------------------------------------------------------

_global_registry: Optional[GraphRegistry] = None


def get_global_graph_registry() -> GraphRegistry:
    """
    Return the global GraphRegistry instance.
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = GraphRegistry()
    return _global_registry
