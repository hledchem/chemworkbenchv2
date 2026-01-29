from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_fluorescence_ascii_detector(tmp_path):
    p = tmp_path / "fl.txt"
    p.write_text("200 1000\n201 1100\n202 1200\n")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(p, p.read_bytes())

    assert fmt == "fluorescence_ascii"
    assert conf > 0.5
