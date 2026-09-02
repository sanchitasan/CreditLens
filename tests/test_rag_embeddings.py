from app.rag.embeddings import EmbeddingProvider


def test_embedding_provider_creates_embeddings():

    provider = EmbeddingProvider()

    texts = [
        "FOIR above 50 percent requires additional review.",
        "Applicants with high debt obligations require assessment.",
    ]

    embeddings = provider.embed(texts)

    assert len(embeddings) == 2

    assert embeddings.shape[1] == 384