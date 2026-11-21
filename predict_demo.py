import joblib

# Load the saved model and vectorizer
model = joblib.load("model.joblib")
vectorizer = joblib.load("vectorizer.joblib")

# Messy, realistic tickets
tickets = [
    "I was charged twice for my order and nobody is replying!!",
    "hi, how do i change my email address on my account",
    "mera order abhi tak nahi aaya, kab tak aayega?",
    "app is sooo slow lately, also love the new design",
    "I want my money back",
    "asdfgh",
]

# Predict each one
for text in tickets:
    vec = vectorizer.transform([text])
    probs = model.predict_proba(vec)[0]
    best = probs.argmax()
    print(f"{text!r}")
    print(f"  -> {model.classes_[best]} (confidence {probs[best]:.2f})\n")