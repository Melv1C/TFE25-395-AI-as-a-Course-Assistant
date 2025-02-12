""" Main application file for the AI Course Assistant API. """
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import ValidationError

from global_types import ResponseModel, BaseDataModel, BaseSubmission
from database import (
    save_data, get_data_by_id, add_submission
)
from ai_manager import AIManager

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

ai_manager = AIManager()

@app.route('/', methods=['GET'])
def home():
    """Returns a welcome message."""
    return jsonify(ResponseModel(message="Welcome to the AI Course Assistant API").model_dump())

@app.route('/ais', methods=['GET'])
def ais():
    """Returns a list of available AI models."""
    return jsonify(ResponseModel(message="Success", data=ai_manager.get_available_ais()).model_dump())

@app.route('/', methods=['POST'])
def save_data_route():
    """Handles data request."""
    if not request.is_json:
        return jsonify(ResponseModel(message="Request must have a JSON body").model_dump()), 400

    if not check_access_token(request.headers):
        return jsonify(ResponseModel(message="Unauthorized").model_dump()), 401

    if not request.json.get('data') or not request.json.get('submission'):
        return jsonify(ResponseModel(message="Request must have 'data' and 'submission' keys").model_dump()), 400
    try:
        data = BaseDataModel(**request.json.get('data'))
        
        available_ais = ai_manager.get_available_ais()
        if data.ai_model not in available_ais:
            return jsonify(ResponseModel(message=f"Model {data.ai_model} is not available").model_dump()), 400

        data_id = save_data(data)
        submission_id = add_submission(data_id, BaseSubmission(**request.json.get('submission')))
        return jsonify(ResponseModel(message="Data saved", data={"data_id": data_id, "submission_id": submission_id}).model_dump()), 201
    except ValidationError as e:
        return jsonify(ResponseModel(message=f"Invalid request: {e}").model_dump()), 400
    except PyMongoError as e:
        return jsonify(ResponseModel(message=f"Failed to save data: {e}").model_dump()), 500
    except Exception as e:
        return jsonify(ResponseModel(message=f"Internal server error: {e}").model_dump()), 500
    
@app.route('/<data_id>/submissions', methods=['POST'])
def add_submission_route(data_id):
    """Handles submission request."""
    if not request.is_json:
        return jsonify(ResponseModel(message="Request must have a JSON body").model_dump()), 400

    if not check_access_token(request.headers):
        return jsonify(ResponseModel(message="Unauthorized").model_dump()), 401

    try:
        submission_id = add_submission(data_id, BaseSubmission(**request.json))
        return jsonify(ResponseModel(message="Submission added", data={"data_id": data_id, "submission_id": submission_id}).model_dump()), 201
    except ValidationError as e:
        return jsonify(ResponseModel(message=f"Invalid request: {e}").model_dump()), 400
    except PyMongoError as e:
        return jsonify(ResponseModel(message=f"Failed to add submission: {e}").model_dump()), 500
    except Exception as e:
        return jsonify(ResponseModel(message=f"Internal server error: {e}").model_dump()), 500
    
@app.route('/<data_id>/submissions/<submission_id>', methods=['GET'])
def get_submission(data_id, submission_id):
    """Retrieves a submission by ID."""
    try:
        data = get_data_by_id(data_id)
        if data is None:
            return jsonify(ResponseModel(message="Data not found").model_dump()), 404

        submission = next(
            (item for item in data.submissions if str(item.id) == submission_id),
            None
        )

        if submission is None:
            return jsonify(ResponseModel(message="Submission not found").model_dump()), 404
        
        return jsonify(ResponseModel(message="Success", data={
            "submission": submission.model_dump(),
            "current_nb_of_feedbacks": len([sub for sub in data.submissions if sub.feedback is not None]),
            "max_nb_of_feedbacks": data.max_nb_of_feedbacks
        }).model_dump())
    except Exception as e:
        return jsonify(ResponseModel(message=f"Internal server error: {e}").model_dump()), 500
    
@app.route('/<data_id>/submissions/<submission_id>/feedback', methods=['GET'])
def get_feedback(data_id, submission_id):
    """Retrieves feedback for a submission by ID."""
    try:
        data = get_data_by_id(data_id)
        if data is None:
            return jsonify(ResponseModel(message="Data not found").model_dump()), 404

        submission = next(
            (item for item in data.submissions if str(item.id) == submission_id),
            None
        )

        if submission is None:
            return jsonify(ResponseModel(message="Submission not found").model_dump()), 404

        if submission.feedback is not None:
            return jsonify(ResponseModel(message="Feedback already exists", data=submission.feedback).model_dump()), 200
        
        if len([sub for sub in data.submissions if sub.feedback is not None]) >= data.max_nb_of_feedbacks:
            return jsonify(ResponseModel(message="Maximum number of feedbacks reached").model_dump()), 400

        ai_response = ai_manager.get_ai_response(data, submission)

        return jsonify(ResponseModel(message="Success", data=ai_response).model_dump())
    except Exception as e:
        return jsonify(ResponseModel(message=f"Internal server error: {e}").model_dump()), 500
    

if __name__ == "__main__":
    app.run(port=PORT, debug=True, host='0.0.0.0')
    print(f"Server running on port {PORT}")
