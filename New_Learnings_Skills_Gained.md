# New Learnings & Skills Gained

> This document captures the technical concepts and professional tools **explored and mastered** during the development of the **Taxi Duration NY Project**.

---

## 🛠 Software Engineering & Infrastructure

### 📦 Project & Environment Management
* **Modern Python Tooling**
    * **uv Project Workflow**: Transitioned to a full project-based workflow using `uv`. By utilizing `pyproject.toml` and lockfiles, I ensured high-performance dependency management and strictly reproducible development environments.
    * **Dev-Dependencies Management**: Implemented a clear separation between production and development dependencies, ensuring a lightweight production build by isolating tools like linters and formatters.
    * **Pathlib Integration**: Adopted `pathlib` for object-oriented filesystem paths, providing a cleaner and more robust alternative to the legacy `os.path`.

### 🛡 Code Quality & Automation
* **CI/CD & Automation**
    * **Justfile (Just Task Runner)**: Implemented a `justfile` to orchestrate project tasks. This provides a unified interface for common commands (e.g., environment setup, running linters, cleaning data), improving developer productivity and ensuring command consistency.
    * **Pre-commit Hooks**: Implemented a `pre-commit` framework to automate code quality checks. This ensures that every commit is automatically linted, formatted, and checked for type safety before entering the version control system.

* **Static Analysis & Linting Ecosystem**
    * **Ruff**: Integrated Ruff as an all-in-one, high-performance linter and formatter to enforce code style and catch potential bugs instantly.
    * **Isort**: Utilized for automated import sorting, ensuring all module inclusions are organized and PEP 8 compliant.
    * **Pylance**: Integrated as the core language server for advanced static analysis and intelligent auto-complete.
    * **Pyright Configuration**: Implemented a `pyrightconfig.json` file to standardize type-checking rules across the project.
    * **pandas-stubs**: Utilized to bring static typing to the Pandas library for stricter validation of DataFrame operations.

* **Advanced Structural Typing**
    * **TypedDict**: Leveraged from the `typing` module to define explicit schemas for dictionaries, ensuring data consistency and a self-documenting codebase.

---
*This file is updated as the project evolves.*