from typing import Dict, List

from chemworkbench.plotting.schema import FigureSchema, PanelSchema, TraceSchema


class GraphRegistry:
    """
    Registry for named graph templates.

    Keys are lower_snake_case strings (e.g. "uvvis_spectrum").
    Values are callables or factories that return FigureSchema instances.
    """

    def __init__(self) -> None:
        self._registry: Dict[str, FigureSchema] = {}

    def register(self, name: str, figure_schema: FigureSchema) -> None:
        if name in self._registry:
            raise ValueError(f"Graph '{name}' is already registered")
        self._registry[name] = figure_schema

    def get(self, name: str) -> FigureSchema:
        try:
            return self._registry[name]
        except KeyError as exc:
            raise KeyError(f"Graph '{name}' is not registered") from exc

    def list_graphs(self) -> List[str]:
        return sorted(self._registry.keys())


_global_graph_registry: GraphRegistry | None = None


def get_global_graph_registry() -> GraphRegistry:
    global _global_graph_registry
    if _global_graph_registry is None:
        _global_graph_registry = GraphRegistry()
        _bootstrap_default_graphs(_global_graph_registry)
    return _global_graph_registry


def _bootstrap_default_graphs(registry: GraphRegistry) -> None:
    """
    Register a few canonical graphs that processors and UIs can rely on.
    """

    # Simple UV-Vis spectrum
    uvvis_figure = FigureSchema(
        id="uvvis_spectrum",
        title="UV-Vis Spectrum",
        n_rows=1,
        n_cols=1,
        panels=[
            PanelSchema(
                id="main",
                title="UV-Vis Spectrum",
                x_label="Wavelength (nm)",
                y_label="Absorbance (a.u.)",
                row=0,
                col=0,
            )
        ],
    )
    registry.register("uvvis_spectrum", uvvis_figure)

    # Placeholder multi-panel dashboard
    dashboard_figure = FigureSchema(
        id="multi_panel_dashboard",
        title="Multi-Panel Dashboard",
        n_rows=2,
        n_cols=2,
        panels=[
            PanelSchema(id="panel_1", row=0, col=0),
            PanelSchema(id="panel_2", row=0, col=1),
            PanelSchema(id="panel_3", row=1, col=0),
            PanelSchema(id="panel_4", row=1, col=1),
        ],
    )
    registry.register("multi_panel_dashboard", dashboard_figure)
