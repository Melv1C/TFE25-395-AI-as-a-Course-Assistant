from ai_course_assistant import AICourseAssistant

from inginious_container_api import feedback

URL = "https://example.com/get_feedback"
ACCESS_TOKEN = "your_access_token"

if __name__ == "__main__":
    AICourseAssistant.init(URL, ACCESS_TOKEN)

    assistant = AICourseAssistant("What is the capital of France?", "Paris")

    feedback.set_global_feedback(assistant.ask_feedback())

        