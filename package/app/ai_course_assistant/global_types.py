from typing import Any, Dict, Optional
from pydantic import BaseModel

class ResponseDataModel(BaseModel):
    """Represents the response data model for the API."""
    data_id: str
    submission_id: str

class ResponseModel(BaseModel):
    """Represents the response model for the API."""
    message: str
    data: Optional[ResponseDataModel] = None

class BaseSubmission(BaseModel):
    """Represents the base submission in the database."""
    student_input: str
    prompt: Optional[str] = None
    metadata: Dict[str, Any] = {}

class BaseDataModel(BaseModel):
    """Represents the base data model for the API."""
    ai_model: str
    question: str
    max_nb_of_feedbacks: Optional[int] = None
    system_prompt: Optional[str] = None
    metadata: Dict[str, Any] = {}
