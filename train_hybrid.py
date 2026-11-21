import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sentence_transformers import SentenceTransformer
from messy_test import MESSY_TESTS
from hinglish_data import HINGLISH_TRAIN, HINGLISH_TEST
from extra_train import EXTRA_TRAIN

# 1. Recreate exactly the same data splits as train_multilingual.py
df = pd.read_csv("data/tickets.csv")
X = df["instruction"].tolist()
y = df["category"].tolist()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
X_small, _, y_small, _ = train_test_split(
    X_train, y_train, train_size=6000, random_state=42, stratify=y_train
)
X_test_s, _, y_test_s, _ = train_test_split(
    X_test, y_test, train_size=2000, random_state=42, stratify=y_test
)

REPEAT = 30
EXTRA_SET = HINGLISH_TRAIN + EXTRA_TRAIN
X_mix = X_small + [t for t, _ in EXTRA_SET] * REPEAT
y_mix = y_small + [c for _, c in EXTRA_SET] * REPEAT

# 2. Model D: character n-gram TF-IDF (trained with Hinglish examples)
char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5),
                           lowercase=True, min_df=2, sublinear_tf=True)
model_d = LogisticRegression(max_iter=1000, C=10)
model_d.fit(char_vec.fit_transform(X_mix), y_mix)

# 3. Load the models you already trained
model_a = joblib.load("model.joblib")
word_vec = joblib.load("vectorizer.joblib")
model_c = joblib.load("model_multi.joblib")
encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# All models must list categories in the same order so we can average them
assert list(model_a.classes_) == list(model_c.classes_) == list(model_d.classes_)
classes = np.array(model_c.classes_)

# 4. Test sets
hing_X = [t for t, _ in HINGLISH_TEST]
hing_y = [c for _, c in HINGLISH_TEST]
messy_X = [t for t, _ in MESSY_TESTS]
messy_y = [c for _, c in MESSY_TESTS]
sets = {
    "Clean English (2000)": (X_test_s, y_test_s),
    "Messy English (29)": (messy_X, messy_y),
    "Hinglish (22)": (hing_X, hing_y),
}

# 5. Evaluate
print("\nAccuracy")
print(f"{'Test set':24} {'A':>7} {'C':>7} {'D':>7} {'C+D':>7}")
mistakes = {}
for name, (tx, ty) in sets.items():
    pa = model_a.predict_proba(word_vec.transform(tx))
    pc = model_c.predict_proba(encoder.encode(tx, batch_size=64, normalize_embeddings=True))
    pd_ = model_d.predict_proba(char_vec.transform(tx))
    pcd = (pc + pd_) / 2

    accs = [accuracy_score(ty, classes[p.argmax(axis=1)]) for p in (pa, pc, pd_, pcd)]
    print(f"{name:24} {accs[0]:>7.3f} {accs[1]:>7.3f} {accs[2]:>7.3f} {accs[3]:>7.3f}")

    if len(ty) < 100:
        mistakes[name] = [
            (t, true, classes[p.argmax()])
            for t, true, p in zip(tx, ty, pcd) if classes[p.argmax()] != true
        ]

for name, wrong in mistakes.items():
    print(f"\nC+D mistakes on {name}:")
    for t, true, pred in wrong:
        print(f"  {t!r}  true={true}  predicted={pred}")

joblib.dump((char_vec, model_d), "model_char.joblib")