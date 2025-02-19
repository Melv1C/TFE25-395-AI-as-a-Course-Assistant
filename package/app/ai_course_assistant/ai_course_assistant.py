import requests
from .global_types import BaseDataModel, BaseSubmission, ResponseDataModel, ResponseModel

class AICourseAssistant:
    @classmethod
    def server(cls, url: str, access_token: str = None):
        """Initializes the server."""
        cls.url = url
        cls.access_token = access_token

    @classmethod
    def _check_server(cls):
        """Checks if the server is initialized."""
        if not hasattr(cls, 'url'):
            raise Exception("The server has not been initialized.")
        
    @classmethod
    def from_data_id(cls, data_id: str) -> 'AICourseAssistant':
        """Initializes the AI course assistant from the data ID."""
        cls._check_server()
        assistant = cls()
        assistant._set_data_id(data_id)
        return assistant

    def __init__(self, data: BaseDataModel = None):
        """Initializes the AI course assistant."""
        self._check_server()
        if data is not None:
            self.data = BaseDataModel(**data.model_dump())

    def _set_data_id(self, data_id: str):
        """Sets the data ID."""
        if self.data is not None:
            raise Exception("The instance cannot have both data and data ID.")
        self.data_id = data_id

    def _has_data_id(self):
        """Checks if the data ID is set."""
        return hasattr(self, 'data_id')

    def set_data(self, data: BaseDataModel):
        """Sets the data."""
        if self._has_data_id():
            raise Exception("The instance cannot have both data and data ID.")
        self.data = BaseDataModel(**data.model_dump())

    def set_ai_model(self, ai_model: str):
        """Sets the AI model."""
        if self._has_data_id():
            raise Exception("The instance cannot have both data and data ID.")
        if not hasattr(self, 'data'):
            self.data = BaseDataModel(ai_model=ai_model, question="")
        else:
            self.data.ai_model = ai_model

    def set_question(self, question: str):
        """Sets the question."""
        if not hasattr(self, 'data'):
            raise Exception("The data has not been set yet. Please set the data or AI model first.")
        self.data.question = question

    def set_max_nb_of_feedbacks(self, max_nb_of_feedbacks: int):
        """Sets the maximum number of feedbacks."""
        if not hasattr(self, 'data'):
            raise Exception("The data has not been set yet. Please set the data or AI model first.")
        self.data.max_nb_of_feedbacks = max_nb_of_feedbacks

    def set_system_prompt(self, system_prompt: str):
        """Sets the system prompt."""
        if not hasattr(self, 'data'):
            raise Exception("The data has not been set yet. Please set the data or AI model first.")
        self.data.system_prompt = system_prompt

    def set_metadata(self, metadata: dict):
        """Sets the metadata."""
        if not hasattr(self, 'data'):
            raise Exception("The data has not been set yet. Please set the data or AI model first.")
        self.data.metadata = metadata

    def set_submission_data(self, submission: BaseSubmission):
        """Sets the submission."""
        self.submission = BaseSubmission(**submission.model_dump())

    def set_student_input(self, student_input: str):
        """Sets the student input."""
        if not hasattr(self, 'submission'):
            self.submission = BaseSubmission(student_input=student_input)
        else:
            self.submission.student_input = student_input

    def set_student_prompt(self, prompt: str):
        """Sets the student prompt."""
        if not hasattr(self, 'submission'):
            raise Exception("The submission has not been set yet. Please set the submission data or student input first.")
        self.submission.prompt = prompt

    def set_submission_metadata(self, metadata: dict):
        """Sets the submission metadata."""
        if not hasattr(self, 'submission'):
            raise Exception("The submission has not been set yet. Please set the submission data or student input first.")
        self.submission.metadata = metadata

    def _send_data(self, timeout: int):
        """Sends the data to the server."""

        if not hasattr(self, 'data'):
            raise Exception("The data has not been set.")

        headers = {'Authorization': f'Bearer {self.access_token}'} if self.access_token else {}
        response = requests.post(
            f'{self.url}/', 
            json={'data': self.data.model_dump(exclude_none=True), 'submission': self.submission.model_dump(exclude_none=True)}, 
            headers=headers,
            timeout=timeout
        )
        return ResponseModel(**response.json())

    def _send_submission(self, timeout: int):
        """Sends the submission to the server."""
        headers = {'Authorization': f'Bearer {self.access_token}'} if self.access_token else {}
        response = requests.post(
            f'{self.url}/{self.data_id}/submissions', 
            json=self.submission.model_dump(exclude_none=True), 
            headers=headers,
            timeout=timeout
        )
        return ResponseModel(**response.json())
        
    def send(self, timeout: int = 5) -> ResponseDataModel:
        """Sends the data and submission to the server."""
        self._check_server()
        if not hasattr(self, 'submission'):
            raise Exception("The submission has not been set.")
        
        try:
            if self._has_data_id():
                res = self._send_submission(timeout)
            else:
                res = self._send_data(timeout)

            if res.data is None:
                raise Exception(f"Data not found in response: {res.message}")
            
            self.res = ResponseDataModel(**res.data.model_dump())
            return self.res
        except requests.exceptions.Timeout:
            raise Exception("The request timed out.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred while sending the request: {e}")
            
    def feedback_url(self):
        """Returns the feedback URL."""
        if not hasattr(self, 'res'):
            raise Exception("The response has not been set.")
        return f'{self.url}/{self.res.data_id}/submissions/{self.res.submission_id}'

