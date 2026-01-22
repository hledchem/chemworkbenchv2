import numpy as np

from chemworkbench.core.models import PlotLayerConfig


def render_contour(ax, layer: PlotLayerConfig):
    if layer.z is None or layer.x is None or layer.y is None:
        return

    X = np.array(layer.x)
    Y = np.array(layer.y)
    Z = np.array(layer.z)

    # Try to reshape if z is 1D
    if Z.ndim == 1 and X.size * Y.size == Z.size:
        Z = Z.reshape(len(Y), len(X))

    cs = ax.contour(
        X,
        Y,
        Z,
        cmap=layer.cmap,
        alpha=layer.alpha,
    )
    ax.clabel(cs, inline=True, fontsize=8)
