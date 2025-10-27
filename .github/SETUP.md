# Quick Setup Guide for GitHub Actions

## 🚀 One-Time Setup Required

### 1. Configure PyPI Token
1. Go to [PyPI Account Settings](https://pypi.org/manage/account/token/)
2. Create a new API token (scope: "Entire account" or project-specific)
3. In GitHub: Settings → Secrets and variables → Actions
4. Add secret: `PYPI_TOKEN` = your PyPI token

### 2. Test the Setup
```bash
# Option 1: Automatic release (recommended)
# Just update version in pyproject.toml and push to main
sed -i 's/version = "0.2.3"/version = "0.2.4"/' pyproject.toml
git add pyproject.toml
git commit -m "bump version to 0.2.4"
git push origin main
# → Auto-release workflow triggers

# Option 2: Manual version bump
# Go to Actions → "Version Bump and Release" → Run workflow
# Choose patch/minor/major and click "Run workflow"
```

## 🔄 Available Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **CI Tests** | Push/PR | Test on multiple OS/Python versions |
| **Auto Release** | Version change on main | Automatic PyPI release |
| **Version Bump** | Manual | Interactive version bumping |
| **Manual Release** | Manual/GitHub release | Release current code |

## ✅ Quality Gates
- All tests must pass
- 83%+ test coverage
- Type checking (mypy)
- Security scanning
- Code formatting

## 🎯 Recommended Workflow
1. Make changes in feature branch
2. Create PR (triggers CI tests)
3. Merge to main
4. Update version in `pyproject.toml`
5. Push to main → automatic release! 🚀

That's it! Your package will be automatically tested, built, and published to PyPI.
