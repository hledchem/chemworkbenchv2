# chemworkbench/utils/normalization.py

"""
Normalization utilities for ChemWorkBench v2.

This module provides canonical text normalization for:
- file paths
- header tokens
- metadata fields
- vendor names
- units
- free-text content

Normalization ensures:
- deterministic matching
- LLM-safe anchor extension
- plugin-safe behavior
- future ML integration
- cross-vendor compatibility

All normalization is idempotent and naming-spec compliant.
"""

import re
import unicodedata
from typing import List


# ------------------------------------------------------------
# Unicode normalization
# ------------------------------------------------------------

def normalize_unicode(text: str) -> str:
    """
    Normalize Unicode characters to their closest ASCII equivalents.
    Example:
        λ → lambda
        µ → micro
        ° → deg
    """
    if not text:
        return ""

    # NFKD decomposition
    decomposed = unicodedata.normalize("NFKD", text)

    # Replace common scientific symbols
    replacements = {
        "λ": "lambda",
        "µ": "micro",
        "°": "deg",
        "Ω": "ohm",
        "×": "x",
    }

    for symbol, replacement in replacements.items():
        decomposed = decomposed.replace(symbol, replacement)

    # Strip diacritics
    ascii_text = decomposed.encode("ascii", "ignore").decode("ascii")
    return ascii_text


# ------------------------------------------------------------
# Separator normalization
# ------------------------------------------------------------

def normalize_separators(text: str) -> str:
    """
    Normalize separators by converting:
    - hyphens
    - underscores
    - slashes
    - multiple spaces

    into a single space.
    """
    if not text:
        return ""

    text = re.sub(r"[-_/]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ------------------------------------------------------------
# Punctuation stripping
# ------------------------------------------------------------

def strip_punctuation(text: str) -> str:
    """
    Remove punctuation except alphanumeric characters and spaces.
    """
    if not text:
        return ""

    return re.sub(r"[^0-9a-zA-Z ]+", "", text)


# ------------------------------------------------------------
# Token normalization (canonical form)
# ------------------------------------------------------------

def normalize_token(text: str) -> str:
    """
    Convert text into a canonical token:
    - lowercase
    - unicode-normalized
    - separator-normalized
    - punctuation-stripped
    - whitespace-collapsed

    Example:
        "UV-Vis" → "uvvis"
        "Wavelength (nm)" → "wavelength nm" → "wavelengthnm"
    """
    if not text:
        return ""

    text = normalize_unicode(text)
    text = text.lower()
    text = normalize_separators(text)
    text = strip_punctuation(text)
    text = text.replace(" ", "")
    return text


# ------------------------------------------------------------
# Header tokenization
# ------------------------------------------------------------

def tokenize_header(header: str) -> List[str]:
    """
    Split a header into canonical tokens.
    Example:
        "Wavelength (nm)" → ["wavelength", "nm"]
        "Absorbance_AU" → ["absorbance", "au"]
    """
    if not header:
        return []

    header = normalize_unicode(header)
    header = header.lower()
    header = normalize_separators(header)
    header = strip_punctuation(header)

    tokens = header.split()
    return [normalize_token(tok) for tok in tokens if tok]


# ------------------------------------------------------------
# Vendor normalization
# ------------------------------------------------------------

def normalize_vendor(text: str) -> str:
    """
    Normalize vendor names to canonical forms.
    Example:
        "OceanOptics" → "ocean optics"
        "PerkinElmer" → "perkinelmer"
    """
    if not text:
        return ""

    text = normalize_unicode(text)
    text = normalize_separators(text)
    text = text.lower()

    vendor_map = {
        "oceanoptics": "ocean optics",
        "perkinelmer": "perkinelmer",
        "stellarnet": "stellarnet",
        "agilent": "agilent",
        "shimadzu": "shimadzu",
        "thermo": "thermo",
        "avantes": "avantes",
        "malvern": "malvern",
        "hitachi": "hitachi",
        "bruker": "bruker",
        "jeol": "jeol",
        "waters": "waters",
        "varian": "varian",
    }

    key = text.replace(" ", "")
    return vendor_map.get(key, text)


# ------------------------------------------------------------
# Unit normalization
# ------------------------------------------------------------

def normalize_unit(text: str) -> str:
    """
    Normalize scientific units.
    Example:
        "nanometers" → "nm"
        "cm-1" → "cm1"
    """
    if not text:
        return ""

    text = normalize_token(text)

    unit_map = {
        "nanometer": "nm",
        "nanometers": "nm",
        "nm": "nm",
        "cm1": "cm1",
        "wavenumber": "cm1",
    }

    return unit_map.get(text, text)


# ------------------------------------------------------------
# Path normalization
# ------------------------------------------------------------

def normalize_path(path: str) -> str:
    """
    Normalize file paths to POSIX-style lowercase canonical form.
    """
    if not path:
        return ""

    path = path.replace("\\", "/")
    path = path.lower()
    return path


# ------------------------------------------------------------
# High-level normalization entry point
# ------------------------------------------------------------

def normalize_text(text: str) -> str:
    """
    Full normalization pipeline for arbitrary text.
    """
    if not text:
        return ""

    text = normalize_unicode(text)
    text = text.lower()
    text = normalize_separators(text)
    text = strip_punctuation(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ------------------------------------------------------------
# Metadata for LLMs and plugin authors
# ------------------------------------------------------------

NORMALIZATION_METADATA = {
    "description": "Canonical normalization utilities for ChemWorkBench v2.",
    "version": "1.0.0",
    "last_updated": "2026-01-27",
    "tags": [
        "normalization",
        "canonicalization",
        "llm-safe",
        "future-proof",
        "vendor-normalization",
        "unit-normalization",
    ],
}
