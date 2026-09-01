import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from app.llm.llm_client import LLMClient


# Find the CreditLens project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load environment variables from .env
load_dotenv(PROJECT_ROOT / ".env")


class GeminiClient(LLMClient):
    """
    LLM client using Google's Gemini API.

    The Gemini API key is loaded from the
    project's .env file.
    """

    def __init__(
        self,
        model: str = "gemini-3.6-flash",
    ):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.model = model

        self.client = genai.Client(
            api_key=api_key
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