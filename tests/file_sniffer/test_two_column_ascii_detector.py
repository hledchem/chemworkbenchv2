from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_twocolumn_ascii_detector(tmp_path):
    p = tmp_path / "two.txt"
    p.write_text("1 2\n3 4\n")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(p, p.read_bytes())

    assert fmt == "ascii_twocolumn"
    assert conf > 0.5
