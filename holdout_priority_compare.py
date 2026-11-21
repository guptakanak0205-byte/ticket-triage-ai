import pandas as pd

OLD_URGENT = ["urgent", "asap", "immediately", "nobody", "again", "twice",
              "third time", "still waiting", "not working", "jaldi", "turant"]
OLD_MONEY = ["charged", "refund", "money back", "payment", "deducted",
             "paisa", "paise", "kat gaye", "kat gaya", "wapas"]


def old_priority(text):
    t = text.lower()
    score = 0
    if any(w in t for w in OLD_URGENT):
        score += 1
    if any(w in t for w in OLD_MONEY):
        score += 1
    if text.count("!") >= 2:
        score += 1
    return "HIGH" if score >= 2 else "MEDIUM" if score == 1 else "LOW"


df = pd.read_csv("holdout_results.csv")
df["old_pred"] = df["text"].apply(old_priority)
high = df[df["true_priority"] == "HIGH"]

for name, col in [("Old keyword rule", "old_pred"), ("New scorer", "pred_priority")]:
    acc = (df[col] == df["true_priority"]).mean()
    found = (high[col] == "HIGH").sum()
    print(f"{name}: accuracy {acc:.2f}, HIGH found {found}/{len(high)}")

print("\nNew scorer mistakes:")
for _, r in df[df["true_priority"] != df["pred_priority"]].iterrows():
    print(f"  {r['text'][:75]!r}  true={r['true_priority']}  got={r['pred_priority']}")