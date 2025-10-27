"""Tests for code quality and linting."""

import subprocess
import sys
from pathlib import Path

import pytest


def run_command(cmd):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=True
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr


def test_black_formatting():
    """Test that all Python files are properly formatted with black."""
    returncode, stdout, stderr = run_command("poetry run black --check .")

    if returncode != 0:
        # Extract the files that need reformatting from black output
        lines = stdout.split("\n") + stderr.split("\n")
        files_to_reformat = []
        for line in lines:
            if "would reformat" in line:
                # Extract filename from "would reformat /path/to/file.py"
                parts = line.split()
                if len(parts) >= 3:
                    files_to_reformat.append(parts[2])

        if files_to_reformat:
            files_str = "\n  ".join(files_to_reformat)
            pytest.fail(
                f"Black formatting check failed. The following files need reformatting:\n"
                f"  {files_str}\n\n"
                f"Run 'poetry run black .' to fix formatting issues."
            )
        else:
            pytest.fail(f"Black formatting check failed:\n{stdout}\n{stderr}")


def test_isort_import_sorting():
    """Test that all imports are properly sorted with isort."""
    returncode, stdout, stderr = run_command("poetry run isort --check-only .")

    if returncode != 0:
        # Extract files with import issues
        lines = stderr.split("\n")
        files_with_issues = []
        for line in lines:
            if "ERROR:" in line and "Imports are incorrectly sorted" in line:
                # Extract filename from error message
                parts = line.split()
                if len(parts) >= 2:
                    files_with_issues.append(parts[1])

        if files_with_issues:
            files_str = "\n  ".join(files_with_issues)
            pytest.fail(
                f"Import sorting check failed. The following files have incorrectly sorted imports:\n"
                f"  {files_str}\n\n"
                f"Run 'poetry run isort .' to fix import sorting issues."
            )
        else:
            pytest.fail(f"Import sorting check failed:\n{stdout}\n{stderr}")


def test_flake8_linting():
    """Test that all Python files pass flake8 linting."""
    returncode, stdout, stderr = run_command("poetry run flake8 src tests")

    if returncode != 0:
        pytest.fail(
            f"Flake8 linting check failed:\n{stdout}\n{stderr}\n\n"
            f"Fix the linting issues above."
        )


@pytest.mark.skipif(sys.platform == "win32", reason="mypy can be flaky on Windows CI")
def test_mypy_type_checking():
    """Test that all Python files pass mypy type checking."""
    returncode, stdout, stderr = run_command("poetry run mypy src")

    if returncode != 0:
        pytest.fail(
            f"MyPy type checking failed:\n{stdout}\n{stderr}\n\n"
            f"Fix the type checking issues above."
        )


def test_project_structure():
    """Test that the project has the expected structure."""
    project_root = Path(__file__).parent.parent

    # Check for essential files
    essential_files = [
        "pyproject.toml",
        "README.md",
        "src/phagetrix/__init__.py",
        "src/phagetrix/api.py",
        "src/phagetrix/cli.py",
        "tests/test_api.py",
    ]

    missing_files = []
    for file_path in essential_files:
        if not (project_root / file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        pytest.fail(f"Missing essential files: {missing_files}")


def test_no_debug_statements():
    """Test that there are no debug statements or breakpoints in source code."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"

    debug_patterns = [
        "import pdb",
        "pdb.set_trace()",
        "breakpoint()",
        # Only catch obvious debug prints, not legitimate output
        "print('DEBUG",
        'print("DEBUG',
        "print(f'DEBUG",
        'print(f"DEBUG',
    ]

    issues = []
    for py_file in src_dir.rglob("*.py"):
        content = py_file.read_text()
        for line_num, line in enumerate(content.splitlines(), 1):
            for pattern in debug_patterns:
                if pattern in line and not line.strip().startswith("#"):
                    # Skip if it's in a docstring or comment
                    if '"""' not in line and "'''" not in line:
                        issues.append(
                            f"{py_file.relative_to(project_root)}:{line_num}: {line.strip()}"
                        )

    if issues:
        issues_str = "\n  ".join(issues)
        pytest.fail(
            f"Found debug statements in source code:\n"
            f"  {issues_str}\n\n"
            f"Remove debug statements before committing."
        )
