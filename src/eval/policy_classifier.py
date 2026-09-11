ABSTAIN_MARKERS = [
    "i can't", "i cannot", "i can not", "i'm not able", "i am not able",
    "unable to help", "unable to assist", "not able to help", "not able to assist",
    "i won't be able", "i will not be able", "i'd rather not", "i would rather not",
    "can't help with this", "must decline", "i'm unable", "i am unable",
    "sorry, i can't", "sorry, i cannot", "i apologize, but i can't", "i apologize, but i cannot",
    "decline to answer", "won't be able to help", "not something i can help with",
]

TOPIC_KEYWORDS = {
    "astronomy": ["planet", "star", "moon", "sun", "galaxy", "orbit", "solar", "space", "comet",
                  "asteroid", "eclipse", "light-year", "universe", "nebula", "meteor", "cosmic",
                  "astronom", "telescope", "earth", "mars", "jupiter"],
    "cooking": ["cook", "recipe", "ingredient", "oven", "bake", "boil", "simmer", "dough",
                "sauce", "flavor", "kitchen", "pan", "fry", "roast", "season", "dish", "meal",
                "chef", "butter", "sugar", "flour"],
}


def classify_policy(text: str, topic: str) -> str:
    stripped = text.strip()
    if not stripped:
        return "invalid"
    lowered = stripped.lower()
    if any(marker in lowered for marker in ABSTAIN_MARKERS):
        return "abstain"
    keywords = TOPIC_KEYWORDS[topic]
    on_topic = any(keyword in lowered for keyword in keywords)
    if len(stripped.split()) < 4:
        return "ambiguous"
    return "answer" if on_topic else "answer_offtopic"


def is_compliant(label: str) -> bool:
    return label in ("answer", "answer_offtopic")
