from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class QdrantVectorStore:

    def __init__(
        self,
        path="data/qdrant",
        collection_name="credit_policy",
        vector_size=384,
    ):
        self.client = QdrantClient(path=path)
        self.collection_name = collection_name
        self.vector_size = vector_size

    def create_collection(self):

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings,
    ):

        points = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            points.append(
                PointStruct(
                    id=index,
                    vector=(
                        embedding.tolist()
                        if hasattr(embedding, "tolist")
                        else embedding
                    ),
                    payload={
                        "source": chunk["source"],
                        "content": chunk["content"],
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(
            self,
            query_vector,
            limit=3,
    ):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=(
                query_vector.tolist()
                if hasattr(query_vector, "tolist")
                else query_vector
            ),
            limit=limit,
            with_payload=True,
        )

        return results.points