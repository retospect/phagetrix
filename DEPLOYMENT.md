# Deployment Guide

This guide covers the complete deployment setup for Phagetrix.

## 🚀 Quick Release (Recommended)

### 1. One-time Setup
1. Get PyPI API token from [PyPI Account Settings](https://pypi.org/manage/account/)
2. Add it as `PYPI_TOKEN` secret in GitHub repository settings
3. Done! 🎉

### 2. Create Release
1. Go to GitHub → Releases → "Create a new release"
2. Tag: `v0.2.4` (must start with 'v')
3. Title: `Phagetrix v0.2.4` 
4. Add release notes
5. Click "Publish release"

**The GitHub Action automatically:**
- ✅ Updates version numbers
- ✅ Runs tests
- ✅ Builds package
- ✅ Publishes to PyPI
- ✅ Uploads release assets

## 🛠️ Manual Release (Alternative)

### Option 1: Using Make
```bash
# Bump version
make bump-version VERSION=0.2.4

# Review and commit
git add -A
git commit -m "Bump version to 0.2.4"
git tag v0.2.4
git push && git push --tags

# Create GitHub release using the tag
```

### Option 2: Using Poetry
```bash
# Bump version
poetry version 0.2.4

# Build and publish
poetry build
poetry publish

# Tag and push
git add -A
git commit -m "Bump version to 0.2.4"
git tag v0.2.4
git push && git push --tags
```

## 📋 Pre-Release Checklist

- [ ] All tests pass: `make check`
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version follows [semantic versioning](https://semver.org/)
- [ ] Example still works: `make example`

## 🔧 Available Tools

| Tool | Command | Purpose |
|------|---------|---------|
| **GitHub Actions** | Create release on GitHub | Fully automated |
| **Make** | `make bump-version VERSION=X.Y.Z` | Local version bump |
| **Poetry** | `poetry version X.Y.Z` | Poetry's version management |
| **Script** | `python scripts/bump_version.py X.Y.Z` | Custom version script |

## 🚨 Troubleshooting

### GitHub Action Fails
1. Check Actions tab for details
2. Common fixes:
   - Regenerate PyPI token
   - Check version format (must be X.Y.Z)
   - Ensure tests pass locally

### PyPI Upload Fails
- Version already exists → bump to next version
- Token expired → regenerate and update secret
- Package name conflict → check PyPI

### Manual Fallback
If automation fails, use manual poetry commands:
```bash
poetry build
poetry publish --username __token__ --password YOUR_PYPI_TOKEN
```

## 📈 Post-Release

1. ✅ Verify on [PyPI](https://pypi.org/project/phagetrix/)
2. ✅ Test install: `pip install phagetrix==X.Y.Z`
3. ✅ Update documentation if needed
4. ✅ Announce release

## 🔗 Resources

- [PyPI Project Page](https://pypi.org/project/phagetrix/)
- [GitHub Releases](https://github.com/retospect/phagetrix/releases)
- [Semantic Versioning](https://semver.org/)
- [Poetry Documentation](https://python-poetry.org/docs/)
