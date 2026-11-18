# Architecture

This project is a foundation for an insurance-document semantic search system.

## Planned flow

1. Ingest source documents from `data/` or an external storage provider.
2. Parse and normalize document text and metadata.
3. Split documents into searchable chunks.
4. Generate embeddings and store them in a vector database.
5. Retrieve the most relevant chunks for a user query.
6. Return results with source metadata for traceability.

The implementation is intentionally minimal at this stage. Configuration belongs
in `configs/`, executable utilities belong in `scripts/`, and reusable Python
code belongs under `src/insure_search/`.
