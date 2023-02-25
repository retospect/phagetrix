#! python3

import phagetrix.trix as trix
import argparse
import re

epilog="""
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
Y4YPFYA
A7AVILM
"""

def process_request(lines, degen_dict):
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
        aas = line[1+re.search(r"\d+", line[1:]).end():]

        # Ensure that the aminoacid in the sequence is the same as the one in the line
        # and provide a good error message if it isn't
        if seq[position-1] != originalAA:
            raise Exception("Amino acid in sequence at position %d is %s, not %s" % (position, seq[position-1], originalAA))

        # Check that all the amino acids in the list are valid
        for aa in aas:
            if aa not in valid_aas:
                raise Exception("Amino acid %s is not valid" % aa)

        # Add the variation to the dictionary
        variations[position] = aas  

    generator = trix.DegenerateCodonGenerator(degen_dict)
    
    # print numbers, so each number takes up 4 digits, for each position
    print("".join(["%4d" % i for i in range(1, len(seq)+1)]))

    # print the original aa sequence, so that each AA takes up 4 characters
    print("".join(["%4s" % aa for aa in seq]))
    
    # Generate the degenerate primers
    codons = []
    for index, aa in enumerate(seq):
        # Get the degenerate codon for the amino acid at this position
        if index+1 in variations:
            aa = variations[index+1]
        codon = generator.get_best_degenerate_codon(aa)
        codons.append(codon)

    # Print the degenerate codons
    print("".join(["%4s" % codon for codon in codons]))

    print()
    print("".join(codons))

        

def main():
    parser = argparse.ArgumentParser(description="PhageTrix", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.description = "PhageTrix"
    parser.long_description = "Generate degenerate primers for phage display libraries"
    parser.epilog = epilog
    parser.version = "0.1.5"
    parser.add_argument("input", type=argparse.FileType('r'), metavar='INPUT_FILE', help="Input file")
    parser.add_argument("-c", "--company", help="Sequence company", default="IDT") # options=trix.degenerate.keys()

    args = parser.parse_args()

    infile = args.input
    degen_dict = trix.degenerate[args.company]

    # Read in the input file
    lines = infile.readlines()
    infile.close()

    process_request(lines, degen_dict)

