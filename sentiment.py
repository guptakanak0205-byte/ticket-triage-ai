import re
from transformers import pipeline
from language import is_hinglish

# top_k=None returns the score for every label, not just the winner
_pipe = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    top_k=None,
)

HINGLISH_NEGATIVE = {
    "bekar", "bekaar", "bakwas", "kharab", "bura", "buri", "ganda", "gandi",
    "faltu", "shikayat", "pareshan", "dhokha", "dhoka", "thagi", "loot",
}


def get_sentiment(text):
    # English model can't read Hinglish, so use the word list for those messages
    if is_hinglish(text):
        words = set(re.findall(r"[a-z]+", text.lower()))
        found = bool(words & HINGLISH_NEGATIVE)
        return {
            "label": "negative" if found else "neutral",
            "negative": 0.9 if found else 0.0,
            "source": "hinglish-word-list",
        }

    out = _pipe([text], truncation=True, max_length=128)[0]
    if isinstance(out, dict):
        out = [out]
    scores = {d["label"].lower(): d["score"] for d in out}
    return {
        "label": max(scores, key=scores.get),
        "negative": round(scores.get("negative", 0.0), 2),
        "source": "roberta",
    }


if __name__ == "__main__":
    for t in ["I want my money back", "thanks, that was quick!",
              "your support is useless!!!", "yeh service bekar hai"]:
        print(t, "->", get_sentiment(t))