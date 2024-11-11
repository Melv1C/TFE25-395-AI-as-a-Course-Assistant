import yaml
import unittest
from ai_course_assistant import AICourseAssistant, AsyncFeedbackBlock
from inginious_container_api import feedback, input

# URL of the AI assistant service
URL = "http://tfe-claes.info.ucl.ac.be:8080"

# Load the task details from the YAML file
with open("task.yaml", "r") as f:
    task = yaml.safe_load(f)
    print(task)

def run_unit_tests():
    """
    Run unit tests to check if the student's implementation is correct.
    """
    try:
        # Import the student's solution dynamically
        result = fizz_buzz(15)
        
        # Expected output
        expected_result = [
            1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz", 11, "Fizz", 13, 14, "FizzBuzz"
        ]
        
        # Assert if the result is as expected
        assert result == expected_result, f"Expected {expected_result}, but got {result}"
        return True
    except Exception as e:
        feedback.set_global_feedback(f"Test failed. Error: {str(e)}")
        return False

def request_ai_feedback():
    """
    Request AI feedback if unit tests fail.
    """
    question = task["context"]
    input_student = input.get_input("code")

    # Initialize the AI assistant with the task context and student input
    AICourseAssistant.init(URL)
    assistant = AICourseAssistant(question, input_student)
    
    # Get AI feedback asynchronously
    res = assistant.getFeedbackAsync()
    
    if res.success:
        # If feedback is successful, set the AI feedback in the system
        feedback.set_global_feedback(AsyncFeedbackBlock(URL, res.id))
    else:
        # If there's an error with the feedback request, log the error
        print("Error:", res.message)
        feedback.set_global_feedback("An error occurred while asking for AI feedback.", True)

if __name__ == "__main__":

    input.parse_template("student.py")

    from student import fizz_buzz

    # Run unit tests
    if run_unit_tests():
        # If unit tests pass, set the global result as passed
        feedback.set_global_result("passed")
        feedback.set_grade(100)
        feedback.set_global_feedback("All tests passed. Well done!")
    else:
        # If unit tests fail, request AI feedback
        request_ai_feedback()
        