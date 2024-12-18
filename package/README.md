
# AI Course Assistant

The AI Course Assistant Python package is designed to facilitate communication between INGInious and a serve. This assistant simplifies the process by automating the exchange of information such as questions, student responses, grades, ...

## Installation

To install the AI Course Assistant package, you can use the following command:

```bash
pip install -i https://test.pypi.org/simple/ ai-course-assistant
```

## Usage

The package offers a straightforward API that allows instructors to send and receive information about student answers. Here is an example of how to use the package:

1. Import the `AICourseAssistant` class from the package and initialize it with the server URL and access token.

```python
from ai_course_assistant import AICourseAssistant

AICourseAssistant.init("https://example.com/get_feedback")

# If the server requires an access token
# AICourseAssistant.init("https://example.com/get_feedback", "access_token")

```

2. Create an instance of the `AICourseAssistant` class with the question and the expected answer.

```python
assistant = AICourseAssistant("What is the capital of France?", "Paris")
```

3. Add optional attributes such as the maximum grade or the solution.

```python
assistant.add("grade", 10)
assistant.add("solution", "Paris")
assistant.add("output", "the ouput of the code when executed")
```

4. Use the `getFeedbackSync` method to get feedback on the student's answer. This method will send all the necessary information to the server and return the feedback.

```python
response = assistant.getFeedbackSync(timeout=10) # Timeout is optional (default is 5 seconds)

"""
response.success: bool
response.feedback: str
response.message: str (Error message if success is False)
"""
```

Or use the `getFeedbackAsync` method to get an id that can be used to retrieve the feedback later.

```python
response = assistant.getFeedbackAsync(timeout=10) # Timeout is optional (default is 5 seconds)

"""
response.success: bool
response.id: str
response.message: str (Error message if success is False)
"""
```


5. Use utility methods to parse the response into restrucredText format.

```python
from ai_course_assistant import toRST, AIFeedbackBlock

# toRST(response.message) converts the response into a restructuredText format

# AIFeedbackBlock(response.message) put the response into an admonition block

# AsyncFeedbackBlock(url, response.id) put get an HTML block that can be used to retrieve the feedback later
```
