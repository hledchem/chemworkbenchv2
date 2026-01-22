from chemworkbench.core.models import PlotLayerConfig


def render_3d_line(ax, layer: PlotLayerConfig):
    # For 3D line, we interpret:
    # x, y, z as 1D arrays of equal length
    if layer.x is None or layer.y is None or layer.z is None:
        return

    ax.plot3D(
        layer.x,
        layer.y,
        layer.z,  # type: ignore[arg-type]
        color=layer.color,
        linewidth=layer.linewidth,
        linestyle=layer.linestyle,
        alpha=layer.alpha,
        label=layer.label,
    )
