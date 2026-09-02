from app.rag.retriever import RAGRetriever


class FakeEmbeddingProvider:

    def embed(self, texts):

        assert texts == [
            "What FOIR is considered high risk?"
        ]

        return [
            [0.1, 0.2, 0.3]
        ]


class FakeVectorStore:

    def __init__(self):

        self.received_vector = None
        self.received_limit = None

    def search(self, query_vector, limit):

        self.received_vector = query_vector
        self.received_limit = limit

        return [
            {
                "content": "FOIR above 50% is high risk.",
                "score": 0.91,
            }
        ]


def test_retriever_embeds_query_and_searches():

    embedding_provider = FakeEmbeddingProvider()
    vector_store = FakeVectorStore()

    retriever = RAGRetriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        "What FOIR is considered high risk?"
    )

    assert vector_store.received_vector == [
        0.1,
        0.2,
        0.3,
    ]

    assert vector_store.received_limit == 3

    assert len(results) == 1
    assert (
        results[0]["content"]
        == "FOIR above 50% is high risk."
    )