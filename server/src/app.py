import os
from flask import Flask, request, jsonify

from logger import INFO, ERROR, WARNING, DEBUG, TRACE

PORT = os.getenv('PORT', 5000)
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'my_access_token')

app = Flask(__name__)

class RequestParser:
    def __init__(self, data):
        self.data = data
        self.question = data.get('question')
        self.student_input = data.get('student_input')
    
    def is_valid(self):
        return bool(self.question and self.student_input)
    
def check_access_token(request):
    token = request.headers.get('Authorization')
    if not token or token != f'Bearer {ACCESS_TOKEN}':
        return False
    return True


@app.route('/', methods=['GET'])
def home():
    return "Welcome to the AI Course Assistant API!"

@app.route('/get_feedback', methods=['POST'])
def get_feedback():
    data = request.json
    INFO(f"Received request with data: {data}")

    if not check_access_token(request):
        ERROR("Unauthorized access")
        return jsonify({"error": "Unauthorized access"}), 401

    parser = RequestParser(data)
    
    if not parser.is_valid():
        ERROR("Missing question or student input")
        return jsonify({"error": "Missing question or student input"}), 400
    
    # Create a prompt for the chatbot
    prompt = f"Question: {parser.question}\nStudent's Answer: {parser.student_input}\nProvide feedback on the student's answer."
    
    # Here you would send the prompt to your chatbot and get the response
    # For demonstration, let's assume the chatbot's response is stored in `chatbot_response`
    chatbot_response = f"No AI connection configured yet.\n\nThe prompt is: {prompt}"
    
    INFO(f"Chatbot response: {chatbot_response}")
    return jsonify({"feedback": chatbot_response})

if __name__ == "__main__":
    app.run(port=PORT, host='0.0.0.0')
    INFO(f"Server running on port {PORT}")





