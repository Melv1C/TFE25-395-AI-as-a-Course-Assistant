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
from global_types import DataModel, DiscussionItem, RequestModel

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
    try:
        parsed_data = DataModel(**data.model_dump())
        inserted_data = collection.insert_one(parsed_data.model_dump())
        print(f"[INFO] Data saved with ID: {inserted_data.inserted_id}")
        return str(inserted_data.inserted_id)
    except PyMongoError as e:
        print(f"[ERROR] Failed to save data: {e}")
    except ValueError as e:
        print(f"[ERROR] Invalid data format: {e}")
    return None

def get_data_by_id(data_id: str) -> Optional[DataModel]:
    """Retrieves data by ID from the database."""
    try:
        data = collection.find_one({"_id": ObjectId(data_id)})
        return DataModel.from_mongo(data) if data else None
    except PyMongoError as e:
        print(f"[ERROR] Failed to retrieve data by ID: {e}")
    return None

def add_discussion_item(data_id: str, discussion_item: Dict[str, Any]) -> bool:
    """Adds a discussion item to an existing data entry."""
    try:
        discussion_item['timestamp'] = datetime.now()
        parsed_item = DiscussionItem(**discussion_item)
        result = collection.update_one(
            {"_id": ObjectId(data_id)},
            {"$push": {"discussion": parsed_item.model_dump()}}
        )
        return result.modified_count > 0
    except PyMongoError as e:
        print(f"[ERROR] Failed to add discussion item: {e}")
    except ValueError as e:
        print(f"[ERROR] Invalid discussion item format: {e}")
    return False

def update_usefulness(data_id: str, is_useful: bool) -> bool:
    """Updates the usefulness rating of a feedback entry."""
    try:
        result = collection.update_one(
            {"_id": ObjectId(data_id)},
            {"$set": {"is_useful": is_useful}}
        )
        return result.modified_count > 0
    except PyMongoError as e:
        print(f"[ERROR] Failed to update feedback usefulness: {e}")
    return False

def get_all_data() -> List[DataModel]:
    """Retrieves all stored data from the database."""
    try:
        data = collection.find()
        return [DataModel.from_mongo(item) for item in data]
    except PyMongoError as e:
        print(f"[ERROR] Failed to retrieve all data: {e}")
    return []

def delete_all_data() -> bool:
    """Deletes all stored data from the database."""
    try:
        result = collection.delete_many({})
        return result.deleted_count > 0
    except PyMongoError as e:
        print(f"[ERROR] Failed to delete all data: {e}")
    return False
