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


#  comment: Start the MLflow tracking server with SQLite and local artifacts
mlflow server:
    mlflow server \
        --backend-store-uri sqlite:///mlflow.db \
        --default-artifact-root ./mlflow_artifacts \
        --host 127.0.0.1 \
        --port 5000


# Lint the README file for formatting issues
md:
    mdformat README.md