from pathlib import Path

from app.config.settings import PROJECT_ROOT, Settings


def test_default_settings():
    settings = Settings.from_environment()

    assert settings.app_name == "CreditLens"
    assert settings.gemini_model == "gemini-3.6-flash"

    assert settings.database_path == (
        PROJECT_ROOT / "data/creditlens.db"
    )

    assert settings.qdrant_path == (
        PROJECT_ROOT / "data/qdrant"
    )

    assert settings.qdrant_collection == "credit_policy"
    assert settings.qdrant_vector_size == 384
    assert settings.embedding_model == "all-MiniLM-L6-v2"


def test_environment_override(monkeypatch):
    monkeypatch.setenv(
        "GEMINI_MODEL",
        "test-gemini-model",
    )

    monkeypatch.setenv(
        "QDRANT_COLLECTION",
        "test_collection",
    )

    monkeypatch.setenv(
        "QDRANT_VECTOR_SIZE",
        "128",
    )

    settings = Settings.from_environment()

    assert settings.gemini_model == "test-gemini-model"
    assert settings.qdrant_collection == "test_collection"
    assert settings.qdrant_vector_size == 128