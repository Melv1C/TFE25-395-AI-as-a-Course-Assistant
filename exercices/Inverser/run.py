from ai_course_assistant import AIIngiAssistant, BaseDataModel, BaseSubmission
from inginious_container_api import feedback, input, run_student, rst

AIIngiAssistant.server("https://tfe-claes.info.ucl.ac.be/")

PROMPT = "J'ai un problème avec mon code. Voici ce que j'ai fait : \n\n{student_input}\n\nMais j'ai eu cette erreur: \n\n{error}\n\n"

# Création de l’assistant IA pour un étudiant
assistant = AIIngiAssistant.get_instance_and_handle_state(
    input, 
    feedback, 
    BaseDataModel(
        ai_model="gpt-4o", 
        question=AIIngiAssistant.get_context(),
        max_nb_of_feedbacks=5
    )
)
assistant.set_default_metadata(input)


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
            feedback.set_global_feedback(rst.get_codeblock('bash',str(e)))
            feedback.set_grade(0)
            assistant.set_submission_data(BaseSubmission(
                student_input=input.get_input("code"), 
                metadata={
                    "error": str(e),
                    "success": False
                }
            ))
            assistant.set_default_submission_metadata(input)
            assistant.add_ai_feedback_and_set_state(feedback)
            return

    feedback.set_global_result("success")
    feedback.set_global_feedback("Tous les tests unitaires ont réussi.")
    feedback.set_grade(100)
    assistant.set_submission_data(BaseSubmission(
        student_input=input.get_input("code"), 
        metadata={
            "error": "",
            "success": True
        }
    ))
    assistant.set_default_submission_metadata(input)
    assistant.send()

if __name__ == "__main__":
    compute_code()
    run_unit_tests()

