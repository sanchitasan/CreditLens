class RAGRetriever:

    def __init__(
        self,
        embedding_provider,
        vector_store,
    ):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        limit: int = 3,
    ):

        query_embedding = self.embedding_provider.embed(
            [query]
        )[0]

        results = self.vector_store.search(
            query_vector=query_embedding,
            limit=limit,
        )

        return results