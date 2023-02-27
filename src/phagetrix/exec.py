#! python3

import phagetrix.trix as trix
import argparse
import python_codon_tables as pct
import re

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
Phagerix will generate the best degenerate codon for each position.

Example:
VLPYMVAQVQ
P3PFYA
Y4YPFYE
A7AVILM

Cite https://doi.org/10.5281/zenodo.7676572
"""


def process_request(lines, degen_dict, codon_frequency=pct.get_codons_table("e_coli")):
    # Get the sequence
    seq = lines[0].strip()

    # Get the desired aminoacid variations
    variations = {}

    # all valid aminoacids in a string for later validation
    valid_aas = "ACDEFGHIKLMNPQRSTVWY"

    for line in lines[1:]:
        line = line.strip()
        if line == "":
            continue

        originalAA = line[0]

        # With a regexp, get the multidigit integer starting at position 1
        # and ending at the first non-digit character
        # This is the position of the amino acid to be changed
        position = int(re.search(r"\d+", line[1:]).group())

        # Get the list of amino acids to be used for the degenerate codon
        # This is the rest of the line
        aas = line[1 + re.search(r"\d+", line[1:]).end() :]

        # Ensure that the aminoacid in the sequence is the same as the one in the line
        # and provide a good error message if it isn't
        if seq[position - 1] != originalAA:
            raise Exception(
                "Amino acid in sequence at position %d is %s, not %s"
                % (position, seq[position - 1], originalAA)
            )

        # Check that all the amino acids in the list are valid
        for aa in aas:
            if aa not in valid_aas:
                raise Exception("Amino acid %s is not valid" % aa)

        # Add the variation to the dictionary
        variations[position] = aas

    generator = trix.DegenerateCodonGenerator(
        degenerate_bases=degen_dict, codon_frequency=codon_frequency
    )

    # print numbers, so each number takes up 4 digits, for each position
    print("".join(["%4d" % i for i in range(1, len(seq) + 1)]))

    # print the original aa sequence, so that each AA takes up 4 characters
    print("".join(["%4s" % aa for aa in seq]))

    # Generate the degenerate primers
    codons = []
    # Keep track of the metadata for each codon
    metadata = []
    target_list = []
    target_score = []
    # Keep track of the on and off target AA's for each codon
    for index, aa in enumerate(seq):
        # Get the degenerate codon for the amino acid at this position
        if index + 1 in variations:
            aa = variations[index + 1]
        codon = generator.get_best_degenerate_codon(aa)
        codons.append(codon)
        meta = generator.degenerate_codons[codon]
        metadata.append(meta)
        on_target = (
            []
        )  # A list of lists of a set with the number of occurances and the AA
        off_target = (
            []
        )  # A list of lists of a set with the number of occurances and the AA
        off_target_total = 0
        on_target_total = 0
        for prod_aa, count in meta["aas"].items():
            if prod_aa in aa:
                on_target.append((count, prod_aa))
                on_target_total += count
            else:
                off_target.append((count, prod_aa))
                off_target_total += count
        on_target.sort(reverse=True)
        off_target.sort(reverse=True)

        target_score.append(on_target_total / (on_target_total + off_target_total))

        # Add the on target AA's to the list
        target_list.append(on_target)
        # If there are off target AA's, add them to the list
        if len(off_target) > 0:
            target_list[index].append((0, "-"))
            target_list[index] += off_target

    # Print the degenerate codons
    print("".join(["%4s" % codon for codon in codons]), "  degenerate codons")

    # Find the longest list of list in target_list
    max_len = 0
    for i in target_list:
        if len(i) > max_len:
            max_len = len(i)

    for i in range(len(seq)):
        if target_score[i] == 1:
            print("    ", end="")
        else:
            print("  {:2d}".format(round(100 * target_score[i])), end="")
    print("   percentage on target")

    for i in range(max_len):
        for j in target_list:
            if len(j) > i:
                if j[i][0] == 0:
                    print("  --", end="")
                else:
                    print(" %2s" % j[i][0], "%1s" % j[i][1], end="", sep="")
            else:
                print("    ", end="")
        print()

    # Print the on and off target AA's

    print()
    print("".join(codons))


def main():
    parser = argparse.ArgumentParser(
        description="PhageTrix", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.description = "PhageTrix"
    parser.long_description = "Generate degenerate primers for phage display libraries"
    parser.epilog = epilog
    parser.version = "0.2.0"
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
    degen_dict = trix.degenerate[args.company]

    codon_frequency = pct.get_codons_table("e_coli")

    # Read in the input file
    lines = infile.readlines()
    infile.close()

    process_request(lines, degen_dict, codon_frequency)
