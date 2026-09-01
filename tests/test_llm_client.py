from app.llm.llm_client import (
    LLMClient,
    MockLLMClient,
)


def test_mock_llm_client_returns_response():

    client = MockLLMClient(
        response="Credit assessment looks reasonable."
    )

    result = client.generate(
        "Analyze this credit application."
    )

    assert result == "Credit assessment looks reasonable."


def test_base_llm_client_requires_implementation():

    client = LLMClient()

    try:
        client.generate("test prompt")
        assert False
    except NotImplementedError:
        assert True