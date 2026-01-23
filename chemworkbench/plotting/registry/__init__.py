"""
Graph registry for reusable, named plotting configurations.

Processors and UIs can request graphs by name (e.g. "uvvis_spectrum"),
and the registry returns a FigureSchema that can be built into PlotConfig
objects via the PlotConfigBuilder.
"""

from .graph_registry import GraphRegistry, get_global_graph_registry

__all__ = ["GraphRegistry", "get_global_graph_registry"]
