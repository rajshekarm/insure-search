
"""Core data models for InsureSearch."""

from datetime import date, datetime, timezone
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    field_validator,
    model_validator,
)


class InsuranceType(StrEnum):
    """Supported insurance categories."""

    HEALTH = "health"
    LIFE = "life"
    PROPERTY = "property"
    CASUALTY = "casualty"
    AUTO = "auto"
    COMMERCIAL = "commercial"
    REINSURANCE = "reinsurance"
    OTHER = "other"
    UNKNOWN = "unknown"


class DocumentType(StrEnum):
    """Supported insurance document categories."""

    POLICY = "policy"
    CLAIM = "claim"
    ENDORSEMENT = "endorsement"
    UNDERWRITING = "underwriting"
    REGULATORY = "regulatory"
    BROCHURE = "brochure"
    CONTRACT = "contract"
    REPORT = "report"
    OTHER = "other"
    UNKNOWN = "unknown"


class CoreModel(BaseModel):
    """Base model for application data schemas."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class DocumentMetadata(CoreModel):
    """Insurance-specific document metadata."""

    insurance_type: InsuranceType = InsuranceType.UNKNOWN
    document_type: DocumentType = DocumentType.UNKNOWN

    title: str | None = None
    source: str = Field(min_length=1)

    insurer: str | None = None
    policy_id: str | None = None
    claim_id: str | None = None

    country: str | None = None
    jurisdiction: str | None = None

    policy_version: str | None = None
    effective_date: date | None = None
    expiration_date: date | None = None

    language: str = "en"
    tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if (
            self.effective_date
            and self.expiration_date
            and self.expiration_date < self.effective_date
        ):
            raise ValueError(
                "Expiration date cannot precede effective date."
            )

        return self


class Document(CoreModel):
    """Original document extracted from a data source."""

    id: UUID = Field(default_factory=uuid4)

    content: str = Field(
        min_length=1,
        repr=False,
    )

    metadata: DocumentMetadata

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class DocumentChunk(CoreModel):
    """Searchable segment of an insurance document."""

    id: UUID = Field(default_factory=uuid4)
    document_id: UUID

    content: str = Field(
        min_length=1,
        repr=False,
    )

    chunk_index: int = Field(ge=0)
    token_count: int | None = Field(default=None, gt=0)

    page_number: int | None = Field(default=None, ge=1)
    section: str | None = None
    clause_number: str | None = None

    metadata: DocumentMetadata


class EmbeddedChunk(CoreModel):
    """Document chunk with its generated dense embedding."""

    chunk: DocumentChunk

    embedding: list[FiniteFloat] = Field(
        min_length=1,
        repr=False,
    )

    embedding_model: str = Field(min_length=1)
    embedding_dimension: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_embedding_dimension(self) -> Self:
        if len(self.embedding) != self.embedding_dimension:
            raise ValueError(
                "Embedding length does not match "
                "the declared embedding dimension."
            )

        return self


class SearchQuery(CoreModel):
    """Standardized semantic search request."""

    query: str = Field(min_length=1, repr=False)
    top_k: int | None = Field(default=None, ge=1, le=100)

    insurance_type: InsuranceType | None = None
    document_type: DocumentType | None = None

    policy_id: str | None = None
    jurisdiction: str | None = None

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Search query cannot be empty.")

        return value.strip()


class SearchResult(CoreModel):
    """Single result returned by the retrieval engine."""

    chunk: DocumentChunk

    score: FiniteFloat
    rank: int = Field(ge=1)
