import yaml

from .global_types import BaseDataModel
from .ai_course_assistant import AICourseAssistant
from .html_utils import feedback_block

class AIIngiAssistant(AICourseAssistant):

    @classmethod
    def get_instance(cls, input, feedback, data: BaseDataModel):
        """Initializes the AI assistant."""
        cls._check_server()
        state = input.get_input("@state")
        if state:
            feedback.set_state(state)
            assistant = cls.from_data_id(state)
        else:
            assistant = cls(data)

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
    
    def add_ai_feedback(self, feedback, timeout: int = 5):
        try:
            self.send(timeout)
            if not hasattr(self, 'res'):
                raise Exception("The response has not been set.")
            feedback.set_state(self.res.data_id)
            feedback.set_global_feedback(self._rst_feedback(), True)
        except Exception as e:
            feedback.set_global_feedback("\n\nAn error occurred while requesting feedback from the AI assistant.", True)
            print(e)
    
    def _rst_feedback(self):
        if not hasattr(self, 'res'):
            raise Exception("The response has not been set.")
        return feedback_block(self.res.submission_id, self.feedback_url())

