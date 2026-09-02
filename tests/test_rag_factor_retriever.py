from types import SimpleNamespace

from app.rag.factor_retriever import RAGFactorRetriever


class FakeRetriever:
    def __init__(self):
        self.queries = []

    def retrieve(self, query, limit):
        self.queries.append((query, limit))

        return [
            SimpleNamespace(
                score=0.9,
                payload={
                    "source": "credit_policy.md",
                    "content": f"Policy for {query}",
                },
            )
        ]


def test_factor_retriever_queries_each_factor():

    retriever = FakeRetriever()
    factor_retriever = RAGFactorRetriever(retriever)

    queries = [
        "FOIR policy",
        "credit score policy",
        "previous default policy",
        "ML default probability policy",
        "APPROVE lending decision policy",
    ]

    results = factor_retriever.retrieve(
        queries=queries,
        limit_per_query=1,
    )

    assert len(results) == 5
    assert len(retriever.queries) == 5
    assert all(limit == 1 for _, limit in retriever.queries)


def test_factor_retriever_removes_duplicate_chunks():

    class DuplicateRetriever:
        def retrieve(self, query, limit):
            return [
                SimpleNamespace(
                    score=0.9,
                    payload={
                        "source": "credit_policy.md",
                        "content": "Same policy chunk",
                    },
                )
            ]

    retriever = DuplicateRetriever()
    factor_retriever = RAGFactorRetriever(retriever)

    queries = [
        "FOIR policy",
        "credit score policy",
    ]

    results = factor_retriever.retrieve(queries)

    assert len(results) == 1