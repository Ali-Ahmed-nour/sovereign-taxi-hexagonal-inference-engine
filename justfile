# STIE Justfile - Sovereign Command Orchestrator (2026 Standards)

# List all available commands (The Menu)
default:
    @just --list

# 🛠️ Setup the environment, install dependencies and pre-commit hooks
setup:
    uv sync
    uv run pre-commit install

# 🧪 Run all quality checks via Pre-commit (Linter, Formatter, Type-checker, Pytest-Cov)
check:
    uv run pre-commit run --all-files

# ✨ Format all Markdown files in the project to maintain industrial standards
md:
    @echo "Formatting all .md files in the project..."
    find . -name "*.md" -not -path "./.venv/*" | xargs uv run mdformat
    @echo "All Markdown files are now sovereign and formatted."

# 📚 Bundle all documentation into a single sovereign context file
all docs:
    @echo "Bundling documentation into all_docs.txt..."
    @find docs -name "*.md" -exec sh -c 'echo "========================================"; echo "FILE: {}"; echo "========================================"; cat {}; echo -e "\n\n"' \; > all_docs.txt
    @echo "Done! Context saved to all_docs.txt"

# 🧠 Start the MLflow tracking server (Sovereign Local Registry)
mlflow:
    uv run mlflow server \
        --backend-store-uri sqlite:///mlflow.db \
        --default-artifact-root ./mlflow-artifacts \
        --host 127.0.0.1 \
        --port 5000

# 🧹 Clean the project from cache, temporary files, and coverage artifacts
clean:
    uv run pre-commit clean
    rm -rf ~/.cache/pre-commit
    rm -rf .pytest_cache .coverage htmlcov .ruff_cache .mypy_cache .pyright_cache
    rm -f all_docs.txt
    find . -type d -name "__pycache__" -exec rm -rf {} +