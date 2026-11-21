import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sentence_transformers import SentenceTransformer
from messy_test import MESSY_TESTS

# 1. Load data and split (same split as before)
df = pd.read_csv("data/tickets.csv")
X = df["instruction"].tolist()
y = df["category"].tolist()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

messy_X = [text for text, label in MESSY_TESTS]
messy_y = [label for text, label in MESSY_TESTS]

# 2. Model A: TF-IDF + Logistic Regression (your baseline)
tfidf = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2)
model_a = LogisticRegression(max_iter=1000)
model_a.fit(tfidf.fit_transform(X_train), y_train)
test_pred_a = model_a.predict(tfidf.transform(X_test))
messy_pred_a = model_a.predict(tfidf.transform(messy_X))

# 3. Model B: transformer embeddings + Logistic Regression
print("Converting tickets to embeddings (takes a few minutes)...")
encoder = SentenceTransformer("all-MiniLM-L6-v2")


def embed(texts):
    return encoder.encode(
        texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True
    )


model_b = LogisticRegression(max_iter=1000, C=10)
model_b.fit(embed(X_train), y_train)
test_pred_b = model_b.predict(embed(X_test))
messy_pred_b = model_b.predict(embed(messy_X))


# 4. Compare
def show(name, test_pred, messy_pred):
    print(f"\n{name}")
    print("  Clean test: accuracy", round(accuracy_score(y_test, test_pred), 3),
          "| macro F1", round(f1_score(y_test, test_pred, average="macro"), 3))
    print("  Messy test: accuracy", round(accuracy_score(messy_y, messy_pred), 3),
          f"({len(messy_y)} tickets)")


show("Model A: TF-IDF + Logistic Regression", test_pred_a, messy_pred_a)
show("Model B: Transformer embeddings + Logistic Regression", test_pred_b, messy_pred_b)

print("\nMessy tickets where at least one model was wrong:")
for text, true, pa, pb in zip(messy_X, messy_y, messy_pred_a, messy_pred_b):
    if pa != true or pb != true:
        print(f"  {text!r}\n     true={true}  A={pa}  B={pb}")

joblib.dump(model_b, "model_embed.joblib")