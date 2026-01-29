from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_ir_ascii_detector(tmp_path):
    p = tmp_path / "ir.txt"
    p.write_text("Wavenumber Absorbance\n4000 0.1\n3990 0.2\n")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(p, p.read_bytes())

    assert fmt == "ir_ascii"
    assert conf > 0.5
