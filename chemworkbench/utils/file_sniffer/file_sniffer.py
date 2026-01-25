"""
utils/file_sniffer/file_sniffer.py

ChemWorkBench v2 unified file sniffer.
This module performs 3-tier detection:

1. Core detectors (extension, magic bytes, directory structure)
2. Spectral detectors (technique-level inference)
3. Vendor-specific detectors (Agilent, Bruker, Thermo, etc.)

Output: DetectedFormat(vendor, technique, subtype, confidence)
"""

from __future__ import annotations
import os
from typing import List

from chemworkbench.core.models import Technique, DetectedFormat

# Tier 1 detectors
from .core_detectors import detect_by_extension, detect_magic_bytes

# Tier 2 detectors
from .spectral_detectors import infer_technique_from_data

# Tier 3 vendor detectors
from .vendor.agilent_detectors import detect_agilent
from .vendor.bruker_detectors import detect_bruker
from .vendor.thermo_detectors import detect_thermo
from .vendor.shimadzu_detectors import detect_shimadzu
from .vendor.perkinelmer_detectors import detect_perkinelmer
from .vendor.waters_detectors import detect_waters
from .vendor.jeol_detectors import detect_jeol
from .vendor.varian_detectors import detect_varian


# ------------------------------------------------------------
# Utility: combine multiple detection candidates
# ------------------------------------------------------------

def _best_candidate(candidates: List[DetectedFormat]) -> DetectedFormat:
    """Return the highest-confidence detection result."""
    if not candidates:
        return DetectedFormat(
            vendor=None,
            technique=Technique.UNKNOWN,
            subtype=None,
            confidence=0.0,
        )
    return max(candidates, key=lambda c: c.confidence)


# ------------------------------------------------------------
# Main sniffer entrypoint
# ------------------------------------------------------------

def sniff_file(path: str) -> DetectedFormat:
    """
    Perform multi-stage detection and return a structured DetectedFormat.
    """

    if not os.path.exists(path):
        return DetectedFormat(
            vendor=None,
            technique=Technique.UNKNOWN,
            subtype=None,
            confidence=0.0,
        )

    candidates: List[DetectedFormat] = []

    # --------------------------------------------------------
    # Tier 1: Core detection (extension + magic bytes)
    # --------------------------------------------------------
    ext_candidate = detect_by_extension(path)
    if ext_candidate:
        candidates.append(ext_candidate)

    magic_candidate = detect_magic_bytes(path)
    if magic_candidate:
        candidates.append(magic_candidate)

    # --------------------------------------------------------
    # Tier 2: Technique inference (UVVis, IR, Raman, etc.)
    # --------------------------------------------------------
    technique_candidate = infer_technique_from_data(path)
    if technique_candidate:
        candidates.append(technique_candidate)

    # --------------------------------------------------------
    # Tier 3: Vendor-specific detection
    # --------------------------------------------------------
    vendor_detectors = [
        detect_agilent,
        detect_bruker,
        detect_thermo,
        detect_shimadzu,
        detect_perkinelmer,
        detect_waters,
        detect_jeol,
        detect_varian,
    ]

    for detector in vendor_detectors:
        try:
            vendor_candidate = detector(path)
            if vendor_candidate:
                candidates.append(vendor_candidate)
        except Exception:
            # Vendor detectors should never crash the sniffer
            continue

    # --------------------------------------------------------
    # Final selection
    # --------------------------------------------------------
    result = _best_candidate(candidates)

    # If technique is unknown but vendor is known, fallback to vendor defaults
    if result.technique == Technique.UNKNOWN and result.vendor:
        result.technique = _infer_default_technique_for_vendor(result.vendor)

    return result


# ------------------------------------------------------------
# Vendor → default technique fallback
# ------------------------------------------------------------

def _infer_default_technique_for_vendor(vendor: str) -> Technique:
    vendor = vendor.lower()

    if vendor == "agilent":
        return Technique.UVVIS
    if vendor == "bruker":
        return Technique.NMR
    if vendor == "horiba":
        return Technique.FLUORESCENCE
    if vendor == "chi":
        return Technique.CV
    if vendor == "waters":
        return Technique.LCMS
    if vendor == "thermo":
        return Technique.IR
    if vendor == "shimadzu":
        return Technique.UVVIS
    if vendor == "perkinelmer":
        return Technique.IR
    if vendor == "jeol":
        return Technique.NMR
    if vendor == "varian":
        return Technique.NMR

    return Technique.UNKNOWN
