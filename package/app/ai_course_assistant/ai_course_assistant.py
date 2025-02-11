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
            raise ValueError("The server has not been initialized.")
        
    @classmethod
    def from_data_id(cls, data_id: int):
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

    def _set_data_id(self, data_id: int):
        """Sets the data ID."""
        self.data_id = data_id

    def set_submission(self, submission: BaseSubmission):
        """Sets the submission."""
        self.submission = BaseSubmission(**submission.model_dump())

    def _send_data(self, timeout: int):
        """Sends the data to the server."""

        if not hasattr(self, 'data'):
            raise ValueError("The data has not been set.")

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
            raise ValueError("The submission has not been set.")
        
        try:
            if hasattr(self, 'data_id'):
                res = self._send_submission(timeout)
            else:
                res = self._send_data(timeout)

            if res.data is None:
                raise ValueError(f"Data not found in response: {res.message}")
            
            return ResponseDataModel(**res.data.model_dump())
        except requests.exceptions.Timeout:
            raise TimeoutError("The request timed out.")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to send data: {e}")
            
    def feedback_url(self, res: ResponseDataModel):
        """Returns the feedback URL."""
        data_id = self.data_id if hasattr(self, 'data_id') else res.data_id
        return f'{self.url}/{data_id}/submissions/{res.submission_id}'

