import os
from pymongo import MongoClient
from bson import ObjectId

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.getenv('MONGO_DB', 'ai_course_assistant')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'data')

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

class DiscussionItem(BaseModel):
    role: str
    message: str
    timestamp: datetime

class DataModel(BaseModel):
    id: Optional[str] = None
    question: str
    student_input: str
    custom_prompt: Optional[str] = None
    model: str = "gpt-4o-mini"
    metadata: Optional[Dict[str, Any]] = None
    discussion: List[DiscussionItem] = []

    @classmethod
    def from_mongo(cls, data: Dict[str, Any]) -> 'DataModel':
        data['id'] = str(data['_id'])
        del data['_id']
        return cls(**data)

# Save data to the database
def save_data(data: Dict[str, Any]) -> Optional[str]:
    try:
        parsed_data = DataModel(**data)
        inserted_data = collection.insert_one(parsed_data.model_dump())
        return str(inserted_data.inserted_id)
    except Exception as e:
        print(e)
        return None

# Get data from the database by submission_id
def get_data_by_id(id: str) -> DataModel:
    data = collection.find_one({"_id": ObjectId(id)})
    return DataModel.from_mongo(data).model_dump() if data else None

# Add a discussion item to the data
def add_discussion_item(id: str, discussion_item: Dict[str, Any]) -> bool:
    discussion_item['timestamp'] = datetime.now()
    parsed_item = DiscussionItem(**discussion_item)
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$push": {"discussion": parsed_item.model_dump()}}
    )
    return result.modified_count > 0

# get all data from the database
def get_all_data() -> List[DataModel]:
    data = collection.find()
    return [DataModel.from_mongo(item).model_dump() for item in data]

# delete all data from the database
def delete_all_data() -> bool:
    result = collection.delete_many({})
    return result.deleted_count > 0
