from chemworkbench.core.models import PlotLayerConfig


def render_3d_scatter(ax, layer: PlotLayerConfig):
    if layer.x is None or layer.y is None or layer.z is None:
        return

    ax.scatter3D(
        layer.x,
        layer.y,
        layer.z,  # type: ignore[arg-type]
        c=layer.color,
        marker=layer.marker or "o",
        s=(layer.markersize or 4.0) ** 2,
        alpha=layer.alpha,
    )
