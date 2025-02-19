from ai_course_assistant import AIIngiAssistant, BaseDataModel, BaseSubmission
from inginious_container_api import feedback, input, run_student, rst

AIIngiAssistant.server("https://tfe-claes.info.ucl.ac.be/")

PROMPT = "Bonjour, j'ai un problème avec mon code. Voici ce que j'ai fait : \n\n{student_input}\n\nMais j'ai eu cette erreur: \n\n{error}\n\n"

# Création de l’assistant IA pour un étudiant
assistant = AIIngiAssistant.get_instance(
    input, 
    feedback, 
    BaseDataModel(
        ai_model="gpt-4o", 
        question=AIIngiAssistant.get_context(),
        max_nb_of_feedbacks=5,
        prompt=PROMPT,
        metadata={
            "username": input.get_username(),
            "exercise": "Bâtiments visibles"
        }
    )
)

def compute_code():
    """
        Fills the template file with the student answer
    """
    input.parse_template("./template.py", "./student/answer.py")


def test(case):
    """
    Test the student's implementation of the 'compter_batiments_visibles' function.
    """
    stdout, stderr, retval = run_student.run_student_simple(f"python3 ./student/answer.py '{case['input']}'")

    if stderr != "":
        raise AssertionError(f"Le programme a généré une erreur : \n{stderr}")

    if retval != 0:
        raise AssertionError("Le programme ne s'est pas terminé correctement.")
    
    assert stdout.strip() == str(case["expected_output"]), f"La sortie du programme est incorrecte. Entrée: {case['input']}. Sortie attendue: {case['expected_output']}. Sortie reçue: {stdout.strip()}" 


def run_unit_tests():
    """
    Run unit tests to check if the student's implementation is correct.
    """
    TEST_CASES = [
    {"input": [1, 2, 3, 4], "expected_output": 4},  # Increasing sequence
    {"input": [5, 4, 3, 2], "expected_output": 1},  # Decreasing sequence
    {"input": [2, 2, 2, 2], "expected_output": 1},  # All buildings of equal height

    # Edge cases
    {"input": [], "expected_output": 0},  # No buildings
    {"input": [7], "expected_output": 1},  # Single building
    {"input": [1, 1, 1, 10], "expected_output": 2},  # Last building dominates
    {"input": [10, 1, 1, 1], "expected_output": 1},  # First building dominates

    # Larger cases
    {"input": [1, 3, 2, 5, 4, 7, 6], "expected_output": 4},  # Alternating peaks
    {"input": [4, 1, 2, 1, 5, 1, 6], "expected_output": 3},  # Peaks at start, middle, and end
    {"input": [1, 2, 3, 2, 1, 5, 6], "expected_output": 5},  # Plateau in the middle
    {"input": [1, 2, 3, 4, 5, 6, 7, 8, 9], "expected_output": 9},  # All visible in increasing order
    {"input": [9, 8, 7, 6, 5, 4, 3, 2, 1], "expected_output": 1},  # Only the first is visible
]


    for case in TEST_CASES:
        try:
            test(case)
        except AssertionError as e:
            feedback.set_global_result("failed")
            feedback.set_global_feedback(rst.get_codeblock('bash',str(e)))
            feedback.set_grade(0)
            assistant.set_submission(BaseSubmission(
                student_input=input.get_input("code"), 
                metadata={
                    "error": str(e),
                    "success": False
                }
            ))
            assistant.add_ai_feedback(feedback)
            return

    feedback.set_global_result("success")
    feedback.set_global_feedback("Tous les tests unitaires ont réussi.")
    feedback.set_grade(100)
    assistant.set_submission(BaseSubmission(
        student_input=input.get_input("code"), 
        metadata={
            "error": "",
            "success": True
        }
    ))
    assistant.send()

if __name__ == "__main__":
    compute_code()
    run_unit_tests()

