# GitHub Actions Workflow Unit Tests

This directory contains unit tests for the GitHub Actions workflows in this repository.

## Test Files

### `test-docker-build.sh`
Comprehensive unit test suite for `.github/workflows/docker-build.yml`

**What it tests:**
- ✅ YAML syntax validation
- ✅ Workflow structure and required keys
- ✅ Environment variables configuration
- ✅ Trigger conditions (tags, workflow_dispatch)
- ✅ BuildKit optimizations and multi-stage builds
- ✅ Multi-platform support (AMD64, ARM64)
- ✅ Security best practices and permissions
- ✅ Caching strategy implementation
- ✅ Docker image validation steps
- ✅ Action versions for security
- ✅ Workflow simulation (if `act` is available)
- ✅ Docker build context validation
- ✅ Workflow inputs and conditional logic

## Running Tests

### Prerequisites

Install optional dependencies for enhanced testing:

```bash
# Install yq for YAML validation (recommended)
sudo snap install yq

# Install act for workflow simulation (optional)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Or using homebrew on macOS
brew install act
```

### Execute Tests

```bash
# Make the test script executable
chmod +x tests/test-docker-build.sh

# Run the test suite
./tests/test-docker-build.sh
```

### Test Output

The test suite provides colored output:
- 🔵 **INFO**: General information
- 🟢 **PASS**: Test passed
- 🔴 **FAIL**: Test failed  
- 🟡 **WARN**: Warning (non-critical issue)

Example output:
```
[INFO] Starting Docker Build Workflow Unit Tests
[INFO] Running test: YAML Syntax Validation
[PASS] YAML Syntax Validation

[INFO] Running test: Workflow Structure
[PASS] Workflow Structure

...

[INFO] Test Summary:
  Total Tests: 14
  Passed: 14
  Failed: 0
[PASS] All tests passed! ✨
```

## CI Integration

You can integrate these tests into your CI pipeline by adding a test job to your GitHub Actions workflow:

```yaml
test-workflow:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Install dependencies
      run: |
        sudo snap install yq
    - name: Run workflow tests
      run: |
        chmod +x tests/test-docker-build.sh
        ./tests/test-docker-build.sh
```

## Test Development

### Adding New Tests

To add a new test function:

1. Create a new function following the naming pattern `test_<name>()`
2. Return 0 for success, 1 for failure
3. Use the helper functions for consistent output
4. Add the test to the main execution section

Example:
```bash
test_new_feature() {
    if grep -q "new-feature" "$WORKFLOW_FILE"; then
        return 0
    else
        log_error "Missing new feature configuration"
        return 1
    fi
}

# Add to main():
run_test "New Feature" test_new_feature
```

### Helper Functions

- `log_info()` - Blue informational messages
- `log_success()` - Green success messages  
- `log_error()` - Red error messages
- `log_warning()` - Yellow warning messages
- `run_test()` - Executes a test function with proper counting

## Coverage

The test suite covers:
- **Syntax**: YAML parsing and structure
- **Configuration**: Required keys and values
- **Security**: Permissions and conditional logic
- **Performance**: BuildKit and caching optimizations
- **Functionality**: Multi-platform builds and testing
- **Best Practices**: Action versions and security patterns

## Limitations

- Cannot test actual Docker builds (requires Docker daemon)
- Registry push operations are not tested
- Secrets and environment variable values are not validated
- Some tests require external tools (`yq`, `act`) for full coverage
