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

# High-level API (recommended for most users)
from .api import optimize  # Short alias
from .api import parse_file  # Short alias
from .api import (
    calculate_library_stats,
    get_available_companies,
    get_available_species,
    get_available_species_with_aliases,
    get_degenerate_codons,
    optimize_codons,
    parse_phagetrix_file,
)
from .constants import SPECIES_ALIASES, VALID_AMINO_ACIDS, degenerate

# Low-level API (for advanced users)
from .core import DegenerateCodonGenerator
from .output import OutputFormatter
from .parser import InputParser

__version__ = "1.0.6"

# Public API - what users see with "from phagetrix import *"
__all__ = [
    # High-level API (recommended)
    "optimize_codons",
    "parse_phagetrix_file",
    "get_available_companies",
    "get_available_species",
    "get_available_species_with_aliases",
    "get_degenerate_codons",
    "calculate_library_stats",
    "optimize",  # alias
    "parse_file",  # alias
    # Low-level API
    "DegenerateCodonGenerator",
    "InputParser",
    "OutputFormatter",
    "degenerate",
    "VALID_AMINO_ACIDS",
    "SPECIES_ALIASES",
]
