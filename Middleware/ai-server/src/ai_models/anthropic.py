from dotenv import load_dotenv
from .base import AbstractAIModel
import anthropic

# Load environment variables
load_dotenv()

class AnthropicAIModel(AbstractAIModel):
    """Anthropic AI model for generating text."""

    API_KEY_ENV: str = "ANTHROPIC_API_KEY"

    def __init__(self, model: str = "claude-3-5-haiku-latest"):
        super()._check_and_set_api_key()
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model

    def get_response(self, prompt: str, system_prompt: str) -> str:
        """
        Generate a response using AnthropAI's API.

        Args:
            prompt (str): The user input prompt.
            system_prompt (str): The system prompt.

        Returns:
            str: The AI-generated response
        """

        response = self.client.messages.create(
            max_tokens=100,
            model=self.model,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        return response.content

