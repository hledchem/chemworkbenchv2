import matplotlib.pyplot as plt

def apply_default_style():
    plt.style.use("default")
    plt.rcParams.update({
        "axes.grid": True,
        "grid.alpha": 0.3,
        "font.size": 12,
        "figure.dpi": 120,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
