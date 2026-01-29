from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_netcdf_detector(tmp_path):
    p = tmp_path / "sample.cdf"
    p.write_bytes(b"CDF\x01xxxx")

    engine = DetectionEngine()
    fmt, conf, _ = engine.detect(p, p.read_bytes())

    assert fmt == "netcdf_andi_ms"
    assert conf > 0.5
