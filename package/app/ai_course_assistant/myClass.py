import signal
import requests
from .myResponse import MyResponse

class AICourseAssistant:
    server_url = None
    access_token = None

    @classmethod
    def init(cls, url, token=None):
        cls.server_url = url
        cls.access_token = token

    @classmethod
    def _check_initialized(cls):
        if not cls.server_url:
            raise ValueError("Server URL must be set before using the assistant.")

    def __init__(self, question, student_input):
        AICourseAssistant._check_initialized()
        self.data = {
            'question': question,
            'student_input': student_input
        }

    def add(self, key, value):
        self.data[key] = value

    def ask_feedback(self, timeout=5):
        AICourseAssistant._check_initialized()
        headers = {
            'Authorization': f'Bearer {AICourseAssistant.access_token}'
        }
        try:
            response = requests.post(AICourseAssistant.server_url, json=self.data, headers=headers, timeout=timeout)
            if response.status_code == 200 or response.status_code == response.json()['code']:
                return MyResponse.parse(response.json())
            else:
                return MyResponse(False, f"{response.status_code} - {response.reason}")
        except requests.exceptions.Timeout:
            return MyResponse(False, "Request timed out.")
        except Exception as e:
            return MyResponse(False, "Unknown error: " + str(e)) 
        
