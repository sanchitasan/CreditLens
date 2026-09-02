from pathlib import Path

from app.rag.embeddings import EmbeddingProvider
from app.rag.retriever import RAGRetriever
from app.rag.vector_store import QdrantVectorStore


def test_policy_retrieval_quality():

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

    evaluation_cases = [
        (
            "What FOIR is considered high risk?",
            "## 2. FOIR Guidelines",
        ),
        (
            "What credit score indicates strong credit quality?",
            "## 3. Credit Score Guidelines",
        ),
        (
            "How should previous defaults affect risk?",
            "## 4. Previous Defaults",
        ),
        (
            "How is ML default probability used?",
            "## 5. ML Default Probability",
        ),
    ]

    for query, expected_section in evaluation_cases:

        results = retriever.retrieve(
            query=query,
            limit=3,
        )

        retrieved_content = [
            result.payload["content"]
            for result in results
        ]

        assert any(
            expected_section in content
            for content in retrieved_content
        ), f"Expected section not retrieved for query: {query}"