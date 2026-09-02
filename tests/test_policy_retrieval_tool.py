from types import SimpleNamespace

from app.tools import policy_retrieval_tool as policy_module


class FakeFactorQueryBuilder:
    def __init__(self):
        self.received = None

    def build(
        self,
        foir,
        credit_score,
        previous_defaults,
        default_probability,
        lending_decision,
    ):
        self.received = {
            "foir": foir,
            "credit_score": credit_score,
            "previous_defaults": previous_defaults,
            "default_probability": default_probability,
            "lending_decision": lending_decision,
        }

        return [
            "FOIR policy",
            "credit score policy",
            "previous defaults policy",
            "ML default probability policy",
            "lending decision policy",
        ]


class FakeFactorRetriever:
    def __init__(self, retriever):
        self.retriever = retriever
        self.received_queries = None
        self.received_limit = None

    def retrieve(self, queries, limit_per_query=1):
        self.received_queries = queries
        self.received_limit = limit_per_query

        return [
            SimpleNamespace(
                payload={
                    "source": "credit_policy.md",
                    "content": "FOIR policy guidance",
                },
                score=0.8,
            )
        ]


class FakeContextBuilder:
    def build(self, results):
        return "FOIR policy guidance"


def test_policy_retrieval_tool_returns_policy_context(monkeypatch):

    fake_query_builder = FakeFactorQueryBuilder()
    fake_factor_retriever = FakeFactorRetriever(None)

    monkeypatch.setattr(
        policy_module,
        "RAGFactorQueryBuilder",
        lambda: fake_query_builder,
    )

    monkeypatch.setattr(
        policy_module,
        "RAGFactorRetriever",
        lambda retriever: fake_factor_retriever,
    )

    monkeypatch.setattr(
        policy_module,
        "RAGRetriever",
        lambda embedding_provider, vector_store: object(),
    )

    monkeypatch.setattr(
        policy_module,
        "EmbeddingProvider",
        lambda: object(),
    )

    monkeypatch.setattr(
        policy_module,
        "QdrantVectorStore",
        lambda path, collection_name, vector_size: object(),
    )

    monkeypatch.setattr(
        policy_module,
        "RAGContextBuilder",
        lambda: FakeContextBuilder(),
    )

    result = policy_module.policy_retrieval_tool(
        foir=25.0,
        credit_score=780,
        previous_defaults=0,
        default_probability=0.03,
        lending_decision="APPROVE",
    )

    assert result == "FOIR policy guidance"

    assert fake_query_builder.received["foir"] == 25.0
    assert fake_query_builder.received["credit_score"] == 780
    assert fake_query_builder.received["previous_defaults"] == 0
    assert fake_query_builder.received["default_probability"] == 0.03
    assert fake_query_builder.received["lending_decision"] == "APPROVE"

    assert len(fake_factor_retriever.received_queries) == 5
    assert fake_factor_retriever.received_limit == 1