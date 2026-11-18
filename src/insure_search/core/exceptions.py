
"""Custom exceptions for InsureSearch."""


class InsureSearchError(Exception):
    """Base exception for all InsureSearch errors."""


class ConfigurationError(InsureSearchError):
    """Invalid application configuration."""


class DocumentError(InsureSearchError):
    """Base exception for document processing failures."""


class DocumentLoadError(DocumentError):
    """Failed to load or extract a document."""


class UnsupportedDocumentTypeError(DocumentError):
    """Unsupported document format."""


class ChunkingError(DocumentError):
    """Failed to split a document into chunks."""


class EmbeddingError(InsureSearchError):
    """Failed to generate an embedding."""


class VectorStorageError(InsureSearchError):
    """Base exception for vector storage failures."""


class VectorConnectionError(VectorStorageError):
    """Failed to connect to the vector database."""


class VectorInsertError(VectorStorageError):
    """Failed to insert or update vectors."""


class RetrievalError(InsureSearchError):
    """Failed to retrieve search results."""
