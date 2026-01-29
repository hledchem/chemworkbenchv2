from pathlib import Path
from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_engine_confidence_priority(tmp_path):
    p = tmp_path / "uvvis.txt"
    p.write_text("Wavelength Abs\n200 0.5\n201 0.6\n")

    engine = DetectionEngine()
    fmt, conf, reasons = engine.detect(p, p.read_bytes())

    assert fmt == "uvvis_ascii"
    assert conf > 0.8
