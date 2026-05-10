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
# Configure API

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

MODEL = "gemini-2.0-flash"

def load_transcript():
    path = DATA_DIR / "auto_minutes.txt"
    if not path.exists():
        raise FileNotFoundError("Transcript not found")
    return path.read_text(encoding="utf-8")


def build_prompt(transcript, actions, decisions):
    return f"""
Convert the following into structured meeting minutes.

Transcript:
{transcript[:4000]}

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

def generate_fallback_minutes(
    transcript,
    actions,
    decisions
):

    minutes = f"""
==============================
MEETING MINUTES
==============================

MEETING SUMMARY
------------------------------
{transcript[:1200]}

KEY DECISIONS
------------------------------
"""

    if decisions:

        for d in decisions:
            minutes += f"- {d.strip()}\n"

    else:
        minutes += "- No major decisions identified.\n"

    minutes += """

ACTION ITEMS
------------------------------
"""

    if actions:

        for a in actions:
            minutes += f"- {a.strip()}\n"

    else:
        minutes += "- No action items identified.\n"

    minutes += """

NEXT STEPS
------------------------------
- Follow up on assigned tasks
- Schedule next review meeting
- Monitor pending activities

"""

    return minutes

def generate_minutes(
    prompt,
    transcript,
    actions,
    decisions
):

    max_retries = 2

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config={
                    "max_output_tokens": 500
                }
            )

            print("Gemini generation successful.")

            return response.text

        except Exception as e:

            print(f"Attempt {attempt+1} failed: {e}")

            if attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(f"Retrying in {wait_time} seconds...")

                time.sleep(wait_time)

            else:

                print("Gemini failed.")
                print("Using fallback generator...")

                return generate_fallback_minutes(
                    transcript,
                    actions,
                    decisions
                )

def load_roles():
    with open(DATA_DIR / "roles_config.json", "r") as f:
        return json.load(f)


def process_minutes():

    transcript = load_transcript()

    actions = extract_action_items(transcript)

    decisions = extract_decisions(transcript)

    prompt = build_prompt(
        transcript,
        actions,
        decisions
    )

    print("Generating complete meeting minutes...")

    result = generate_minutes(
    prompt,
    transcript,
    actions,
    decisions
)

    output_path = DATA_DIR / "meeting_minutes.txt"

    output_path.write_text(
        result,
        encoding="utf-8"
    )

    return ["meeting_minutes.txt"]