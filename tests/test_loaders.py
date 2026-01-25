import pytest
from chemworkbench.utils.loaders.registry import iter_loaders

def test_loader_sniff_and_universal(tmp_path):
    # Create a synthetic CSV file
    p = tmp_path / "fake.csv"
    p.write_text("1,2\n3,4\n")

    for loader in iter_loaders():
        if loader.sniff(str(p)):
            raw = loader.load_raw(str(p))
            meta = loader.extract_metadata(raw)
            univ = loader.to_universal(raw, meta)

            assert "x" in univ
            assert "y" in univ
            assert "axis_units" in univ
            return

    pytest.fail("No loader sniffed the synthetic CSV file")
