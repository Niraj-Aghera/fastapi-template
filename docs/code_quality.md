# Code Quality Tools

All quality tools run automatically via **pre-commit hooks** on every commit.

## Tools Overview

| Tool              | Purpose                  | Config File         |
| ----------------- | ------------------------ | ------------------- |
| **Ruff**          | Linting + Formatting     | `.rc/ruff.toml`     |
| **Pylint**        | Static Analysis          | `.rc/.pylintrc`     |
| **MyPy**          | Type Checking            | `.rc/mypy.ini`      |
| **Vulture**       | Dead Code Detection      | Pre-commit config   |
| **Import Linter** | Architecture Enforcement | `.rc/.importlinter` |

## Quick Commands

```bash
# Run all quality checks
uv run pre-commit run --all-files

# Individual tools
uv run ruff check .                    # Linting
uv run ruff format .                   # Formatting
uv run pylint app libs                 # Static analysis
uv run mypy .                          # Type checking
```

## Key Configurations

**Ruff** (`.rc/ruff.toml`):

- Line length: 140 characters
- Python 3.13 target
- Extensive rulesets: pycodestyle, pyflakes, bandit, etc.
- Auto-fix enabled for most rules

**Pylint** (`.rc/.pylintrc`):

- 10.00/10 score requirement
- Matches ruff exclusions for consistency
- SQLAlchemy-aware configurations

**MyPy** (`.rc/mypy.ini`):

- Strict type checking enabled
- Pydantic plugin integration
- Framework-specific overrides

## Troubleshooting

**Pre-commit fails?**

```bash
uv sync --group local                  # Install dev tools
uv run pre-commit install --overwrite # Reinstall hooks
```

**Tool not found?**

- Ensure hooks use `uv run ...` prefix
- Check `.pre-commit-config.yaml` configuration
