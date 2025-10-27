# Phagetrix

[![PyPI version](https://badge.fury.io/py/phagetrix.svg)](https://badge.fury.io/py/phagetrix)
[![Python](https://img.shields.io/pypi/pyversions/phagetrix.svg)](https://pypi.org/project/phagetrix/)
[![License](https://img.shields.io/pypi/l/phagetrix.svg)](https://github.com/retospect/phagetrix/blob/main/LICENSE)
[![CI](https://github.com/retospect/phagetrix/actions/workflows/check.yml/badge.svg)](https://github.com/retospect/phagetrix/actions/workflows/check.yml)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/retospect/phagetrix/blob/main/examples/phagetrix.ipynb)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.7676572-blue)](https://doi.org/10.5281/zenodo.7676572)

**A powerful codon optimization tool for [phage display library](https://bio.libretexts.org/Bookshelves/Biochemistry/Supplemental_Modules_(Biochemistry)/4._Biotechnology_2/4.3%3A_M13_Phage_Display_Libraries) generation and protein engineering.**

Phagetrix helps researchers design optimal degenerate codon libraries for phage display, directed evolution, and synthetic biology applications. Maximize your library diversity while staying within experimental constraints.

## Table of Contents

- [Key Features](#key-features)
- [Use Cases](#use-cases)  
- [The Library Diversity Problem](#the-library-diversity-problem)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Advanced Features](#advanced-features)
- [Documentation & Support](#documentation--support)
- [Citation](#citation)
- [Related Tools](#related-tools)
- [License](#license)

## Key Features

- **Intelligent codon optimization** - Automatically selects the best degenerate codons for your amino acid requirements
- **Library statistics** - Calculate theoretical diversity and material requirements  
- **Multi-vendor support** - Compatible with IDT, Eurofins, and NEB degenerate codon sets
- **Species-specific** - Supports codon usage tables for multiple organisms
- **Easy to use** - Simple file format and command-line interface
- **Python integration** - Use as a library in your bioinformatics pipelines

## Use Cases

- **Phage display library design** - Optimize antibody/peptide libraries
- **Directed evolution** - Design mutagenesis libraries for protein engineering  
- **Synthetic biology** - Create diverse protein variants for screening
- **Molecular biology research** - Plan degenerate PCR experiments

## The Library Diversity Problem

When creating phage display libraries, you're limited by experimental constraints:
- **1 liter of phage solution** ≈ **10¹² different sequences**
- **Random mutagenesis**: 20⁹ ≈ 10¹² permutations (only ~9 variable positions)
- **Smart degenerate codons**: 6¹⁵ ≈ 10¹² permutations (**~15 variable positions!**)

**Phagetrix maximizes your library diversity** by intelligently selecting degenerate codons from manufacturers like [IDT](https://www.idtdna.com/pages/support/faqs/what-are-the-base-degeneracy-codes-that-you-use-(eg.-r-w-k-v-s-)), Eurofins, and NEB, allowing you to target more positions with rational amino acid choices.

## Quick Start

### Python Library (Recommended)

```python
import phagetrix

# Optimize degenerate codons for your sequence
result = phagetrix.optimize_codons(
    sequence="VLAYMVAQVQ",
    variations={3: "AGVIL", 4: "YFW", 7: "AVIL"}
)

print("Optimized DNA sequence:", result["final_sequence"])
print("Efficiency per position:", result["efficiency"])
```

### Command Line Interface

Create a simple text file specifying your target sequence and desired variations:

```txt
VLAYMVAQVQ
A3AGVIL
Y4YFW
A7AVIL
```

Run Phagetrix:

```bash
phagetrix input.txt
```

### Output

```txt
   1   2   3   4   5   6   7   8   9  10
   V   L   A   Y   M   V   A   Q   V   Q
 GTT CTT VBA TDK ATG GTT VYA CAG GTT CAG   degenerate codons
          56  50          67               percentage on target
  1V  1L  1V  1Y  1M  1V  1V  1Q  1V  1Q
          1L  1W          1L
          1I  1F          1I
          1G  --          1A
          1A  1L          --
          --  1C          1T
          2R  1*          1P

Final sequence: GTTCTTVBATDKATGGTTVYACAGGTTCAG
```

**Output includes:**
- **Degenerate codons** (VBA, TDK, etc.) optimized for your requirements
- **Efficiency percentages** showing on-target vs off-target products
- **Amino acid breakdown** for each position
- **Ready-to-order sequence** for DNA synthesis

## Installation

### Using pip (recommended)
```bash
pip install phagetrix
```

### Using Poetry (for development)
```bash
git clone https://github.com/retospect/phagetrix.git
cd phagetrix
poetry install
poetry run phagetrix --help
```

### Try Online
[![Open in Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/retospect/phagetrix/blob/main/examples/phagetrix.ipynb)

Try Phagetrix interactively in your browser with comprehensive examples!

**Requirements:** Python 3.10 or higher

## Library Usage

### Common Functions

```python
import phagetrix

# Get available companies and species
companies = phagetrix.get_available_companies()
species = phagetrix.get_available_species()

# Parse existing Phagetrix files
seq, variations, config = phagetrix.parse_phagetrix_file("input.phagetrix")

# Calculate library statistics
stats = phagetrix.calculate_library_stats("ACDEF", {1: "AG", 3: "DEF"})
print(f"Library diversity: {stats['diversity']:,} variants")

# Compare different companies
for company in ["IDT", "Eurofins", "NEB"]:
    result = phagetrix.optimize_codons("ACDEF", {1: "AG"}, company=company)
    print(f"{company}: {result['final_sequence']}")
```

### Batch Processing

```python
# Process multiple sequences
sequences = [
    ("CDR1", "RASQSISSWLA", {4: "QE", 6: "ST"}),
    ("CDR2", "AASSLQS", {3: "ST", 5: "LI"}),
    ("CDR3", "QQSYSTPLT", {3: "ST", 7: "PT"})
]

for name, seq, vars in sequences:
    result = phagetrix.optimize_codons(seq, vars)
    print(f"{name}: {result['final_sequence']}")
```

For complete examples, see **[Library Usage Guide](LIBRARY_USAGE.md)** and run:
```bash
python examples/library_examples.py
```

## Advanced Features

### Custom Numbering
Add position offsets for working with longer sequences:

```txt
# offset = 20
VLAYMVAQVQ
A23AGVIL  # Position 23 in the full protein
```

### Multiple Vendors
Choose your preferred DNA synthesis company:

```bash
phagetrix --company IDT input.txt      # Default
phagetrix --company Eurofins input.txt
phagetrix --company NEB input.txt
```

### Species-Specific Codon Usage
Optimize for different organisms:

```bash
phagetrix --species e_coli input.txt           # Default
phagetrix --species h_sapiens_9606 input.txt  # Human
phagetrix --species s_cerevisiae_4932 input.txt  # Yeast
```

## Documentation & Support

- **[Library Usage Guide](LIBRARY_USAGE.md)** - Complete Python library documentation
- **[Contributing Guidelines](CONTRIBUTING.md)** - Help improve Phagetrix
- **[Release Process](RELEASE.md)** - How to create releases
- **[GitHub Workflows](.github/WORKFLOWS.md)** - Automated CI/CD and release process
- **[Changelog](CHANGELOG.md)** - See what's new
- **[Examples](examples/)** - Code examples and tutorials

## Citation

If you use Phagetrix in your research, please cite:

```bibtex
@software{phagetrix,
  title = {Phagetrix: Codon optimization for phage display libraries},
  author = {Stamm, Reto},
  doi = {10.5281/zenodo.7676572},
  url = {https://github.com/retospect/phagetrix}
}
```

## Related Tools

- **[varVAMP](https://github.com/jonas-fuchs/varVAMP)** - Primers for highly variable genomes
- **[Biopython](https://biopython.org/)** - Python bioinformatics toolkit

## Acknowledgments

This package has been enhanced and maintained with assistance from **[Windsurf](https://codeium.com/windsurf)**, an AI-powered development environment that helped implement modern development practices, comprehensive testing, type safety, security scanning, and automated CI/CD workflows.

## License

This project is licensed under the GPL-3.0-or-later License - see the [LICENSE](LICENSE) file for details.
