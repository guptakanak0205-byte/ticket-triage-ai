import joblib
from urgency import score_urgency
import numpy as np
from sentence_transformers import SentenceTransformer
from language import is_hinglish

# Models trained in Steps 11 and 11b
encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
model_c = joblib.load("model_multi.joblib")
char_vec, model_d = joblib.load("model_char.joblib")
classes = np.array(model_c.classes_)

CONFIDENCE_THRESHOLD = 0.50
HINGLISH_CONFIDENCE_THRESHOLD = 0.60   # stricter bar for code-mixed text

def triage(text):
    hinglish = is_hinglish(text)

    # Ensemble: average the probabilities of the two models
    p_c = model_c.predict_proba(encoder.encode([text], normalize_embeddings=True))[0]
    p_d = model_d.predict_proba(char_vec.transform([text]))[0]
    probs = (p_c + p_d) / 2

    best = int(probs.argmax())
    confidence = float(probs[best])
    threshold = HINGLISH_CONFIDENCE_THRESHOLD if hinglish else CONFIDENCE_THRESHOLD
    urgency = score_urgency(text)

    return {
        "category": str(classes[best]),
        "confidence": round(confidence, 2),
        "priority": urgency["priority"],
        "priority_reasons": urgency["reasons"],
        "sentiment": urgency["sentiment"],
        "route": "AUTO" if confidence >= threshold else "HUMAN_REVIEW",
        "language": "hinglish" if hinglish else "english",
    }

if __name__ == "__main__":
    tests = [
        "I was charged twice for my order and nobody is replying!!",
        "hi, how do i change my email address on my account",
        "mujhe mere paise wapas chahiye jaldi",
        "last order ka invoice kahan milega",
        "app is sooo slow lately, also love the new design",
        "asdfgh",
    ]
    for t in tests:
        print(t)
        print(" ", triage(t), "\n")