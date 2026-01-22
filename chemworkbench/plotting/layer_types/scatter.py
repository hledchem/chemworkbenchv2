from chemworkbench.core.models import PlotLayerConfig


def render_scatter(ax, layer: PlotLayerConfig):
    ax.scatter(
        layer.x,
        layer.y,
        color=layer.color,
        marker=layer.marker or "o",
        s=(layer.markersize or 4.0) ** 2,
        alpha=layer.alpha,
        label=layer.label,
    )
