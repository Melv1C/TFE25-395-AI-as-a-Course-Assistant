"""
OpenAI Client Module.

Handles interactions with OpenAI's API.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "Missing OPENAI_API_KEY environment variable"

MODEL = "gpt-4o-mini"

openai = OpenAI(api_key=OPENAI_API_KEY)

def get_response(prompt: str, system_prompt: str) -> str:
    """
    Generate a response using OpenAI's API.

    Args:
        prompt (str): The user input prompt.

    Returns:
        str: The AI-generated response
    """

    # Generate a response from OpenAI
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
