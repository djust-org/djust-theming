# djust-theming Tests

## Running Tests

### Prerequisites

```bash
pip install -e ".[dev]"
```

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_presets.py
```

### Run with Coverage

```bash
pytest --cov=djust_theming
```

## Test Structure

- `test_presets.py` - Tests for theme presets
- More tests to be added...

## Writing Tests

When adding tests:
1. Create test file: `test_<module>.py`
2. Import modules to test
3. Write test functions starting with `test_`
4. Use pytest fixtures for setup/teardown
5. Run tests to verify

## Future Test Areas

- [ ] Theme manager tests
- [ ] CSS generator tests
- [ ] Component rendering tests
- [ ] Template tag tests
- [ ] CLI command tests
- [ ] Integration tests
- [ ] Performance tests
