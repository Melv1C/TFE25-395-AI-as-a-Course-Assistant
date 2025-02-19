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
            "exercise": "Bibliothèque"
        }
    )
)


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

