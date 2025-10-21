# Contributing to pysx126x

Thank you for your interest in contributing to pysx126x! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Clone the repository:
   ```shell
   git clone https://github.com/nbdy/pysx126x.git
   cd pysx126x
   ```

2. Install development dependencies:

   **Using uv (recommended):**
   ```shell
   # Install uv if you haven't already
   # See https://docs.astral.sh/uv/getting-started/installation/
   
   # Install dependencies
   uv sync --all-extras
   ```

   **Using pip (alternative):**
   ```shell
   pip install -e ".[dev]"
   ```

## Running Tests

Tests require a physical SX126X device connected to your Raspberry Pi. Run tests locally before creating a new tag:

```shell
pytest
```

Note: Tests are not run in the GitHub Actions workflow because they require physical hardware.

## Code Style

Please follow the existing code style in the project.

## Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Submit a pull request

## Releasing New Versions

This project uses GitHub Actions to automatically build and publish new releases to PyPI when a new tag is created.

### Setting up PyPI API Token

For the GitHub Actions workflow to publish to PyPI, you need to set up a PyPI API token as a GitHub secret:

1. Create an API token on PyPI:
   - Go to https://pypi.org/manage/account/
   - Create an API token with the scope "Upload to PyPI"
   - Copy the token value

2. Add the token as a GitHub secret:
   - Go to your GitHub repository
   - Navigate to Settings > Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste the token you copied from PyPI
   - Click "Add secret"

### Release Process

1. Update the version number in both `pyproject.toml` and `sx126x/__init__.py`
2. Run tests locally to ensure everything works (tests require physical hardware)
3. Commit your changes
4. Create and push a new tag with the semantic versioning format `vX.Y.Z` (e.g., `v2.0.2`):
   ```shell
   # Run tests locally first
   pytest

   # Then create and push the tag
   git tag v2.0.2
   git push origin v2.0.2
   ```

The GitHub Actions workflow will automatically build the package and publish it to PyPI. Note that the workflow does not run tests because they require physical hardware.
