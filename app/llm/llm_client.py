class LLMClient:
    """
    Interface for Large Language Model clients.

    CreditLens interacts with LLM providers through
    this interface instead of depending directly
    on a specific provider.
    """

    def generate(self, prompt: str) -> str:
        """
        Generate a response from the supplied prompt.

        Concrete LLM clients must implement this method.
        """

        raise NotImplementedError(
            "LLM clients must implement generate()."
        )


class MockLLMClient(LLMClient):
    """
    Deterministic LLM client used for testing.

    No external API call is made.
    """

    def __init__(self, response: str = ""):
        self.response = response

    def generate(self, prompt: str) -> str:
        """
        Return the predefined response.
        """

        return self.response