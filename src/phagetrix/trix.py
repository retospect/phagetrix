# Phagetrix library

from collections import defaultdict
import python_codon_tables as pct

# Source: https://www.idtdna.com/pages/support/faqs/what-are-the-base-degeneracy-codes-that-you-use-(eg.-r-w-k-v-s)-
# Retrieved 2023-FEB-23
degenerate = {
    "IDT": {
        "R": "AG",
        "Y": "CT",
        "M": "AC",
        "K": "GT",
        "S": "CG",
        "W": "AT",
        "H": "ACT",
        "B": "CGT",
        "V": "ACG",
        "D": "AGT",
        "N": "ACGT",
    },
    # Source: https://www.eurofinsgenomics..com/en/products/dnarna-sythesis/degenerate-bases
    # Retrieved 2023-FEB-24
    "Eurofins": {
        "R": "AG",
        "Y": "CT",
        "M": "AC",
        "K": "GT",
        "S": "CG",
        "W": "AT",
        "B": "CGT",
        "D": "AGT",
        "H": "ACT",
        "V": "ACG",
        "N": "ACGT",
    },
    # Source: https://www.neb.com/tools-and-resources/usage-guidelines/single-letter-codes
    # Retrieved 2023-FEB-24
    "NEB": {
        "B": "CGT",
        "D": "AGT",
        "H": "ACT",
        "K": "GT",
        "M": "AC",
        "N": "ACGT",
        "R": "AG",
        "S": "CG",
        "V": "ACG",
        "W": "AT",
        "Y": "CT",
    },
}

# TODO: look up UIPAC code for degenerate bases and add it here:


class DegenerateCodonGenerator:
    # Maintains a list of all the degenerate codons and their associated amino acids
    # Can find the best degenerate codon for a given list of aminoacids
    def __init__(
        self,
        degenerate_bases=degenerate["IDT"],
        codon_frequency=pct.get_codons_table("e_coli"),
    ):
        self.degenerate_bases = degenerate_bases
        self.codon_frequency = codon_frequency

        # Add ATGC to the degenerate dictionary
        for base in "ATGC":
            self.degenerate_bases[base] = base

        # Create a dictionary of all the degenerate codons and
        # their associated amino acids
        # For each degenerate codon, we keep the following
        # in the dictionary:
        #   - aas: The amino acids that it codes for, and how
        #     many times it codes for each in a map
        #   - expanded_codon_count: The number of permutations
        #     of normal codons that it can make
        self.degenerate_codons = defaultdict(
            lambda: {"aas": defaultdict(int), "expanded_codon_count": 0}
        )

        # Reverse map the aminoacids from the codon frequency table
        self.codon_to_aa = {}

        for aa, codons in self.codon_frequency.items():
            for codon in codons:
                self.codon_to_aa[codon] = aa

        # Create a dictionary of all the amino acids and a list of all their
        # associated degenerate codons
        self.amino_acid_dict = defaultdict(list)
        for base1 in self.degenerate_bases.keys():
            for base2 in self.degenerate_bases.keys():
                for base3 in self.degenerate_bases.keys():
                    degenerate_codon = base1 + base2 + base3
                    for normalCodon in self.get_normal_codons(degenerate_codon):
                        aa = self.codon_to_aa[normalCodon]
                        self.degenerate_codons[degenerate_codon]["aas"][aa] += 1

                        self.amino_acid_dict[aa].append(degenerate_codon)
                        self.degenerate_codons[degenerate_codon][
                            "expanded_codon_count"
                        ] += 1

        # Convert the amioacid list codons to a set
        for aa in self.amino_acid_dict.keys():
            self.amino_acid_dict[aa] = set(self.amino_acid_dict[aa])

    def get_normal_codons(self, degenerate_codon):
        # Returns a list of all the normal codons that can be made
        # from a degenerate codon
        normal_codons = []
        for b1 in self.degenerate_bases[degenerate_codon[0]]:
            for b2 in self.degenerate_bases[degenerate_codon[1]]:
                for b3 in self.degenerate_bases[degenerate_codon[2]]:
                    assert b1 in "ATGC"
                    assert b2 in "ATGC"
                    assert b3 in "ATGC"
                    normal_codons.append(b1 + b2 + b3)
        return normal_codons

    def get_best_degenerate_codon(self, amino_acids):
        # Returns the best degenerate codon for a given list of amino acids
        # The best degenerate codon is the one that codes for all the
        # amino acids in the list and the fewest other amino acids.
        # If there is a tie, the one with the fewest permutations is chosen.
        # If there is still a tie, the one with the highest frequency is chosen.

        # For each aminoacid in the list, get the set of degenerate codons that
        # code for it and OR the sets together to find the set of degenerate
        # codons that code for all the amino acids in the list.
        degenerate_codons = set(self.degenerate_codons.keys())
        for aa in amino_acids:
            degenerate_codons = degenerate_codons & self.amino_acid_dict[aa]

        # there's an NNN combo that should alwayws work
        assert degenerate_codons != set()

        # Find the best degenerate codon
        best_degenerate_codon = None
        best_degenerate_codon_aas = None
        best_degenerate_codon_expanded_codon_count = None
        best_degenerate_codon_frequency = None
        for degenerate_codon in degenerate_codons:
            # Get the number of amino acids that the degenerate codon codes for
            aas = self.degenerate_codons[degenerate_codon]["aas"]
            num_aas = len(aas)

            # Get the number of permutations of normal codons
            # that the degenerate codon makes
            expanded_codon_count = self.degenerate_codons[degenerate_codon][
                "expanded_codon_count"
            ]

            # Get the frequency of the degenerate codon
            frequency = 1  # self.codon_frequency[degenerate_codon]

            # If the degenerate codon is better than the current best, replace it
            if (
                best_degenerate_codon is None
                or (num_aas < best_degenerate_codon_aas)
                or (
                    num_aas == best_degenerate_codon_aas
                    and expanded_codon_count
                    < best_degenerate_codon_expanded_codon_count
                )
                or (
                    num_aas == best_degenerate_codon_aas
                    and expanded_codon_count
                    == best_degenerate_codon_expanded_codon_count
                    and frequency > best_degenerate_codon_frequency
                )
            ):
                best_degenerate_codon = degenerate_codon
                best_degenerate_codon_aas = num_aas
                best_degenerate_codon_expanded_codon_count = expanded_codon_count
                best_degenerate_codon_frequency = frequency

        # Return the best degenerate codon
        return best_degenerate_codon
