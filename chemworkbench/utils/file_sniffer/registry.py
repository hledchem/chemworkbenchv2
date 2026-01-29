from .detectors.spc_detector import SPCDetector
from .detectors.opus_detector import OpusDetector
from .detectors.agilent_masshunter_detector import AgilentMassHunterDetector
from .detectors.bruker_nmr_detector import BrukerNMRDetector
from .detectors.varian_fid_detector import VarianFIDDetector
from .detectors.waters_raw_detector import WatersRAWDetector
from .detectors.jeol_jdf_detector import JeolJDFDetector

from .detectors.raman_dpt_detector import RamanDPTDetector
from .detectors.fluorescence_ascii_detector import FluorescenceAsciiDetector
from .detectors.uvvis_ascii_detector import UVVisAsciiDetector
from .detectors.ir_ascii_detector import IRAsciiDetector

from .detectors.jcamp_detector import JCAMPDetector
from .detectors.netcdf_detector import NetCDFDetector

from .detectors.multicolumn_ascii_detector import MultiColumnAsciiDetector
from .detectors.twocolumn_ascii_detector import TwoColumnAsciiDetector


DETECTOR_CLASSES = [
    # Binary spectroscopy
    SPCDetector,
    OpusDetector,
    JeolJDFDetector,

    # Vendor directory structures
    AgilentMassHunterDetector,
    BrukerNMRDetector,
    VarianFIDDetector,
    WatersRAWDetector,

    # Spectroscopy ASCII
    RamanDPTDetector,
    FluorescenceAsciiDetector,
    UVVisAsciiDetector,
    IRAsciiDetector,
    JCAMPDetector,

    # Chromatography interchange
    NetCDFDetector,

    # Generic ASCII fallbacks
    MultiColumnAsciiDetector,
    TwoColumnAsciiDetector,
]
