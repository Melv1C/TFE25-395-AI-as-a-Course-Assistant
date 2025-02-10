from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel

class AIEnum(str, Enum):
    """AI types enumeration."""
    gemini = "gemini"
    openai = "openai"

class RequestModel(BaseModel):
    """Represents the request model for the API."""
    question: str
    student_input: str
    custom_prompt: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ResponseModel(BaseModel):
    """Represents the response model for the API."""
    success: bool
    message: str
    id: Optional[str] = None