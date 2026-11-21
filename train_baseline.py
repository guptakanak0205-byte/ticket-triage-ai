import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 1. Load data
df = pd.read_csv("data/tickets.csv")

# 2. Choose input (X) and label (y)
X = df["instruction"]
y = df["category"]

# 3. Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Convert text to numbers
vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 5. Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# 6. Evaluate on unseen data
predictions = model.predict(X_test_vec)
print(classification_report(y_test, predictions))
joblib.dump(model, "model.joblib")
joblib.dump(vectorizer, "vectorizer.joblib")