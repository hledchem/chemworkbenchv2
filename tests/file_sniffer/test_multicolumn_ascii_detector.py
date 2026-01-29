from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_multicolumn_ascii_detector(tmp_path):
    p = tmp_path / "multi.csv"
    p.write_text("1 2 3\n4 5 6\n")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(p, p.read_bytes())

    assert fmt == "ascii_multicolumn"
    assert conf > 0.5
