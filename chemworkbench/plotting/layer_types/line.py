def render_line(ax, layer):
    ax.plot(
        layer.x,
        layer.y,
        color=layer.color,
        linewidth=layer.linewidth,
        linestyle=layer.linestyle,
        alpha=layer.alpha,
        label=layer.label,
    )
