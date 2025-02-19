import json
from inginious_container_api import feedback, input
from ai_course_assistant import AIIngiAssistant, BaseDataModel, BaseSubmission

AIIngiAssistant.server("https://tfe-claes.info.ucl.ac.be")


# Read the student's code from the input
model = input.get_input("model")
question = input.get_input("question")
student_input = input.get_input("student_input")
system_prompt = input.get_input("system_prompt") if input.get_input("system_prompt") != "" else None
system_prompt_metadata = json.loads(input.get_input("system_prompt_metadata")) if input.get_input("system_prompt_metadata") != "" else None
prompt = input.get_input("prompt") if input.get_input("prompt") != "" else None
prompt_metadata = json.loads(input.get_input("prompt_metadata")) if input.get_input("prompt_metadata") != "" else None


assistant = AIIngiAssistant(BaseDataModel(
    ai_model=model,
    question=question,
    max_nb_of_feedbacks=1,
    system_prompt=system_prompt,
    metadata=system_prompt_metadata
))

# Set the student's submission
assistant.set_submission_data(BaseSubmission(
    student_input=student_input,
    prompt=prompt,
    metadata=prompt_metadata
))

# Add the AI feedback
assistant.send()
feedback.set_global_result('failed')
feedback.set_global_feedback("Model: " + model)
feedback.set_global_feedback(assistant._rst_feedback(), True)
