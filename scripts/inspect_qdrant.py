from pathlib import Path

from app.rag.vector_store import QdrantVectorStore


def main():

    project_root = Path(__file__).resolve().parent.parent

    vector_store = QdrantVectorStore(
        path=str(project_root / "data" / "qdrant"),
        collection_name="credit_policy",
        vector_size=384,
    )

    collection_info = vector_store.client.get_collection(
        "credit_policy"
    )

    print("Collection:", vector_store.collection_name)
    print("Vector size:", collection_info.config.params.vectors.size)
    print("Points:", collection_info.points_count)

    points, _ = vector_store.client.scroll(
        collection_name="credit_policy",
        limit=3,
        with_payload=True,
        with_vectors=False,
    )

    print("\nSample points:")

    for point in points:

        print("\nID:", point.id)
        print("Source:", point.payload["source"])
        print("Content:")
        print(point.payload["content"])


if __name__ == "__main__":
    main()