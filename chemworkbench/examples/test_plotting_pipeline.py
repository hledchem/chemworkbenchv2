from chemworkbench.core.pipeline import run_pipeline
from chemworkbench.processors.uvvis.processor import UVVisProcessor
from chemworkbench.processors.uvvis.config import UVVisConfig
from chemworkbench.utils.plotting_utils import render_dashboard, show_dashboard

# Fake test data (simple sine wave)
import numpy as np
x = np.linspace(200, 800, 1000)
y = np.sin(x / 40) + 0.1 * np.random.randn(len(x))

data = {
    "x": x.tolist(),
    "y": y.tolist(),
}

processor = UVVisProcessor()
config = UVVisConfig()

result = run_pipeline(processor, config, data)

figures = render_dashboard(result)
show_dashboard(figures)
