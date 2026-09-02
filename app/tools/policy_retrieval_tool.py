from app.rag.context import RAGContextBuilder
from app.rag.embeddings import EmbeddingProvider
from app.rag.factor_queries import RAGFactorQueryBuilder
from app.rag.factor_retriever import RAGFactorRetriever
from app.rag.retriever import RAGRetriever
from app.rag.vector_store import QdrantVectorStore


def policy_retrieval_tool(
    foir: float,
    credit_score: float,
    previous_defaults: int,
    default_probability: float,
    lending_decision: str,
) -> str:
    """
    Retrieve policy context relevant to the applicant's
    credit-risk factors.

    This tool retrieves policy guidance only.
    It does not make or override a lending decision.
    """

    query_builder = RAGFactorQueryBuilder()

    queries = query_builder.build(
        foir=foir,
        credit_score=credit_score,
        previous_defaults=previous_defaults,
        default_probability=default_probability,
        lending_decision=lending_decision,
    )

    retriever = RAGRetriever(
        embedding_provider=EmbeddingProvider(),
        vector_store=QdrantVectorStore(
            path="data/qdrant",
            collection_name="credit_policy",
            vector_size=384,
        ),
    )

    factor_retriever = RAGFactorRetriever(
        retriever=retriever
    )

    results = factor_retriever.retrieve(
        queries=queries,
        limit_per_query=1,
    )

    context_builder = RAGContextBuilder()

    return context_builder.build(results)