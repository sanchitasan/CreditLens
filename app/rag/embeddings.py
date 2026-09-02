from sentence_transformers import SentenceTransformer


class EmbeddingProvider:

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def embed(
        self,
        texts: list[str],
    ):
        return self.model.encode(texts)