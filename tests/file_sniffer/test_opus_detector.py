from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_opus_detector(tmp_path):
    p = tmp_path / "sample.0"
    p.write_bytes(b"##TITLE= OPUS FILE")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(p, p.read_bytes())

    assert fmt == "opus_binary"
    assert conf > 0.5
