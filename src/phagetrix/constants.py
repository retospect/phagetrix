"""Constants for phagetrix package."""

# Source: https://www.idtdna.com/pages/support/faqs/what-are-the-base-degeneracy-codes-that-you-use-(eg.-r-w-k-v-s)-
# Retrieved 2023-FEB-23
# Source: https://www.eurofinsgenomics..com/en/products/dnarna-sythesis/degenerate-bases
# Retrieved 2023-FEB-24
# Source: https://www.neb.com/tools-and-resources/usage-guidelines/single-letter-codes
# Retrieved 2023-FEB-24

degenerate = {
    "IDT": {
        "R": "AG",
        "Y": "CT",
        "M": "AC",
        "K": "GT",
        "S": "CG",
        "W": "AT",
        "H": "ACT",
        "B": "CGT",
        "V": "ACG",
        "D": "AGT",
        "N": "ACGT",
    },
    "Eurofins": {
        "R": "AG",
        "Y": "CT",
        "M": "AC",
        "K": "GT",
        "S": "CG",
        "W": "AT",
        "B": "CGT",
        "D": "AGT",
        "H": "ACT",
        "V": "ACG",
        "N": "ACGT",
    },
    "NEB": {
        "B": "CGT",
        "D": "AGT",
        "H": "ACT",
        "K": "GT",
        "M": "AC",
        "N": "ACGT",
        "R": "AG",
        "S": "CG",
        "V": "ACG",
        "W": "AT",
        "Y": "CT",
    },
}

# Valid amino acids for validation
VALID_AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

# Species aliases for common names
SPECIES_ALIASES = {
    "e_coli": "e_coli_316407",
}
