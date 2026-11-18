"""Centralized configuration for InsureSearch."""

from functools import lru_cache
from typing import Literal, Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True,
        frozen=True,
    )

    # Application settings
    app_name: str = "InsureSearch"
    app_env: Literal[
        "development", "testing", "production"
    ] = "development"
    log_level: str = "INFO"

    # Embedding settings
    embedding_model: str = "BAAI/bge-m3"
    embedding_dimension: int = Field(default=1024, gt=0)
    embedding_device: str = "cpu"
    embedding_batch_size: int = Field(default=8, gt=0)
    embedding_use_fp16: bool = False
    embedding_max_length: int = Field(default=1024, gt=0)

    # Qdrant settings
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "insurance_documents"
    qdrant_api_key: SecretStr | None = None
    qdrant_timeout: float = Field(default=30.0, gt=0)

    # Chunking settings
    chunk_size: int = Field(default=512, gt=0)
    chunk_overlap: int = Field(default=64, ge=0)

    # Retrieval settings
    search_top_k: int = Field(default=10, ge=1, le=100)

    @model_validator(mode="after")
    def validate_configuration(self) -> Self:
        """Validate relationships between settings."""

        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "Chunk overlap must be smaller than chunk size."
            )

        if self.chunk_size > self.embedding_max_length:
            raise ValueError(
                "Chunk size cannot exceed embedding max length."
            )

        if (
            self.embedding_device == "cpu"
            and self.embedding_use_fp16
        ):
            raise ValueError(
                "FP16 is disabled for CPU inference."
            )

        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached application settings instance."""
    return Settings()
