from app.rag.vector_store import QdrantVectorStore


def test_qdrant_vector_store_initializes():

    vector_store = QdrantVectorStore(
        path="data/test_qdrant"
    )

    assert vector_store.client is not None

def test_qdrant_collection_is_created(tmp_path):

    vector_store = QdrantVectorStore(
        path=str(tmp_path)
    )

    vector_store.create_collection()

    collections = vector_store.client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    assert "credit_policy" in collection_names

def test_qdrant_can_index_chunks(tmp_path):

    vector_store = QdrantVectorStore(
        path=str(tmp_path)
    )

    vector_store.create_collection()

    chunks = [
        {
            "source": "credit_policy.md",
            "chunk_id": 0,
            "content": "FOIR below 40% is considered low risk.",
        },
        {
            "source": "credit_policy.md",
            "chunk_id": 1,
            "content": "Credit scores above 750 indicate strong credit quality.",
        },
    ]

    embeddings = [
        [0.1] * 384,
        [0.2] * 384,
    ]

    vector_store.add_chunks(
        chunks,
        embeddings,
    )

    collection_info = vector_store.client.get_collection(
        "credit_policy"
    )

    assert collection_info.points_count == 2