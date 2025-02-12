import yaml

from .global_types import BaseDataModel, BaseSubmission
from .ai_course_assistant import AICourseAssistant
from .html_utils import feedback_block

class AIIngiAssistant(AICourseAssistant):

    @classmethod
    def get(cls, state: str, data: BaseDataModel, submission: BaseSubmission) -> 'AIIngiAssistant':
        """Initializes the AI assistant."""
        cls._check_server()
        if state:
            assistant = cls.from_data_id(state)
        else:
            assistant = cls(data)

        assistant.set_submission(submission)
        return assistant

    @staticmethod
    def get_context() -> str:
        with open("task.yaml", "r") as f:
            task = yaml.safe_load(f)
        return task["context"]
    
    @staticmethod
    def get_problem_header(problem_id: str) -> str:
        with open("task.yaml", "r") as f:
            task = yaml.safe_load(f)
        return task["problems"][problem_id]["header"]
    
    def add_ai_feedback(self, feedback, save_state: bool = True, timeout: int = 5):
        try:
            self.send(timeout)
            if save_state:
                feedback.set_state(self.res.data_id)
            feedback.set_global_feedback(self.rst_feedback(self.res), True)
        except Exception as e:
            feedback.set_global_feedback("An error occurred while requesting feedback from the AI assistant.", True)
            print(e)
    
    def _rst_feedback(self):
        if not hasattr(self, 'res'):
            raise ValueError("The response has not been set.")
        return feedback_block(self.res.submission_id, self.feedback_url(self.res))

