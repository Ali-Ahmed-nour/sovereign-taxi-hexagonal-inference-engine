# 🚕 NYC Taxi Duration Prediction: End-to-End MLOps Pipeline

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![MLOps](https://img.shields.io/badge/MLOps-Engineering-orange.svg)](https://en.wikipedia.org/wiki/MLOps)
[![Environment Management](https://img.shields.io/badge/Managed%20by-uv-purple.svg)](https://github.com/astral-sh/uv)

A production-ready MLOps project designed to predict taxi trip durations in NYC. This project transitions from a research notebook to a robust, maintainable pipeline, emphasizing engineering excellence and reproducible workflows.

## 🎯 Business Problem
Predicting trip duration is critical for urban mobility services. Accurate estimates improve user experience, optimize driver dispatching, and enhance fare estimation. This project builds a baseline model to tackle this challenge using NYC Taxi & Limousine Commission (TLC) data.

## 🏗️ Architecture & Engineering Principles
The project is built with a **"Production-First"** mindset:
* **Single Source of Truth (SSoT):** A centralized configuration layer manages all paths, features, and model parameters, ensuring consistency across Training, Validation, and Inference.
* **Memory Optimization:** Implementation of vectorized downcasting to handle millions of rows with a minimum memory footprint (e.g., using `float32`).
* **Type Safety:** Fully typed using Python's `TypedDict` and verified with **Pyright** (Pylance core) to catch bugs before runtime.
* **Local-First CI:** Quality checks run locally via system hooks to save cloud resources and avoid network dependencies.

## 🛠️ Tech Stack
* **Environment:** [uv](https://github.com/astral-sh/uv) (Extremely fast Python package installer and resolver).
* **Automation:** [Just](https://github.com/casey/just) (Command runner for simplified workflows).
* **Quality Control:** Ruff (Linting & Formatting), Pyright (Static Type Checking).
* **Data Science:** Pandas, NumPy, Scikit-learn, XGBoost.
* **Experiment Tracking:** MLflow (In progress).
* **Orchestration:** Prefect (In progress).

## 🚀 Getting Started

### 1. Prerequisites
Ensure `uv` is installed:
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh


### 2. Setup & Development
I use `just` to automate repetitive tasks. If you don't have it, install it via `sudo apt install just`.

| Task | Command | Description |
| :--- | :--- | :--- |
| **Setup** | `just setup` | Installs dependencies and pre-commit hooks. |
| **Quality Check** | `just check` | Runs Ruff and Pyright on all files. |
| **Clean** | `just clean` | Cleans pre-commit cache and temp files. |

## 🛠️ Development Workflow
To ensure high code quality, I follow these steps:
1. **Develop:** Write code in notebooks or scripts.
2. **Format & Lint:** Run `just check` to catch unused imports or formatting issues.
3. **Validate:** Only commit code that passes all local "Quality Gates".

---
*Note: This project is under active development. Upcoming features include MLflow tracking and Prefect orchestration.*