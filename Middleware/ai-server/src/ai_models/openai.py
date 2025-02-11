from dotenv import load_dotenv
from .base import AbstractAIModel
from openai import OpenAI

# Load environment variables
load_dotenv()

class OpenAIModel(AbstractAIModel):
    """OpenAI GPT-3 model for generating text."""

    API_KEY_ENV: str = "OPENAI_API_KEY"

    def __init__(self, model: str = "gpt-4o-mini"):
        super().__init__()
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def get_response(self, prompt: str, system_prompt: str) -> str:
        """
        Generate a response using OpenAI's API.

        Args:
            prompt (str): The user input prompt.
            system_prompt (str): The system prompt.

        Returns:
            str: The AI-generated response
        """

        # Generate a response from OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content


