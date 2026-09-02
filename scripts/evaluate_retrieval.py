from pathlib import Path

from app.rag.embeddings import EmbeddingProvider
from app.rag.factor_queries import RAGFactorQueryBuilder
from app.rag.factor_retriever import RAGFactorRetriever
from app.rag.retriever import RAGRetriever
from app.rag.vector_store import QdrantVectorStore


def main():

    project_root = Path(__file__).resolve().parent.parent

    embedding_provider = EmbeddingProvider()

    vector_store = QdrantVectorStore(
        path=str(project_root / "data" / "qdrant"),
        collection_name="credit_policy",
        vector_size=384,
    )

    retriever = RAGRetriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    factor_query_builder = RAGFactorQueryBuilder()

    factor_retriever = RAGFactorRetriever(
        retriever=retriever,
    )

    applicants = [
        {
            "name": "Low-risk applicant",
            "foir": 25.0,
            "credit_score": 780,
            "previous_defaults": 0,
            "default_probability": 0.10,
            "risk_level": "LOW",
            "lending_decision": "APPROVE",
        },
        {
            "name": "High-risk applicant",
            "foir": 58.0,
            "credit_score": 680,
            "previous_defaults": 2,
            "default_probability": 0.72,
            "risk_level": "HIGH",
            "lending_decision": "REJECT",
        },
    ]

    for applicant in applicants:

        print("\n" + "=" * 70)
        print(applicant["name"])
        print("=" * 70)

        queries = factor_query_builder.build(
            foir=applicant["foir"],
            credit_score=applicant["credit_score"],
            previous_defaults=applicant["previous_defaults"],
            default_probability=applicant["default_probability"],
            lending_decision=applicant["lending_decision"],
        )

        print("\nFACTOR QUERIES")

        for index, query in enumerate(queries, start=1):
            print(f"\nQuery {index}:")
            print(query)

        results = factor_retriever.retrieve(
            queries=queries,
            limit_per_query=1,
        )

        print("\nRETRIEVED POLICY CHUNKS")

        for index, result in enumerate(results, start=1):

            print(f"\nResult {index}")
            print("Score:", result.score)
            print("Source:", result.payload["source"])
            print("Content:")
            print(result.payload["content"])


if __name__ == "__main__":
    main()