# Phagetrix

[![Open in Google Colab](
https://colab.research.google.com/assets/colab-badge.svg)](
https://colab.research.google.com/github/retospect/phagetrix/blob/main/phagetrix.ipynb)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7676572.svg)](
https://doi.org/10.5281/zenodo.7676572)
[![PyPI version](https://badge.fury.io/py/phagetrix.svg)](https://badge.fury.io/py/phagetrix)
[![Action Status](https://github.com/retospect/phagetrix/actions/workflows/check.yml/badge.svg)](https://github.com/retospect/phagetrix/actions/workflows/check.yml)

A codon optimizer for [phage display library](
https://bio.libretexts.org/Bookshelves/Biochemistry/Supplemental_Modules_(Biochemistry)/4._Biotechnology_2/4.3%3A_M13_Phage_Display_Libraries)
generation.

When making phage display libraries, it's easy to run out of permutations. 1 liter of phage solution can hold about
$10^{12}$ different sequences.

We can approximate how many combinations we generate with $(nr\ of\ choices)^{(nr\ of\ positions)}$.
If we change the aminoacids to "any" aminoacid, we can change about 9 AA's: $20^9 \approx 10^{12}$
permutations.

If we use the degenerate codon capabilities of the manufactureres such as
[IDT](https://www.idtdna.com/pages/support/faqs/what-are-the-base-degeneracy-codes-that-you-use-(eg.-r-w-k-v-s)-)
to the fullest, we can probably make combinations that are partially rational, and allow for 6 permutations in any
postion.

That allows us to check out many more combinations that are likely to work: $6^{15} \approx 10^{12}$, so about 15
variable AA's instead of 9.

This tool allows you to easily specify what AA permutations you want, in which position, and calculates the best
sequence of degenerate codons.

## Example

PhageTrix is a tool to generate phage display libraries.
You probably have an idea what AA's you want to replace, and what
you want to replace them with.
The sequence companies have a reasonable number of
The file format has the AA sequence on the first line.
Each following line is the AA to be changed,
the digits indicating its position,
and the AA options that should be generated for that position.
The AA options are concatenated together with no spaces.
Phagetrix will generate the best degenerate codon for each position.

Example:

```txt
VLAYMVAQVQ
A3AGVIL
Y4YFW
A7AVIL
```

1. The first line is the sequence you want to alter.
2. The P in position 3 should be either a P, F, Y or an A
3. The Y in position 4 should be either a Y, P, F, or an E
4. The A in position 7 should be either an A, V, I, L or an M

Output:

```txt
phagetrix ./sample.phagetrix
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
          1T
          1P

GTTCTTVBATDKATGGTTVYACAGGTTCAG
```

The lines of the output show:
1. number of the AA on the first line
2. original AA on the second line
3. codon made from degenerate basepairs
4. the percentage of product for this codon that matches what the user specified
5. how many codons code for which aminoacid. The AA below the ```--``` line are off-target codons that were not
   requested.
- the last line shows the codons made from degenerate basepairs again, in a format that can easily be copied and pasted.

By default this uses the degenerate codons from
[IDT](
https://www.idtdna.com/pages/support/faqs/what-are-the-base-degeneracy-codes-that-you-use-(eg.-r-w-k-v-s)-).

# Try it

- [![Open in Google Colab](
https://colab.research.google.com/assets/colab-badge.svg)](
https://colab.research.google.com/github/retospect/phagetrix/blob/main/phagetrix.ipynb)
- Install it on your machine ```pip install phagetrix``` to get the ```phagetrix``` command line tool. Requires python3.
