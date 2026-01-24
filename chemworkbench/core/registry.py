from __future__ import annotations

from pathlib import Path
from typing import List, Type

from chemworkbench.utils.loaders.base_loader import BaseVendorLoader

# Universal loaders
from chemworkbench.utils.loaders.csv_loader import CSVLoader
from chemworkbench.utils.loaders.xlsx_loader import XLSXLoader
from chemworkbench.utils.loaders.jcamp_loader import JCAMPLoader

# Vendor loaders
from chemworkbench.utils.loaders.agilent import (
    AgilentUVLoader,
    AgilentSPLoader,
    AgilentDUVVisLoader,
    AgilentDChromLoader,
)

from chemworkbench.utils.loaders.bruker import (
    BrukerOPUSLoader,
    BrukerNMRLoader,
    BrukerEPRLoader,
)

from chemworkbench.utils.loaders.thermo import (
    ThermoSPALoader,
    ThermoSPCLoader,
    ThermoSRSLoader,
)

from chemworkbench.utils.loaders.shimadzu import (
    ShimadzuSPCLoader,
    ShimadzuIRXLoader,
    ShimadzuUVSLoader,
    ShimadzuLCDLoader,
)

from chemworkbench.utils.loaders.perkinelmer import (
    PerkinElmerSPLoader,
    PerkinElmerSPCLoader,
)

from chemworkbench.utils.loaders.waters import WatersRAWLoader
from chemworkbench.utils.loaders.jeol import JEOLJDFLoader
from chemworkbench.utils.loaders.varian import VarianNMRLoader

# Raman loaders
from chemworkbench.utils.loaders.raman import (
    DPTLoader,
    RRUFFLoader,
    RRUFFGZLoader,
)

# New vendor loaders
from chemworkbench.utils.loaders.horiba import HoribaFluorescenceLoader
from chemworkbench.utils.loaders.ch_instruments import CHIDTALoader


class LoaderRegistry:
    """
    Central registry for all loaders.
    """

    def __init__(self):
        self.loaders: List[Type[BaseVendorLoader]] = [
            # Universal
            CSVLoader,
            XLSXLoader,
            JCAMPLoader,

            # Vendor loaders
            AgilentUVLoader,
            AgilentSPLoader,
            AgilentDUVVisLoader,
            AgilentDChromLoader,

            BrukerOPUSLoader,
            BrukerNMRLoader,
            BrukerEPRLoader,

            ThermoSPALoader,
            ThermoSPCLoader,
            ThermoSRSLoader,

            ShimadzuSPCLoader,
            ShimadzuIRXLoader,
            ShimadzuUVSLoader,
            ShimadzuLCDLoader,

            PerkinElmerSPLoader,
            PerkinElmerSPCLoader,

            WatersRAWLoader,
            JEOLJDFLoader,
            VarianNMRLoader,

            # Raman
            DPTLoader,
            RRUFFLoader,
            RRUFFGZLoader,

            # New vendors
            HoribaFluorescenceLoader,
            CHIDTALoader,
        ]

    def sniff_loader(self, path: Path) -> BaseVendorLoader:
        """
        Return the first loader whose sniff() returns True.
        """
        for loader_cls in self.loaders:
            loader = loader_cls()
            if loader.sniff(path):
                return loader
        raise ValueError(f"No loader found for file: {path}")
