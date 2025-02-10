import requests
from .global_types import AIEnum, RequestModel, ResponseModel

class AICourseAssistant:
    server_url: str = None
    access_token: str = None
    ai_model: AIEnum = AIEnum.openai

    @classmethod
    def init(cls, url: str, token: str = None):
        cls.server_url = url
        cls.access_token = token

    @classmethod
    def use(cls, ai: AIEnum):
        cls.ai_model = ai

    @classmethod
    def _check_initialized(cls):
        if not cls.server_url:
            raise ValueError("Server URL must be set before using the assistant.")
        
    def __init__(self, question: str, student_input: str):
        AICourseAssistant._check_initialized()
        self.request: RequestModel = RequestModel(question=question, student_input=student_input)

    def add(self, key, value):
        setattr(self.request.metadata, key, value)

    def set_prompt(self, prompt: str):
        self.request.custom_prompt = prompt

    def get_feedback(self, timeout: int = 5):
        AICourseAssistant._check_initialized()
        headers = {
            'Authorization': f'Bearer {AICourseAssistant.access_token}'
        }

        try:
            response = requests.post(
                f"{AICourseAssistant.server_url}/get_feedback", 
                json={**self.request.model_dump(), "ai_model": AICourseAssistant.ai_model}, 
                headers=headers, 
                timeout=timeout
            )
            if response.status_code == 200 or response.status_code == response.json()['code']:
                return ResponseModel(success=True, message=response.json()['message'], id=response.json()['data'])
            else:
                return ResponseModel(success=False, message=f"{response.status_code} - {response.reason}")
        except requests.exceptions.Timeout:
            return ResponseModel(success=False, message="Request timed out.")
        except Exception as e:
            return ResponseModel(success=False, message=str(e))
        
    @staticmethod
    def feedback_url(id: str):
        if AICourseAssistant.server_url is None:
            raise ValueError("Server URL must be set before using the assistant.")
        return f"{AICourseAssistant.server_url}/feedback/{id}"