
"""Unit tests for application configuration."""

import pytest
from pydantic import ValidationError

from insure_search.core.config import Settings, get_settings


def test_valid_settings() -> None:
    settings = Settings(
        _env_file=None,
        embedding_dimension=1024,
        embedding_device="cpu",
        embedding_use_fp16=False,
        embedding_max_length=1024,
        chunk_size=512,
        chunk_overlap=64,
    )

    assert settings.embedding_dimension == 1024
    assert settings.chunk_size == 512
    assert settings.chunk_overlap == 64


def test_invalid_chunk_overlap() -> None:
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            chunk_size=100,
            chunk_overlap=100,
        )


def test_invalid_embedding_dimension() -> None:
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            embedding_dimension=0,
        )


def test_invalid_chunk_size() -> None:
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            chunk_size=2048,
            chunk_overlap=64,
            embedding_max_length=1024,
        )


def test_environment_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("EMBEDDING_DIMENSION", "768")

    settings = Settings(_env_file=None)

    assert settings.embedding_dimension == 768


def test_settings_cache() -> None:
    get_settings.cache_clear()

    try:
        first = get_settings()
        second = get_settings()

        assert first is second
    finally:
        get_settings.cache_clear()
