from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    """
    Central configuration for the local CreditLens application.
    """

    app_name: str
    gemini_api_key: str | None
    gemini_model: str
    database_path: Path
    qdrant_path: Path
    qdrant_collection: str
    qdrant_vector_size: int
    embedding_model: str

    @classmethod
    def from_environment(cls):
        return cls(
            app_name=os.getenv(
                "CREDITLENS_APP_NAME",
                "CreditLens",
            ),
            gemini_api_key=os.getenv(
                "GEMINI_API_KEY"
            ),
            gemini_model=os.getenv(
                "GEMINI_MODEL",
                "gemini-3.6-flash",
            ),
            database_path=PROJECT_ROOT / os.getenv(
                "CREDITLENS_DATABASE_PATH",
                "data/creditlens.db",
            ),
            qdrant_path=PROJECT_ROOT / os.getenv(
                "CREDITLENS_QDRANT_PATH",
                "data/qdrant",
            ),
            qdrant_collection=os.getenv(
                "QDRANT_COLLECTION",
                "credit_policy",
            ),
            qdrant_vector_size=int(
                os.getenv(
                    "QDRANT_VECTOR_SIZE",
                    "384",
                )
            ),
            embedding_model=os.getenv(
                "EMBEDDING_MODEL",
                "all-MiniLM-L6-v2",
            ),
        )


settings = Settings.from_environment()