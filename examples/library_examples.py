#!/usr/bin/env python3
"""
Phagetrix Library Examples

This script demonstrates how to use Phagetrix as a Python library.
Run with: python examples/library_examples.py
"""

import phagetrix


def example_1_basic_usage():
    """Example 1: Basic codon optimization"""
    print("=" * 60)
    print("Example 1: Basic Codon Optimization")
    print("=" * 60)

    # Simple optimization
    result = phagetrix.optimize_codons(
        sequence="VLAYMVAQVQ", variations={3: "AGVIL", 4: "YFW", 7: "AVIL"}
    )

    print(f"Original sequence: {result['sequence']}")
    print(f"Optimized DNA:     {result['final_sequence']}")
    print(f"Degenerate codons: {result['degenerate_codons']}")
    print(f"Efficiency:        {result['efficiency']}%")
    print()


def example_2_different_companies():
    """Example 2: Compare different DNA synthesis companies"""
    print("=" * 60)
    print("Example 2: Compare DNA Synthesis Companies")
    print("=" * 60)

    sequence = "ACDEF"
    variations = {1: "AG", 3: "DEF"}

    companies = phagetrix.get_available_companies()
    print(f"Available companies: {companies}")
    print()

    for company in companies:
        result = phagetrix.optimize_codons(sequence, variations, company=company)
        print(f"{company:10}: {result['final_sequence']}")
    print()


def example_3_species_comparison():
    """Example 3: Different species codon usage"""
    print("=" * 60)
    print("Example 3: Species-Specific Codon Usage")
    print("=" * 60)

    sequence = "ACDEF"
    variations = {1: "AG", 3: "DEF"}

    species_list = ["e_coli", "h_sapiens_9606", "s_cerevisiae_4932"]

    for species in species_list:
        try:
            result = phagetrix.optimize_codons(sequence, variations, species=species)
            print(f"{species:20}: {result['final_sequence']}")
        except Exception as e:
            print(f"{species:20}: Error - {e}")
    print()


def example_4_library_statistics():
    """Example 4: Calculate library statistics"""
    print("=" * 60)
    print("Example 4: Library Statistics")
    print("=" * 60)

    sequence = "CARSGDYYGMDVW"  # CDR3-like sequence
    variations = {
        4: "ST",  # Position 4: Ser or Thr
        6: "DE",  # Position 6: Asp or Glu
        7: "YF",  # Position 7: Tyr or Phe
        8: "YF",  # Position 8: Tyr or Phe
    }

    # Get optimization results
    result = phagetrix.optimize_codons(sequence, variations)

    # Calculate statistics
    stats = phagetrix.calculate_library_stats(sequence, variations)

    print(f"Target sequence:      {sequence}")
    print(f"Optimized DNA:        {result['final_sequence']}")
    print(f"Theoretical diversity: {stats['diversity']:,} variants")
    print(f"Single probability:   {stats['probability_single']:.2e}")
    print(f"Material needed:      {stats['material_amount']}")
    print(
        f"Average efficiency:   {sum(result['efficiency'])/len(result['efficiency']):.1f}%"
    )
    print()


def example_5_file_parsing():
    """Example 5: Parse Phagetrix files"""
    print("=" * 60)
    print("Example 5: File Parsing")
    print("=" * 60)

    # Parse the sample file
    try:
        sequence, variations, config = phagetrix.parse_phagetrix_file(
            "examples/sample.phagetrix"
        )

        print(f"Parsed sequence:   {sequence}")
        print(f"Parsed variations: {variations}")
        print(f"Parsed config:     {config}")

        # Use parsed data for optimization
        result = phagetrix.optimize_codons(sequence, variations)
        print(f"Optimized result:  {result['final_sequence']}")

    except FileNotFoundError:
        print("Sample file not found. Make sure you're running from the project root.")
    except Exception as e:
        print(f"Error parsing file: {e}")
    print()


def example_6_error_handling():
    """Example 6: Error handling"""
    print("=" * 60)
    print("Example 6: Error Handling")
    print("=" * 60)

    # Test various error conditions
    test_cases = [
        ("Invalid amino acid", "ACDEFX", {1: "AG"}),
        ("Position out of range", "ACDEF", {10: "AG"}),
        ("Invalid company", "ACDEF", {1: "AG"}, "InvalidCompany"),
        ("Invalid amino acid in variations", "ACDEF", {1: "XY"}),
    ]

    for description, sequence, variations, *args in test_cases:
        try:
            company = args[0] if args else "IDT"
            result = phagetrix.optimize_codons(sequence, variations, company=company)
            print(f"✓ {description}: Success")
        except ValueError as e:
            print(f"✗ {description}: {e}")
    print()


def example_7_batch_processing():
    """Example 7: Batch processing multiple sequences"""
    print("=" * 60)
    print("Example 7: Batch Processing")
    print("=" * 60)

    # Multiple sequences to process
    sequences = [
        ("CDR1", "RASQSISSWLA", {4: "QE", 6: "ST", 8: "ST"}),
        ("CDR2", "AASSLQS", {3: "ST", 5: "LI", 7: "ST"}),
        ("CDR3", "QQSYSTPLT", {3: "ST", 5: "ST", 7: "PT"}),
    ]

    print("Processing multiple CDR sequences:")
    print("-" * 40)

    for name, seq, vars in sequences:
        result = phagetrix.optimize_codons(seq, vars)
        avg_eff = sum(result["efficiency"]) / len(result["efficiency"])

        print(f"{name}:")
        print(f"  Original: {seq}")
        print(f"  Optimized: {result['final_sequence']}")
        print(f"  Avg efficiency: {avg_eff:.1f}%")
        print()


def example_8_advanced_usage():
    """Example 8: Advanced usage with low-level API"""
    print("=" * 60)
    print("Example 8: Advanced Usage")
    print("=" * 60)

    # Use low-level API for more control
    import python_codon_tables as pct

    from phagetrix import DegenerateCodonGenerator, degenerate

    # Create custom generator
    generator = DegenerateCodonGenerator(
        degenerate_bases=degenerate["IDT"],
        codon_frequency=pct.get_codons_table("h_sapiens_9606"),
    )

    # Test different amino acid combinations
    aa_combinations = ["A", "AG", "DEF", "FYWH"]

    print("Testing amino acid combinations:")
    for aas in aa_combinations:
        best_codon = generator.get_best_degenerate_codon(aas)
        normal_codons = generator.get_normal_codons(best_codon)

        print(f"  {aas:6} -> {best_codon:4} -> {normal_codons}")
    print()


def main():
    """Run all examples"""
    print("Phagetrix Library Examples")
    print("=" * 60)
    print("This script demonstrates various ways to use Phagetrix as a library.")
    print()

    examples = [
        example_1_basic_usage,
        example_2_different_companies,
        example_3_species_comparison,
        example_4_library_statistics,
        example_5_file_parsing,
        example_6_error_handling,
        example_7_batch_processing,
        example_8_advanced_usage,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")
            print()

    print("=" * 60)
    print("All examples completed!")
    print("For more information, see: https://github.com/retospect/phagetrix")


if __name__ == "__main__":
    main()
