# GitHub Workflows

This directory contains GitHub Actions workflow files for automating various tasks in the repository.

## Workflows

### publish.yml

This workflow is triggered when a new tag is pushed with the format `x.y.z`. It builds the package and publishes it to PyPI.

### test.yml

This workflow is triggered on push to the main branch and on pull requests to the main branch. It runs the mock tests to ensure that the mock implementation of the SX126X class is working correctly.

The workflow:
1. Sets up Python 3.11
2. Installs dependencies
3. Runs the mock tests specifically (MockSX126XTest)
4. Runs all tests (which will skip hardware tests automatically)

## Mock Testing

The mock tests use the `MockSX126X` class to simulate the behavior of the SX126X hardware. This allows testing the library's functionality without requiring the actual hardware, which is ideal for CI environments.

The mock implementation includes:
- Simulation of register behavior
- Bit-encoded properties that match the hardware
- Channel range validation (0-83)
- Transmission and reception simulation

By running these tests in the CI pipeline, we can ensure that the mock implementation continues to work correctly as the codebase evolves.