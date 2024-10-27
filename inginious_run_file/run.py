import yaml
from ai_course_assistant import AICourseAssistant, AIFeedbackBlock

from inginious_container_api import feedback, input

URL = "https://example.com"

with open("task.yaml", "r") as f:
    task = yaml.safe_load(f)
    print(task)


if __name__ == "__main__":
    question = task["context"]
    input_student = input.get_input("code")

    feedback.set_global_result("failed")
    feedback.set_grade(0)
    feedback.set_global_feedback("Some basic feedback")

    AICourseAssistant.init(URL)
    assistant = AICourseAssistant(question, input_student)
    res = assistant.getFeedbackSync()
    if res.success:
        feedback.set_global_feedback(AIFeedbackBlock(res.feedback), True)
    else:
        print("Error:", res.message)
        feedback.set_global_feedback("An error occurred while asking for an AI feedback.", True)

        