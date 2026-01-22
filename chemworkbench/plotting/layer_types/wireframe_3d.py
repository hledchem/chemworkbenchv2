import numpy as np

from chemworkbench.core.models import PlotLayerConfig


def render_3d_wireframe(ax, layer: PlotLayerConfig):
    if layer.x is None or layer.y is None or layer.z is None:
        return

    X = np.array(layer.x)
    Y = np.array(layer.y)
    Z = np.array(layer.z)

    # Try to reshape if z is 1D
    if Z.ndim == 1 and X.size * Y.size == Z.size:
        Z = Z.reshape(len(Y), len(X))

    ax.plot_wireframe(
        X,
        Y,
        Z,
        color=layer.color,
        alpha=layer.alpha,
    )
