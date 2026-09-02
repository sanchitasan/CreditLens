import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    """
    Central configuration for the local CreditLens application.

    Configuration is loaded from environment variables when provided,
    otherwise sensible local defaults are used.
    """

    # -------------------------
    # Application
    # -------------------------

    app_name: str = os.getenv(
        "CREDITLENS_APP_NAME",
        "CreditLens",
    )

    # -------------------------
    # Gemini / LLM
    # -------------------------

    gemini_api_key: str | None = os.getenv(
        "GEMINI_API_KEY"
    )

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.6-flash",
    )

    # -------------------------
    # SQLite
    # -------------------------

    database_path: Path = PROJECT_ROOT / os.getenv(
        "CREDITLENS_DATABASE_PATH",
        "data/creditlens.db",
    )

    # -------------------------
    # Qdrant
    # -------------------------

    qdrant_path: Path = PROJECT_ROOT / os.getenv(
        "CREDITLENS_QDRANT_PATH",
        "data/qdrant",
    )

    qdrant_collection: str = os.getenv(
        "QDRANT_COLLECTION",
        "credit_policy",
    )

    qdrant_vector_size: int = int(
        os.getenv(
            "QDRANT_VECTOR_SIZE",
            "384",
        )
    )

    # -------------------------
    # Embeddings
    # -------------------------

    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "all-MiniLM-L6-v2",
    )


settings = Settings()