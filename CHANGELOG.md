# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Modern Poetry package configuration with PEP 621 format
- Comprehensive development tooling (Black, isort, flake8, pytest)
- GitHub Actions CI/CD pipeline with latest action versions
- Pre-commit hooks for code quality
- Makefile with common development tasks
- Type checking setup with mypy
- Code coverage reporting
- Modern .gitignore with comprehensive exclusions

### Changed
- Updated to modern Poetry project structure
- Migrated from deprecated Poetry configuration to PEP 621 format
- Updated GitHub Actions to use latest versions (checkout@v4, setup-python@v5)
- Improved error handling (replaced asserts with proper exceptions)
- Updated Python version requirement to >=3.8.1
- Pinned dependencies to specific version ranges

### Fixed
- Fixed hardcoded species parameter bug - now properly uses --species argument
- Fixed typo "Phagerix" → "Phagetrix" in documentation
- Fixed trailing whitespace issues
- Fixed README documentation inconsistencies
- Removed undefined tox environments and unused variables

### Removed
- Removed support for Python 3.7 (EOL)
- Removed unstable Python development versions from CI

## [0.2.3] - 2023-XX-XX

### Added
- Initial release with basic phage display library optimization functionality
- Support for multiple degenerate codon providers (IDT, Eurofins, NEB)
- Command-line interface with species and company options
- Basic test suite

[Unreleased]: https://github.com/retospect/phagetrix/compare/v0.2.3...HEAD
[0.2.3]: https://github.com/retospect/phagetrix/releases/tag/v0.2.3
