import numpy as np

def render_heatmap(ax, layer):
    data = np.array(layer.z)
    ax.imshow(
        data,
        cmap=layer.cmap,
        aspect="auto",
        origin="lower",
        alpha=layer.alpha,
    )
