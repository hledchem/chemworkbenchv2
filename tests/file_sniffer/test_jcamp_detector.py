from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_jcamp_detector(tmp_path):
    p = tmp_path / "sample.dx"
    p.write_text("##TITLE= Test\n##JCAMP-DX= 5.01\n##XYDATA= (X++(Y..Y))\n")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(p, p.read_bytes())

    assert fmt == "jcamp_dx"
    assert conf > 0.5
