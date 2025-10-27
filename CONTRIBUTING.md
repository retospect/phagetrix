# Contributing to Phagetrix

Thank you for your interest in contributing to Phagetrix! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites
- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### Getting Started

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/phagetrix.git
   cd phagetrix
   ```

2. **Install dependencies**
   ```bash
   poetry install --with dev
   ```

3. **Install pre-commit hooks**
   ```bash
   poetry run pre-commit install
   ```

## Development Workflow

### Available Commands

Use the Makefile for common development tasks:

```bash
make help          # Show all available commands
make install       # Install dependencies
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run linting tools
make format        # Format code
make check         # Run all checks (lint + test)
make clean         # Clean build artifacts
make example       # Run example
```

### Code Quality

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **pytest** for testing
- **mypy** for type checking (optional)

Run `make check` before submitting a pull request.

### Testing

- Write tests for new functionality
- Ensure all tests pass: `make test`
- Aim for good test coverage: `make test-cov`
- Tests are located in the `tests/` directory

### Code Style

- Follow PEP 8 (enforced by flake8)
- Use Black for formatting (line length: 88)
- Sort imports with isort
- Write clear, descriptive commit messages

## Submitting Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the style guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Run quality checks**
   ```bash
   make check
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add descriptive commit message"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Guidelines

- **Clear description**: Explain what your PR does and why
- **Reference issues**: Link to relevant GitHub issues
- **Small, focused changes**: Keep PRs manageable
- **Tests included**: Add tests for new features
- **Documentation updated**: Update docs if needed
- **CI passes**: Ensure all checks pass

## Reporting Issues

When reporting bugs or requesting features:

1. **Search existing issues** first
2. **Use issue templates** if available
3. **Provide clear reproduction steps** for bugs
4. **Include relevant system information**

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for all contributors

## Questions?

Feel free to open an issue for questions about contributing or reach out to the maintainers.

Thank you for contributing to Phagetrix! 🧬
