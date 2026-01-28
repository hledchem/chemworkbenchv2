"""
Normalization Layer — ChemWorkBench v2.2
========================================

LLM‑friendly commentary
-----------------------
This module provides the *canonical normalization layer* for ChemWorkBench v2.2.
It contains two categories of functionality:

1. Low‑level normalization utilities
   - unicode normalization
   - separator normalization
   - punctuation stripping
   - token canonicalization
   - vendor normalization
   - unit normalization
   - path normalization
   - free‑text normalization

2. High‑level v2.2 entrypoint:
       normalize_file(path) → NormalizedFileInfo

The entrypoint prepares a file for technique detection by extracting
canonical tokens from filenames and headers. It does NOT:
- detect technique
- interpret scientific meaning
- select loaders
- route to processors

This separation keeps the architecture deterministic, plugin‑safe,
and LLM‑friendly.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import List, Mapping, Any


# ======================================================================
# Unicode normalization
# ======================================================================

def normalize_unicode(text: str) -> str:
    """
    Normalize Unicode characters to ASCII equivalents.
    Example:
        λ → lambda
        µ → micro
        ° → deg
    """
    if not text:
        return ""

    decomposed = unicodedata.normalize("NFKD", text)

    replacements = {
        "λ": "lambda",
        "µ": "micro",
        "°": "deg",
        "Ω": "ohm",
        "×": "x",
    }

    for symbol, replacement in replacements.items():
        decomposed = decomposed.replace(symbol, replacement)

    ascii_text = decomposed.encode("ascii", "ignore").decode("ascii")
    return ascii_text


# ======================================================================
# Separator normalization
# ======================================================================

def normalize_separators(text: str) -> str:
    """
    Normalize separators:
    - hyphens
    - underscores
    - slashes
    - multiple spaces
    """
    if not text:
        return ""

    text = re.sub(r"[-_/]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ======================================================================
# Punctuation stripping
# ======================================================================

def strip_punctuation(text: str) -> str:
    """Remove punctuation except alphanumeric characters and spaces."""
    if not text:
        return ""
    return re.sub(r"[^0-9a-zA-Z ]+", "", text)


# ======================================================================
# Token normalization (canonical form)
# ======================================================================

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
        "Wavelength (nm)" → "wavelengthnm"
    """
    if not text:
        return ""

    text = normalize_unicode(text)
    text = text.lower()
    text = normalize_separators(text)
    text = strip_punctuation(text)
    text = text.replace(" ", "")
    return text


# ======================================================================
# Header tokenization
# ======================================================================

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

    parts = header.split()
    return [normalize_token(tok) for tok in parts if tok]


# ======================================================================
# Vendor normalization
# ======================================================================

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


# ======================================================================
# Unit normalization
# ======================================================================

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


# ======================================================================
# Path normalization
# ======================================================================

def normalize_path(path: str) -> str:
    """Normalize file paths to POSIX-style lowercase canonical form."""
    if not path:
        return ""
    path = path.replace("\\", "/")
    return path.lower()


# ======================================================================
# Free-text normalization
# ======================================================================

def normalize_text(text: str) -> str:
    """Full normalization pipeline for arbitrary text."""
    if not text:
        return ""
    text = normalize_unicode(text)
    text = text.lower()
    text = normalize_separators(text)
    text = strip_punctuation(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ======================================================================
# Metadata for LLMs and plugin authors
# ======================================================================

NORMALIZATION_METADATA = {
    "description": "Canonical normalization utilities for ChemWorkBench v2.2.",
    "version": "2.2.0",
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


# ======================================================================
# v2.2 High-Level Normalization Entrypoint
# ======================================================================

@dataclass
class NormalizedFileInfo:
    """
    NormalizedFileInfo (v2.2)

    The canonical representation of a file for the anchor engine.
    """
    path: Path
    tokens: List[str]
    headers: List[str]
    extra: Mapping[str, Any]


def _extract_header_tokens(path: Path) -> List[str]:
    """
    Lightweight header extraction for CSV/TXT-like files.
    Uses tokenize_header() for canonicalization.
    """
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            first_line = f.readline().strip()
            if not first_line:
                return []

            parts = (
                first_line.replace(",", " ")
                .replace("\t", " ")
                .split()
            )

            return [
                tok
                for part in parts
                for tok in tokenize_header(part)
                if tok
            ]
    except Exception:
        return []


def _extract_filename_tokens(path: Path) -> List[str]:
    """Tokenize the filename using canonical header tokenization."""
    return tokenize_header(path.stem)


def normalize_file(path: Path) -> NormalizedFileInfo:
    """
    normalize_file(path) → NormalizedFileInfo

    v2.2 entrypoint for the normalization layer.
    Produces canonical tokens for the anchor engine.
    """
    path = Path(path)

    filename_tokens = _extract_filename_tokens(path)
    header_tokens = _extract_header_tokens(path)

    tokens = sorted(set(filename_tokens + header_tokens))

    return NormalizedFileInfo(
        path=path,
        tokens=tokens,
        headers=header_tokens,
        extra={},
    )
