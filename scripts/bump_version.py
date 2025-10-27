#!/usr/bin/env python3
"""
Simple version bumping script for Phagetrix.
Usage: python scripts/bump_version.py 0.2.4
"""

import re
import sys
from pathlib import Path


def update_version(new_version: str) -> None:
    """Update version in all relevant files."""

    # Validate version format
    if not re.match(r"^\d+\.\d+\.\d+$", new_version):
        print(f"Error: Invalid version format '{new_version}'. Use format: X.Y.Z")
        sys.exit(1)

    files_to_update = [
        ("pyproject.toml", r'version = ".*"', f'version = "{new_version}"'),
        (
            "src/phagetrix/__init__.py",
            r'__version__ = ".*"',
            f'__version__ = "{new_version}"',
        ),
        (
            "src/phagetrix/cli.py",
            r'parser\.version = ".*"',
            f'parser.version = "{new_version}"',
        ),
    ]

    for file_path, pattern, replacement in files_to_update:
        path = Path(file_path)
        if not path.exists():
            print(f"Warning: {file_path} not found")
            continue

        content = path.read_text()
        new_content = re.sub(pattern, replacement, content)

        if content != new_content:
            path.write_text(new_content)
            print(f"✅ Updated {file_path}")
        else:
            print(f"⚠️  No changes needed in {file_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/bump_version.py <version>")
        print("Example: python scripts/bump_version.py 0.2.4")
        sys.exit(1)

    new_version = sys.argv[1]
    print(f"Bumping version to {new_version}...")

    update_version(new_version)

    print(f"\n✅ Version bumped to {new_version}")
    print("\nNext steps:")
    print("1. Review changes: git diff")
    print(
        "2. Commit changes: git add -A && git commit -m 'Bump version to {}'".format(
            new_version
        )
    )
    print("3. Create tag: git tag v{}".format(new_version))
    print("4. Push: git push && git push --tags")
    print("5. Create GitHub release using the tag")


if __name__ == "__main__":
    main()
