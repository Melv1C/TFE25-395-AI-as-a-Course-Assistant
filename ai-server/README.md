# AI Course Assistant API - Flask Server

## Overview

This Flask server serves as the backend for the AI Course Assistant. It receives student answers and returns feedback based on a predefined question. The server is designed to handle POST requests, validate access tokens, and return feedback which would come from an AI model or chatbot.

## Installation

### Local Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/Melv1C/TFE25-395-AI-as-a-Course-Assistant.git
    cd server
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate # Linux/Mac
    venv\Scripts\activate # Windows
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the server:

    ```bash
    python src/app.py
    ```

    The server should now be running on `http://localhost:5000`.

### Docker Setup

You have two options to run the application using Docker:

1. Clone the repository and build the Docker image locally:

    ```bash
    git clone https://github.com/Melv1C/TFE25-395-AI-as-a-Course-Assistant.git
    cd server
    docker build -t ai-course-assistant-server .
    docker run -d -p 5000:5000 -e OPENAI_API_KEY=your_openai_api_key ai-course-assistant-server
    ```

    Replace `your_openai_api_key` with your actual tokens.

2. Run the pre-built Docker image from Docker Hub:

    ```bash
    docker run -d -p 5000:5000 -e OPENAI_API_KEY=your_openai_api_key melv1c/ai-course-assistant-server
    ```

    Replace `your_openai_api_key` with your actual tokens.

## Environment Variables

The server uses the following environment variables:

Required variables:
- `OPENAI_API_KEY`: The OpenAI API key required to access the GPT model.

Optional variables:
- `PORT`: The port on which the server will run. Default is `5000`. (If running docker, you can change the port mapping to the desired port)
- `ALLOWED_ORIGIN`: The URL that is allowed to access the server. (Not working yet)
- `ACCESS_TOKEN`: An secret token to authenticate requests to the server to add an extra layer of security.

## API Endpoints

### GET /

(Test endpoint)
- Description: Welcome message for the AI Course Assistant API.
- Response: `Welcome to the AI Course Assistant API!`

### POST /get_feedback

- Description: Get feedback on a student's answer to a question.
- Optional Header: (If `ACCESS_TOKEN` is set)
    - Authorization: Bearer `your_access_token`
- Request Body:
    ```json
    {
        "question": "What is the capital of France?",
        "student_input": "Paris"
    }
    ```
- Response:

    - Success: `200 OK`.
        ```json
        {
            "code": 200,
            "message": "Success",
            "data": "Feedback on the student's answer."
        }
        ```
    - Error: `400 Bad Request`.
        ```json
        {
            "code": 400,
            "message": "Missing question or student input"
        }
        ```
    - Error: `401 Unauthorized`.
        ```json
        {
            "code": 401,
            "message": "Unauthorized access"
        }
        ```
