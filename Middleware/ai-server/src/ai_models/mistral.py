from dotenv import load_dotenv
from .base import AbstractAIModel
from mistralai import Mistral

# Load environment variables
load_dotenv()

class MistralAIModel(AbstractAIModel):
    """Mistral AI model for generating text."""

    API_KEY_ENV: str = "MISTRAL_API_KEY"

    def __init__(self, model: str = "mistral-small-latest"):
        super().__init__()
        self.client = Mistral(api_key=self.api_key)
        self.model = model

    def get_response(self, prompt: str, system_prompt: str) -> str:
        """
        Generate a response using the Mistral AI model.

        Args:
            prompt (str): The user input prompt.
            system_prompt (str): The system prompt.

        Returns:
            str: The AI-generated response
        """

        # Generate a response from Mistral
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content