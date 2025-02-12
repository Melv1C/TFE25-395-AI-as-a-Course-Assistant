from ai_models.base import AbstractAIModel
from ai_models.openai import OpenAIModel
from ai_models.gemini import GeminiAIModel
from ai_models.deepseek import DeepseekAIModel
from ai_models.anthropic import AnthropicAIModel
from ai_models.mistral import MistralAIModel

from global_types import DataModel, Submission, Feedback
from prompts import generate_prompt

from database import add_feedback

class AIManager:
    """Manages available AI backends."""

    AI_CLASSES: dict[str, tuple[type[AbstractAIModel], dict]] = {
        "openai": (OpenAIModel, {}),
        "gemini": (GeminiAIModel, {}),
        "deepseek": (DeepseekAIModel, {}),
        "claude": (AnthropicAIModel, {}),
        "mistral": (MistralAIModel, {}),
    }

    def __init__(self):
        """Initialize available AI backends."""
        self.available_ais = {}
        print("Initializing AI backends...")
        for name, (ai_class, kwargs) in self.AI_CLASSES.items():
            print(f"Initializing {ai_class.__name__}: {name}")
            try:
                self.available_ais[name] = ai_class(**kwargs)
            except Exception as e:
                print(f"Failed to initialize {ai_class.__name__}: {e}")

    def get_available_ais(self) -> list[str]:
        """Return a list of available AI names."""
        return list(self.available_ais.keys())

    def get_ai_instance(self, name: str) -> AbstractAIModel | None:
        """Return an instance of the specified AI backend, if available."""
        return self.available_ais.get(name)
    
    def get_ai_response(self, data: DataModel, submission: Submission) -> str:
        """
        Get the response from the AI model based on the request data.

        Args:
            data (DataModel): The request data.

        Returns:
            str: The AI-generated response.
        """

        ai_instance = self.get_ai_instance(data.ai_model)
        if not ai_instance:
            raise Exception(f"Invalid AI type: {data.ai_model}")

        system_prompt = generate_prompt(data.system_prompt, {
            "question": data.question,
            **data.metadata,
        })
        prompt = generate_prompt(data.prompt, {
            "student_input": submission.student_input,
            **submission.metadata,
        })

        assistant_response = ai_instance.get_response(prompt, system_prompt)

        feedback = Feedback(
            system_prompt=system_prompt,
            prompt=prompt,
            feedback=assistant_response,
        )

        add_feedback(data.id, submission.id, feedback)

        return assistant_response
