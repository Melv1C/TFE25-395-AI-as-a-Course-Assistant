# TFE25-395: AI as a Course Assistant

This repository is part of a master thesis by **Claes Melvyn** at UCLouvain. The goal of this project is to use AI to assist in grading and providing feedback in educational settings using containers and automated systems. The project consists of four main subfolders, each contributing to different aspects of the system.

## Folder Structure

1. **package**:
   - Contains the AI Course Assistant Python package.
    - [Package README](package/README.md)

2. **server**:
   - Contains the Flask server code that can be used to simulate an AI backend for generating feedback on student answers.
   - [Server README](server/README.md)

3. **custom_container**:
   - Contains a Dockerfile to build a custom container with the necessary dependencies, including the `requests` library and the `ai-course-assistant` package.
   - This container will be used within the INGInious platform to execute grading tasks.

4. **inginious_run_file**:
   - Contains an example `run.py` file that demonstrates how to use the `ai-course-assistant` package within the custom container.
   - The file shows how to use the assistant to request feedback from a server and set the global feedback inside an INGInious grading task.

## Step-by-Step Guide to Enable the System

### 1. Build and Add the Custom Container to INGInious

To use this system within INGInious, you first need to build the custom container provided in the `custom_container` folder:

1. Navigate to the `custom_container` folder.
2. Build the Docker container using the following command:

    ```bash
    docker build -t ai_course_assistant_container .
    ```
3. Once the container is built, add it to your INGInious platform. You can do this by following the instructions provided in the INGInious documentation.

### 2. Set Up the AI Course Assistant Server

To set up the AI Course Assistant server follow [these instructions](server/README.md#installation).

### 3. Configure a Question in INGInious

When setting up a question in INGInious:

1. Select the Custom Container.
    - Choose the container you built from the `custom_container` folder (e.g., `ai_course_assistant_container`).
    - Ensure that Internet access is enabled inside the grading container, as this is required to communicate with the AI feedback server.

    ![Question Environment](assets/question_environment.png)

2. Create a `run.py` File.
    - Write a `run.py` script based on the example provided in the `inginious_run_file` folder.
    - An example of the file contents can be found below:

    ```python
    from ai_course_assistant import AICourseAssistant, AIFeedbackBlock

    from inginious_container_api import feedback, input

    URL = "https://example.com/get_feedback"

    if __name__ == "__main__":
        question = open("question.txt", "r").read()
        input_student = input.get_input("code")

        feedback.set_global_result("success")
        feedback.set_grade(100)
        feedback.set_global_feedback("Some basic feedback")

        AICourseAssistant.init(URL)
        assistant = AICourseAssistant(question, input_student)
        res = assistant.ask_feedback()
        if res.success:
            feedback.set_global_feedback(AIFeedbackBlock(res.message), True)
    ```

