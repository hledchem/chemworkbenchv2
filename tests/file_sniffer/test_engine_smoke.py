from chemworkbench.utils.file_sniffer.engine import DetectionEngine

def test_engine_initializes():
    engine = DetectionEngine()
    assert len(engine.detectors) > 5
  
