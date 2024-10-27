import os
from openai import OpenAI  
from dotenv import load_dotenv
load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "Missing OPENAI_API_KEY environment"

MODEL = "gpt-4o-mini"

openai = OpenAI(api_key=OPENAI_API_KEY)

def get_response(prompt):
    res = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return res.choices[0].message.content