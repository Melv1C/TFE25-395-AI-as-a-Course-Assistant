from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class AIEnum(str, Enum):
    """AI types enumeration."""
    gemini = "gemini"
    openai = "openai"

class RequestModel(BaseModel):
    """Represents the request model for the API."""
    ai: AIEnum
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
    timestamp: str


class DataModel(RequestModel):
    """Represents the main data model stored in the database."""
    id: Optional[str] = None
    discussion: List[DiscussionItem] = []
    is_useful: Optional[bool] = None

    @classmethod
    def from_mongo(cls, data: Dict[str, Any]) -> 'DataModel':
        """Converts MongoDB document to a DataModel instance."""
        data['id'] = str(data['_id'])
        del data['_id']
        return cls(**data)

    