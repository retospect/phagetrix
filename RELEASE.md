# Release Process

This document explains how to create releases for Phagetrix using GitHub's automated release system.

## Setup (One-time)

### 1. Get PyPI API Token

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Name: `phagetrix-github-actions`
5. Scope: Select "Entire account" or specific to phagetrix project
6. Copy the token (starts with `pypi-`)

### 2. Add GitHub Secret

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_TOKEN`
5. Value: Paste the PyPI token from step 1
6. Click "Add secret"

## Creating a Release

### Method 1: GitHub Web Interface (Recommended)

1. Go to your GitHub repository
2. Click "Releases" (right sidebar)
3. Click "Create a new release"
4. **Tag version**: Enter version like `v0.2.4` (must start with 'v')
5. **Release title**: `Phagetrix v0.2.4`
6. **Description**: Add release notes (see template below)
7. Click "Publish release"

The GitHub Action will automatically:
- ✅ Update version numbers in all files
- ✅ Run tests to ensure quality
- ✅ Build the package
- ✅ Publish to PyPI
- ✅ Upload build artifacts to the release

### Method 2: Command Line

```bash
# Create and push a tag
git tag v0.2.4
git push origin v0.2.4

# Then create the release on GitHub web interface using the tag
```

## Release Notes Template

```markdown
## What's Changed

### Added
- New feature descriptions

### Changed  
- Improvements and modifications

### Fixed
- Bug fixes

### Security
- Security improvements

**Full Changelog**: https://github.com/retospect/phagetrix/compare/v0.2.3...v0.2.4
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backward compatible
- **Patch** (0.0.1): Bug fixes, backward compatible

## Troubleshooting

### Release Failed
1. Check the Actions tab for error details
2. Common issues:
   - PyPI token expired or incorrect
   - Version already exists on PyPI
   - Tests failed

### PyPI Token Issues
1. Regenerate token on PyPI
2. Update the `PYPI_TOKEN` secret in GitHub
3. Retry the release

### Manual Release (Fallback)
If automated release fails:

```bash
# Update version manually
poetry version 0.2.4

# Build and publish
poetry build
poetry publish
```

## Post-Release

1. ✅ Verify package appears on [PyPI](https://pypi.org/project/phagetrix/)
2. ✅ Test installation: `pip install phagetrix==0.2.4`
3. ✅ Update CHANGELOG.md if needed
4. ✅ Announce on relevant channels
