from chemworkbench.core.models import PlotLayerConfig


def render_pie(ax, layer: PlotLayerConfig):
    if layer.y is None:
        return

    labels = layer.labels
    explode = layer.explode
    values = layer.y

    ax.pie(
        values,
        labels=labels,
        explode=explode,
        autopct="%1.1f%%" if layer.normalize else None,
        colors=None if layer.color is None else [layer.color] * len(values),
    )
