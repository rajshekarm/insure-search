"""Verify InsureSearch development environment."""

import os

from dotenv import load_dotenv
from FlagEmbedding import BGEM3FlagModel
from qdrant_client import QdrantClient


def main() -> None:
    load_dotenv()

    print("Verifying InsureSearch environment...")
    print("-" * 50)

    # Verify Qdrant connectivity
    client = QdrantClient(
        url=os.getenv(
            "QDRANT_URL",
            "http://localhost:6333"
        ),
        api_key=os.getenv("QDRANT_API_KEY") or None,
    )

    collections = client.get_collections()

    print("[PASS] Qdrant connection successful")
    print(f"Collections: {len(collections.collections)}")

    # Initialize embedding model
    model = BGEM3FlagModel(
        os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3"),
        devices=os.getenv("EMBEDDING_DEVICE", "cpu"),
        use_fp16=(
            os.getenv("EMBEDDING_USE_FP16", "false")
            .lower() == "true"
        ),
    )

    texts = [
        "The insurance policy covers accidental damage.",
        "Flood damage is excluded from coverage.",
    ]

    result = model.encode(
        texts,
        batch_size=2,
        max_length=512,
        return_dense=True,
        return_sparse=False,
        return_colbert_vecs=False,
    )

    vectors = result["dense_vecs"]

    expected_dimension = int(
        os.getenv("EMBEDDING_DIMENSION", "1024")
    )

    if vectors.shape != (len(texts), expected_dimension):
        raise ValueError(
            f"Unexpected embedding shape: {vectors.shape}"
        )

    print("[PASS] Embedding model loaded successfully")
    print(f"Embedding shape: {vectors.shape}")

    print("-" * 50)
    print("InsureSearch environment is ready!")


if __name__ == "__main__":
    main()