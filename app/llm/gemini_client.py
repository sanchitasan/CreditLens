from google import genai

from app.config.settings import Settings
from app.llm.llm_client import LLMClient


class GeminiClient(LLMClient):
    """
    LLM client using Google's Gemini API.
    """

    def __init__(
        self,
        model: str | None = None,
    ):
        current_settings = Settings.from_environment()

        if not current_settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.model = (
            model
            if model is not None
            else current_settings.gemini_model
        )

        self.client = genai.Client(
            api_key=current_settings.gemini_api_key
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to Gemini and return
        the generated text.
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text