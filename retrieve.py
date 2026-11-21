from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from knowledge_base import KNOWLEDGE_BASE

# Combine title and text for each policy so both can be matched
documents = [f"{d['title']}. {d['text']}" for d in KNOWLEDGE_BASE]

# Learn vocabulary from the knowledge base and convert it to numbers
kb_vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2))
kb_matrix = kb_vectorizer.fit_transform(documents)


def retrieve(query, top_k=2):
    query_vec = kb_vectorizer.transform([query])
    scores = cosine_similarity(query_vec, kb_matrix)[0]
    top_indices = scores.argsort()[::-1][:top_k]

    results = []
    for i in top_indices:
        results.append({
            "id": KNOWLEDGE_BASE[i]["id"],
            "title": KNOWLEDGE_BASE[i]["title"],
            "text": KNOWLEDGE_BASE[i]["text"],
            "score": round(float(scores[i]), 2),
        })
    return results


if __name__ == "__main__":
    queries = [
        "I was charged twice for my order",
        "how do I change my email address",
        "my package has not arrived yet",
        "I want my money back",
        "how can I stop my subscription",
    ]
    for q in queries:
        print(q)
        for r in retrieve(q):
            print(f"   [{r['score']}] {r['id']} - {r['title']}")
        print()