class RAGFactorRetriever:
    def __init__(self, retriever):
        self.retriever = retriever

    def retrieve(self, queries: list[str], limit_per_query: int = 1):
        results = []
        seen_chunks = set()

        for query in queries:
            retrieved = self.retriever.retrieve(
                query=query,
                limit=limit_per_query,
            )

            for result in retrieved:
                payload = result.payload or {}
                content = payload.get("content", "")

                if content in seen_chunks:
                    continue

                seen_chunks.add(content)
                results.append(result)

        return results