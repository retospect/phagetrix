"""
Phagetrix: Codon optimization for phage display libraries.

Easy-to-use library for optimizing degenerate codons in phage display libraries.

Quick Start:
    >>> import phagetrix
    >>> result = phagetrix.optimize_codons(
    ...     sequence="ACDEF",
    ...     variations={1: "AG", 3: "DEF"}
    ... )
    >>> print(result["final_sequence"])

For more examples, see: https://github.com/retospect/phagetrix
"""

from importlib.metadata import version

# High-level API (recommended for most users)
from .api import (
    calculate_library_stats,
    get_available_companies,
    get_available_species,
    get_available_species_with_aliases,
    get_degenerate_codons,
    optimize,  # Short alias
    optimize_codons,
    parse_file,  # Short alias
    parse_phagetrix_file,
)
from .constants import SPECIES_ALIASES, VALID_AMINO_ACIDS, degenerate

# Low-level API (for advanced users)
from .core import DegenerateCodonGenerator
from .output import OutputFormatter
from .parser import InputParser

__version__ = version("phagetrix")

# Public API - what users see with "from phagetrix import *"
__all__ = [
    "SPECIES_ALIASES",
    "VALID_AMINO_ACIDS",
    "DegenerateCodonGenerator",
    "InputParser",
    "OutputFormatter",
    "calculate_library_stats",
    "degenerate",
    "get_available_companies",
    "get_available_species",
    "get_available_species_with_aliases",
    "get_degenerate_codons",
    "optimize",
    "optimize_codons",
    "parse_file",
    "parse_phagetrix_file",
]
