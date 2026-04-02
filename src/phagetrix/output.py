"""Output formatting for phagetrix results."""

from quantiphy import Quantity

from .core import DegenerateCodonGenerator


class OutputFormatter:
    """Formats and displays phagetrix results."""

    def __init__(self, avogadro: float = 6.02214076e23):
        self.avogadro = avogadro

    def format_results(
        self,
        seq: str,
        variations: dict[int, str],
        config: dict[str, float],
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
        print("".join([f"{int(i) + offset:4d}" for i in range(1, len(seq) + 1)]))

        # Print the original amino acid sequence
        print("".join([f"{aa:>4s}" for aa in seq]))

        # Generate and analyze codons
        codons, target_list, target_score = self._generate_codons(
            seq, variations, generator
        )

        # Print the degenerate codons
        print("".join([f"{codon:>4s}" for codon in codons]), "  degenerate codons")

        # Print efficiency percentages
        self._print_efficiency(seq, target_score)

        # Print amino acid breakdown
        self._print_amino_acid_breakdown(target_list)

        # Print statistics
        self._print_statistics(target_list, codons)

    def _generate_codons(
        self, seq: str, variations: dict[int, str], generator: DegenerateCodonGenerator
    ) -> tuple[list[str], list[list[tuple[int, str]]], list[float]]:
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

    def _print_efficiency(self, seq: str, target_score: list[float]) -> None:
        """Print the efficiency percentages."""
        for i in range(len(seq)):
            if target_score[i] == 1:
                print("    ", end="")
            else:
                print(f"  {round(100 * target_score[i]):2d}", end="")
        print("   percentage on target")

    def _print_amino_acid_breakdown(
        self, target_list: list[list[tuple[int, str]]]
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
                        print(f" {j[i][0]:>2}{j[i][1]:<1}", end="")
                else:
                    print("    ", end="")
            print()

    def _print_statistics(
        self, target_list: list[list[tuple[int, str]]], codons: list[str]
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
