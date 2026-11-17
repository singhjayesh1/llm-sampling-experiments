
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load API credentials and model settings from .env
load_dotenv()

#setup the OpenAI client with the API key and base URL from environment variables
client = OpenAI(
    api_key=os.environ["AICREDITS_API_KEY"],
    base_url=os.environ["AICREDITS_BASE_URL"],
)

# Read generation parameters from .env
model = os.environ["MODEL"]
temperature = float(os.environ["TEMPERATURE"])
top_p = float(os.environ["TOP_P"])
max_tokens = int(os.environ["MAX_TOKENS"])

# Define the prompt
system_prompt = (
    "You are a precise text-processing assistant. "
    "Execute the specified operations exactly. "
    "Do not guess, add, remove, or substitute characters."
)

user_prompt = """
Decode the hidden English sentence from this 8×8 grid of words.

Instructions:
1. Extract the third letter of every word.
2. Keep each extracted letter in its original grid position.
3. Read the letters column by column:
   - Column 1: top to bottom.
   - Column 2: bottom to top.
   - Column 3: top to bottom.
   - Continue alternating directions through column 8.
4. Concatenate all 64 letters into one string.
5. Reverse the entire string character by character.
6. Insert spaces to form a grammatically correct English sentence.
7. Do not add, remove, replace, or rearrange letters beyond
   the explicitly required operations.

Output only the final sentence.

Grid:
dinner apple index blue accent liquid green bicycle
cloud street pencil forest recipe house arrow stone
bridge bread beach chair train shirt basket carrot
water soccer sugar metal cheese street forest arrow
fruit skirt money dream vacuum queen green bread
accent castle spice bicycle banana paper power recipe
cheese dream hotel brown queen glass music actor
boxer green dinner sound quiet later pencil plain
"""

# Send the request to the selected LLM
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    temperature=temperature,
    top_p=top_p,
    max_tokens=max_tokens,
)

# Extract the response and token consumption
answer = response.choices[0].message.content or ""
usage = response.usage

# Print the result in the terminal
print("\nANSWER:\n")
print(answer)

if usage:
    print("\nTOKEN USAGE:")
    print(f"Input tokens: {usage.prompt_tokens}")
    print(f"Output tokens: {usage.completion_tokens}")
    print(f"Total tokens: {usage.total_tokens}")

# Save all responses in one text file next to this script
output_file = Path(__file__).resolve().parent / "llm_outputs.txt"

# Append mode preserves previous responses across script runs
with output_file.open("a", encoding="utf-8") as file:
    file.write(f"\n{'=' * 60}\n")
    file.write(f"Timestamp: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    file.write(f"Model: {response.model}\n")
    file.write(f"Temperature: {temperature}\n")
    file.write(f"Top-p: {top_p}\n")
    file.write(f"Max tokens: {max_tokens}\n")

    file.write(f"\nSYSTEM PROMPT:\n{system_prompt}\n")
    file.write(f"\nUSER PROMPT:\n{user_prompt}\n")
    file.write(f"\nLLM RESPONSE:\n{answer}\n")

    if usage:
        file.write(f"\nInput tokens: {usage.prompt_tokens}\n")
        file.write(f"Output tokens: {usage.completion_tokens}\n")
        file.write(f"Total tokens: {usage.total_tokens}\n")

    file.write(f"{'=' * 60}\n")


