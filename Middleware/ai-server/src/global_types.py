import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from prompts import DEFAULT_PROMPT, DEFAULT_SYSTEM_PROMPT

DEFAULT_MAX_NB_OF_FEEDBACKS = os.getenv("DEFAULT_MAX_NB_OF_FEEDBACKS", 10)

class ResponseModel(BaseModel):
    """Represents the response model for the API."""
    message: str
    data: Optional[Any] = None
    
class Feedback(BaseModel):
    """Represents a feedback in the database."""
    timestamp: datetime = datetime.now()
    system_prompt: str
    prompt: str
    feedback: str

class BaseSubmission(BaseModel):
    """Represents the base submission in the database."""
    student_input: str
    prompt: str = DEFAULT_PROMPT
    metadata: Dict[str, Any] = {}

class Submission(BaseSubmission):
    """Represents a submission in the database."""
    id: str
    timestamp: datetime = datetime.now()
    feedback: Optional[Feedback] = None

class BaseDataModel(BaseModel):
    """Represents the base data model for the API."""
    ai_model: str
    question: str
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    max_nb_of_feedbacks: int = DEFAULT_MAX_NB_OF_FEEDBACKS
    metadata: Dict[str, Any] = {}

class DataModel(BaseDataModel):
    """Represents the data model for the API."""
    id: str
    submissions: List[Submission] = []