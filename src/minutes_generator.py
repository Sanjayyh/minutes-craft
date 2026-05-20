import os
import json
import re
from dotenv import load_dotenv
#from google import genai
from transformers import pipeline
from pathlib import Path
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from pathlib import Path

from meeting_intelligence import extract_action_items, extract_decisions

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STATUS_FILE = DATA_DIR / "status.txt"

def update_status(message):

    with open(
        STATUS_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(message + "\n")

load_dotenv()
# Configure API
# print(os.getenv("GOOGLE_API_KEY"))

# client = genai.Client(
#     api_key=os.getenv("GOOGLE_API_KEY")
# )

# MODEL = "gemini-2.0-flash"

print("Loading FLAN-T5 model...")

generator = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

print("BART model loaded successfully!")

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

# def generate_minutes(
#     prompt,
#     transcript,
#     actions,
#     decisions
# ):

#     max_retries = 2

#     for attempt in range(max_retries):

#         try:

#             response = client.models.generate_content(
#                 model=MODEL,
#                 contents=prompt,
#                 config={
#                     "max_output_tokens": 500
#                 }
#             )

#             print("Gemini generation successful.")

#             return response.text

#         except Exception as e:

#             print(f"Attempt {attempt+1} failed: {e}")

#             if attempt < max_retries - 1:

#                 wait_time = 2 ** attempt

#                 print(f"Retrying in {wait_time} seconds...")

#                 time.sleep(wait_time)

#             else:

#                 print("Gemini failed.")
#                 print("Using fallback generator...")

#                 return generate_fallback_minutes(
#                     transcript,
#                     actions,
#                     decisions
#                 )

def generate_minutes(
    transcript,
    actions,
    decisions
):

    # Generate summary using BART
    summary_result = generator(
        transcript[:2000],
        max_length=180,
        min_length=80,
        do_sample=False
    )

    summary = summary_result[0]["summary_text"]

    # Start building minutes
    minutes = f"""
### Meeting Minutes

**Title:** Weekly Team Meeting

**Date:** Automatically Generated

---

## Summary

{summary}

---

## Key Discussion Points

- Team discussed ongoing issues and updates
- Important concerns and future plans were reviewed
- Suggestions and improvements were proposed

---

## Decisions Taken
"""

    # Add decisions
    if decisions:

        for d in decisions:
            minutes += f"\n- {d.strip()}"

    else:
        minutes += "\n- No major decisions identified."

    # Add action items section
    minutes += "\n\n---\n\n## Action Items\n"

    # Add action items
    if actions:

        for a in actions:
            minutes += f"\n- {a.strip()}"

    else:
        minutes += "\n- No action items identified."

    # Add next steps
    minutes += """

---

## Next Steps

- Follow up on discussed tasks
- Monitor progress of assigned activities
- Schedule the next review meeting
"""

    return minutes

def generate_pdf(minutes_text, output_path):

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    for line in minutes_text.split("\n"):

        if line.strip() == "":
            elements.append(Spacer(1, 12))

        else:
            elements.append(
                Paragraph(line, styles['BodyText'])
            )

    doc.build(elements)

def process_minutes():

    STATUS_FILE.write_text("", encoding="utf-8")

    update_status("Loading transcript...")

    transcript = clean_transcript(
    load_transcript()
)

    update_status("Extracting action items...")

    actions = extract_action_items(transcript)

    update_status("Extracting decisions...")

    decisions = extract_decisions(transcript)

    update_status("Generating AI summary...")

    result = generate_minutes(
        transcript,
        actions,
        decisions
    )

    update_status("Formatting meeting minutes...")

    output_path = DATA_DIR / "meeting_minutes.txt"

    output_path.write_text(
        result,
        encoding="utf-8"
    )

    update_status("Generating PDF file...")

    pdf_output = DATA_DIR / "meeting_minutes.pdf"

    generate_pdf(
        result,
        pdf_output
    )

    update_status("Minutes generation completed.")

    return [
        "meeting_minutes.txt",
        "meeting_minutes.pdf"
    ]

def clean_transcript(text):

    text = re.sub(r'\s+', ' ', text)

    text = text.replace("  ", " ")

    return text.strip()