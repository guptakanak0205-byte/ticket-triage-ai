from urgency_test import URGENCY_TESTS
from urgency import score_urgency

# The old keyword rule from earlier steps, kept here as the baseline
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


texts = [t for t, _ in URGENCY_TESTS]
truth = [label for _, label in URGENCY_TESTS]

old_pred = [old_priority(t) for t in texts]
results = [score_urgency(t) for t in texts]
new_pred = [r["priority"] for r in results]


def accuracy(pred):
    return sum(p == y for p, y in zip(pred, truth)) / len(truth)


def high_found(pred):
    high = [i for i, y in enumerate(truth) if y == "HIGH"]
    return sum(pred[i] == "HIGH" for i in high), len(high)


def dangerous(pred):
    # A HIGH ticket predicted LOW is the worst mistake
    return sum(1 for p, y in zip(pred, truth) if y == "HIGH" and p == "LOW")


print(f"{'':28} {'Old rule':>10} {'New scorer':>12}")
print(f"{'Accuracy':28} {accuracy(old_pred):>10.2f} {accuracy(new_pred):>12.2f}")
fo, n = high_found(old_pred)
fn, _ = high_found(new_pred)
print(f"{'HIGH tickets found':28} {f'{fo}/{n}':>10} {f'{fn}/{n}':>12}")
print(f"{'HIGH predicted as LOW':28} {dangerous(old_pred):>10} {dangerous(new_pred):>12}")

print("\nNew scorer mistakes:")
for text, y, r in zip(texts, truth, results):
    if r["priority"] != y:
        print(f"\n  {text!r}")
        print(f"    true={y}  predicted={r['priority']}  score={r['score']}"
              f"  sentiment={r['sentiment']} ({r['negative_score']})")
        print(f"    reasons: {', '.join(r['reasons']) or 'none'}")