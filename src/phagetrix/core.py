# Phagetrix library

from collections import defaultdict
from typing import Any, Dict, List, Optional, Set

import python_codon_tables as pct

from .constants import degenerate

# TODO: look up UIPAC code for degenerate bases and add it here:


class DegenerateCodonGenerator:
    # Maintains a list of all the degenerate codons and their associated amino acids
    # Can find the best degenerate codon for a given list of aminoacids
    def __init__(
        self,
        degenerate_bases: Dict[str, str] = degenerate["IDT"],
        codon_frequency: Dict[str, List[str]] = pct.get_codons_table("e_coli_316407"),
    ) -> None:
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
        self.degenerate_codons: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"aas": defaultdict(int), "expanded_codon_count": 0}
        )

        # Reverse map the aminoacids from the codon frequency table
        self.codon_to_aa: Dict[str, str] = {}

        for aa, codons in self.codon_frequency.items():
            for codon in codons:
                self.codon_to_aa[codon] = aa

        # Create a dictionary of all the amino acids and a list of all their
        # associated degenerate codons
        temp_amino_acid_dict: Dict[str, List[str]] = defaultdict(list)
        for base1 in self.degenerate_bases.keys():
            for base2 in self.degenerate_bases.keys():
                for base3 in self.degenerate_bases.keys():
                    degenerate_codon = base1 + base2 + base3
                    for normalCodon in self.get_normal_codons(degenerate_codon):
                        aa = self.codon_to_aa[normalCodon]
                        self.degenerate_codons[degenerate_codon]["aas"][aa] += 1

                        temp_amino_acid_dict[aa].append(degenerate_codon)
                        self.degenerate_codons[degenerate_codon][
                            "expanded_codon_count"
                        ] += 1

        # Convert the amioacid list codons to a set
        self.amino_acid_dict: Dict[str, Set[str]] = {}
        for aa in temp_amino_acid_dict.keys():
            self.amino_acid_dict[aa] = set(temp_amino_acid_dict[aa])

    def get_normal_codons(self, degenerate_codon: str) -> List[str]:
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

    def get_best_degenerate_codon(self, amino_acids: str) -> str:
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

        # there's an NNN combo that should always work
        if not degenerate_codons:
            raise ValueError(
                f"No degenerate codon found for amino acids: {amino_acids}. "
                "This should not happen as NNN should always work."
            )

        # Find the best degenerate codon
        best_degenerate_codon: Optional[str] = None
        best_degenerate_codon_aas: Optional[int] = None
        best_degenerate_codon_expanded_codon_count: Optional[int] = None
        best_degenerate_codon_frequency: Optional[float] = None
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
            frequency = 1.0  # self.codon_frequency[degenerate_codon]

            # If the degenerate codon is better than the current best, replace it
            if (
                best_degenerate_codon is None
                or (
                    best_degenerate_codon_aas is not None
                    and num_aas < best_degenerate_codon_aas
                )
                or (
                    best_degenerate_codon_aas is not None
                    and best_degenerate_codon_expanded_codon_count is not None
                    and num_aas == best_degenerate_codon_aas
                    and expanded_codon_count
                    < best_degenerate_codon_expanded_codon_count
                )
                or (
                    best_degenerate_codon_aas is not None
                    and best_degenerate_codon_expanded_codon_count is not None
                    and best_degenerate_codon_frequency is not None
                    and num_aas == best_degenerate_codon_aas
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
        if best_degenerate_codon is None:
            raise ValueError("No suitable degenerate codon found")
        return best_degenerate_codon
