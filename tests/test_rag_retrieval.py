from app.rag.vector_store import QdrantVectorStore


def test_qdrant_search_returns_relevant_point(tmp_path):

    vector_store = QdrantVectorStore(
        path=str(tmp_path),
        collection_name="credit_policy",
        vector_size=3,
    )

    vector_store.create_collection()

    chunks = [
        {
            "source": "credit_policy.md",
            "chunk_id": 0,
            "content": "FOIR above 50% is considered high risk.",
        },
        {
            "source": "credit_policy.md",
            "chunk_id": 1,
            "content": "Credit scores above 750 indicate strong credit quality.",
        },
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]

    vector_store.add_chunks(
        chunks,
        embeddings,
    )

    query_vector = [1.0, 0.0, 0.0]

    results = vector_store.search(
        query_vector=query_vector,
        limit=1,
    )

    assert len(results) == 1

    assert (
        results[0].payload["content"]
        == "FOIR above 50% is considered high risk."
    )

