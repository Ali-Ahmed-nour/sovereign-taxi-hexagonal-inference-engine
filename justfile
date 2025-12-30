# List all available commands (The Menu)
default:
    @just --list

# Run all quality checks (Linter, Formatter, Type-checker)
check:
    uv run pre-commit run --all-files

# Setup the environment, install dependencies and pre-commit hooks
setup:
    uv sync
    uv run pre-commit install

# Clean the project, pre-commit cache and temporary files
clean:
    uv run pre-commit clean
    rm -rf ~/.cache/pre-commit
    rm -rf .pytest_cache
    rm -rf .ruff_cache
    rm -rf .mypy_cache