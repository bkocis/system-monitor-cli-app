# Development Guide

This guide covers setting up a development environment and contributing to the System Monitor CLI Dashboard.

## Development Setup

### Prerequisites
- Python 3.12+
- Git
- Linux system (Ubuntu/Debian recommended)

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd system-monitor-cli-app
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   # or using make
   make install-dev
   ```

## Project Structure

```
system-monitor-cli-app/
├── README.md                 # Main documentation
├── CHANGELOG.md             # Version history
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── setup.py                # Package setup (legacy)
├── pyproject.toml          # Modern package configuration
├── Makefile                # Development commands
├── .gitignore              # Git ignore rules
├── .flake8                 # Linting configuration
├── src/                    # Source code
│   └── system_monitor/
│       ├── __init__.py     # Package initialization
│       ├── main.py         # CLI entry point
│       ├── dashboard.py    # Main dashboard logic
│       └── config.py       # Configuration management
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_dashboard.py   # Dashboard tests
│   └── test_config.py      # Configuration tests
├── scripts/                # Shell scripts
│   ├── run_dashboard.sh    # Main launcher
│   └── monitoring_terms.sh # Terminal launcher
├── config/                 # Configuration files
│   └── default.json        # Default configuration
├── docs/                   # Documentation
│   ├── CONFIGURATION.md    # Configuration guide
│   └── DEVELOPMENT.md      # This file
└── venv/                   # Virtual environment (gitignored)
```

## Development Workflow

### Available Make Commands

```bash
make help              # Show available commands
make install          # Install package in development mode
make install-dev      # Install with development dependencies
make test             # Run test suite
make test-coverage    # Run tests with coverage report
make lint             # Run linting tools (ruff)
make format           # Format code (ruff)
make format-check     # Check code formatting
make clean            # Clean build artifacts
make run              # Run the dashboard directly
make run-script       # Run using shell script
make build            # Build distribution packages
make dev-setup        # Set up complete development environment
```

### Code Quality Tools

**Ruff** - All-in-one linter and formatter:
```bash
# Format code
ruff format src tests
# or
make format

# Lint code (includes style, imports, type hints, and more)
ruff check src tests
# or  
make lint

# Fix auto-fixable issues
ruff check --fix src tests

# Check formatting without changes
ruff format --check src tests
```

Ruff replaces Black, isort, flake8, and many mypy checks in a single fast tool.

### Testing

1. **Run all tests:**
   ```bash
   pytest
   # or
   make test
   ```

2. **Run with coverage:**
   ```bash
   pytest --cov=src --cov-report=html
   # or
   make test-coverage
   ```

3. **Run specific test file:**
   ```bash
   pytest tests/test_dashboard.py
   ```

4. **Run specific test:**
   ```bash
   pytest tests/test_dashboard.py::TestSystemDashboard::test_init
   ```

### Adding New Features

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Write tests first (TDD approach):**
   ```bash
   # Add test cases to appropriate test file
   pytest tests/test_dashboard.py -v
   ```

3. **Implement the feature:**
   ```bash
   # Edit source files in src/system_monitor/
   ```

4. **Ensure code quality:**
   ```bash
   make format
   make lint
   make test
   ```

5. **Update documentation:**
   ```bash
   # Update README.md, CONFIGURATION.md, or add new docs
   ```

6. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat: add new monitoring feature"
   git push origin feature/my-new-feature
   ```

## Testing Guidelines

### Unit Tests
- Test all public methods
- Mock external dependencies (subprocess calls, file system)
- Test edge cases and error conditions
- Maintain >90% code coverage

### Test Structure
```python
class TestClassName(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_method_name(self):
        """Test description."""
        # Arrange
        # Act
        # Assert
```

### Mocking External Dependencies
```python
@patch('subprocess.check_output')
def test_gpu_temp(self, mock_subprocess):
    mock_subprocess.return_value = "GPU Core Temperature: 65.0 C"
    temp = self.dashboard.get_gpu_temp()
    self.assertEqual(temp, 65)
```

## Configuration Management

### Adding New Configuration Options

1. **Update default configuration in `config.py`:**
   ```python
   DEFAULT_CONFIG = {
       # ... existing options ...
       "new_option": "default_value"
   }
   ```

2. **Add property accessor:**
   ```python
   @property
   def new_option(self) -> str:
       return self.get("new_option", "default_value")
   ```

3. **Update configuration documentation:**
   ```markdown
   # In docs/CONFIGURATION.md
   ### New Option
   - **new_option**: Description (default: "default_value")
   ```

4. **Add tests:**
   ```python
   def test_new_option(self):
       config = Config(self.config_file)
       self.assertEqual(config.new_option, "default_value")
   ```

## Release Process

1. **Update version numbers:**
   - `src/system_monitor/__init__.py`
   - `setup.py`
   - `pyproject.toml`

2. **Update CHANGELOG.md**

3. **Run full test suite:**
   ```bash
   make lint
   make test-coverage
   ```

4. **Build and test package:**
   ```bash
   make build
   pip install dist/*.whl
   system-monitor  # Test installation
   ```

5. **Tag release:**
   ```bash
   git tag -a v1.0.1 -m "Release version 1.0.1"
   git push origin v1.0.1
   ```

## Contributing Guidelines

1. **Code Style:**
   - Follow PEP 8 (enforced by Ruff)
   - Use type hints where appropriate
   - Write descriptive docstrings
   - Maximum line length: 88 characters

2. **Commit Messages:**
   - Use conventional commit format
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for tests
   - `refactor:` for refactoring

3. **Pull Requests:**
   - Include tests for new features
   - Update documentation
   - Ensure CI passes
   - Get code review approval

## Debugging

### Common Issues

1. **Import errors after restructuring:**
   ```bash
   pip install -e .  # Reinstall in development mode
   ```

2. **Test import failures:**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

3. **Configuration not loading:**
   ```bash
   # Check file permissions and JSON validity
   python -c "import json; json.load(open('config/default.json'))"
   ```

### Debugging Dashboard Issues

1. **Enable verbose output:**
   ```python
   # Add to dashboard.py for debugging
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Test individual components:**
   ```python
   from src.system_monitor.dashboard import SystemDashboard
   dashboard = SystemDashboard()
   print(dashboard.get_cpu_temp())
   print(dashboard.get_gpu_temp())
   ```

3. **Mock hardware for testing:**
   ```python
   # Use unittest.mock to simulate hardware responses
   ```
