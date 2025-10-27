"""Input parsing and validation for phagetrix."""

import re
from typing import Dict, List, Tuple

from .constants import VALID_AMINO_ACIDS


class InputParser:
    """Parses and validates phagetrix input files."""

    def __init__(self) -> None:
        self.valid_aas = VALID_AMINO_ACIDS

    def parse(self, lines: List[str]) -> Tuple[str, Dict[int, str], Dict[str, float]]:
        """
        Parse input lines into sequence, variations, and configuration.

        Args:
            lines: List of input lines from file

        Returns:
            Tuple of (sequence, variations_dict, config_dict)
        """
        # Validate input size to prevent DoS
        if len(lines) == 0:
            raise ValueError("Input file is empty")
        if len(lines) > 1000:  # Reasonable limit
            raise ValueError(f"Input file too large: {len(lines)} lines (max 1000)")

        # Get and validate the sequence
        seq = lines[0].strip()
        if not seq:
            raise ValueError("First line (sequence) cannot be empty")
        if len(seq) > 10000:  # Reasonable protein length limit
            raise ValueError(f"Sequence too long: {len(seq)} amino acids (max 10000)")

        # Validate sequence contains only valid amino acids
        for i, aa in enumerate(seq):
            if aa not in self.valid_aas:
                raise ValueError(
                    f"Invalid amino acid '{aa}' at position {i+1} in sequence"
                )

        # Parse variations and configuration
        variations: Dict[int, str] = {}
        config: Dict[str, float] = {"offset": 0.0}

        for line in lines[1:]:
            line = line.strip()
            if line == "":
                continue

            if line.startswith("#"):
                self._parse_config_line(line, config)
            else:
                self._parse_variation_line(line, seq, variations)

        return seq, variations, config

    def _parse_config_line(self, line: str, config: Dict[str, float]) -> None:
        """Parse a configuration line starting with #."""
        if re.match(r"#\s*\w+\s*=\s*\d+\.?\d*", line):
            # Get the name of the variable with validation
            var_match = re.search(r"\w+", line[1:])
            if not var_match:
                raise ValueError(f"Invalid configuration line: {line}")
            var_name = var_match.group()

            # Whitelist allowed configuration variables for security
            allowed_vars = {"offset"}
            if var_name not in allowed_vars:
                raise ValueError(
                    f"Configuration variable '{var_name}' not allowed. Allowed: {allowed_vars}"
                )

            # Get the value of the variable with validation
            val_match = re.search(r"\d+\.?\d*", line[1:])
            if not val_match:
                raise ValueError(f"Invalid configuration value in line: {line}")
            var_value = float(val_match.group())

            # Validate numeric ranges for security
            if var_name == "offset" and (var_value < -1000000 or var_value > 1000000):
                raise ValueError(
                    f"Offset value {var_value} out of reasonable range (-1000000 to 1000000)"
                )

            config[var_name] = var_value
        else:
            # Malformed configuration line
            raise ValueError(f"Invalid configuration line: {line}")

    def _parse_variation_line(
        self, line: str, seq: str, variations: Dict[int, str]
    ) -> None:
        """Parse a variation line specifying amino acid changes."""
        # Validate line has content
        if len(line) < 2:
            raise ValueError(f"Invalid line format (too short): {line}")

        original_aa = line[0]

        # Get the position number
        pos_match = re.search(r"\d+", line[1:])
        if not pos_match:
            raise ValueError(f"No position number found in line: {line}")
        position = int(pos_match.group())

        # Validate position is within sequence bounds
        if position < 1 or position > len(seq):
            raise ValueError(
                f"Position {position} is out of bounds for sequence of length {len(seq)}"
            )

        # Get the list of amino acids to be used for the degenerate codon
        aas = line[1 + pos_match.end() :]

        # Validate we have amino acids specified
        if not aas:
            raise ValueError(f"No amino acids specified in line: {line}")

        # Ensure that the amino acid in the sequence matches the one in the line
        if seq[position - 1] != original_aa:
            raise ValueError(
                f"Amino acid in sequence at position {position} is {seq[position - 1]}, not {original_aa}"
            )

        # Check that all the amino acids in the list are valid
        for aa in aas:
            if aa not in self.valid_aas:
                raise ValueError(f"Amino acid {aa} is not valid")

        # Add the variation to the dictionary
        variations[position] = aas
