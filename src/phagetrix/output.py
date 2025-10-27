"""Output formatting for phagetrix results."""

from typing import Dict, List, Tuple

from quantiphy import Quantity

from .core import DegenerateCodonGenerator


class OutputFormatter:
    """Formats and displays phagetrix results."""

    def __init__(self, avogadro: float = 6.02214076e23):
        self.avogadro = avogadro

    def format_results(
        self,
        seq: str,
        variations: Dict[int, str],
        config: Dict[str, float],
        generator: DegenerateCodonGenerator,
    ) -> None:
        """
        Format and print the results of codon optimization.

        Args:
            seq: The amino acid sequence
            variations: Dictionary of position -> allowed amino acids
            config: Configuration dictionary (contains offset)
            generator: The codon generator instance
        """
        offset = int(config["offset"])

        # Print header with position numbers
        print("".join(["%4d" % (int(i) + offset) for i in range(1, len(seq) + 1)]))

        # Print the original amino acid sequence
        print("".join(["%4s" % aa for aa in seq]))

        # Generate and analyze codons
        codons, target_list, target_score = self._generate_codons(
            seq, variations, generator
        )

        # Print the degenerate codons
        print("".join(["%4s" % codon for codon in codons]), "  degenerate codons")

        # Print efficiency percentages
        self._print_efficiency(seq, target_score)

        # Print amino acid breakdown
        self._print_amino_acid_breakdown(target_list)

        # Print statistics
        self._print_statistics(target_list, codons)

    def _generate_codons(
        self, seq: str, variations: Dict[int, str], generator: DegenerateCodonGenerator
    ) -> Tuple[List[str], List[List[Tuple[int, str]]], List[float]]:
        """Generate codons and analyze their efficiency."""
        codons = []
        target_list = []
        target_score = []

        for index, aa in enumerate(seq):
            # Get the degenerate codon for the amino acid at this position
            if index + 1 in variations:
                aa = variations[index + 1]

            codon = generator.get_best_degenerate_codon(aa)
            codons.append(codon)

            meta = generator.degenerate_codons[codon]
            on_target = []
            off_target = []
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

        return codons, target_list, target_score

    def _print_efficiency(self, seq: str, target_score: List[float]) -> None:
        """Print the efficiency percentages."""
        for i in range(len(seq)):
            if target_score[i] == 1:
                print("    ", end="")
            else:
                print("  {:2d}".format(round(100 * target_score[i])), end="")
        print("   percentage on target")

    def _print_amino_acid_breakdown(
        self, target_list: List[List[Tuple[int, str]]]
    ) -> None:
        """Print the amino acid breakdown for each position."""
        # Find the longest list in target_list
        max_len = max(len(i) for i in target_list) if target_list else 0

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

    def _print_statistics(
        self, target_list: List[List[Tuple[int, str]]], codons: List[str]
    ) -> None:
        """Print probability and material statistics."""
        probs_out_of = []
        for t in target_list:
            s = sum(i[0] for i in t)
            probs_out_of.append(s)

        prob = 1.0
        for x in probs_out_of:
            if x > 0:  # Avoid division by zero
                prob /= x

        print()
        print("Probability for any one outcome: ", Quantity(prob, ""), "=1/", 1 / prob)

        # Calculate material requirements
        one_particle_in_moles = 1.0 / self.avogadro
        print("Amount of material to get all the combinations, ")
        print("assuming each one occurs once only")
        print(Quantity(one_particle_in_moles * 1 / prob, "M"))

        print()
        print("".join(codons))
