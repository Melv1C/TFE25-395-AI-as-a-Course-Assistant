from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class ResponseModel(BaseModel):
    """Represents the response model for the API."""
    message: str
    data: Optional[Any] = None

class AIEnum(str, Enum):
    """AI types enumeration."""
    gemini = "gemini"
    openai = "openai"

class RequestModel(BaseModel):
    """Represents the request model for the API."""
    model_ai: AIEnum
    question: str
    student_input: str
    custom_prompt: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class RoleEnum(str, Enum):
    """Role types enumeration."""
    system = "system"
    ai = "ai"
    student = "student"

class DiscussionItem(BaseModel):
    """Represents a discussion entry in the database."""
    role: RoleEnum
    message: str
    timestamp: datetime

class DataModel(RequestModel):
    """Represents the main data model stored in the database."""
    id: str
    discussion: List[DiscussionItem] = []

    @classmethod
    def from_mongo(cls, data: Dict[str, Any]) -> 'DataModel':
        """Converts MongoDB document to a DataModel instance."""
        data['id'] = str(data['_id'])
        del data['_id']
        return cls(**data)

class DataWithouIDModel(RequestModel):
    """Represents the main data model stored in the database without ID."""
    discussion: List[DiscussionItem] = []
    