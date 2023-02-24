
from phagetrix.trix import DegenerateCodonGenerator

def test_single_aminoacid_codon():
    codon_gen = DegenerateCodonGenerator()
    assert codon_gen.get_best_degenerate_codon('A') in ['GCT', 'GCC', 'GCA', 'GCG']

def test_pairs_of_aminoacid_codons():
    codon_gen = DegenerateCodonGenerator()

    assert codon_gen.get_best_degenerate_codon('HQ') in ['CAM', 'CAK', 'CAS', 'CAW']
    assert codon_gen.get_best_degenerate_codon('MTKR') in ['ANG']
    # string that contains all aminoacids
    s = 'FLIMVSPTAYHQNKDECWRSG'

    assert codon_gen.get_best_degenerate_codon(s) in ['NNS', 'NNN']



