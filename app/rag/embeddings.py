from sentence_transformers import SentenceTransformer


from sentence_transformers import SentenceTransformer

from app.config.settings import settings


class EmbeddingProvider:

    def __init__(
        self,
        model_name: str | None = None,
    ):
        model_name = (
            model_name
            if model_name is not None
            else settings.embedding_model
        )

        self.model = SentenceTransformer(model_name)

    def embed(
        self,
        texts: list[str],
    ):
        return self.model.encode(texts)