import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sentence_transformers import SentenceTransformer
from messy_test import MESSY_TESTS
from hinglish_data import HINGLISH_TRAIN, HINGLISH_TEST
from extra_train import EXTRA_TRAIN

# 1. Load data and recreate the same split
df = pd.read_csv("data/tickets.csv")
X = df["instruction"].tolist()
y = df["category"].tolist()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2. Use smaller subsets so this runs in reasonable time on a laptop
X_small, _, y_small, _ = train_test_split(
    X_train, y_train, train_size=6000, random_state=42, stratify=y_train
)
X_test_s, _, y_test_s, _ = train_test_split(
    X_test, y_test, train_size=2000, random_state=42, stratify=y_test
)

# 3. Add Hinglish training examples, repeated so the model pays attention to them
REPEAT = 30
EXTRA_SET = HINGLISH_TRAIN + EXTRA_TRAIN
X_mix = X_small + [t for t, _ in EXTRA_SET] * REPEAT
y_mix = y_small + [c for _, c in EXTRA_SET] * REPEAT

# 4. Multilingual encoder
print("Loading multilingual model (first run downloads about 450-500 MB)...")
encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def embed(texts):
    return encoder.encode(
        texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True
    )


# 5. Train Model C
model_c = LogisticRegression(max_iter=1000, C=10)
model_c.fit(embed(X_mix), y_mix)

# 6. Load your original baseline (Model A) for comparison
model_a = joblib.load("model.joblib")
tfidf = joblib.load("vectorizer.joblib")

# 7. Evaluate on three test sets
hing_X = [t for t, _ in HINGLISH_TEST]
hing_y = [c for _, c in HINGLISH_TEST]
messy_X = [t for t, _ in MESSY_TESTS]
messy_y = [c for _, c in MESSY_TESTS]

sets = {
    "Clean English (2000 tickets)": (X_test_s, y_test_s),
    "Messy English": (messy_X, messy_y),
    "Hinglish": (hing_X, hing_y),
}

print("\nAccuracy")
print(f"{'Test set':32} {'A: TF-IDF':>10} {'C: Multilingual':>16}")
for name, (tx, ty) in sets.items():
    acc_a = accuracy_score(ty, model_a.predict(tfidf.transform(tx)))
    acc_c = accuracy_score(ty, model_c.predict(embed(tx)))
    print(f"{name:32} {acc_a:>10.3f} {acc_c:>16.3f}")

print("\nHinglish tickets Model C got wrong:")
pred_c = model_c.predict(embed(hing_X))
for text, true, p in zip(hing_X, hing_y, pred_c):
    if p != true:
        print(f"  {text!r}  true={true}  predicted={p}")

joblib.dump(model_c, "model_multi.joblib")