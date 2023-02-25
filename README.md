# Phagetrix

[![Open in Google Colab](
https://colab.research.google.com/assets/colab-badge.svg)](
https://colab.research.google.com/github/retospect/phagetrix/blob/main/phagetrix.ipynb)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7676572.svg)](
https://doi.org/10.5281/zenodo.7676572)
[![Action status](
https://github.com/retospect/phagetrix/actions/workflows/check.yml/badge.svg)](
https://github.com/retospect/phageterix/actions/workflows/check.yml)

A codon optimizer for phage display library generation.

## Example

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

```txt
VLPYMVAQVQ
P3PFYA
Y4YPFYE
A7AVILM
```

1. The first line is the sequence you want to alter.
2. The P in position 3 should be either a P, F, Y or an A
3. The Y in position 4 should be either a Y, P, F, or an E
4. The A in position 7 should be either an A, V, I, L or an M

Output:

```txt
   1   2   3   4   5   6   7   8   9  10
   V   L   P   Y   M   V   A   Q   V   Q
 GTT CTT BHC BHW ATG GTT DYR CAG GTT CAG

GTTCTTBHCBHWATGGTTDYRCAGGTTCAG
```

By default this uses the degenerate codons from
[IDT](
https://www.idtdna.com/pages/support/faqs/what-are-the-base-degeneracy-codes-that-you-use-(eg.-r-w-k-v-s)-)

## Try before buy

Try in Google Colab for free right now:
[![Open in Google Colab](
https://colab.research.google.com/assets/colab-badge.svg)](
https://colab.research.google.com/github/retospect/phagetrix/blob/main/phagetrix.ipynb)
