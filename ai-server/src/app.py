import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from AI.OpenAI import get_response
from database import save_data, get_data_by_id, add_discussion_item, get_all_data, delete_all_data
from prompts import generate_prompt

def INFO(message):
    print(f"[INFO] {message}")

def ERROR(message):
    print(f"[ERROR] {message}")

PORT = os.getenv('PORT', 5000)
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', None)

class MyResponse:
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data
    
    def json(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }

app = Flask(__name__)
CORS(app)

class RequestParser:
    def __init__(self, data):
        self.data = data
        self.question = data.get('question')
        self.student_input = data.get('student_input')
    
    def is_valid(self):
        return bool(self.question and self.student_input)
    
def check_access_token(request):
    if ACCESS_TOKEN is None:
        return True
    token = request.headers.get('Authorization')
    if not token or token != f'Bearer {ACCESS_TOKEN}':
        return False
    return True



@app.route('/', methods=['GET'])
def home():
    res = MyResponse(200, "Welcome to the AI Course Assistant API!")
    return jsonify(res.json())

@app.route('/database', methods=['GET'])
def get_database():
    data = get_all_data()
    res = MyResponse(200, "Success", data)
    return jsonify(res.json())

@app.route('/database', methods=['DELETE'])
def delete_database():
    if not check_access_token(request):
        ERROR("Unauthorized access")
        return jsonify(MyResponse(401, "Unauthorized access").json()), 401
    
    if delete_all_data():
        res = MyResponse(200, "Success")
        return jsonify(res.json())
    else:
        res = MyResponse(500, "Failed to delete data")
        return jsonify(res.json()), 500

@app.route('/getFeedbackAsync', methods=['POST'])
def get_feedback_async():
    if not request.is_json:
        return jsonify(MyResponse(400, "Request must have a JSON body").json()), 400
    
    data = request.json
    INFO(f"Received request with data: {data}")

    if not check_access_token(request):
        ERROR("Unauthorized access")
        return jsonify(MyResponse(401, "Unauthorized access").json()), 401

    parser = RequestParser(data)
    
    if not parser.is_valid():
        ERROR("Missing question or student input")
        return jsonify(MyResponse(400, "Missing question or student input").json()), 400
    
    # Save data to the database
    data_id = save_data(parser.data)
    
    res = MyResponse(200, "Success", data_id)
    return jsonify(res.json())

@app.route('/getFeedbackAsync/<id>', methods=['GET'])
def get_feedback_async_by_id(id):
    data = get_data_by_id(id)
    if data is None:
        res = MyResponse(404, "Data not found")
        return jsonify(res.json()), 404
    
    prompt = generate_prompt(data)
    add_discussion_item(id, {"role": "teacher", "message": prompt})

    chatbot_response = get_response(prompt)
    add_discussion_item(id, {"role": "ai", "message": chatbot_response})

    res = MyResponse(200, "Success", chatbot_response)
    return jsonify(res.json())

@app.route('/getFeedbackSync', methods=['POST'])
def get_feedback_sync():
    if not request.is_json:
        return jsonify(MyResponse(400, "Request must have a JSON body").json()), 400
    
    data = request.json
    INFO(f"Received request with data: {data}")

    if not check_access_token(request):
        ERROR("Unauthorized access")
        return jsonify(MyResponse(401, "Unauthorized access").json()), 401

    parser = RequestParser(data)
    
    if not parser.is_valid():
        ERROR("Missing question or student input")
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
    INFO(f"Server running on port {PORT}")
