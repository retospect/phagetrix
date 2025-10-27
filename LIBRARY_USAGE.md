# Phagetrix Library Usage Guide

This guide shows how to use Phagetrix as a Python library after installing with `pip install phagetrix`.

## Quick Start

```python
import phagetrix

# Simple codon optimization
result = phagetrix.optimize_codons(
    sequence="VLAYMVAQVQ",
    variations={3: "AGVIL", 4: "YFW", 7: "AVIL"}
)

print("Optimized sequence:", result["final_sequence"])
print("Efficiency:", result["efficiency"])
```

## High-Level API Functions

### 1. `optimize_codons()` - Main Function

Optimize degenerate codons for your protein sequence.

```python
import phagetrix

result = phagetrix.optimize_codons(
    sequence="ACDEFGHIKL",           # Your amino acid sequence
    variations={                     # Position -> allowed amino acids
        1: "AG",                     # Position 1: A or G
        3: "DEF",                    # Position 3: D, E, or F  
        5: "GHIKL"                   # Position 5: G, H, I, K, or L
    },
    company="IDT",                   # DNA synthesis company
    species="e_coli",                # Organism for codon usage
    offset=0                         # Position numbering offset
)

# Results
print("Original sequence:", result["sequence"])
print("Degenerate codons:", result["degenerate_codons"])
print("Final DNA sequence:", result["final_sequence"])
print("Efficiency per position:", result["efficiency"])
```

### 2. `parse_phagetrix_file()` - File Parsing

Parse standard Phagetrix input files.

```python
# Parse a .phagetrix file
sequence, variations, config = phagetrix.parse_phagetrix_file("input.phagetrix")

print(f"Sequence: {sequence}")
print(f"Variations: {variations}")
print(f"Config: {config}")

# Use parsed data for optimization
result = phagetrix.optimize_codons(sequence, variations)
```

### 3. `get_available_companies()` - Supported Vendors

```python
companies = phagetrix.get_available_companies()
print("Supported companies:", companies)
# Output: ['IDT', 'Eurofins', 'NEB']
```

### 4. `get_available_species()` - Supported Organisms

```python
species = phagetrix.get_available_species()
print("Available species:", species[:5])  # Show first 5
# Output: ['e_coli_316407', 'h_sapiens_9606', 's_cerevisiae_4932', ...]
```

### 5. `get_degenerate_codons()` - Vendor Codon Maps

```python
# Get degenerate codon mappings
idt_codons = phagetrix.get_degenerate_codons("IDT")
print("IDT degenerate codes:")
for code, bases in idt_codons.items():
    print(f"  {code} = {bases}")

# Output:
#   R = AG
#   Y = CT  
#   M = AC
#   ...
```

### 6. `calculate_library_stats()` - Library Statistics

```python
stats = phagetrix.calculate_library_stats(
    sequence="ACDEF",
    variations={1: "AG", 3: "DEF"}
)

print(f"Theoretical diversity: {stats['diversity']:,}")
print(f"Single variant probability: {stats['probability_single']:.2e}")
print(f"Material needed: {stats['material_amount']}")
print(f"Final sequence: {stats['final_sequence']}")
```

## Common Use Cases

### Case 1: Simple Antibody CDR Optimization

```python
import phagetrix

# CDR3 loop optimization
cdr3_sequence = "CARSGDYYGMDVW"
variations = {
    4: "SGTN",      # Position 4: Ser, Gly, Thr, or Asn
    5: "GAST",      # Position 5: Gly, Ala, Ser, or Thr  
    6: "DEQN",      # Position 6: Asp, Glu, Gln, or Asn
    7: "YFW",       # Position 7: Tyr, Phe, or Trp
    8: "YFW"        # Position 8: Tyr, Phe, or Trp
}

result = phagetrix.optimize_codons(
    sequence=cdr3_sequence,
    variations=variations,
    company="IDT",
    species="h_sapiens_9606"  # Human codon usage
)

print("CDR3 optimized sequence:", result["final_sequence"])
print("Efficiency:", [f"{e}%" for e in result["efficiency"]])
```

### Case 2: Batch Processing Multiple Sequences

```python
import phagetrix

sequences = [
    ("peptide1", "ACDEF", {1: "AG", 3: "DEF"}),
    ("peptide2", "GHIKL", {2: "HK", 4: "KL"}),
    ("peptide3", "MNPQR", {1: "MN", 5: "QR"})
]

results = {}
for name, seq, vars in sequences:
    result = phagetrix.optimize_codons(seq, vars)
    results[name] = result["final_sequence"]
    print(f"{name}: {result['final_sequence']}")
```

### Case 3: Compare Different Companies

```python
import phagetrix

sequence = "ACDEF"
variations = {1: "AG", 3: "DEF"}

for company in phagetrix.get_available_companies():
    result = phagetrix.optimize_codons(sequence, variations, company=company)
    print(f"{company}: {result['final_sequence']}")
```

### Case 4: Library Design with Statistics

```python
import phagetrix

# Design a focused library
sequence = "CARSGDYYGMDVW"
variations = {4: "ST", 6: "DE", 7: "YF"}  # Conservative changes

# Get optimization results
result = phagetrix.optimize_codons(sequence, variations)

# Calculate library statistics  
stats = phagetrix.calculate_library_stats(sequence, variations)

print("Library Design Summary:")
print(f"  Target sequence: {sequence}")
print(f"  Optimized DNA: {result['final_sequence']}")
print(f"  Theoretical diversity: {stats['diversity']:,} variants")
print(f"  Material needed: {stats['material_amount']}")
print(f"  Average efficiency: {sum(result['efficiency'])/len(result['efficiency']):.1f}%")
```

## Advanced Usage

### Working with Raw Classes

For advanced users who need more control:

```python
from phagetrix import DegenerateCodonGenerator, degenerate
import python_codon_tables as pct

# Create generator with specific settings
generator = DegenerateCodonGenerator(
    degenerate_bases=degenerate["IDT"],
    codon_frequency=pct.get_codons_table("h_sapiens_9606")
)

# Get best codon for specific amino acids
best_codon = generator.get_best_degenerate_codon("AG")
print(f"Best codon for A or G: {best_codon}")

# Get all possible codons from degenerate codon
normal_codons = generator.get_normal_codons("VBA")
print(f"VBA expands to: {normal_codons}")
```

### Error Handling

```python
import phagetrix

try:
    result = phagetrix.optimize_codons(
        sequence="ACDEFX",  # Invalid amino acid X
        variations={1: "AG"}
    )
except ValueError as e:
    print(f"Error: {e}")

try:
    result = phagetrix.optimize_codons(
        sequence="ACDEF",
        variations={10: "AG"},  # Position out of range
        company="InvalidCompany"  # Invalid company
    )
except ValueError as e:
    print(f"Error: {e}")
```

## Integration Examples

### With Pandas for Data Analysis

```python
import pandas as pd
import phagetrix

# Create a DataFrame of sequences to optimize
data = pd.DataFrame({
    'name': ['seq1', 'seq2', 'seq3'],
    'sequence': ['ACDEF', 'GHIKL', 'MNPQR'],
    'variations': ['{1: "AG"}', '{2: "HK"}', '{1: "MN"}']
})

# Apply optimization
def optimize_row(row):
    vars_dict = eval(row['variations'])  # In production, use safer parsing
    result = phagetrix.optimize_codons(row['sequence'], vars_dict)
    return result['final_sequence']

data['optimized'] = data.apply(optimize_row, axis=1)
print(data)
```

### With Jupyter Notebooks

```python
# Great for interactive analysis
import phagetrix
import matplotlib.pyplot as plt

# Analyze efficiency across positions
result = phagetrix.optimize_codons("ACDEFGHIKL", {i: "AG" for i in [1,3,5,7,9]})

plt.bar(range(len(result['efficiency'])), result['efficiency'])
plt.xlabel('Position')
plt.ylabel('Efficiency (%)')
plt.title('Codon Optimization Efficiency')
plt.show()
```

## Tips and Best Practices

1. **Start Simple**: Use `optimize_codons()` for most cases
2. **Validate Inputs**: Check sequences and positions before optimization
3. **Consider Species**: Use appropriate codon usage tables for your expression system
4. **Compare Vendors**: Different companies may give different results
5. **Check Efficiency**: Monitor the efficiency percentages for each position
6. **Library Size**: Use `calculate_library_stats()` to estimate diversity

## Getting Help

- **Documentation**: https://github.com/retospect/phagetrix
- **Issues**: https://github.com/retospect/phagetrix/issues
- **Examples**: See the `examples/` directory in the repository

## Next Steps

- Try the examples above with your own sequences
- Explore the command-line interface: `phagetrix --help`
- Check out the Jupyter notebook examples
- Read the full API documentation
