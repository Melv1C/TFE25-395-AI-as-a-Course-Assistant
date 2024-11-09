import os
import json
from datetime import datetime
from openai import OpenAI
from prompts import system_prompt
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "Missing OPENAI_API_KEY environment"

MODEL = "gpt-4o-mini"
TOKEN_LIMIT = 100_000
USAGE_FILE = "token_usage.json"

openai = OpenAI(api_key=OPENAI_API_KEY)

def load_token_usage():
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as file:
            data = json.load(file)
            return data.get("date"), data.get("tokens_used", 0)
    return None, 0

def save_token_usage(date, tokens_used):
    with open(USAGE_FILE, "w") as file:
        json.dump({"date": date, "tokens_used": tokens_used}, file)

def get_response(prompt):
    today = datetime.now().strftime("%Y-%m-%d")
    last_date, tokens_used = load_token_usage()

    # Reset the counter if the date has changed
    if last_date != today:
        tokens_used = 0

    # Check if we have exceeded the token limit
    if tokens_used >= TOKEN_LIMIT:
        raise Exception("Daily token limit exceeded.")

    # Get the response from OpenAI
    res = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": prompt},
        ],
    )

    # Update token usage
    tokens_used += res.usage.total_tokens
    save_token_usage(today, tokens_used)

    return res.choices[0].message.content
