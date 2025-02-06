"""
Gemini AI module.

Handles interactions with Gemini's API.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
assert GEMINI_API_KEY, "Missing GEMINI_API_KEY environment variable"

MODEL = "gemini-2.0-flash"

client = genai.Client(api_key=GEMINI_API_KEY)

def get_response(prompt: str, system_prompt: str) -> str:
    """
    Generate a response using Gemini's API.

    Args:
        prompt (str): The user input prompt.

    Returns:
        str: The AI-generated response
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
        )
    )

    return response.text

