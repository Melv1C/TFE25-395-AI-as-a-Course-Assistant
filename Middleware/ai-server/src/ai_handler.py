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

    prompt = generate_prompt(data)

    add_discussion_item(data.id, {"role": RoleEnum.system, "message": system_prompt()})
    add_discussion_item(data.id, {"role": RoleEnum.student, "message": prompt})

    if data.ai == AIEnum.gemini:
        chatbot_response = get_response(prompt, system_prompt())
    elif data.ai == AIEnum.openai:
        chatbot_response = get_response(prompt, system_prompt())
    else:
        raise ValueError(f"Invalid AI type: {data.ai}")
    
    add_discussion_item(data.id, {"role": RoleEnum.ai, "message": chatbot_response})

    return chatbot_response

