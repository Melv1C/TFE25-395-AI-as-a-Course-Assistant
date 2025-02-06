

from enum import Enum
from pydantic import BaseModel


class AIEnum(str, Enum):
    """AI types enumeration."""
    gemini = "gemini"
    openai = "openai"
    
class RequestModel(BaseModel):
    """Request model for the API."""
    ai: AIEnum
    question: str
    student_input: str