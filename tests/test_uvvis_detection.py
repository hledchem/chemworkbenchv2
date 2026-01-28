from chemworkbench.core.detection_engine import DetectionEngine
from chemworkbench.core.models import Technique


def test_uvvis_detection():
    engine = DetectionEngine()

    file_path = "data/UV/Absorbance_Sample1.csv"
    header = ["Wavelength (nm)", "Absorbance"]
    sample_text = "Wavelength,Absorbance\n200,0.123\n250,0.456"

    tech = engine.detect(file_path, header, sample_text)

    assert tech == Technique.UVVIS
