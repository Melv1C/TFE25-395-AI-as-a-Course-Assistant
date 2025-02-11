import os
from abc import ABC, abstractmethod

class AbstractAIModel(ABC):
    """Abstract base class for AI backends."""

    API_KEY_ENV: str = ""  # To be set in subclasses

    def __init__(self):
        """Initialize the AI backend with the API key."""
        api_key = os.getenv(self.API_KEY_ENV)
        if not api_key:
            raise ValueError(f"Missing API key for {self.__class__.__name__}")
        self.api_key = api_key  # Store API key for requests

    @abstractmethod
    def get_response(self, prompt: str, system_prompt: str) -> str:
        """Send a request to the AI and return the response."""
        pass
