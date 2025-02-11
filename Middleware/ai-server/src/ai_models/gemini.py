from dotenv import load_dotenv
from .base import AbstractAIModel
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

class GeminiAIModel(AbstractAIModel):
    """Gemini AI model for generating text."""

    API_KEY_ENV: str = "GEMINI_API_KEY"

    def __init__(self, model: str = "gemini-2.0-flash"):
        super().__init__()
        self.client = genai.Client(api_key=self.api_key)
        self.model = model

    def get_response(self, prompt: str, system_prompt: str) -> str:
        """
        Generate a response using Gemini's API.

        Args:
            prompt (str): The user input prompt.
            system_prompt (str): The system prompt.

        Returns:
            str: The AI-generated response
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            )
        )

        return response.text

