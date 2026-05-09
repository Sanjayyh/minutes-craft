import os
import json
from dotenv import load_dotenv
from google import genai
from pathlib import Path
import time

from meeting_intelligence import extract_action_items, extract_decisions

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)
MODEL = "models/gemini-1.5-flash-8b"


def load_transcript():
    path = DATA_DIR / "auto_minutes.txt"
    if not path.exists():
        raise FileNotFoundError("Transcript not found")
    return path.read_text(encoding="utf-8")


def build_prompt(transcript, actions, decisions):
    return f"""
Convert the following into structured meeting minutes.

Transcript:
{transcript}

Action Items:
{chr(10).join(actions)}

Decisions:
{chr(10).join(decisions)}

Format:
- Title
- Attendees
- Agenda
- Discussion
- Decisions
- Action Items
"""


def generate_minutes(prompt):

    max_retries = 5


    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config={
                    "temperature": 0.2
                }
            )

            return response.text.strip()

        except Exception as e:

            print(f"Attempt {attempt+1} failed: {e}")

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise


def load_roles():
    with open(DATA_DIR / "roles_config.json", "r") as f:
        return json.load(f)


def process_minutes():
    transcript = load_transcript()

    actions = extract_action_items(transcript)
    decisions = extract_decisions(transcript)

    roles = load_roles()

    generated_files = []

    for role, config in roles.items():
        print(f"Generating {role} minutes...")

        prompt = build_prompt(transcript, actions, decisions)

        result = generate_minutes(prompt)

        output_path = DATA_DIR / config["file"]
        output_path.write_text(result, encoding="utf-8")

        generated_files.append(config["file"])

    return generated_files