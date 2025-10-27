#! python3

import argparse

import python_codon_tables as pct
from quantiphy import Quantity

import phagetrix.core as core

from .output import OutputFormatter
from .parser import InputParser

Quantity.set_prefs(output_sf="QRYZEPTGMkmunpfazyrq")
# From wikipedia
avogadro = 6.02214076e23

epilog = """
PhageTrix is a tool to generate phage display libraries.
You probably have an idea what AA's you want to replace, and what
you wish to replace them with.
The sequence companies have a reasonable number of
The file format has the AA sequence on the first line.
Each following line is the AA to be changed,
the digits indicating its position,
and the AA options that should be generated for that position.
The AA options are concatenated together with no spaces.
Phagetrix will generate the best degenerate codon for each position.

Example:
VLPYMVAQVQ
P3PFYA
Y4YPFYE
A7AVILM

Cite https://doi.org/10.5281/zenodo.7676572
"""


def process_request(lines, degen_dict, codon_frequency=pct.get_codons_table("e_coli")):
    """Process input lines and generate codon optimization results."""
    # Parse input
    parser = InputParser()
    seq, variations, config = parser.parse(lines)

    # Generate results
    generator = core.DegenerateCodonGenerator(
        degenerate_bases=degen_dict, codon_frequency=codon_frequency
    )

    # Format and display output
    formatter = OutputFormatter(avogadro)
    formatter.format_results(seq, variations, config, generator)


def main():
    parser = argparse.ArgumentParser(
        description="PhageTrix", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.description = "PhageTrix"
    parser.long_description = "Generate degenerate primers for phage display libraries"
    parser.epilog = epilog
    parser.version = "0.2.3"
    parser.add_argument(
        "input", type=argparse.FileType("r"), metavar="INPUT_FILE", help="Input file"
    )
    parser.add_argument("-c", "--company", help="Sequence company", default="IDT")
    parser.add_argument(
        "-s",
        "--species",
        help="Species for codon frequency table from python_codon_tables, default is e_coli",
        default="e_coli",
    )

    args = parser.parse_args()

    infile = args.input

    # Validate company parameter
    if args.company not in core.degenerate:
        available_companies = ", ".join(core.degenerate.keys())
        raise ValueError(
            f"Unknown company '{args.company}'. Available: {available_companies}"
        )

    degen_dict = core.degenerate[args.company]

    # Validate species parameter
    try:
        codon_frequency = pct.get_codons_table(args.species)
    except Exception as e:
        raise ValueError(f"Unknown species '{args.species}': {e}")

    # Read in the input file
    lines = infile.readlines()
    infile.close()

    process_request(lines, degen_dict, codon_frequency)
