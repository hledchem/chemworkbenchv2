from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_raman_dpt_detector(tmp_path):
    p = tmp_path / "raman.dpt"
    p.write_text("XYDATA\n100 200\n101 201\n")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(p, p.read_bytes())

    assert fmt == "raman_dpt_ascii"
    assert conf > 0.5
