from pathlib import Path

from app.rag.chunker import DocumentChunker
from app.rag.loader import DocumentLoader


def test_document_chunker_creates_sections():

    knowledge_directory = Path(
        "app/rag/knowledge"
    )

    loader = DocumentLoader(
        knowledge_directory
    )

    documents = loader.load_documents()

    chunker = DocumentChunker()

    chunks = chunker.chunk_documents(
        documents
    )

    assert len(chunks) > 1

    assert all(
        chunk["source"] == "credit_policy.md"
        for chunk in chunks
    )

    contents = [
        chunk["content"]
        for chunk in chunks
    ]

    assert any(
        "FOIR Guidelines" in content
        for content in contents
    )

    assert any(
        "Credit Score Guidelines" in content
        for content in contents
    )