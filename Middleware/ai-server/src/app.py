""" Main application file for the AI Course Assistant API. """
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import ValidationError

from global_types import RequestModel, RoleEnum, ResponseModel
from database import (
    save_data, get_data_by_id
)
from ai_handler import get_response_by_ai

from pymongo.errors import PyMongoError

PORT = int(os.getenv('PORT', '5000'))
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', None)

def check_access_token(request_headers):
    """Checks if the request has a valid access token."""
    if ACCESS_TOKEN is None:
        return True
    token = request_headers.get('Authorization')
    if not token or token != f'Bearer {ACCESS_TOKEN}':
        return False
    return True

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    """Returns a welcome message."""
    return jsonify(ResponseModel(message="Welcome to the AI Course Assistant API").model_dump())


@app.route('/feedbacks', methods=['POST'])
def save_feedback_data():
    """Handles feedback request."""
    if not request.is_json:
        return jsonify(ResponseModel(message="Request must have a JSON body").model_dump()), 400

    if not check_access_token(request.headers):
        return jsonify(ResponseModel(message="Unauthorized").model_dump()), 401

    try:
        data = RequestModel(**request.json)
        data_id = save_data(data)
        return jsonify(ResponseModel(message="Feedback data saved", data=data_id).model_dump()), 201
    except ValidationError as e:
        return jsonify(ResponseModel(message=f"Invalid request: {e}").model_dump()), 400
    except PyMongoError as e:
        return jsonify(ResponseModel(message=f"Failed to save data: {e}").model_dump()), 500
    except Exception as e:
        return jsonify(ResponseModel(message=f"Internal server error: {e}").model_dump()), 500

@app.route('/feedbacks/<feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    """Retrieves AI-generated feedback by ID."""
    try:
        data = get_data_by_id(feedback_id)
        if data is None:
            return jsonify(ResponseModel(message="Data not found").model_dump()), 404

        # Check if an 'ai' role response already exists in the discussion
        ai_feedback = next(
            (item.message for item in data.discussion if item.role == RoleEnum.ai),
            None
        )

        if ai_feedback is None:
            return jsonify(ResponseModel(message="AI feedback not found").model_dump()), 404
        
        return jsonify(ResponseModel(message="Success", data=ai_feedback).model_dump())
    except Exception as e:
        return jsonify(ResponseModel(message=f"Internal server error: {e}").model_dump()), 500

@app.route('/feedbacks/<feedback_id>/generate', methods=['POST'])
def generate_feedback(feedback_id):
    """Generates AI feedback for a given feedback ID."""
    try:
        data = get_data_by_id(feedback_id)
        if data is None:
            return jsonify(ResponseModel(message="Data not found").model_dump()), 404

        ai_feedback = get_response_by_ai(data)

        if ai_feedback is None:
            return jsonify(ResponseModel(message="Failed to generate AI feedback").model_dump()), 500
        
        return jsonify(ResponseModel(message="Success", data=ai_feedback).model_dump())
    except Exception as e:
        return jsonify(ResponseModel(message=f"Internal server error: {e}").model_dump()), 500

if __name__ == "__main__":
    app.run(port=PORT, debug=True, host='0.0.0.0')
    print(f"Server running on port {PORT}")
