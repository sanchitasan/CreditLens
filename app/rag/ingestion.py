class RAGIngestionService:

    def __init__(
        self,
        loader,
        chunker,
        embedding_provider,
        vector_store,
    ):
        self.loader = loader
        self.chunker = chunker
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def ingest(self):

        documents = self.loader.load_documents()

        chunks = self.chunker.chunk_documents(
            documents
        )

        texts = [
            chunk["content"]
            for chunk in chunks
        ]

        embeddings = self.embedding_provider.embed(
            texts
        )

        self.vector_store.add_chunks(
            chunks,
            embeddings,
        )