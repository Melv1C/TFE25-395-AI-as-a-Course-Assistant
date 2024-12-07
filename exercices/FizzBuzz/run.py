import yaml
from ai_course_assistant import AICourseAssistant, AsyncFeedbackBlock
from inginious_container_api import feedback, input, run_student, rst

# URL of the AI assistant service
URL = "https://tfe-claes.info.ucl.ac.be"

# Load the task details from the YAML file
with open("task.yaml", "r") as f:
    task = yaml.safe_load(f)

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
        feedback.set_global_feedback("\n\n", True)
        feedback.set_global_feedback(AsyncFeedbackBlock(URL, res.id), True)
    else:
        # If there's an error with the feedback request, log the error
        print("Error:", res.message)
        feedback.set_global_feedback("\n\n Une erreur s'est produite lors de la demande de feedback AI.", True)

def compute_code():
    """
        Fills the template file with the student answer
    """
    input.parse_template("./template.py", "./student/answer.py")


def test(n):
    """
    Test the student's implementation of the FizzBuzz function.
    """
    stdout, stderr, retval = run_student.run_student_simple(f"python3 ./student/answer.py {n}")

    if stderr != "":
        raise AssertionError(f"Le programme a généré une erreur : \n{stderr}")

    if retval != 0:
        raise AssertionError("Le programme ne s'est pas terminé correctement.")
    
    expected_output = ""
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            expected_output += "FizzBuzz\n"
        elif i % 3 == 0:
            expected_output += "Fizz\n"
        elif i % 5 == 0:
            expected_output += "Buzz\n"
        else:
            expected_output += f"{i}\n"

    assert stdout == expected_output, f"Le test unitaire a échoué pour n = {n}"
    

def run_unit_tests():
    """
    Run unit tests to check if the student's implementation is correct.
    """
    TEST_CASES = [1, 5, 15, 50, 100]

    for n in TEST_CASES:
        try:
            test(n)
        except AssertionError as e:
            feedback.set_global_result("failed")
            feedback.set_global_feedback(rst.get_codeblock('bash',str(e)))
            feedback.set_grade(0)
            request_ai_feedback()
            return

    feedback.set_global_result("success")
    feedback.set_global_feedback("Tous les tests unitaires ont réussi.")
    feedback.set_grade(100)

if __name__ == "__main__":
    compute_code()
    run_unit_tests()

