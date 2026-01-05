# Configuration Strategy: "Explicit Contract"

This document outlines the recommended pattern for configuring the integration between a microservice and the shared library (`my-company-core`).

## The Philosophy
**Explicit is Better.**
Avoid having the shared library read environment variables directly. Instead, pass configuration objects explicitly. This ensures:
1.  **No Hidden Magic:** You know exactly what values the library is using.
2.  **Testability:** You can easily pass dummy configs during tests without mocking `os.environ`.
3.  **Validation:** The app validates the config *before* the library tries to use it.

## The Pattern

### 1. The Shared Library (`my-company-core`)
Defines the "Contract" using Pydantic Models. It does NOT read `.env` files.

```python
# my_company_core/config.py
from pydantic import BaseModel, PostgresDsn

class DatabaseConfig(BaseModel):
    dsn: PostgresDsn
    pool_size: int = 10

class LoggerConfig(BaseModel):
    level: str = "INFO"
    json_format: bool = True
```

The setup functions accept these models:

```python
# my_company_core/database.py
from .config import DatabaseConfig

def setup_db(config: DatabaseConfig):
    # Setup engine using config.dsn and config.pool_size
    pass
```

### 2. The Microservice (`app/`)
The microservice is responsible for reading the environment (via `pydantic-settings`) and converting it into the format the library expects.

```python
# app/core/config.py
from pydantic_settings import BaseSettings
# from my_company_core.config import DatabaseConfig # Imported from lib

class Settings(BaseSettings):
    # App specific
    PROJECT_NAME: str = "My Service"
    
    # Required by Library (names match environment variables)
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: str = None
    
    # Property to construct the Library's config object
    @property
    def db_config(self):
        """Construct the library's config object from our flat env vars"""
        # return DatabaseConfig(
        #     dsn=self.SQLALCHEMY_DATABASE_URI,
        #     pool_size=20
        # )
        return {} # Placeholder until lib is ready
```

### 3. Wiring it up (`app/main.py`)
Pass the config explicitly.

```python
# app/main.py
# from my_company_core.database import setup_db
from app.core.config import settings

# Explicit passing - clean and obvious!
# setup_db(settings.db_config)
```
