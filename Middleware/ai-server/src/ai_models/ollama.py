import os
from dotenv import load_dotenv
from .base import AbstractAIModel
from ollama import Client

# Load environment variables
load_dotenv()

class OllamaAIModel(AbstractAIModel):

    def __init__(self, model: str = "llama3.2"):
        self.client = Client(
            host=os.getenv("OLLAMA_HOST"),
        )
        self.client.pull(model)
        self.model = model

    def get_response(self, prompt: str, system_prompt: str) -> str:
        """
        Generate a response using the Ollama AI model.

        Args:
            prompt (str): The user input prompt.
            system_prompt (str): The system prompt.

        Returns:
            str: The AI-generated response
        """
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )

        return response.message.content
    

class OllamaAIModelWithoutSystemPrompt(AbstractAIModel):

    def __init__(self, model: str = "deepseek-r1"):
        self.client = Client(
            host=os.getenv("OLLAMA_HOST"),
        )
        self.client.pull(model)
        self.model = model

    def get_response(self, prompt: str, system_prompt: str) -> str:
        """
        Generate a response using the Ollama AI model.

        Args:
            prompt (str): The user input prompt.
            system_prompt (str): The system prompt.

        Returns:
            str: The AI-generated response
        """
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": f"#Instructions:\n{system_prompt}\n#Prompt:\n{prompt}"},
            ],
        )

        return response.message.content
