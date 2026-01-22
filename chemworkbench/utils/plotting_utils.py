from typing import List
from chemworkbench.core.models import PipelineResult, PlotConfig
from chemworkbench.plotting.engine.base_engine import PlotEngine
import matplotlib.pyplot as plt

def show_dashboard(figures):
    for fig in figures:
        if fig is not None:
            fig.show()
    plt.show()   # <-- keeps the window open



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

