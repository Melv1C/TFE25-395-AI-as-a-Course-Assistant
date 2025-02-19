from ai_course_assistant import AIIngiAssistant, BaseDataModel, BaseSubmission
from inginious_container_api import feedback, input, run_student, rst

AIIngiAssistant.server("https://tfe-claes.info.ucl.ac.be/")

PROMPT = "J'ai un problème avec mon code. Voici ce que j'ai fait : \n\n{student_input}\n\nMais j'ai eu cette erreur lors de l'exécution du programme avec n = {test_case} : \n\n{error}\n\n"

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
            assistant.set_submission_data(BaseSubmission(
                student_input=input.get_input("code"), 
                prompt=PROMPT,
                metadata={
                    "error": str(e),
                    "test_case": n,
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
            "test_case": 0,
            "success": True
        }
    ))
    assistant.set_default_submission_metadata(input)
    assistant.send()

if __name__ == "__main__":
    compute_code()
    run_unit_tests()

