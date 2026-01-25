import pytest
from pathlib import Path

from chemworkbench.utils.loaders.agilent.agilent_d_chrom_loader import AgilentDChromLoader


def test_d_chrom_sniff(tmp_path):
    # Create a fake .D directory
    ddir = tmp_path / "sample.D"
    ddir.mkdir()

    # Add a chromatogram-like CSV file
    chrom = ddir / "CHROM1.CSV"
    chrom.write_text("0,10\n1,20\n2,30\n")

    loader = AgilentDChromLoader()

    # Should sniff correctly
    assert loader.sniff(str(ddir)) is True


def test_d_chrom_load_raw(tmp_path):
    ddir = tmp_path / "sample.D"
    ddir.mkdir()

    chrom = ddir / "CHROM1.CSV"
    chrom.write_text("0,10\n1,20\n2,30\n")

    loader = AgilentDChromLoader()

    raw = loader.load_raw(str(ddir))

    assert "chromatograms" in raw
    assert "CHROM1.CSV" in raw["chromatograms"]

    trace = raw["chromatograms"]["CHROM1.CSV"]
    assert trace["time"] == [0.0, 1.0, 2.0]
    assert trace["intensity"] == [10.0, 20.0, 30.0]


def test_d_chrom_metadata(tmp_path):
    ddir = tmp_path / "sample.D"
    ddir.mkdir()

    chrom = ddir / "CHROM1.CSV"
    chrom.write_text("0,10\n1,20\n2,30\n")

    loader = AgilentDChromLoader()
    raw = loader.load_raw(str(ddir))
    meta = loader.extract_metadata(raw)

    assert meta["vendor"] == "agilent"
    assert meta["format"] == "d_chrom"
    assert meta["num_traces"] == 1
    assert meta["trace_names"] == ["CHROM1.CSV"]


def test_d_chrom_to_universal(tmp_path):
    ddir = tmp_path / "sample.D"
    ddir.mkdir()

    chrom = ddir / "CHROM1.CSV"
    chrom.write_text("0,10\n1,20\n2,30\n")

    loader = AgilentDChromLoader()
    raw = loader.load_raw(str(ddir))
    meta = loader.extract_metadata(raw)
    uni = loader.to_universal(raw, meta)

    assert uni["kind"] == "chromatogram_set"
    assert "chromatograms" in uni
    assert uni["axis_units"]["x"] == "min"
    assert uni["axis_units"]["y"] == "intensity"
