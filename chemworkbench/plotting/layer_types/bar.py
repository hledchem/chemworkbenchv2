from chemworkbench.core.models import PlotLayerConfig


def render_bar(ax, layer: PlotLayerConfig):
    ax.bar(
        layer.x,
        layer.y,
        width=layer.width if layer.width is not None else 0.8,
        color=layer.color,
        alpha=layer.alpha,
        label=layer.label,
    )
