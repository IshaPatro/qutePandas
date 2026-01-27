# Release Guide for qutePandas

This document outlines the complete process for releasing a new version of qutePandas to PyPI.

## Pre-Release Checklist

Before creating a new release, ensure:

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated with new features/fixes
- [ ] All code changes are committed to git
- [ ] You have PyPI credentials configured

## Version Number Locations

When releasing a new version, you must update the version number in **THREE** locations:

### 1. `pyproject.toml`
```toml
[project]
version = "X.Y.Z"  # Line 7
```

### 2. `setup.py`
```python
setup(
    version="X.Y.Z",  # Line 5
)
```

### 3. `qutePandas/__init__.py`
```python
__version__ = "X.Y.Z"  # Last line (currently line 92)
```

## Version Numbering Convention

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.X.0): New features, backwards-compatible
- **PATCH** (0.0.X): Bug fixes, backwards-compatible

## Release Process

### Step 1: Update Version Numbers

Update the version in all three files listed above to the new version number.

```bash
# Example: Updating to version 1.1.0
# Edit pyproject.toml, setup.py, and qutePandas/__init__.py
```

### Step 2: Clean Previous Builds

Remove any previous build artifacts:

```bash
cd qutePandas
rm -rf build/ dist/ *.egg-info
```

### Step 3: Build the Distribution

Build both source distribution and wheel:

```bash
python -m build
```

This creates:
- `dist/qutePandas-X.Y.Z.tar.gz` (source distribution)
- `dist/qutePandas-X.Y.Z-py3-none-any.whl` (wheel)

### Step 4: Verify the Build

Check that the build was successful:

```bash
ls -lh dist/
```

You should see both `.tar.gz` and `.whl` files with the correct version number.

### Step 5: Upload to PyPI

Upload using twine:

```bash
python -m twine upload dist/*
```

You will be prompted for:
- Username: `__token__`
- Password: Your PyPI API token (starts with `pypi-`)

### Step 6: Verify the Upload

1. Visit https://pypi.org/project/qutePandas/
2. Confirm the new version is listed
3. Check that the README renders correctly

### Step 7: Test Installation

Test installing the new version in a fresh environment:

```bash
pip install --upgrade qutePandas
python -c "import qutePandas; print(qutePandas.__version__)"
```

### Step 8: Tag the Release in Git

Create a git tag for the release:

```bash
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0
```

## Troubleshooting

### Common Issues

#### 1. `403 Forbidden` Error
- **Cause**: Invalid or expired PyPI token
- **Solution**: Generate a new API token at https://pypi.org/manage/account/token/

#### 2. `400 Bad Request - File already exists`
- **Cause**: Version already uploaded to PyPI
- **Solution**: Increment the version number and rebuild

#### 3. `InvalidDistribution` Error
- **Cause**: Issues with metadata in `setup.py` or `pyproject.toml`
- **Solution**: Validate metadata, ensure all required fields are present

#### 4. `zsh: no matches found` Error
- **Cause**: Shell glob expansion with `dist/*`
- **Solution**: Use quotes: `python -m twine upload "dist/*"`

## Quick Reference Commands

```bash
# Full release workflow
cd /Users/isha/Desktop/Projects/qutePandas/qutePandas

# 1. Clean
rm -rf build/ dist/ *.egg-info

# 2. Build
python -m build

# 3. Upload (using .env credentials)
set -a && source /Users/isha/Desktop/Projects/qutePandas/.env && set +a
python -m twine upload dist/*

# 4. Verify
pip install --upgrade qutePandas
python -c "import qutePandas; print(qutePandas.__version__)"
```

## PyPI Credentials

### Option 1: Environment Variables (Recommended)

Store your PyPI API token in the project's `.env` file (located at `/Users/isha/Desktop/Projects/qutePandas/.env`):

```bash
# PyPI Credentials for Twine
TWINE_USERNAME="__token__"
TWINE_PASSWORD="pypi-YOUR_TOKEN_HERE"
```

Then upload using:

```bash
export TWINE_USERNAME="__token__" && export TWINE_PASSWORD="YOUR_TOKEN" && python -m twine upload dist/*
```

Or source the .env file:

```bash
set -a && source /Users/isha/Desktop/Projects/qutePandas/.env && set +a
python -m twine upload dist/*
```

### Option 2: .pypirc File

Alternatively, store your PyPI API token in `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

This allows uploading without entering credentials each time.

### Generating a New PyPI Token

If you get a `403 Forbidden` error, your token may be invalid or expired. Generate a new one:

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Set the token name (e.g., "qutePandas Upload")
4. Set scope to "Project: qutePandas" (recommended) or "Entire account"
5. Click "Add token"
6. **Copy the token immediately** - you won't be able to see it again!
7. Update your `.env` file or `~/.pypirc` with the new token

## Post-Release

After a successful release:

1. Update documentation website if needed
2. Announce the release (GitHub, social media, etc.)
3. Monitor for issues or bug reports
4. Plan next release cycle

## Notes

- PyPI does **not** allow replacing or deleting uploaded files
- Once a version is uploaded, that version number is permanently taken
- Always test in a development environment before releasing
- Keep a CHANGELOG.md to track changes between versions
