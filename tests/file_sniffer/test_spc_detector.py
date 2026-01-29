from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_spc_detector(tmp_path):
    p = tmp_path / "sample.spc"
    p.write_bytes(b"\x4B\x02XXXX")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(p, p.read_bytes())

    assert fmt == "spc_binary"
    assert conf > 0.5
