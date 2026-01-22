import numpy as np

from chemworkbench.core.models import PlotLayerConfig


def render_image(ax, layer: PlotLayerConfig):
    if layer.z is None:
        return
    data = np.array(layer.z)
    ax.imshow(
        data,
        cmap=layer.cmap,
        aspect="equal",
        origin="lower",
        alpha=layer.alpha,
    )
