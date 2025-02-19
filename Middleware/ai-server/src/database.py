"""Database module for AI Course Assistant.

This module provides database interaction functions using MongoDB for storing and retrieving
AI-generated feedback and discussions.
"""

import os

from pymongo import MongoClient
from bson import ObjectId
from global_types import DataModel, BaseDataModel, Submission, BaseSubmission, Feedback

# Load environment variables
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.getenv('MONGO_DB', 'ai_course_assistant')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'data')

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def save_data(data: BaseDataModel) -> str:
    """Saves data to the database and returns the inserted ID."""
    parsed_data = DataModel(
        id=str(ObjectId()),
        **data.model_dump(),
    )
    collection.insert_one(parsed_data.model_dump())
    return parsed_data.id

def get_data_by_id(data_id: str) -> DataModel:
    """Retrieves data from the database by ID."""
    data = collection.find_one({"id": data_id})
    if data is None:
        raise Exception(f"Data with ID {data_id} not found.")
    return DataModel(**data)

def add_submission(data_id: str, submission: BaseSubmission) -> str:
    """Adds a submission to the data by ID and returns the inserted ID."""
    parsed_submission = Submission(
        id=str(ObjectId()),
        **submission.model_dump(),
    )

    collection.update_one(
        {"id": data_id},
        {"$push": {"submissions": parsed_submission.model_dump()}}
    )
    return parsed_submission.id

def add_feedback(data_id: str, submission_id: str, feedback: Feedback):
    """Adds feedback to a submission by ID and returns the inserted ID."""
    collection.update_one(
        {"id": data_id, "submissions.id": submission_id},
        {"$set": {"submissions.$.feedback": feedback.model_dump()}}
    )

def get_all_data() -> list[DataModel]:
    """Retrieves all data from the database."""
    return [DataModel(**data) for data in collection.find()]

