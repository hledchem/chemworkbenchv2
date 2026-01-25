from chemworkbench.core.models import Technique
from chemworkbench.processors.uvvis_processor import UVVisProcessor

def test_uvvis_processor_pipeline():
    synthetic = {
        "kind": "spectrum",
        "x": [200, 210, 220, 230],
        "y": [0.1, 0.2, 0.3, 0.25],
        "axis_units": {"x": "nm", "y": "absorbance"},
    }

    metadata = {"vendor": "synthetic", "format": "synthetic"}

    processor = UVVisProcessor()
    result = processor.process(synthetic, metadata)

    assert result.technique == Technique.UVVIS
    assert isinstance(result.results, dict)
    assert isinstance(result.plot_config, dict)
    assert "series" in result.plot_config
