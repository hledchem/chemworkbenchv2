from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_varian_fid_detector(tmp_path):
    d = tmp_path / "fid_dir"
    d.mkdir()
    (d / "fid").write_text("x")
    (d / "procpar").write_text("x")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(d, None)

    assert fmt == "varian_fid_dir"
    assert conf > 0.5
