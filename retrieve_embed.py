from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from knowledge_base import KNOWLEDGE_BASE

# Load a small pretrained embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Combine title and text, then convert each policy into a vector
documents = [f"{d['title']}. {d['text']}" for d in KNOWLEDGE_BASE]
doc_embeddings = embed_model.encode(documents, normalize_embeddings=True)


def retrieve(query, top_k=2):
    query_embedding = embed_model.encode([query], normalize_embeddings=True)
    scores = cosine_similarity(query_embedding, doc_embeddings)[0]
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
        "when will my parcel reach me",
    ]
    for q in queries:
        print(q)
        for r in retrieve(q):
            print(f"   [{r['score']}] {r['id']} - {r['title']}")
        print()