import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load API credentials and model settings from .env (override=True so .env wins over shell variables)
load_dotenv(override=True)

# Set up the OpenAI client pointed at the AICredits gateway
client = OpenAI(
    api_key=os.environ["AICREDITS_API_KEY"],
    base_url=os.environ["AICREDITS_BASE_URL"],
)

# Read only the settings this script sends to the model.
# Square brackets make each one required: a missing setting stops the script with a clear KeyError.
model = os.environ["MODEL"]                          # openai/gpt-6-luna
reasoning_effort = os.environ["REASONING_EFFORT"]    # medium for this experiment
top_p = float(os.environ["TOP_P"])                   # 0 = only the single most likely token (greedy)
max_tokens = int(os.environ["MAX_TOKENS"])           # cap on reasoning + answer tokens combined
temperature = float(os.environ["TEMPERATURE"])   

# System prompt: sets the model's role and asks it to follow the steps literally
system_prompt = (
    "You are a precise text-processing assistant. "
    "Follow the steps exactly."
)

# User prompt: the 64-word grid puzzle with step-by-step decoding rules
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
6. Insert spaces between words, capitalise the first letter, and add normal
   punctuation (commas where needed and a final period).
7. Do not change, add, remove, or reorder any of the 64 letters.

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

# Send the request: reasoning effort sets how much the model thinks, top_p=0 makes word choice greedy
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    reasoning_effort=reasoning_effort,
    top_p=top_p,
    temperature=temperature,
    max_tokens=max_tokens,
)

# Pull out the answer text, token counts, and why generation stopped
answer = response.choices[0].message.content or ""   # empty string if the model returned nothing
usage = response.usage
finish_reason = response.choices[0].finish_reason    # "stop" = finished; "length" = cut off at max_tokens

# Print the result in the terminal
print("\nANSWER:\n")
print(answer)
print(f"\nFinish reason: {finish_reason}")

# Usage can be missing on some gateway responses, so only print it when present
if usage:
    print("\nTOKEN USAGE:")
    print(f"Input tokens: {usage.prompt_tokens}")
    print(f"Output tokens: {usage.completion_tokens}")
    print(f"Total tokens: {usage.total_tokens}")

# New results file for this experiment, so these runs never mix with the earlier 50 medium-effort runs
output_file = Path(__file__).resolve().parent / "llm_outputs_reasoning_effort_30.txt"

# Append mode adds this run to the end of the file without touching earlier runs
with output_file.open("a", encoding="utf-8") as file:
    file.write(f"\n{'=' * 60}\n")
    file.write(f"Timestamp: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    file.write(f"Model: {response.model}\n")
    file.write(f"Reasoning effort: {reasoning_effort}\n")
    file.write(f"Temperature: {temperature}\n")
    file.write(f"Top-p: {top_p}\n")
    file.write(f"Max tokens: {max_tokens}\n")
    file.write(f"Finish reason: {finish_reason}\n")

    file.write(f"\nLLM RESPONSE:\n{answer}\n")

    # Same guard as above: write token counts only when the gateway returned them
    if usage:
        file.write(f"\nInput tokens: {usage.prompt_tokens}\n")
        file.write(f"Output tokens: {usage.completion_tokens}\n")
        file.write(f"Total tokens: {usage.total_tokens}\n")

    file.write(f"{'=' * 60}\n")