from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_jdf_detector(tmp_path):
    p = tmp_path / "sample.jdf"
    p.write_bytes(b"JEOL\x00\x01\x02")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(p, p.read_bytes())

    assert fmt == "jeol_jdf_binary"
    assert conf > 0.5
