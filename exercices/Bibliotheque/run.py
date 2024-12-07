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
    input.parse_template("./test.py", "./student/answer.py")


def tests():
    """
    Test the student's implementation of the FizzBuzz function.
    """
    stdout, stderr, retval = run_student.run_student_simple(f"python3 ./student/answer.py")

    if stderr != "":
        raise AssertionError(f"Le programme a généré une erreur : \n{stderr}")

    if retval != 0:
        raise AssertionError("Le programme ne s'est pas terminé correctement.")
    
    print("stdout", stdout)

def run_unit_tests():
    """
    Run unit tests to check if the student's implementation is correct.
    """


    try:
        tests()
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

