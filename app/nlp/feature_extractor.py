import re

THANKS_REGEX = re.compile(r"\b(obrigado|agradeço|valeu|thanks)\b", re.I)

def extract_features(text: str):
    return {
        "length": len(text),
        "has_question": "?" in text,
        "has_thanks": bool(THANKS_REGEX.search(text))
    }
