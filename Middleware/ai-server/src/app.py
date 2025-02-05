""" Main application file for the AI Course Assistant API. """
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from ai.open_ai import get_response
from database import (
    save_data, get_data_by_id, add_discussion_item,
    get_all_data, delete_all_data, update_usefulness
)
from ai.prompts import generate_prompt

def info(message):
    """Logs an info message to the console."""
    print(f"[INFO] {message}")

def error(message):
    """Logs an error message to the console."""
    print(f"[ERROR] {message}")

PORT = int(os.getenv('PORT', '5000'))
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', None)

# pylint: disable=too-few-public-methods
class MyResponse:
    """Represents a standardized response format for the API."""

    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data

    def json(self):
        """Returns the response as a JSON object."""
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }

# pylint: disable=too-few-public-methods
class RequestParser:
    """Parses and validates the request body for the API."""

    def __init__(self, data):
        self.data = data
        self.question = data.get('question')
        self.student_input = data.get('student_input')

    def is_valid(self):
        """Checks if the request body is valid."""
        return bool(self.question and self.student_input)

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
    res = MyResponse(200, "Welcome to the AI Course Assistant API!")
    return jsonify(res.json())

@app.route('/database', methods=['GET'])
def get_database():
    """Retrieves all stored data."""
    data = get_all_data()
    res = MyResponse(200, "Success", data)
    return jsonify(res.json())

@app.route('/database', methods=['DELETE'])
def delete_database():
    """Deletes all stored data (requires authorization)."""
    if not check_access_token(request.headers):
        error("Unauthorized access")
        return jsonify(MyResponse(401, "Unauthorized access").json()), 401

    if delete_all_data():
        res = MyResponse(200, "Success")
        return jsonify(res.json())

    res = MyResponse(500, "Failed to delete data")
    return jsonify(res.json()), 500

@app.route('/getFeedbackAsync', methods=['POST'])
def get_feedback_async():
    """Handles asynchronous feedback request."""
    if not request.is_json:
        return jsonify(MyResponse(400, "Request must have a JSON body").json()), 400

    data = request.json
    info(f"Received request with data: {data}")

    if not check_access_token(request.headers):
        error("Unauthorized access")
        return jsonify(MyResponse(401, "Unauthorized access").json()), 401

    parser = RequestParser(data)

    if not parser.is_valid():
        error("Missing question or student input")
        return jsonify(MyResponse(400, "Missing question or student input").json()), 400

    # Save data to the database
    data_id = save_data(parser.data)

    res = MyResponse(200, "Success", data_id)
    return jsonify(res.json())

@app.route('/getFeedbackAsync/<feedback_id>', methods=['GET'])
def get_feedback_async_by_id(feedback_id):
    """Retrieves AI-generated feedback by ID."""
    data = get_data_by_id(feedback_id)
    if data is None:
        res = MyResponse(404, "Data not found")
        return jsonify(res.json()), 404

    # Check if an 'ai' role response already exists in the discussion
    ai_feedback = next(
        (item['message'] for item in data['discussion'] if item['role'] == 'ai'),
        None
    )

    if ai_feedback:
        # Directly return the existing AI feedback
        res = MyResponse(200, "Success", ai_feedback)
        return jsonify(res.json())

    prompt = generate_prompt(data)
    add_discussion_item(feedback_id, {"role": "teacher", "message": prompt})

    chatbot_response = get_response(prompt)
    add_discussion_item(feedback_id, {"role": "ai", "message": chatbot_response})

    res = MyResponse(200, "Success", chatbot_response)
    return jsonify(res.json())

@app.route('/getFeedbackAsync/<feedback_id>', methods=['POST'])
def update_feedback_usefulness(feedback_id):
    """Updates the usefulness rating of feedback."""
    if not request.is_json:
        return jsonify(MyResponse(400, "Request must have a JSON body").json()), 400

    data = request.json
    info(f"Received request with data: {data}")

    is_useful = data.get('useful')
    if is_useful is None:
        error("Missing 'useful' field in request body")
        return jsonify(MyResponse(400, "Missing 'useful' field in request body").json()), 400

    feedback_data = get_data_by_id(feedback_id)
    if feedback_data is None:
        res = MyResponse(404, "Data not found")

        return jsonify(res.json()), 404

    # Update the usefulness of the feedback
    if not update_usefulness(feedback_id, is_useful):
        res = MyResponse(500, "Failed to update feedback usefulness")
        return jsonify(res.json()), 500

    res = MyResponse(200, "Success")
    return jsonify(res.json())

@app.route('/getFeedbackSync', methods=['POST'])
def get_feedback_sync():
    """Handles synchronous feedback request."""
    if not request.is_json:
        return jsonify(MyResponse(400, "Request must have a JSON body").json()), 400

    data = request.json
    info(f"Received request with data: {data}")

    if not check_access_token(request.headers):
        error("Unauthorized access")
        return jsonify(MyResponse(401, "Unauthorized access").json()), 401

    parser = RequestParser(data)

    if not parser.is_valid():
        error("Missing question or student input")
        return jsonify(MyResponse(400, "Missing question or student input").json()), 400

    # Save data to the database
    data_id = save_data(parser.data)

    data = get_data_by_id(data_id)
    if data is None:
        res = MyResponse(404, "Data not found")
        return jsonify(res.json()), 404

    prompt = generate_prompt(data)
    add_discussion_item(data_id, {"role": "teacher", "message": prompt})

    chatbot_response = get_response(prompt)
    add_discussion_item(data_id, {"role": "ai", "message": chatbot_response})

    res = MyResponse(200, "Success", chatbot_response)
    return jsonify(res.json())

if __name__ == "__main__":
    app.run(port=PORT, debug=True, host='0.0.0.0')
    info(f"Server running on port {PORT}")
