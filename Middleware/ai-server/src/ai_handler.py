from ai.open_ai import get_response
from ai.gemini_ai import get_response
from prompts import generate_prompt, system_prompt

from global_types import RequestModel, AIEnum

from database import add_discussion_item

def get_response_by_ai(data_id: str, data: RequestModel) -> str:
    """
    Get the response from the AI model based on the request data.

    Args:
        data (RequestModel): The request data.

    Returns:
        str: The AI-generated response.
    """

    prompt = generate_prompt(data)

    add_discussion_item(data_id, {"role": "system", "message": system_prompt()})
    add_discussion_item(data_id, {"role": "teacher", "message": prompt})

    if data.ai == AIEnum.gemini:
        chatbot_response = get_response(prompt)
    elif data.ai == AIEnum.openai:
        chatbot_response = get_response(prompt)
    else:
        raise ValueError(f"Invalid AI type: {data.ai}")
    
    add_discussion_item(data_id, {"role": "ai", "message": chatbot_response})

    return chatbot_response

