from app.rag.ingestion import RAGIngestionService


class FakeLoader:

    def load_documents(self):

        return [
            {
                "source": "credit_policy.md",
                "content": "Policy content",
            }
        ]


class FakeChunker:

    def chunk_documents(self, documents):

        return [
            {
                "source": "credit_policy.md",
                "chunk_id": 0,
                "content": "Policy chunk",
            }
        ]


class FakeEmbeddingProvider:

    def embed(self, texts):

        return [
            [0.1] * 384
        ]


class FakeVectorStore:

    def __init__(self):

        self.chunks = None
        self.embeddings = None

    def add_chunks(self, chunks, embeddings):

        self.chunks = chunks
        self.embeddings = embeddings


def test_rag_ingestion_pipeline():

    loader = FakeLoader()
    chunker = FakeChunker()
    embedding_provider = FakeEmbeddingProvider()
    vector_store = FakeVectorStore()

    service = RAGIngestionService(
        loader=loader,
        chunker=chunker,
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    service.ingest()

    assert vector_store.chunks is not None
    assert vector_store.embeddings is not None
    assert len(vector_store.chunks) == 1
    assert len(vector_store.embeddings) == 1