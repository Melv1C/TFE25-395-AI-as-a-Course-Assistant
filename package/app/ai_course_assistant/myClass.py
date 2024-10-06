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
        self.previous_input = None

    def add_grade(self, grade):
        self.grade = grade

    def add_solution(self, solution):
        self.solution = solution

    def add_previous_input(self, previous_input):
        self.previous_input = previous_input

    def ask_feedback(self):
        AICourseAssistant._check_initialized()
        data = {
            'question': self.question,
            'student_input': self.student_input,
            'grade': self.grade,
            'solution': self.solution,
            'previous_input': self.previous_input
        }
        headers = {
            'Authorization': f'Bearer {AICourseAssistant.access_token}'
        }
        try:
            response = requests.post(AICourseAssistant.server_url, json=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return e.response.json(), e.response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500
        
        return response.json()["feedback"]
