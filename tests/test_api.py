"""Tests for the phagetrix API module."""

import tempfile
import os
import pytest

from phagetrix import api


def test_optimize_codons_basic():
    """Test basic codon optimization functionality."""
    result = api.optimize_codons(
        sequence="ACDEF",
        variations={1: "AG", 3: "DEF"},
        company="IDT",
        species="e_coli"
    )
    
    assert result["sequence"] == "ACDEF"
    assert result["company"] == "IDT"
    assert result["species"] == "e_coli"
    assert result["offset"] == "0"
    assert len(result["degenerate_codons"]) == 5
    assert len(result["efficiency"]) == 5
    assert "final_sequence" in result
    assert "variations" in result


def test_optimize_codons_with_offset():
    """Test codon optimization with offset."""
    result = api.optimize_codons(
        sequence="ACDEF",
        variations={1: "AG"},
        offset=10
    )
    
    assert result["offset"] == "10"


def test_optimize_codons_different_companies():
    """Test optimization with different companies."""
    for company in ["IDT", "Eurofins", "NEB"]:
        result = api.optimize_codons(
            sequence="AC",
            variations={1: "AG"},
            company=company
        )
        assert result["company"] == company


def test_optimize_codons_different_species():
    """Test optimization with different species."""
    result = api.optimize_codons(
        sequence="AC",
        variations={1: "AG"},
        species="h_sapiens_9606"
    )
    assert result["species"] == "h_sapiens_9606"


def test_optimize_codons_invalid_sequence():
    """Test that invalid amino acids in sequence are rejected."""
    with pytest.raises(ValueError, match="Invalid amino acid"):
        api.optimize_codons("ACXDEF", {})


def test_optimize_codons_invalid_variations():
    """Test that invalid amino acids in variations are rejected."""
    with pytest.raises(ValueError, match="Invalid amino acid"):
        api.optimize_codons("ACDEF", {1: "AX"})


def test_optimize_codons_position_out_of_range():
    """Test that positions out of range are rejected."""
    with pytest.raises(ValueError, match="Position 10 out of range"):
        api.optimize_codons("ACDEF", {10: "AG"})


def test_optimize_codons_invalid_company():
    """Test that invalid company is rejected."""
    with pytest.raises(ValueError, match="Unknown company"):
        api.optimize_codons("AC", {}, company="InvalidCompany")


def test_optimize_codons_invalid_species():
    """Test that invalid species is rejected."""
    with pytest.raises(ValueError, match="Unknown species"):
        api.optimize_codons("AC", {}, species="invalid_species")


def test_parse_phagetrix_file():
    """Test parsing a phagetrix file."""
    content = """VLAYMVAQVQ
A3AGVIL
Y4YFW
A7AVIL
#offset=5
"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.phagetrix') as f:
        f.write(content)
        temp_path = f.name
    
    try:
        seq, variations, config = api.parse_phagetrix_file(temp_path)
        
        assert seq == "VLAYMVAQVQ"
        assert variations == {3: "AGVIL", 4: "YFW", 7: "AVIL"}
        assert config == {"offset": 5.0}
    finally:
        os.unlink(temp_path)


def test_parse_phagetrix_file_nonexistent():
    """Test parsing a non-existent file."""
    with pytest.raises(FileNotFoundError):
        api.parse_phagetrix_file("/nonexistent/file.phagetrix")


def test_get_available_companies():
    """Test getting available companies."""
    companies = api.get_available_companies()
    
    assert isinstance(companies, list)
    assert "IDT" in companies
    assert "Eurofins" in companies
    assert "NEB" in companies


def test_get_available_species():
    """Test getting available species."""
    species = api.get_available_species()
    
    assert isinstance(species, list)
    assert len(species) > 0
    assert "e_coli_316407" in species


def test_get_available_species_with_aliases():
    """Test getting available species including aliases."""
    species = api.get_available_species_with_aliases()
    
    assert isinstance(species, list)
    assert "e_coli" in species  # alias
    assert "e_coli_316407" in species  # full name


def test_get_degenerate_codons():
    """Test getting degenerate codon mappings."""
    codons = api.get_degenerate_codons("IDT")
    
    assert isinstance(codons, dict)
    assert "R" in codons
    assert codons["R"] == "AG"


def test_get_degenerate_codons_invalid_company():
    """Test getting degenerate codons for invalid company."""
    with pytest.raises(ValueError, match="Unknown company"):
        api.get_degenerate_codons("InvalidCompany")


def test_calculate_library_stats():
    """Test calculating library statistics."""
    stats = api.calculate_library_stats(
        sequence="ACDEF",
        variations={1: "AG", 3: "DEF"}
    )
    
    assert isinstance(stats, dict)
    assert "diversity" in stats
    assert "probability_single" in stats
    assert "material_moles" in stats
    assert "material_amount" in stats
    assert "codons_used" in stats
    assert "final_sequence" in stats
    
    assert stats["diversity"] > 0
    assert 0 < stats["probability_single"] <= 1
    assert stats["material_moles"] > 0


def test_calculate_library_stats_different_company():
    """Test library stats with different company."""
    stats = api.calculate_library_stats(
        sequence="AC",
        variations={1: "AG"},
        company="Eurofins"
    )
    
    assert stats["diversity"] > 0


def test_species_alias_resolution():
    """Test that species aliases are resolved correctly."""
    # Test with alias
    result1 = api.optimize_codons("AC", {}, species="e_coli")
    
    # Test with full name
    result2 = api.optimize_codons("AC", {}, species="e_coli_316407")
    
    # Both should work and produce similar results
    assert result1["species"] == "e_coli"
    assert result2["species"] == "e_coli_316407"
    assert len(result1["degenerate_codons"]) == len(result2["degenerate_codons"])


def test_resolve_species_alias_function():
    """Test the internal species alias resolution function."""
    # Test alias resolution
    assert api._resolve_species_alias("e_coli") == "e_coli_316407"
    
    # Test non-alias (should return as-is)
    assert api._resolve_species_alias("h_sapiens_9606") == "h_sapiens_9606"


def test_api_convenience_aliases():
    """Test that convenience aliases work."""
    # Test optimize alias
    result1 = api.optimize("AC", {})
    result2 = api.optimize_codons("AC", {})
    
    assert result1["sequence"] == result2["sequence"]
    
    # Test parse_file alias
    content = "AC\n"
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.phagetrix') as f:
        f.write(content)
        temp_path = f.name
    
    try:
        seq1, vars1, config1 = api.parse_file(temp_path)
        seq2, vars2, config2 = api.parse_phagetrix_file(temp_path)
        
        assert seq1 == seq2
        assert vars1 == vars2
        assert config1 == config2
    finally:
        os.unlink(temp_path)
