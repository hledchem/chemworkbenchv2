from chemworkbench.core.models import PlotLayerConfig


def render_step(ax, layer: PlotLayerConfig):
    ax.step(
        layer.x,
        layer.y,
        where="mid",
        color=layer.color,
        linewidth=layer.linewidth,
        linestyle=layer.linestyle,
        alpha=layer.alpha,
        label=layer.label,
    )
