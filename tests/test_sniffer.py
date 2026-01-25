import os
from chemworkbench.core.models import Technique
from chemworkbench.utils.file_sniffer.file_sniffer import sniff_file

def test_sniffer_unknown_file(tmp_path):
    p = tmp_path / "empty.xyz"
    p.write_text("")

    fmt = sniff_file(str(p))
    assert fmt.vendor is None
    assert fmt.technique == Technique.UNKNOWN

def test_sniffer_csv(tmp_path):
    p = tmp_path / "fake_uvvis.csv"
    p.write_text("200,0.1\n210,0.2\n")

    fmt = sniff_file(str(p))
    assert fmt.vendor == "universal"
    assert fmt.subtype == "csv"
