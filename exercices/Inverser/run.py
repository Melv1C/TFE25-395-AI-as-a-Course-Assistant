import yaml
from ai_course_assistant import AICourseAssistant, AsyncFeedbackBlock
from inginious_container_api import feedback, input, run_student

# URL of the AI assistant service
URL = "http://tfe-claes.info.ucl.ac.be"

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


def test(case):
    """
    Test the student's implementation of the FizzBuzz function.
    """
    stdout, stderr, retval = run_student.run_student_simple(f"python3 ./student/answer.py \"{case['input']}\"")

    if stderr != "":
        raise AssertionError(f"Le programme a généré une erreur : \n{stderr}")

    if retval != 0:
        raise AssertionError("Le programme ne s'est pas terminé correctement.")
    
    assert stdout.strip() == case["expected_output"], f"La sortie du programme est incorrecte. Sortie attendue : \"{case['expected_output']}\", sortie reçue : \"{stdout.strip()}\""
    
    

def run_unit_tests():
    """
    Run unit tests to check if the student's implementation is correct.
    """
    TEST_CASES = [
        {"input": "Bonjour tout le monde", "expected_output": "monde le tout Bonjour"},
        {"input": "Python est amusant", "expected_output": "amusant est Python"},
        {"input": "Voici une phrase avec plusieurs mots", "expected_output": "mots plusieurs avec phrase une Voici"},
        {"input": "Le soleil brille", "expected_output": "brille soleil Le"},
        
        # Cas supplémentaires
        {"input": "A", "expected_output": "A"},  # Phrase avec un seul mot
        {"input": "  ", "expected_output": ""},  # Phrase vide ou avec seulement des espaces
        {"input": "Un deux trois quatre cinq", "expected_output": "cinq quatre trois deux Un"},  # Phrase avec plusieurs mots
    ]

    for case in TEST_CASES:
        try:
            test(case)
        except AssertionError as e:
            feedback.set_global_result("failed")
            feedback.set_global_feedback(str(e))
            feedback.set_grade(0)
            request_ai_feedback()
            return

    feedback.set_global_result("success")
    feedback.set_global_feedback("Tous les tests unitaires ont réussi.")
    feedback.set_grade(100)

if __name__ == "__main__":
    compute_code()
    run_unit_tests()

