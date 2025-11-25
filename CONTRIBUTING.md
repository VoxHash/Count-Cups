# Contributing to Count-Cups

Thank you for your interest in contributing to Count-Cups! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Issue Guidelines](#issue-guidelines)
- [Pull Request Guidelines](#pull-request-guidelines)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- A code editor (VS Code, PyCharm, etc.)
- Basic knowledge of Python and PyQt6

### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Count-Cups.git
   cd Count-Cups
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

6. **Run the application**:
   ```bash
   python -m app.main
   ```

## Development Workflow

### Branch Naming

Use descriptive branch names:
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(detection): add MediaPipe hand tracking support
fix(ui): resolve theme switching issue
docs(api): update detection engine documentation
```

## Code Style

### Python Code

We use several tools to maintain code quality:

- **Black**: Code formatting (88 character line length)
- **Ruff**: Fast linting and import sorting
- **MyPy**: Static type checking
- **Pre-commit**: Automated checks before commits

### Running Code Quality Checks

```bash
# Format code
black app/ tests/

# Lint code
ruff check app/ tests/
ruff format app/ tests/

# Type check
mypy app/

# Run all checks
pre-commit run --all-files
```

### Code Guidelines

1. **Type Hints**: Use type hints for all function parameters and return values
2. **Docstrings**: Use Google-style docstrings for all public functions and classes
3. **Error Handling**: Use specific exception types and provide meaningful error messages
4. **Logging**: Use the logging module instead of print statements
5. **Constants**: Use UPPER_CASE for module-level constants
6. **Imports**: Group imports (standard library, third-party, local) with blank lines

### Example Code

```python
from typing import Optional, List
from app.core.logging import get_logger

logger = get_logger(__name__)

class ExampleClass:
    """Example class demonstrating code style."""
    
    def __init__(self, value: int) -> None:
        """Initialize with a value.
        
        Args:
            value: The initial value
        """
        self.value = value
        logger.debug(f"Initialized with value: {value}")
    
    def process_data(self, data: List[str]) -> Optional[str]:
        """Process a list of data.
        
        Args:
            data: List of strings to process
            
        Returns:
            Processed string or None if processing fails
            
        Raises:
            ValueError: If data is empty
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        try:
            result = " ".join(data)
            logger.info(f"Processed {len(data)} items")
            return result
        except Exception as e:
            logger.error(f"Failed to process data: {e}")
            return None
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_sip_logic.py -v

# Run tests matching pattern
pytest tests/ -k "test_detection" -v
```

### Writing Tests

1. **Test Structure**: Use descriptive test names and organize tests in classes
2. **Fixtures**: Use pytest fixtures for common setup
3. **Mocking**: Mock external dependencies and I/O operations
4. **Coverage**: Aim for high test coverage (90%+)
5. **Edge Cases**: Test edge cases and error conditions

### Example Test

```python
import pytest
from unittest.mock import Mock, patch
from app.core.sip_logic import SipAggregator

class TestSipAggregator:
    """Test sip aggregator functionality."""
    
    def test_process_detection_success(self):
        """Test successful sip detection processing."""
        aggregator = SipAggregator()
        
        detection = Mock()
        detection.has_sip = True
        detection.confidence = 0.8
        
        with patch('time.time', return_value=1.0):
            result = aggregator.process_detection(detection)
            
        assert result is not None
        assert result.has_sip is True
```

## Documentation

### Code Documentation

- **Docstrings**: Document all public functions, classes, and methods
- **Comments**: Add comments for complex logic
- **Type Hints**: Use type hints for better documentation
- **README Updates**: Update README for new features

### User Documentation

- **User Guide**: Update `docs/README.md` for new features
- **API Documentation**: Update `docs/API.md` for API changes
- **Architecture**: Update `docs/ARCHITECTURE.md` for structural changes

## Submitting Changes

### Before Submitting

1. **Run all tests**: `pytest tests/ -v`
2. **Run code quality checks**: `pre-commit run --all-files`
3. **Update documentation**: Update relevant docs
4. **Test your changes**: Test the application thoroughly

### Pull Request Process

1. **Create a pull request** from your feature branch
2. **Fill out the PR template** completely
3. **Link related issues** using keywords (fixes #123, closes #456)
4. **Request review** from maintainers
5. **Address feedback** promptly and thoroughly

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Fixes #(issue number)
```

## Issue Guidelines

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check documentation** for solutions
3. **Test with latest version** to ensure issue still exists

### Issue Templates

Use the appropriate issue template:
- **Bug Report**: For reporting bugs
- **Feature Request**: For requesting new features
- **Documentation**: For documentation issues
- **Question**: For general questions

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python Version: [e.g., 3.10.0]
- Count-Cups Version: [e.g., 1.0.0]

## Additional Context
Any other relevant information
```

## Pull Request Guidelines

### Review Process

1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one maintainer approval required
3. **Testing**: Manual testing may be requested
4. **Documentation**: Documentation must be updated

### Merge Requirements

- [ ] All tests pass
- [ ] Code review approved
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] CI/CD pipeline passes

## Development Tips

### Debugging

1. **Use logging**: Add debug logs for troubleshooting
2. **Test in isolation**: Test components separately
3. **Use debugger**: Set breakpoints for complex issues
4. **Check logs**: Review application logs for errors

### Performance

1. **Profile code**: Use profiling tools for performance issues
2. **Optimize bottlenecks**: Focus on the slowest parts
3. **Memory usage**: Monitor memory consumption
4. **Database queries**: Optimize database operations

### UI Development

1. **Test on different platforms**: Test on Windows, macOS, Linux
2. **Responsive design**: Ensure UI works at different sizes
3. **Accessibility**: Test with screen readers and keyboard navigation
4. **Theme compatibility**: Test with all themes

## Getting Help

- **GitHub Discussions**: Ask questions in discussions
- **Discord**: Join our Discord server (if available)
- **Email**: Contact maintainers directly
- **Documentation**: Check the docs first

## Recognition

Contributors will be recognized in:
- **README**: Listed as contributors
- **Release Notes**: Mentioned in release notes
- **GitHub**: Shown in contributors graph

Thank you for contributing to Count-Cups! 🎉
