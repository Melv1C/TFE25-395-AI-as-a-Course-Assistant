import requests

class AICourseAssistant:
    server_url = None
    access_token = None

    @classmethod
    def init(cls, url, token):
        cls.server_url = url
        cls.access_token = token

    @classmethod
    def _check_initialized(cls):
        if not cls.server_url or not cls.access_token:
            raise ValueError("Server URL and access token must be set before using the assistant.")

    def __init__(self, question, student_input):
        AICourseAssistant._check_initialized()
        self.question = question
        self.student_input = student_input
        self.grade = None
        self.solution = None
        self.output = None

    def add_grade(self, grade):
        self.grade = grade

    def add_solution(self, solution):
        self.solution = solution

    def add_output(self, output):
        self.output = output


    def ask_feedback(self):
        AICourseAssistant._check_initialized()
        data = {
            'question': self.question,
            'student_input': self.student_input,
            'grade': self.grade,
            'solution': self.solution,
            'output': self.output
        }
        headers = {
            'Authorization': f'Bearer {AICourseAssistant.access_token}'
        }
        try:
            response = requests.post(AICourseAssistant.server_url, json=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return f"HTTP error: {e}",
        except requests.exceptions.RequestException as e:
            return f"Request error: {e}",
        
        return response.json()["feedback"]
