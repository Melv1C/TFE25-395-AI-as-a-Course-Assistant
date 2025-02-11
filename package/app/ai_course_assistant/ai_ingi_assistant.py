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
    def rst_feedback(res: ResponseDataModel):
        return feedback_block(res.submission_id, AIIngiAssistant.feedback_url(res))

