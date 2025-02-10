"""Database module for AI Course Assistant.

This module provides database interaction functions using MongoDB for storing and retrieving
AI-generated feedback and discussions.
"""

import os
from datetime import datetime
from typing import List, Optional, Dict, Any

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from global_types import DataModel, DataWithouIDModel, DiscussionItem, RequestModel

# Load environment variables
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.getenv('MONGO_DB', 'ai_course_assistant')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'data')

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def save_data(data: RequestModel) -> Optional[str]:
    """Saves data to the database and returns the inserted ID."""
    parsed_data = DataWithouIDModel(**data.model_dump())
    inserted_data = collection.insert_one(parsed_data.model_dump())
    return str(inserted_data.inserted_id)

def get_data_by_id(data_id: str) -> Optional[DataModel]:
    """Retrieves data by ID from the database."""
    try:
        data = collection.find_one({"_id": ObjectId(data_id)})
        return DataModel.from_mongo(data) if data else None
    except PyMongoError as e:
        return None


def add_discussion_item(data_id: str, discussion_item: Dict[str, Any]) -> bool:
    """Adds a discussion item to an existing data entry."""
    discussion_item['timestamp'] = datetime.now()
    parsed_item = DiscussionItem(**discussion_item)
    result = collection.update_one(
        {"_id": ObjectId(data_id)},
        {"$push": {"discussion": parsed_item.model_dump()}}
    )
    return result.modified_count > 0
