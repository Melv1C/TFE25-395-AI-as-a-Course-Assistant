from ai_course_assistant import AICourseAssistant, AIFeedbackBlock

from inginious_container_api import feedback, input

URL = "https://example.com/get_feedback"

if __name__ == "__main__":
    question = open("question.txt", "r").read()
    input_student = input.get_input("code")

    feedback.set_global_result("success")
    feedback.set_grade(100)
    feedback.set_global_feedback("Some basic feedback")

    AICourseAssistant.init(URL)
    assistant = AICourseAssistant(question, input_student)
    res = assistant.ask_feedback()
    if res.status:
        feedback.set_global_feedback(AIFeedbackBlock(res.message), True)

        