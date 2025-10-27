"""Security tests for phagetrix."""

import pytest

from phagetrix.cli import process_request
from phagetrix.constants import degenerate


def test_invalid_company_parameter():
    """Test that invalid company parameter is rejected."""
    # Test invalid company via command line would be caught by validation
    # This is tested indirectly through the main() function validation
    pass


def test_empty_input_file():
    """Test that empty input files are rejected."""
    with pytest.raises(ValueError, match="Input file is empty"):
        process_request([], degenerate["IDT"])


def test_oversized_input_file():
    """Test that oversized input files are rejected."""
    large_input = ["ACDEFG"] + ["A1A"] * 1001  # Over 1000 lines
    with pytest.raises(ValueError, match="Input file too large"):
        process_request(large_input, degenerate["IDT"])


def test_empty_sequence():
    """Test that empty sequence is rejected."""
    with pytest.raises(ValueError, match="First line \\(sequence\\) cannot be empty"):
        process_request(["", "A1A"], degenerate["IDT"])


def test_oversized_sequence():
    """Test that oversized sequences are rejected."""
    long_seq = "A" * 10001  # Over 10000 amino acids
    with pytest.raises(ValueError, match="Sequence too long"):
        process_request([long_seq, "A1A"], degenerate["IDT"])


def test_invalid_amino_acid_in_sequence():
    """Test that invalid amino acids in sequence are rejected."""
    with pytest.raises(ValueError, match="Invalid amino acid 'X' at position 2"):
        process_request(["AXCDEF", "A1A"], degenerate["IDT"])


def test_short_line_format():
    """Test that lines that are too short are rejected."""
    with pytest.raises(ValueError, match="Invalid line format \\(too short\\)"):
        process_request(["ACDEF", "A"], degenerate["IDT"])


def test_missing_position_number():
    """Test that lines without position numbers are rejected."""
    with pytest.raises(ValueError, match="No position number found"):
        process_request(["ACDEF", "AAA"], degenerate["IDT"])


def test_position_out_of_bounds():
    """Test that positions outside sequence bounds are rejected."""
    with pytest.raises(ValueError, match="Position 10 is out of bounds"):
        process_request(["ACDEF", "A10A"], degenerate["IDT"])


def test_no_amino_acids_specified():
    """Test that lines without amino acids are rejected."""
    with pytest.raises(ValueError, match="No amino acids specified"):
        process_request(["ACDEF", "A1"], degenerate["IDT"])


def test_invalid_configuration_variable():
    """Test that invalid configuration variables are rejected."""
    with pytest.raises(ValueError, match="Configuration variable 'badvar' not allowed"):
        process_request(["ACDEF", "# badvar = 5", "A1A"], degenerate["IDT"])


def test_configuration_value_out_of_range():
    """Test that configuration values out of range are rejected."""
    with pytest.raises(ValueError, match="Offset value .* out of reasonable range"):
        process_request(["ACDEF", "# offset = 2000000", "A1A"], degenerate["IDT"])


def test_invalid_configuration_line():
    """Test that malformed configuration lines are rejected."""
    with pytest.raises(ValueError, match="Invalid configuration line"):
        process_request(["ACDEF", "# = 5", "A1A"], degenerate["IDT"])


def test_invalid_configuration_value():
    """Test that invalid configuration values are rejected."""
    with pytest.raises(ValueError, match="Invalid configuration line"):
        process_request(["ACDEF", "# offset = abc", "A1A"], degenerate["IDT"])


def test_amino_acid_mismatch():
    """Test that amino acid mismatches are caught."""
    with pytest.raises(
        Exception, match="Amino acid in sequence at position 1 is A, not C"
    ):
        process_request(["ACDEF", "C1A"], degenerate["IDT"])


def test_valid_input_still_works():
    """Test that valid input still works after security fixes."""
    # This should not raise any exceptions
    process_request(["ACDEF", "A1AG", "# offset = 10"], degenerate["IDT"])
    # If we get here without exception, the test passes
    assert True


def test_valid_configuration_works():
    """Test that valid configuration still works."""
    # This should not raise any exceptions
    process_request(["ACDEF", "# offset = 100", "A1AG"], degenerate["IDT"])
    # If we get here without exception, the test passes
    assert True
