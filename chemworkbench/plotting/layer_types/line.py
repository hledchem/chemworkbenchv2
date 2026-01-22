from chemworkbench.core.models import PlotLayerConfig


def render_line(ax, layer: PlotLayerConfig):
    ax.plot(
        layer.x,
        layer.y,
        color=layer.color,
        linewidth=layer.linewidth,
        linestyle=layer.linestyle,
        marker=layer.marker,
        markersize=layer.markersize,
        alpha=layer.alpha,
        label=layer.label,
    )
