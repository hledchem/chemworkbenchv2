from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_waters_raw_detector(tmp_path):
    raw_dir = tmp_path / "sample.RAW"
    raw_dir.mkdir()
    (raw_dir / "_FUNC001.DAT").write_text("x")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(raw_dir, None)

    assert fmt == "waters_raw_dir"
    assert conf > 0.5
