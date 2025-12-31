# New Learnings & Skills Gained

> This document captures the technical concepts and professional tools **explored and mastered** during the development of the **Taxi Duration NY Project**.

---

## 🧪 Machine Learning & Optimization

### 🚀 Model Tuning & Performance
* **Bayesian Hyperparameter Optimization**
    * **Hyperopt**: Integrated `Hyperopt` for automated hyperparameter tuning. Leveraged the **Tree of Parzen Estimators (TPE)** algorithm to efficiently navigate the search space, significantly reducing optimization time compared to traditional Grid or Random Search methods.
    * **Search Space Definition**: Mastered defining complex search spaces using `hp.quniform`, `hp.loguniform`, and `hp.choice` to optimize model convergence.

---

## 🛠 Software Engineering & Infrastructure

### 📦 Project & Environment Management
* **Modern Python Tooling**
    * **uv Project Workflow**: Transitioned to a full project-based workflow using `uv`. By utilizing `pyproject.toml` and lockfiles, I ensured high-performance dependency management and strictly reproducible development environments.
    * **Dev-Dependencies Management**: Implemented a clear separation between production and development dependencies, ensuring a lightweight production build.
    * **Pathlib Integration**: Adopted `pathlib` for object-oriented filesystem paths, providing a cleaner alternative to the legacy `os.path`.

### 🛡 Code Quality, Security & Automation
* **Workflow Automation**
    * **Justfile (Just Task Runner)**: Implemented a `justfile` to orchestrate project tasks, providing a unified interface for commands like environment setup and linting.
    * **Pre-commit Hooks**: Implemented a `pre-commit` framework to automate code quality checks before version control entry.

* **Security & Dependency Analysis**
    * **Mend (Mend Advisor)**: Integrated Mend to scan third-party dependencies for security vulnerabilities (SCA). Used Mend Advisor to evaluate the health of open-source libraries before integration.
    * **SonarQube for IDE**: Integrated SonarQube for real-time deep code analysis, identifying "Code Smells" and logic patterns.

* **Static Analysis & Linting Ecosystem**
    * **Ruff & Isort**: Leveraged Ruff for high-performance linting/formatting and Isort for automated import organization.
    * **Pylance & Pyright**: Leveraged for advanced static analysis and strict type-checking via `pyrightconfig.json`.
    * **pandas-stubs**: Utilized to bring static typing to the Pandas library.

* **Advanced Structural Typing**
    * **TypedDict**: Leveraged from the `typing` module to define explicit schemas for dictionaries, ensuring data consistency.

---
*This file is updated as the project evolves.*