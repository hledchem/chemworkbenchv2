import pytest
from chemworkbench.utils.loaders.loader_registry import LOADER_REGISTRY, iter_loaders
from chemworkbench.utils.loaders.base_loader import BaseVendorLoader

def test_registry_keys_are_lowercase():
    for (vendor, fmt) in LOADER_REGISTRY.keys():
        assert vendor == vendor.lower()
        assert fmt == fmt.lower()

def test_registry_values_are_loader_classes():
    for cls in LOADER_REGISTRY.values():
        assert issubclass(cls, BaseVendorLoader)

def test_iter_loaders_instantiates_all():
    for loader in iter_loaders():
        assert isinstance(loader, BaseVendorLoader)
        assert hasattr(loader, "sniff")
        assert hasattr(loader, "load_raw")
        assert hasattr(loader, "extract_metadata")
        assert hasattr(loader, "to_universal")
