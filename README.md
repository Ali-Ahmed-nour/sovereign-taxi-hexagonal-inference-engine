# 🚕 NYC Taxi Duration Prediction: End-to-End MLOps Pipeline

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![MLOps](https://img.shields.io/badge/MLOps-Engineering-orange.svg)](https://en.wikipedia.org/wiki/MLOps)
[![Environment Management](https://img.shields.io/badge/Managed%20by-uv-purple.svg)](https://github.com/astral-sh/uv)
[![Architecture](https://img.shields.io/badge/Design-Hexagonal-green.svg)](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))

A production-ready MLOps project designed to predict taxi trip durations in NYC. This project transitions from research notebooks to a robust, cloud-agnostic pipeline, emphasizing **Software Architecture** and engineering excellence.

## 🎯 Business Problem
Predicting trip duration is critical for urban mobility services. Accurate estimates improve user experience, optimize driver dispatching, and enhance fare estimation. This project builds a high-performance model to tackle this challenge using NYC Taxi & Limousine Commission (TLC) data.

## 🏗️ Architecture & Engineering Principles
The project is built with a **"Production-First"** mindset, adhering to modern software design patterns:

* **Hexagonal Architecture (Ports & Adapters):** Decouples core ML logic from external infrastructure. This allows switching between local storage and Google Cloud Storage (GCS) or changing tracking tools without touching the core training logic.
* **Single Source of Truth (SSoT):** A centralized configuration layer manages all paths, features, and model parameters.
* **Memory Optimization:** Vectorized downcasting and efficient data handling to process millions of records with a minimal memory footprint.
* **Type Safety & Quality:** Fully typed using Python's `TypedDict` and verified with **Pyright** and **Ruff**.

## 📂 Project Structure
```text
.
├── src/
│   ├── config.py          # Centralized SSoT Configuration
│   ├── core/              # The Hexagon: Pure ML Logic (Preprocessing, Training)
│   ├── ports/             # Abstract Interfaces (StoragePort, TrackerPort)
│   └── adapters/          # Implementation details (GCS, Local, MLflow)
├── notebooks/             # Exploratory Data Analysis & Research
├── data/                  # Local data storage (Git ignored)
├── models/                # Local model artifacts (Git ignored)
├── justfile               # Workflow automation commands
└── pyproject.toml         # Dependency management (uv)
```


## 🛠️ Tech Stack

* **Environment:** `uv` (Extremely fast Python package manager).
* **Automation:** `Just` (Command runner for development workflows).
* **Core ML:** `Scikit-learn`, `XGBoost`, `Pandas`.
* **Optimization:** `Hyperopt` (Bayesian Optimization via TPE).
* **Experiment Tracking:** `MLflow` (Integrated with autologging and artifact management).
* **Static Analysis:** `Ruff` (Linting), `Pyright` (Static Typing).

## 🚀 Getting Started

### 1. Prerequisites
Ensure `uv` is installed:
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

## 2. Setup & Development
I use `just` to automate repetitive tasks.

| Task | Command | Description |
| :--- | :--- | :--- |
| **Setup** | `just setup` | Installs dependencies and pre-commit hooks. |
| **Quality Check** | `just check` | Runs Ruff and Pyright on all files. |
| **Clean** | `just clean` | Cleans cache and temporary files. |


## 🛠️ Development Workflow
To maintain high engineering standards, the project follows a structured lifecycle:

* **Research:** Prototyping in `notebooks/` for EDA and initial model experiments.
* **Refactor:** Porting stable logic into `src/core/` while defining necessary Ports.
* **Implement Adapters:** Creating specific implementations for local or cloud environments.
* **Optimize:** Running Hyperopt trials to find best-in-class hyperparameters.
* **Quality Gate:** Running `just check` to ensure zero linting errors and type safety before committing.

---
> **Note:** > **🚧 Project Status & Current Focus:** > This project is undergoing a major architectural refactor to implement **Hexagonal Architecture**.

### 🧩 Domain Model Visualized
This diagram represents our core business logic (The Hexagon Center), ensuring that our ML entities are decoupled from infrastructure.

```mermaid
classDiagram
    direction LR
    class TaxiTrip {
        +String trip_id
        +datetime pickup_time
        +datetime dropoff_time
        +Location pickup_loc
        +Location dropoff_loc
        +duration() float
        +is_valid_for_model() bool
    }
    class Location {
        +String location_id
    }
    class PassengerCount {
        +int count
    }
    class Fare {
        +float amount
    }

    TaxiTrip "1" *-- "2" Location : involves
    TaxiTrip "1" --> "1" PassengerCount : carries
    TaxiTrip "1" --> "1" Fare : generates