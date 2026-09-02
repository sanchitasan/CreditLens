from pathlib import Path

from app.rag.loader import DocumentLoader


def test_document_loader_loads_credit_policy():

    knowledge_directory = Path(
        "app/rag/knowledge"
    )

    loader = DocumentLoader(
        knowledge_directory
    )

    documents = loader.load_documents()

    assert len(documents) >= 1

    assert documents[0]["source"] == "credit_policy.md"

    assert "FOIR" in documents[0]["content"]

    assert "Credit Score" in documents[0]["content"]