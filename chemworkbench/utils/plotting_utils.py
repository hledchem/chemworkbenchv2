from typing import List
from chemworkbench.core.models import PipelineResult, PlotConfig
from chemworkbench.plotting.engine.base_engine import PlotEngine


def render_dashboard(result: PipelineResult):
    """
    Processor-agnostic dashboard renderer.
    Takes a PipelineResult and returns a list of Matplotlib figures.
    """
    if not result.plots:
        raise ValueError("No plots found in PipelineResult.")

    # Render all PlotConfig objects using the universal engine
    figures = PlotEngine.render_all(result.plots)
    return figures

def show_dashboard(figures):
    """Convenience helper for local testing."""
    for fig in figures:
        fig.show()
