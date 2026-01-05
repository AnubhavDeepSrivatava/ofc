from typing import List, Union

from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Microservice Template"
    API_V1_STR: str = "/api/v1"
    
    # DATABASE
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "1234"
    POSTGRES_DB: str = "Ofc"
    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Union[str, None], info) -> AnyHttpUrl:
        if isinstance(v, str):
            return v
        if not info.data:
            return None
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER", "Ofc"),
            password=info.data.get("POSTGRES_PASSWORD", "1234"),
            host=info.data.get("POSTGRES_SERVER", "localhost"),
            path=f"{info.data.get('POSTGRES_DB', 'Ofc') or ''}",
        )

    # REDIS
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
