from chemworkbench.core.models import PlotLayerConfig


def render_errorbar(ax, layer: PlotLayerConfig):
    ax.errorbar(
        layer.x,
        layer.y,
        yerr=layer.yerr,
        xerr=layer.xerr,
        fmt=layer.marker or "o",
        color=layer.color,
        linewidth=layer.linewidth,
        linestyle=layer.linestyle,
        alpha=layer.alpha,
        label=layer.label,
    )
