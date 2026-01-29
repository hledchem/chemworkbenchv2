from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_masshunter_detector(tmp_path):
    d = tmp_path / "sample.d"
    d.mkdir()
    (d / "AcqData").mkdir()
    (d / "AcqData" / "sample_info.xml").write_text("<xml>")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(d, None)

    assert fmt == "agilent_masshunter_dir"
    assert conf > 0.5
