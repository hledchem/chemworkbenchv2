from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_bruker_nmr_detector(tmp_path):
    d = tmp_path / "bruker"
    d.mkdir()
    (d / "fid").write_bytes(b"\x00\x01")
    (d / "acqus").write_text("x")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(d, None)

    assert fmt == "bruker_nmr_dir"
    assert conf > 0.5
