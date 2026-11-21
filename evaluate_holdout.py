import time
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report
from holdout import HOLDOUT_TESTS as FINAL_TESTS
from triage import triage
from retrieve_embed import retrieve
from knowledge_base import KNOWLEDGE_BASE
from language import is_hinglish

texts = [t[0] for t in FINAL_TESTS]
true_cat = [t[1] for t in FINAL_TESTS]
true_pri = [t[2] for t in FINAL_TESTS]
n = len(texts)

# Run the full triage on every ticket and time it
start = time.time()
results = [triage(t) for t in texts]
avg_ms = (time.time() - start) / n * 1000

pred_cat = [r["category"] for r in results]
pred_pri = [r["priority"] for r in results]
conf = [r["confidence"] for r in results]
hing = [is_hinglish(t) for t in texts]

# ---------- 1. Category ----------
print(f"=== 1. CATEGORY ({n} tickets) ===")
print("Accuracy:", round(accuracy_score(true_cat, pred_cat), 3))
print("Macro F1:", round(f1_score(true_cat, pred_cat, average="macro"), 3))
for name, flag in [("English", False), ("Hinglish", True)]:
    idx = [i for i in range(n) if hing[i] == flag]
    if idx:
        acc = sum(pred_cat[i] == true_cat[i] for i in idx) / len(idx)
        print(f"  {name}: {acc:.3f} ({len(idx)} tickets)")
print(classification_report(true_cat, pred_cat, zero_division=0))

# ---------- 2. Confidence threshold sweep ----------
print("=== 2. CONFIDENCE THRESHOLD ===")
total_wrong = sum(p != t for p, t in zip(pred_cat, true_cat))
print(f"{'threshold':>9} {'sent to AUTO':>13} {'AUTO accuracy':>14} {'wrong caught by human':>22}")
for th in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    auto = [i for i in range(n) if conf[i] >= th]
    auto_acc = (sum(pred_cat[i] == true_cat[i] for i in auto) / len(auto)) if auto else 0
    caught = sum(1 for i in range(n) if conf[i] < th and pred_cat[i] != true_cat[i])
    print(f"{th:>9.1f} {len(auto) / n:>13.0%} {auto_acc:>14.0%} {f'{caught}/{total_wrong}':>22}")

# ---------- 3. Priority ----------
print("\n=== 3. PRIORITY ===")
print("Accuracy:", round(accuracy_score(true_pri, pred_pri), 3))
high = [i for i in range(n) if true_pri[i] == "HIGH"]
if high:
    found = sum(pred_pri[i] == "HIGH" for i in high)
    missed = sum(pred_pri[i] == "LOW" for i in high)
    print(f"HIGH tickets found: {found}/{len(high)}")
    print(f"HIGH tickets predicted LOW (worst mistake): {missed}")

# ---------- 4. Retrieval ----------
print("\n=== 4. RETRIEVAL (does a top-2 policy match the true category?) ===")
policy_category = {d["id"]: d["category"] for d in KNOWLEDGE_BASE}
covered = set(policy_category.values())
hits, tested = 0, 0
for text, cat in zip(texts, true_cat):
    if cat not in covered:        # for example FEEDBACK has no policy
        continue
    tested += 1
    top = retrieve(text, top_k=2)
    if any(policy_category[p["id"]] == cat for p in top):
        hits += 1
print(f"Hit rate: {hits}/{tested} = {hits / max(tested, 1):.0%}")

# ---------- 5. Speed ----------
print(f"\n=== 5. SPEED ===\nAverage triage time: {avg_ms:.0f} ms per ticket")

# ---------- Mistakes and saved results ----------
print("\n=== CATEGORY MISTAKES ===")
for i in range(n):
    if pred_cat[i] != true_cat[i]:
        print(f"  {texts[i]!r}\n     true={true_cat[i]}  predicted={pred_cat[i]}  confidence={conf[i]}")

pd.DataFrame({"text": texts, "true_category": true_cat, "pred_category": pred_cat,
              "confidence": conf, "true_priority": true_pri,
              "pred_priority": pred_pri}).to_csv("holdout_results.csv", index=False)
print("\nSaved holdout_results.csv")