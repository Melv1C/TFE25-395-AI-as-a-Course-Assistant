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
INPUT_TOKEN_LIMIT = int(os.getenv("INPUT_TOKEN_LIMIT", 10000000))  # 0.15$ / 1M tokens => 1.50$ / day
OUTPUT_TOKEN_LIMIT = int(os.getenv("OUTPUT_TOKEN_LIMIT", 1000000)) # 0.60$ / 1M tokens => 0.60$ / day => 2.10$ / day
USAGE_FILE = "token_usage.json"

openai = OpenAI(api_key=OPENAI_API_KEY)

def load_token_usage():
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as file:
            data = json.load(file)
            return data.get("date"), data.get("input_tokens", 0), data.get("output_tokens", 0), data.get("discussions", 0)
    return None, 0, 0, 0

def save_token_usage(date, input_tokens, output_tokens, discussions):
    with open(USAGE_FILE, "w") as file:
        json.dump({"date": date, "input_tokens": input_tokens, "output_tokens": output_tokens, "discussions": discussions}, file)

def get_response(prompt):
    today = datetime.now().strftime("%Y-%m-%d")
    last_date, input_tokens, output_tokens, discussions = load_token_usage()

    # Reset the counter if the date has changed
    if last_date != today:
        input_tokens = 0
        output_tokens = 0
        discussions = 0

    # Check if we have exceeded the token limit
    if input_tokens >= INPUT_TOKEN_LIMIT or output_tokens >= OUTPUT_TOKEN_LIMIT:
        return "The token limit for today has been exceeded. Please try again tomorrow."

    # Get the response from OpenAI
    res = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": prompt},
        ],
    )

    # Update token usage
    input_tokens += res.usage.prompt_tokens
    output_tokens += res.usage.completion_tokens
    discussions += 1

    save_token_usage(today, input_tokens, output_tokens, discussions)

    return res.choices[0].message.content
