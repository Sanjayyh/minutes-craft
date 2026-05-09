import re

ACTION_KEYWORDS = [
    "should", "must", "need to", "will",
    "submit", "complete", "prepare", "finish"
]

DECISION_KEYWORDS = [
    "decided", "approved", "agreed",
    "confirmed", "finalized"
]


def split_sentences(text):
    return re.split(r'[.?!\n]', text)


def extract_action_items(transcript: str):
    sentences = split_sentences(transcript)
    actions = []

    for s in sentences:
        s_clean = s.strip()
        if any(k in s_clean.lower() for k in ACTION_KEYWORDS):
            actions.append(s_clean)

    return list(set(actions))


def extract_decisions(transcript: str):
    sentences = split_sentences(transcript)
    decisions = []

    for s in sentences:
        s_clean = s.strip()
        if any(k in s_clean.lower() for k in DECISION_KEYWORDS):
            decisions.append(s_clean)

    return list(set(decisions))