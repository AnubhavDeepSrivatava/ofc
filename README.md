# FastAPI Microservice Template

This repository acts as the **"Scaffolding"** for new microservices in our ecosystem. It is designed to work in tandem with the **"Plumbing"** provided by our shared library, `my-company-core`.

## 1. High-Level Architecture

We split our code into two distinct categories to maximize reusability and maintainability:

1.  **`my-company-core` (Library):** The "Plumbing". Contains logic we don't want to rewrite:
    *   Authentication & Authorization (SpiceDB wrappers).
    *   Logging (Loguru setup with JSON & correlation IDs).
    *   Middleware (Error handling, Request context).
    *   Infrastructure Connectors (Redis Bus, Postgres Engine, NATS).
2.  **`microservice-template` (This Repo):** The "Scaffolding". The starting point for any new service:
    *   Standard folder structure.
    *   Business logic specific to the domain.
    *   Database migrations (Alembic) and Models for this specific service.

---

## 2. Directory Structure

This project follows a **Layered Architecture** pattern.

```text
microservice-name/
├── app/
│   ├── api/                 # API Layer: Routes and Controllers
│   │   ├── v1/              # Versioned API
│   │   │   └── endpoints/   # Route handlers (keep these thin!)
│   ├── core/                # Config: Settings & Security
│   │   ├── config.py        # Pydantic Settings & Library Config Contract
│   │   └── security.py      # Local Auth helpers
│   ├── crud/                # Data Access: Database queries
│   ├── models/              # Persistence: DB Schema definitions (SQLAlchemy)
│   ├── schemas/             # Transfer: Pydantic request/response models
│   ├── services/            # Business Logic: The "Brains" of the operation
│   ├── worker/              # Background Tasks: Stream consumers
│   └── main.py              # Entry Glue: Initializes FastAPI & Middleware
├── tests/                   # Pytest suite
├── migrations/              # Alembic (Database migrations)
├── scripts/                 # Maintenance scripts
├── Dockerfile               # Optimized multi-stage build (uv)
└── pyproject.toml           # Dependency management (uv)
```

---

## 3. Key Concepts

### A. The "Glue" (`app/main.py`)
This file is intentionally thin. It imports setup functions from `my-company-core` and "glues" them to the FastAPI application.

```python
# app/main.py
from my_company_core.logging import setup_logging
from app.core.config import settings

setup_logging(settings.logger_config) # Initialize shared logging
```

### B. Configuration Strategy ("Explicit Contract")
We do **not** let the shared library read environment variables directly. Instead, we use an **Explicit Configuration** pattern.

1.  **Shared Library**: Defines a Pydantic Model for what it needs (e.g., `DatabaseConfig`).
2.  **Microservice**: Reads `.env` vars and constructs that config object.
3.  **Wiring**: The config object is passed explicitly to the library.

*See [docs/configuration_strategy.md](docs/configuration_strategy.md) for full details.*

### C. External Services (Postgres, Redis, NATS)

#### Postgres (SQLAlchemy)
*   **Shared Lib**: Provides the `Engine` creation and `get_db` session generator.
*   **Microservice**: Defines the **Models** (`app/models/`) and manages **Migrations** (`migrations/`) locally.

#### Messaging (Redis/NATS)
*   **Shared Lib**: Handles connection lifecycle (connect/reconnect) and provides generic `Publisher`/`Consumer` abstrations.
*   **Microservice**: Uses these abstractions in `app/services/` to publish events (e.g., `await bus.publish("user.created", data)`).

### D. Logging
Logging is centralized in the shared library to ensure consistency (JSON format, correlation IDs). The microservice simply initializes it and calls standard Python logging.

---

## 4. Getting Started

### Prerequisites
*   Python 3.11+
*   `uv` (for dependency management)
*   Docker

### Installation

1.  **Clone & Rename**:
    ```bash
    git clone <this-repo> my-new-service
    cd my-new-service
    ```

2.  **Install Dependencies**:
    ```bash
    uv sync
    ```

3.  **Configure Environment**:
    ```bash
    cp .env.example .env
    # Edit .env with your local credentials
    ```

4.  **Run Locally**:
    ```bash
    uv run uvicorn app.main:app --reload
    ```
