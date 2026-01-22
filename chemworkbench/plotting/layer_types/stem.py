from chemworkbench.core.models import PlotLayerConfig


def render_stem(ax, layer: PlotLayerConfig):
    markerfmt = layer.marker or "o"
    linefmt = layer.color or "C0"
    basefmt = "k-"

    markerline, stemlines, baseline = ax.stem(
        layer.x,
        layer.y,
        linefmt=linefmt,
        markerfmt=markerfmt,
        basefmt=basefmt,
        label=layer.label,
    )
    markerline.set_alpha(layer.alpha)
    stemlines.set_alpha(layer.alpha)
