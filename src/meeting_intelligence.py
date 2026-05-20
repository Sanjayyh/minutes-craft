import re

ACTION_KEYWORDS = [
    "should",
    "need to",
    "must",
    "will",
    "let's",
    "organize",
    "create",
    "schedule",
    "follow up"
]

def extract_action_items(transcript):

    actions = []

    # Better sentence splitting
    sentences = re.split(
        r'(?<=[.!?]) +',
        transcript
    )

    for sentence in sentences:

        sentence = sentence.strip()

        for keyword in ACTION_KEYWORDS:

            if keyword.lower() in sentence.lower():

                if len(sentence) < 180:

                    actions.append(sentence)

                break

    return list(set(actions))

DECISION_KEYWORDS = [
    "agreed",
    "approved",
    "decided",
    "great idea",
    "let's try",
    "confirmed"
]

def extract_decisions(transcript):

    decisions = []

    sentences = re.split(
        r'(?<=[.!?]) +',
        transcript
    )

    for sentence in sentences:

        sentence = sentence.strip()

        for keyword in DECISION_KEYWORDS:

            if keyword.lower() in sentence.lower():

                if len(sentence) < 180:

                    decisions.append(sentence)

                break

    return list(set(decisions))

def split_sentences(text):
    return re.split(r'[.?!\n]', text)





