from chemworkbench.core.models import PlotLayerConfig


def render_histogram(ax, layer: PlotLayerConfig):
    if layer.y is None:
        return

    ax.hist(
        layer.y,
        bins=layer.bins if layer.bins is not None else 30,
        color=layer.color,
        alpha=layer.alpha,
        stacked=layer.stacked,
        label=layer.label,
    )
