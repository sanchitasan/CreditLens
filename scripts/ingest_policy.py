from pathlib import Path

from app.rag.loader import DocumentLoader
from app.rag.chunker import DocumentChunker
from app.rag.embeddings import EmbeddingProvider
from app.rag.vector_store import QdrantVectorStore
from app.rag.ingestion import RAGIngestionService



def main():

    project_root = Path(__file__).resolve().parent.parent

    knowledge_directory = (
        project_root / "app" / "rag" / "knowledge"
    )

    loader = DocumentLoader(
        knowledge_directory=knowledge_directory
    )

    chunker = DocumentChunker()

    embedding_provider = EmbeddingProvider()

    vector_store = QdrantVectorStore(
        path=str(project_root / "data" / "qdrant"),
        collection_name="credit_policy",
        vector_size=384,
    )

    existing_collections = [
        collection.name
        for collection in vector_store.client.get_collections().collections
    ]

    if "credit_policy" not in existing_collections:
        vector_store.create_collection()

    service = RAGIngestionService(
        loader=loader,
        chunker=chunker,
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    service.ingest()

    collection_info = vector_store.client.get_collection(
        "credit_policy"
    )

    print(
        f"Indexed {collection_info.points_count} policy chunks."
    )


if __name__ == "__main__":
    main()