from typing import List, Union

from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Microservice Template"
    API_V1_STR: str = "/api/v1"
    
    # SERVER
    PORT: int = 6536
    
    # DATABASE
    POSTGRES_SERVER: str = "postgres-new.dev.orahi.com"
    POSTGRES_PORT: int = 6536
    POSTGRES_USER: str = "ofc_admin"
    POSTGRES_PASSWORD: str = "l9uVlK097hGH"
    POSTGRES_DB: str = "db_ofc_2"
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
            username=info.data.get("POSTGRES_USER", "ofc_admin"),
            password=info.data.get("POSTGRES_PASSWORD", "l9uVlK097hGH"),
            host=info.data.get("POSTGRES_SERVER", "postgres-new.dev.orahi.com"),
            port=info.data.get("POSTGRES_PORT", 6536),
            path=f"{info.data.get('POSTGRES_DB', 'db_ofc_2') or ''}",
        )

    # REDIS
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
