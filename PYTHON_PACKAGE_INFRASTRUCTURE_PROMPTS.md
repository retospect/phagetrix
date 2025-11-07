# Python Package Infrastructure Setup Prompts

This document provides comprehensive prompts for setting up a modern Python package with complete infrastructure including packaging, testing, code quality, CI/CD, and documentation.

## Table of Contents

1. [Package Setup & Configuration](#1-package-setup--configuration)
2. [Code Style & Formatting](#2-code-style--formatting)
3. [Testing Infrastructure](#3-testing-infrastructure)
4. [CI/CD & Automation](#4-cicd--automation)
5. [Project Structure & Documentation](#5-project-structure--documentation)
6. [Security & Quality Assurance](#6-security--quality-assurance)
7. [Release Management](#7-release-management)

---

## 1. Package Setup & Configuration

### Prompt: Modern Python Package Setup

```
Create a modern Python package with the following specifications:

**Package Details:**
- Package name: [PACKAGE_NAME]
- Description: [BRIEF_DESCRIPTION]
- Author: [AUTHOR_NAME] <[EMAIL]>
- License: [LICENSE] (e.g., MIT, GPL-3.0-or-later, Apache-2.0)
- Python versions: 3.10, 3.11, 3.12, 3.13
- Keywords: [RELEVANT_KEYWORDS]

**Requirements:**
1. Use Poetry for dependency management
2. Create pyproject.toml with proper project metadata
3. Set up src/ layout with package in src/[package_name]/
4. Configure entry points for CLI if needed
5. Include optional development dependencies
6. Set up proper classifiers for PyPI

**Dependencies to include:**
- Core dependencies: [LIST_CORE_DEPS]
- Development dependencies: pytest, black, isort, flake8, mypy, pre-commit, tox, bandit

**Project structure:**
```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── cli.py (if CLI needed)
│       └── core.py
├── tests/
├── examples/
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

Configure the pyproject.toml with:
- Build system using poetry-core
- Project metadata with proper classifiers
- Dependencies with version constraints
- Tool configurations for black, isort, pytest, mypy, coverage
- Entry points for scripts if needed
```

### Example pyproject.toml Template

```toml
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[project]
name = "your-package"
version = "0.1.0"
description = "Your package description"
authors = [{name = "Your Name", email = "your.email@example.com"}]
readme = "README.md"
license = "MIT"
keywords = ["keyword1", "keyword2"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
requires-python = ">=3.10"
dependencies = [
    # Add your core dependencies here
]

[project.urls]
Homepage = "https://github.com/username/package"
Repository = "https://github.com/username/package"
"Bug Tracker" = "https://github.com/username/package/issues"

[project.scripts]
your-package = "your_package.cli:main"  # If CLI needed

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0,<9.0.0",
    "pytest-cov>=4.1.0,<6.0.0",
    "black>=23.0.0,<25.0.0",
    "isort>=5.12.0,<6.0.0",
    "flake8>=6.0.0,<8.0.0",
    "mypy>=1.5.0,<2.0.0",
    "pre-commit>=3.4.0,<4.0.0",
    "tox>=4.11.0,<5.0.0",
    "bandit>=1.7.5,<2.0.0",
]

[tool.poetry]
packages = [{include = "your_package", from = "src"}]
```

---

## 2. Code Style & Formatting

### Prompt: Code Quality Setup

```
Set up comprehensive code quality tools for a Python project:

**Tools to configure:**
1. **Black** - Code formatting
2. **isort** - Import sorting
3. **flake8** - Linting
4. **mypy** - Type checking
5. **pre-commit** - Git hooks
6. **bandit** - Security scanning

**Requirements:**
- Line length: 88 characters (Black default)
- Python versions: 3.10+
- Type hints required for all functions
- Import organization with isort profile "black"
- Pre-commit hooks for automatic formatting
- Security scanning with bandit

**Configuration files needed:**
- .pre-commit-config.yaml
- .flake8 (or in pyproject.toml)
- Tool configurations in pyproject.toml

**Pre-commit hooks to include:**
- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-added-large-files
- check-merge-conflict
- debug-statements
- black formatting
- isort import sorting
- flake8 linting
- mypy type checking

**Makefile targets:**
- format: Run black and isort
- lint: Check formatting and linting
- type-check: Run mypy
- pre-commit: Run all pre-commit hooks
```

### Example Configuration Files

**.pre-commit-config.yaml:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]
```

**Tool configurations in pyproject.toml:**
```toml
[tool.black]
line-length = 88
target-version = ['py310', 'py311', 'py312', 'py313']
include = '\.pyi?$'
extend-exclude = '''
/(
  \.eggs
  | \.git
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["your_package"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
```

---

## 3. Testing Infrastructure

### Prompt: Comprehensive Testing Setup

```
Create a comprehensive testing infrastructure for a Python package:

**Testing Framework:**
- pytest as the main testing framework
- pytest-cov for coverage reporting
- Support for multiple Python versions (3.10-3.13)

**Test Structure:**
```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_core.py         # Core functionality tests
├── test_cli.py          # CLI tests (if applicable)
├── test_integration.py  # Integration tests
└── fixtures/            # Test data files
```

**Coverage Requirements:**
- Minimum 90% code coverage
- HTML and XML coverage reports
- Coverage exclusions for debug code and abstract methods

**Test Configuration:**
- pytest.ini or pyproject.toml configuration
- Strict markers and config
- Test discovery patterns
- Coverage reporting setup

**Tox Configuration:**
- Test against multiple Python versions
- Separate environments for linting and type checking
- Integration with GitHub Actions

**Makefile targets:**
- test: Run basic tests
- test-cov: Run tests with coverage
- tox: Run tests across all Python versions

**Test Types to Include:**
1. Unit tests for core functionality
2. Integration tests for workflows
3. CLI tests (if applicable)
4. Property-based testing (optional)
5. Performance tests (if needed)
```

### Example Test Configuration

**pytest configuration in pyproject.toml:**
```toml
[tool.pytest.ini_options]
minversion = "7.4.0"
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=your_package",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
```

**tox.ini:**
```ini
[tox]
envlist = py310, py311, py312, py313, lint, type
isolated_build = True

[testenv]
description = run unit tests
allowlist_externals = poetry
commands_pre =
    poetry install --no-root --sync
commands =
    poetry run pytest {posargs}

[testenv:lint]
description = run linting tools
allowlist_externals = poetry
commands_pre =
    poetry install --no-root --sync
commands =
    poetry run black --check .
    poetry run isort --check-only .
    poetry run flake8 src tests

[testenv:type]
description = run type checks
allowlist_externals = poetry
commands_pre =
    poetry install --no-root --sync
commands =
    poetry run mypy src
```

---

## 4. CI/CD & Automation

### Prompt: GitHub Actions CI/CD Pipeline

```
Create a comprehensive CI/CD pipeline using GitHub Actions:

**Workflows needed:**
1. **check.yml** - Run tests, linting, and type checking
2. **release.yml** - Automated releases to PyPI
3. **auto-release.yml** - Automatic version bumping and releases
4. **version-bump.yml** - Manual version bumping

**check.yml requirements:**
- Test on multiple Python versions (3.10-3.13)
- Test on multiple OS (ubuntu, windows, macos)
- Run linting (black, isort, flake8)
- Run type checking (mypy)
- Run security scanning (bandit)
- Upload coverage reports to codecov
- Cache dependencies for faster builds

**release.yml requirements:**
- Trigger on tag push or manual dispatch
- Build package with poetry
- Publish to PyPI using trusted publishing
- Create GitHub release with changelog

**Security considerations:**
- Use trusted publishing for PyPI
- Secure token handling
- Dependency scanning
- SAST scanning with bandit

**Branch protection:**
- Require PR reviews
- Require status checks to pass
- Require branches to be up to date

**Additional features:**
- Dependabot for dependency updates
- Issue and PR templates
- Automated changelog generation
```

### Example GitHub Actions Workflow

**.github/workflows/check.yml:**
```yaml
name: Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.10", "3.11", "3.12", "3.13"]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: latest
        virtualenvs-create: true
        virtualenvs-in-project: true
    
    - name: Load cached venv
      id: cached-poetry-dependencies
      uses: actions/cache@v3
      with:
        path: .venv
        key: venv-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}
    
    - name: Install dependencies
      if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
      run: poetry install --no-interaction --no-root
    
    - name: Install project
      run: poetry install --no-interaction
    
    - name: Run tests
      run: poetry run pytest --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run black
      run: poetry run black --check .
    
    - name: Run isort
      run: poetry run isort --check-only .
    
    - name: Run flake8
      run: poetry run flake8 src tests
    
    - name: Run mypy
      run: poetry run mypy src
    
    - name: Run bandit
      run: poetry run bandit -r src/
```

---

## 5. Project Structure & Documentation

### Prompt: Project Documentation Setup

```
Create comprehensive documentation for a Python package:

**Documentation structure:**
```
project/
├── README.md              # Main project documentation
├── CHANGELOG.md           # Version history
├── CONTRIBUTING.md        # Contribution guidelines
├── LICENSE               # License file
├── SECURITY.md           # Security policy
├── CODE_OF_CONDUCT.md    # Community guidelines
├── docs/                 # Detailed documentation
│   ├── installation.md
│   ├── usage.md
│   ├── api.md
│   └── examples/
└── examples/             # Code examples
    ├── basic_usage.py
    └── advanced_usage.py
```

**README.md requirements:**
- Project badges (PyPI, CI, coverage, license)
- Clear description and value proposition
- Installation instructions
- Quick start example
- Table of contents
- Links to documentation
- Citation information (if academic)
- License information

**CONTRIBUTING.md requirements:**
- Development setup instructions
- Code style guidelines
- Testing requirements
- PR process
- Issue reporting guidelines

**Additional documentation:**
- API documentation with docstrings
- Usage examples
- Installation guide
- Troubleshooting guide
- FAQ section

**Docstring style:**
- Use Google or NumPy style docstrings
- Include type hints
- Document all public functions and classes
- Include examples in docstrings
```

### Example README.md Template

```markdown
# Your Package Name

[![PyPI version](https://badge.fury.io/py/your-package.svg)](https://badge.fury.io/py/your-package)
[![Python](https://img.shields.io/pypi/pyversions/your-package.svg)](https://pypi.org/project/your-package/)
[![License](https://img.shields.io/pypi/l/your-package.svg)](https://github.com/username/your-package/blob/main/LICENSE)
[![CI](https://github.com/username/your-package/actions/workflows/check.yml/badge.svg)](https://github.com/username/your-package/actions/workflows/check.yml)
[![Coverage](https://codecov.io/gh/username/your-package/branch/main/graph/badge.svg)](https://codecov.io/gh/username/your-package)

**Brief description of what your package does and why it's useful.**

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

```bash
pip install your-package
```

## Quick Start

```python
import your_package

# Basic usage example
result = your_package.main_function("example")
print(result)
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Documentation

- [Full Documentation](docs/)
- [API Reference](docs/api.md)
- [Examples](examples/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

## License

This project is licensed under the [LICENSE_NAME] License - see the [LICENSE](LICENSE) file for details.
```

---

## 6. Security & Quality Assurance

### Prompt: Security and Quality Setup

```
Implement comprehensive security and quality assurance measures:

**Security tools:**
1. **bandit** - Security linting for Python
2. **safety** - Check for known security vulnerabilities
3. **pip-audit** - Audit Python packages for vulnerabilities
4. **Dependabot** - Automated dependency updates

**Quality assurance:**
1. **Code coverage** - Minimum 90% coverage requirement
2. **Type checking** - Strict mypy configuration
3. **Linting** - flake8 with security plugins
4. **Documentation** - Docstring coverage checking

**Security configuration:**
- bandit configuration for security scanning
- .gitignore for sensitive files
- Security policy (SECURITY.md)
- Vulnerability reporting process

**Quality gates:**
- All tests must pass
- Coverage threshold must be met
- No security issues allowed
- Type checking must pass
- Linting must pass

**Automated security:**
- Dependabot configuration
- Security scanning in CI
- Automated vulnerability alerts
- Regular dependency updates
```

### Example Security Configuration

**bandit configuration in pyproject.toml:**
```toml
[tool.bandit]
exclude_dirs = ["tests", "build", "dist"]
skips = ["B101", "B601"]  # Skip assert_used and shell_injection_subprocess
```

**SECURITY.md:**
```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Please report security vulnerabilities to security@example.com.
Do not report security vulnerabilities through public GitHub issues.
```

---

## 7. Release Management

### Prompt: Automated Release Management

```
Set up automated release management:

**Version management:**
- Semantic versioning (MAJOR.MINOR.PATCH)
- Automated version bumping
- Changelog generation
- Git tagging

**Release process:**
1. Version bump (manual or automated)
2. Update changelog
3. Create git tag
4. Build package
5. Publish to PyPI
6. Create GitHub release

**Tools needed:**
- bumpver or bump2version for version management
- GitHub Actions for automation
- Poetry for building and publishing
- Trusted publishing for PyPI

**Release workflows:**
- Manual release workflow
- Automated release on tag push
- Pre-release support
- Hotfix release process

**Changelog management:**
- Keep a Changelog format
- Automated changelog generation
- Release notes in GitHub

**Configuration files:**
- bumpver configuration
- Release workflow
- Version bump script
```

### Example Release Configuration

**bumpver configuration in pyproject.toml:**
```toml
[tool.bumpver]
current_version = "0.1.0"
version_pattern = "MAJOR.MINOR.PATCH"
commit_message = "bump version {old_version} -> {new_version}"
commit = true
tag = true
push = true

[tool.bumpver.file_patterns]
"pyproject.toml" = ['version = "{version}"']
"src/your_package/__init__.py" = ['__version__ = "{version}"']
```

**Makefile release targets:**
```makefile
bump-version: ## Bump version (usage: make bump-version VERSION=0.2.0)
	@if [ -z "$(VERSION)" ]; then echo "Usage: make bump-version VERSION=0.2.0"; exit 1; fi
	bumpver update --set-version $(VERSION)

release: ## Create a release
	@echo "Creating release..."
	git push origin main --tags
```

---

## Usage Instructions

1. **Choose the relevant prompts** based on your project needs
2. **Customize the templates** with your specific package information
3. **Follow the prompts in order** for a complete setup
4. **Adapt configurations** to your specific requirements
5. **Test the setup** thoroughly before releasing

Each prompt can be used independently or combined for a complete package infrastructure setup.
