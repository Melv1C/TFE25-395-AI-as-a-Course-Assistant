import yaml

from .ai_course_assistant import AICourseAssistant
from .global_types import ResponseModel
from .html_utils import feedback_block


class AIIngiAssistant(AICourseAssistant):
    
    @staticmethod
    def get_question():
        with open("task.yaml", "r") as f:
            task = yaml.safe_load(f)

        return task["context"]
    
    @staticmethod
    def rst_feedback(res: ResponseModel):
        if not res.success:
            print(res.message)
            return f"A problem occurred while processing your request. Please try again later."
        
        return feedback_block(res.id, AIIngiAssistant.feedback_url(res.id))

