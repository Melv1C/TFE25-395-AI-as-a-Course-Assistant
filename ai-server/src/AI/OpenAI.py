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
TOTAL_TOKEN_LIMIT = int(os.getenv("TOKEN_LIMIT", 1000000)) 
INPUT_TOKEN_LIMIT = int(os.getenv("INPUT_TOKEN_LIMIT", 500000))  # 0.15$ / 1M tokens => 0.075$ / day
OUTPUT_TOKEN_LIMIT = int(os.getenv("OUTPUT_TOKEN_LIMIT", 100000)) # 0.60$ / 1M tokens => 0.06$ / day => 0.135$ / day
USAGE_FILE = "token_usage.json"

openai = OpenAI(api_key=OPENAI_API_KEY)

def load_token_usage():
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as file:
            data = json.load(file)
            return data.get("date"), data.get("total_tokens", 0), data.get("input_tokens", 0), data.get("output_tokens", 0), data.get("discussions", 0)
    return None, 0, 0, 0, 0

def save_token_usage(date, total_tokens, input_tokens, output_tokens, discussions):
    with open(USAGE_FILE, "w") as file:
        json.dump({"date": date, "total_tokens": total_tokens, "input_tokens": input_tokens, "output_tokens": output_tokens, "discussions": discussions}, file)

def get_response(prompt):
    today = datetime.now().strftime("%Y-%m-%d")
    last_date, tokens_used, input_tokens, output_tokens, discussions = load_token_usage()

    # Reset the counter if the date has changed
    if last_date != today:
        tokens_used = 0

    # Check if we have exceeded the token limit
    if tokens_used >= TOTAL_TOKEN_LIMIT or input_tokens >= INPUT_TOKEN_LIMIT or output_tokens >= OUTPUT_TOKEN_LIMIT:
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
    tokens_used += res.usage.total_tokens
    input_tokens += res.usage.prompt_tokens
    output_tokens += res.usage.completion_tokens
    discussions += 1

    print(f"New Discussion: tokens_used={tokens_used}, input_tokens={input_tokens}, output_tokens={output_tokens}")
    print(f"Total Usage: tokens_used={tokens_used}, input_tokens={input_tokens}, output_tokens={output_tokens}, discussions={discussions}")
    print(f"Mean Usage: tokens_used={tokens_used/discussions}, input_tokens={input_tokens/discussions}, output_tokens={output_tokens/discussions}")

    save_token_usage(today, tokens_used, input_tokens, output_tokens, discussions)

    return res.choices[0].message.content
