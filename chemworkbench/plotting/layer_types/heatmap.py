import numpy as np

from chemworkbench.core.models import PlotLayerConfig


def render_heatmap(ax, layer: PlotLayerConfig):
    if layer.z is None:
        return
    data = np.array(layer.z)
    ax.imshow(
        data,
        cmap=layer.cmap,
        aspect="auto",
        origin="lower",
        alpha=layer.alpha,
    )
