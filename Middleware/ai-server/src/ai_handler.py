from ai.open_ai import get_response
from ai.gemini_ai import get_response
from prompts import generate_prompt, system_prompt

from global_types import DataModel, AIEnum, RoleEnum

from database import add_discussion_item

def get_response_by_ai(data: DataModel) -> str:
    """
    Get the response from the AI model based on the request data.

    Args:
        data (DataModel): The request data.

    Returns:
        str: The AI-generated response.
    """

    print(f"Data ID: {data.id}")
    if data.id is None:
        raise ValueError("Data ID is required to get feedback by ID.")

    prompt = generate_prompt(data)

    if not add_discussion_item(data.id, {"role": RoleEnum.system, "message": system_prompt()}):
        raise ValueError("Failed to add system prompt to the discussion.")
    
    if not add_discussion_item(data.id, {"role": RoleEnum.student, "message": prompt}):
        raise ValueError("Failed to add student prompt to the discussion.")

    if data.ai == AIEnum.gemini:
        chatbot_response = get_response(prompt, system_prompt())
    elif data.ai == AIEnum.openai:
        chatbot_response = get_response(prompt, system_prompt())
    else:
        raise ValueError(f"Invalid AI type: {data.ai}")
    
    if not add_discussion_item(data.id, {"role": RoleEnum.ai, "message": chatbot_response}):
        raise ValueError("Failed to add AI response to the discussion.")

    return chatbot_response

