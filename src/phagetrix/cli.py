#! python3

import argparse
from typing import List

from quantiphy import Quantity

from . import api
from .output import OutputFormatter

Quantity.set_prefs(output_sf="QRYZEPTGMkmunpfazyrq")
# From wikipedia
avogadro = 6.02214076e23

epilog = """
FILE FORMAT:
  Line 1: Amino acid sequence (e.g., VLAYMVAQVQ)
  Line 2+: [Original AA][Position][Allowed AAs] (e.g., A3AGVIL)

  Optional configuration lines start with # (e.g., # offset = 10)

EXAMPLE INPUT FILE:
  VLAYMVAQVQ
  A3AGVIL
  Y4YFW
  A7AVIL

SUPPORTED COMPANIES:
  IDT, Eurofins, NEB (default: IDT)

COMMON SPECIES:
  e_coli (default), h_sapiens_9606, s_cerevisiae_4932
  Use --species to see all available options

For more help: https://github.com/retospect/phagetrix
Citation: https://doi.org/10.5281/zenodo.7676572
"""


def process_request(
    lines: List[str], company: str = "IDT", species: str = "e_coli"
) -> None:
    """Process input lines and generate codon optimization results."""
    # Parse input using API
    import os
    import tempfile

    # Create temporary file for parsing
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".phagetrix") as f:
        for line in lines:
            if not line.endswith("\n"):
                line += "\n"
            f.write(line)
        temp_path = f.name

    try:
        seq, variations, config = api.parse_phagetrix_file(temp_path)
    finally:
        os.unlink(temp_path)

    # Format and display output using existing formatter
    import python_codon_tables as pct

    from .core import DegenerateCodonGenerator

    # Create generator for formatter compatibility
    codon_frequency = pct.get_codons_table(species)
    generator = DegenerateCodonGenerator(
        degenerate_bases=api.get_degenerate_codons(company),
        codon_frequency=codon_frequency,
    )

    formatter = OutputFormatter(avogadro)
    formatter.format_results(seq, variations, config, generator)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Phagetrix - Codon optimization for phage display libraries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.description = "Phagetrix - Codon optimization for phage display libraries"
    # parser.long_description is not a valid attribute, removing
    parser.epilog = epilog
    # parser.version is not a valid attribute, removing
    parser.add_argument(
        "input",
        type=argparse.FileType("r"),
        metavar="INPUT_FILE",
        help="Input file containing sequence and variations",
    )
    parser.add_argument(
        "-c",
        "--company",
        help="DNA synthesis company (IDT, Eurofins, NEB)",
        default="IDT",
        choices=["IDT", "Eurofins", "NEB"],
    )
    parser.add_argument(
        "-s",
        "--species",
        help="Species for codon usage optimization (default: e_coli)",
        default="e_coli",
    )

    args = parser.parse_args()

    infile = args.input

    # Validate company parameter using API
    available_companies = api.get_available_companies()
    if args.company not in available_companies:
        available_str = ", ".join(available_companies)
        raise ValueError(
            f"Unknown company '{args.company}'. Available: {available_str}"
        )

    # Validate species parameter using API (including aliases)
    available_species = api.get_available_species()
    from .constants import SPECIES_ALIASES

    available_aliases = list(SPECIES_ALIASES.keys())
    if args.species not in available_species and args.species not in available_aliases:
        raise ValueError(
            f"Unknown species '{args.species}'. Use --species to see available options."
        )

    # Read in the input file
    lines = infile.readlines()
    infile.close()

    process_request(lines, args.company, args.species)
