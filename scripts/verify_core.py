
"""Demonstrate InsureSearch core functionality."""

from insure_search.core import (
    Document,
    DocumentChunk,
    DocumentMetadata,
    DocumentType,
    InsuranceType,
    SearchQuery,
    get_settings,
)


def main() -> None:
    settings = get_settings()

    print("Application:", settings.app_name)
    print("Embedding model:", settings.embedding_model)
    print("Vector dimension:", settings.embedding_dimension)
    print("Vector database:", settings.qdrant_url)

    metadata = DocumentMetadata(
        source="health_policy.pdf",
        insurance_type=InsuranceType.HEALTH,
        document_type=DocumentType.POLICY,
        insurer="Example Insurance",
        policy_id="POL-2026-001",
        policy_version="1.0",
        jurisdiction="Illinois",
        country="USA",
    )

    document = Document(
        content=(
            "The policy covers accidental hospitalization. "
            "Cosmetic surgery is excluded from coverage."
        ),
        metadata=metadata,
    )

    chunk = DocumentChunk(
        document_id=document.id,
        content="Cosmetic surgery is excluded from coverage.",
        chunk_index=0,
        page_number=12,
        section="Coverage Exclusions",
        clause_number="4.2",
        metadata=document.metadata,
    )

    query = SearchQuery(
        query="Does insurance cover cosmetic surgery?",
        insurance_type=InsuranceType.HEALTH,
        top_k=5,
    )

    print("\n--- Document ---")
    print(document.model_dump_json(indent=2))

    print("\n--- Document Chunk ---")
    print(chunk.model_dump_json(indent=2))

    print("\n--- Search Query ---")
    print(query.model_dump_json(indent=2))

    print("\nCore verification completed successfully.")


if __name__ == "__main__":
    main()
