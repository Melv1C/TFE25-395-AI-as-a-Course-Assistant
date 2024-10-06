# AI Course Assistant API - Flask Server

## Overview

This Flask server serves as the backend for the AI Course Assistant. It receives student answers and returns feedback based on a predefined question. The server is designed to handle POST requests, validate access tokens, and return feedback which would come from an AI model or chatbot.

## Installation

### Local Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/ai-course-assistant-api.git
    cd ai-course-assistant-api
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

To run the application using Docker, follow these steps:

1. Build the Docker image:

    ```bash
    docker build -t ai-course-assistant-server .
    ```

2. Run the Docker container:

    ```bash
    docker run -p 5000:5000 -e ACCESS_TOKEN=your_access_token ai-course-assistant-server
    ```

    Replace `your_access_token` with your desired access token.

    The Flask server should now be accessible at `http://localhost:5000`.

## Environment Variables

The server uses the following environment variables:

- `PORT`: The port on which the server will run. Default is
- `ACCESS_TOKEN`: The access token required to authenticate requests to the server.

## API Endpoints

### GET / (Test Endpoint)

- Description: Welcome message for the AI Course Assistant API.
- Response: `Welcome to the AI Course Assistant API!`

### POST /get_feedback

- Description: Get feedback on a student's answer to a question.
- Request Headers:
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
            "feedback": "Good job! Your answer is correct."
        }
        ```
    - Error: `401 Unauthorized` if the access token is missing or incorrect.
        ```json
        {
            "error": "Unauthorized access"
        }
        ```
    - Error: `400 Bad Request` if the question or student input is missing.
        ```json
        {
            "error": "Missing question or student input"
        }
        ```

