"""Phagetrix: Codon optimization for phage display libraries."""

from .constants import VALID_AMINO_ACIDS, degenerate
from .core import DegenerateCodonGenerator
from .output import OutputFormatter
from .parser import InputParser

__version__ = "0.2.3"

__all__ = [
    "DegenerateCodonGenerator",
    "InputParser",
    "OutputFormatter",
    "degenerate",
    "VALID_AMINO_ACIDS",
]
