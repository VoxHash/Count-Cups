# Contributing to Count-Cups

Thanks for helping improve Count-Cups!

## Code of Conduct

Please read and follow our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Development Setup

```bash
# Clone
git clone https://github.com/VoxHash/Count-Cups.git
cd Count-Cups

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install deps
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v
```

## Branching & Commit Style

- **Branches**: `feature/…`, `fix/…`, `docs/…`, `chore/…`
- **Conventional Commits**: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

Examples:
- `feat(detection): add MediaPipe hand tracking support`
- `fix(ui): resolve theme switching issue`
- `docs(api): update detection engine documentation`

## Pull Requests

- Link related issues, add tests, update docs
- Follow the PR template in `.github/PULL_REQUEST_TEMPLATE.md`
- Keep diffs focused and well-documented
- Ensure all tests pass: `pytest tests/ -v`
- Run code quality checks: `ruff check . && mypy app/`

## Code Quality

### Formatting & Linting

```bash
# Format code
ruff format app/ tests/

# Lint code
ruff check app/ tests/

# Type check
mypy app/
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_sip_logic.py -v
```

## Release Process

- Semantic Versioning (MAJOR.MINOR.PATCH)
- Update [CHANGELOG.md](CHANGELOG.md) before release
- Tag releases with version number

## Getting Help

- Check [docs/](docs/) for detailed documentation
- Open an issue for questions or problems
- See [SUPPORT.md](SUPPORT.md) for support options
