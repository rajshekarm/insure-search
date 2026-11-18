
"""Unit tests for InsureSearch data schemas."""

from datetime import date

import pytest
from pydantic import ValidationError

from insure_search.core.schemas import (
    Document,
    DocumentChunk,
    DocumentMetadata,
    DocumentType,
    EmbeddedChunk,
    InsuranceType,
    SearchQuery,
    SearchResult,
)


@pytest.fixture
def metadata() -> DocumentMetadata:
    return DocumentMetadata(
        source="sample_policy.pdf",
        insurance_type=InsuranceType.HEALTH,
        document_type=DocumentType.POLICY,
        policy_id="POL-001",
    )


@pytest.fixture
def document(
    metadata: DocumentMetadata,
) -> Document:
    return Document(
        content="Accidental hospitalization is covered.",
        metadata=metadata,
    )


@pytest.fixture
def chunk(document: Document) -> DocumentChunk:
    return DocumentChunk(
        document_id=document.id,
        content=document.content,
        chunk_index=0,
        metadata=document.metadata,
    )


def test_document_creation(document: Document) -> None:
    assert document.id is not None
    assert document.metadata.policy_id == "POL-001"


def test_empty_document(metadata: DocumentMetadata) -> None:
    with pytest.raises(ValidationError):
        Document(content="", metadata=metadata)


def test_chunk_creation(chunk: DocumentChunk) -> None:
    assert chunk.chunk_index == 0
    assert chunk.document_id is not None


def test_valid_embedding(chunk: DocumentChunk) -> None:
    embedded = EmbeddedChunk(
        chunk=chunk,
        embedding=[0.1] * 1024,
        embedding_model="BAAI/bge-m3",
        embedding_dimension=1024,
    )

    assert len(embedded.embedding) == 1024


def test_invalid_embedding(chunk: DocumentChunk) -> None:
    with pytest.raises(ValidationError):
        EmbeddedChunk(
            chunk=chunk,
            embedding=[0.1] * 512,
            embedding_model="BAAI/bge-m3",
            embedding_dimension=1024,
        )


def test_invalid_policy_dates() -> None:
    with pytest.raises(ValidationError):
        DocumentMetadata(
            source="policy.pdf",
            effective_date=date(2026, 1, 1),
            expiration_date=date(2025, 1, 1),
        )


def test_empty_search_query() -> None:
    with pytest.raises(ValidationError):
        SearchQuery(query="   ")


def test_search_result(chunk: DocumentChunk) -> None:
    result = SearchResult(
        chunk=chunk,
        score=0.95,
        rank=1,
    )

    assert result.score == 0.95
    assert result.rank == 1


def test_document_serialization(document: Document) -> None:
    payload = document.model_dump(mode="json")

    assert isinstance(payload["id"], str)
    assert payload["metadata"]["insurance_type"] == "health"
