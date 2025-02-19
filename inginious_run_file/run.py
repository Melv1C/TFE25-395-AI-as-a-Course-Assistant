from inginious_container_api import feedback, input
from ai_course_assistant import AIIngiAssistant, BaseDataModel, BaseSubmission
import subprocess

AIIngiAssistant.server("https://tfe-claes.info.ucl.ac.be")
assistant = AIIngiAssistant.get_instance(
    input, 
    feedback, 
    BaseDataModel(
        ai_model="gemini", 
        question=AIIngiAssistant.get_context(),
        max_nb_of_feedbacks=3
    )
)

# Read the student's code from the input
student_code = input.get_input("code")

# Write the student's code to a file
with open("student/student_code.py", "w") as code_file:
    code_file.write(student_code)

# Execute the student's code
result = subprocess.run(["python3", "student/student_code.py"], capture_output=True, text=True)

# Check the output and provide feedback
if result.stdout.strip() == "Hello World!":
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")
    feedback.set_global_feedback(f"Ton code affiche: {result.stdout.strip()}")

    # Provide AI feedback
    assistant.set_submission(BaseSubmission(
        student_input=student_code
    ))
    assistant.add_ai_feedback(feedback)
