import yaml
from .ai_course_assistant import AICourseAssistant
from .global_types import ResponseDataModel
from .html_utils import feedback_block

class AIIngiAssistant(AICourseAssistant):
    
    @staticmethod
    def get_context():
        with open("task.yaml", "r") as f:
            task = yaml.safe_load(f)
        return task["context"]
    
    @staticmethod
    def get_problem_header(problem_id: str):
        with open("task.yaml", "r") as f:
            task = yaml.safe_load(f)
        return task["problems"][problem_id]["header"]
    
    def rst_feedback(self, res: ResponseDataModel):
        return feedback_block(res.submission_id, self.feedback_url(res))

