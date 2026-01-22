import numpy as np

def render_3d_surface(ax, layer):
    X = np.array(layer.x)
    Y = np.array(layer.y)
    Z = np.array(layer.z)
    ax.plot_surface(X, Y, Z, cmap=layer.cmap, alpha=layer.alpha)
