from app.llm.gemini_client import GeminiClient


def test_gemini_client_requires_api_key(monkeypatch):

    monkeypatch.delenv(
        "GEMINI_API_KEY",
        raising=False,
    )

    try:
        GeminiClient()
        assert False
    except ValueError as error:
        assert "GEMINI_API_KEY" in str(error)