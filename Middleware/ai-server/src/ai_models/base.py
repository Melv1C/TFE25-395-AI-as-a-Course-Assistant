import os
from abc import ABC, abstractmethod

class AbstractAIModel(ABC):
    """Abstract base class for AI backends."""

    API_KEY_ENV: str = ""  # To be set in subclasses

    def _check_and_set_api_key(self):
        """Initialize the AI backend with the API key."""
        api_key = os.getenv(self.API_KEY_ENV)
        if not api_key:
            raise Exception(f"Missing API key for {self.__class__.__name__}")
        self.api_key = api_key

    @abstractmethod
    def get_response(self, prompt: str, system_prompt: str) -> str:
        """Send a request to the AI and return the response."""
        pass
