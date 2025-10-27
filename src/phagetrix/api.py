"""
High-level API for Phagetrix - Easy-to-use interface for library users.

This module provides simple, convenient functions for common use cases.
"""

from typing import Any, Dict, List, Tuple

import python_codon_tables as pct

from .constants import SPECIES_ALIASES, VALID_AMINO_ACIDS, degenerate
from .core import DegenerateCodonGenerator
from .parser import InputParser


def _resolve_species_alias(species: str) -> str:
    """Resolve species alias to full species name."""
    return SPECIES_ALIASES.get(species, species)


def optimize_codons(
    sequence: str,
    variations: Dict[int, str],
    company: str = "IDT",
    species: str = "e_coli",
    offset: int = 0,
) -> Dict[str, Any]:
    """
    Optimize degenerate codons for a protein sequence.

    This is the main high-level function for codon optimization.

    Args:
        sequence: Amino acid sequence (e.g., "ACDEFG")
        variations: Dictionary mapping positions to allowed amino acids
                   {1: "AG", 3: "DEF"} means position 1 can be A or G,
                   position 3 can be D, E, or F
        company: DNA synthesis company ("IDT", "Eurofins", or "NEB")
        species: Species for codon usage ("e_coli", "h_sapiens_9606", etc.)
        offset: Position offset for numbering (default 0)

    Returns:
        Dictionary containing:
        - "sequence": Original amino acid sequence
        - "degenerate_codons": List of optimized degenerate codons
        - "final_sequence": DNA sequence ready for synthesis
        - "efficiency": List of on-target percentages for each position
        - "variations": Applied variations

    Example:
        >>> result = optimize_codons(
        ...     sequence="ACDEF",
        ...     variations={1: "AG", 3: "DEF"},
        ...     company="IDT"
        ... )
        >>> print(result["final_sequence"])
        'RCTGAYTTTGAA'
    """
    # Validate inputs
    if company not in degenerate:
        available = ", ".join(degenerate.keys())
        raise ValueError(f"Unknown company '{company}'. Available: {available}")

    # Validate sequence
    for i, aa in enumerate(sequence):
        if aa not in VALID_AMINO_ACIDS:
            raise ValueError(f"Invalid amino acid '{aa}' at position {i+1}")

    # Validate variations
    for pos, aas in variations.items():
        if pos < 1 or pos > len(sequence):
            raise ValueError(
                f"Position {pos} out of range for sequence length {len(sequence)}"
            )
        for aa in aas:
            if aa not in VALID_AMINO_ACIDS:
                raise ValueError(f"Invalid amino acid '{aa}' in variations")

    # Resolve species alias and get codon frequency table
    resolved_species = _resolve_species_alias(species)
    try:
        codon_frequency = pct.get_codons_table(resolved_species)
    except Exception as e:
        raise ValueError(f"Unknown species '{species}': {e}")

    # Generate optimized codons
    generator = DegenerateCodonGenerator(
        degenerate_bases=degenerate[company], codon_frequency=codon_frequency
    )

    codons = []
    efficiency = []

    for i, aa in enumerate(sequence):
        pos = i + 1
        target_aas = variations.get(pos, aa)

        # Get best degenerate codon
        best_codon = generator.get_best_degenerate_codon(target_aas)
        codons.append(best_codon)

        # Calculate efficiency
        meta = generator.degenerate_codons[best_codon]
        on_target_total = sum(
            count for prod_aa, count in meta["aas"].items() if prod_aa in target_aas
        )
        total = sum(meta["aas"].values())
        efficiency.append(round(100 * on_target_total / total) if total > 0 else 0)

    return {
        "sequence": sequence,
        "degenerate_codons": codons,
        "final_sequence": "".join(codons),
        "efficiency": efficiency,
        "variations": dict(variations),
        "company": company,
        "species": species,
        "offset": str(offset),
    }


def parse_phagetrix_file(
    file_path: str,
) -> Tuple[str, Dict[int, str], Dict[str, float]]:
    """
    Parse a Phagetrix input file.

    Args:
        file_path: Path to the .phagetrix file

    Returns:
        Tuple of (sequence, variations, config)

    Example:
        >>> seq, vars, config = parse_phagetrix_file("input.phagetrix")
        >>> print(f"Sequence: {seq}")
        >>> print(f"Variations: {vars}")
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    parser = InputParser()
    return parser.parse(lines)


def get_available_companies() -> List[str]:
    """
    Get list of supported DNA synthesis companies.

    Returns:
        List of company names

    Example:
        >>> companies = get_available_companies()
        >>> print(companies)
        ['IDT', 'Eurofins', 'NEB']
    """
    return list(degenerate.keys())


def get_available_species() -> List[str]:
    """
    Get list of available species for codon optimization.

    Returns:
        List of species identifiers

    Example:
        >>> species = get_available_species()
        >>> print(species[:3])
        ['e_coli_316407', 'h_sapiens_9606', 's_cerevisiae_4932']
    """
    return list(pct.available_codon_tables_names)


def get_available_species_with_aliases() -> List[str]:
    """
    Get list of available species including convenient aliases.

    Returns:
        List of species identifiers and aliases

    Example:
        >>> species = get_available_species_with_aliases()
        >>> print('e_coli' in species)  # True
        >>> print('e_coli_316407' in species)  # True
    """
    species_list = list(pct.available_codon_tables_names)
    aliases = list(SPECIES_ALIASES.keys())
    return sorted(set(species_list + aliases))


def get_degenerate_codons(company: str = "IDT") -> Dict[str, str]:
    """
    Get degenerate codon mappings for a company.

    Args:
        company: DNA synthesis company name

    Returns:
        Dictionary mapping degenerate bases to nucleotides

    Example:
        >>> codons = get_degenerate_codons("IDT")
        >>> print(codons["R"])  # R = A or G
        'AG'
    """
    if company not in degenerate:
        available = ", ".join(degenerate.keys())
        raise ValueError(f"Unknown company '{company}'. Available: {available}")

    return degenerate[company].copy()


def calculate_library_stats(
    sequence: str, variations: Dict[int, str], company: str = "IDT"
) -> Dict[str, Any]:
    """
    Calculate theoretical statistics for a degenerate library.

    Args:
        sequence: Amino acid sequence
        variations: Position variations
        company: DNA synthesis company

    Returns:
        Dictionary with library statistics

    Example:
        >>> stats = calculate_library_stats("ACDEF", {1: "AG", 3: "DEF"})
        >>> print(f"Theoretical diversity: {stats['diversity']}")
        >>> print(f"Material needed: {stats['material_amount']}")
    """
    # Get codon generator
    generator = DegenerateCodonGenerator(degenerate_bases=degenerate[company])

    total_combinations = 1
    codons_used = []

    for i, aa in enumerate(sequence):
        pos = i + 1
        target_aas = variations.get(pos, aa)

        best_codon = generator.get_best_degenerate_codon(target_aas)
        codons_used.append(best_codon)

        # Count combinations for this position
        meta = generator.degenerate_codons[best_codon]
        combinations = sum(meta["aas"].values())
        total_combinations *= combinations

    # Calculate material requirements (simplified)
    avogadro = 6.02214076e23
    one_particle_in_moles = 1.0 / avogadro
    material_moles = (
        one_particle_in_moles / total_combinations if total_combinations > 0 else 0
    )

    return {
        "diversity": total_combinations,
        "probability_single": 1.0 / total_combinations if total_combinations > 0 else 0,
        "material_moles": material_moles,
        "material_amount": f"{material_moles:.2e} M" if material_moles > 0 else "N/A",
        "codons_used": codons_used,
        "final_sequence": "".join(codons_used),
    }


# Convenience aliases for common use cases
optimize = optimize_codons  # Short alias
parse_file = parse_phagetrix_file  # Short alias
