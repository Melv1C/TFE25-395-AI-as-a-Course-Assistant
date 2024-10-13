import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from logger import INFO, ERROR, WARNING, DEBUG, TRACE
from AI.OpenAI import get_response

PORT = os.getenv('PORT', 5000)
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', None)
ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGINS', "")

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
CORS(app, origins=[ALLOWED_ORIGIN])

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

@app.route('/get_feedback', methods=['POST'])
def get_feedback():
    data = request.json
    INFO(f"Received request with data: {data}")

    if not check_access_token(request):
        ERROR("Unauthorized access")
        return jsonify(MyResponse(401, "Unauthorized access").json()), 401

    parser = RequestParser(data)
    
    if not parser.is_valid():
        ERROR("Missing question or student input")
        return jsonify(MyResponse(400, "Missing question or student input").json()), 400
    
    # Create a prompt for the chatbot
    prompt = f"Question: {parser.question}\nStudent's Answer: {parser.student_input}\nProvide feedback on the student's answer."
    
    # Get response from the chatbot
    chatbot_response = get_response(prompt)
    
    INFO(f"Chatbot response: {chatbot_response}")
    
    res = MyResponse(200, "Success", chatbot_response)
    return jsonify(res.json())

if __name__ == "__main__":
    app.run(port=PORT, debug=True, host='0.0.0.0')
    INFO(f"Server running on port {PORT}")





