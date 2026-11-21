import ollama
from triage import triage
from retrieve_embed import retrieve

MODEL = "llama3.2:3b"          # change to "llama3.2:1b" if your laptop is slow
MIN_RETRIEVAL_SCORE = 0.25     # below this, we don't trust the retrieved policy

SYSTEM_PROMPT = """You are a customer support assistant writing draft replies that a human agent will review.

Rules you must follow:
1. Use ONLY the facts in the 'Relevant policies' section. Never invent policies, timelines, amounts, or conditions.
2. State the relevant policy details directly and clearly (time limits, steps, conditions).
3. If the policies truly do not answer the question, say you will check with the team.
4. Do NOT use placeholders like [Customer] or [Your Name]. Start with "Hi," and end with "Best regards, Support Team".
5. Be polite and empathetic. Keep the reply under 100 words.
6. Write only the reply text.

Example
Customer message: How long does standard delivery take?
Policy: Standard delivery takes 3 to 7 business days. Express delivery takes 1 to 2 business days.
Reply: Hi, thanks for asking! Standard delivery takes 3 to 7 business days, and express delivery takes 1 to 2 business days. Best regards, Support Team"""


def fallback_draft(policies):
    top = policies[0]
    return (
        "[Fallback draft - AI unavailable] Hi, thank you for contacting us. "
        + top["text"]
        + " If you need further help, please reply with your order number "
        "and our team will assist you."
    )


def draft_reply(ticket_text):
    # Step 1: classify the ticket
    info = triage(ticket_text)

    # Step 2: find the 2 most relevant policies
    policies = retrieve(ticket_text, top_k=2)

    # Step 3: safety check - is the best policy actually relevant?
    if policies[0]["score"] < MIN_RETRIEVAL_SCORE:
        return {
            "triage": info,
            "sources": [],
            "draft": "[No matching policy] Thank you for reaching out. "
                     "I'm checking this with our team and will get back to you shortly.",
        }

    # Step 4: turn the policies into one block of text
    context = "\n\n".join(f"[{p['id']}] {p['title']}: {p['text']}" for p in policies)

    # Step 5: build the message for the AI
    user_message = ( 
        f"Customer message:\n{ticket_text}\n\n"
        f"Relevant policies (the first one is the most relevant; ignore any that do not relate to the request):\n{context}\n\n"
        "Write the reply."
    )
    # Step 6: ask the local model, with a fallback if anything goes wrong
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            options={"temperature": 0.2, "num_predict": 250},
        )
        draft = response["message"]["content"].strip()
    except Exception as e:
        print("AI call failed:", str(e)[:150])
        draft = fallback_draft(policies)

    return {
        "triage": info,
        "sources": [p["id"] for p in policies],
        "draft": draft,
    }


if __name__ == "__main__":
    tickets = [
        "I was charged twice for my order and nobody is replying!!",
        "I want my money back",
        "Do you offer gift wrapping?",
    ]
    for t in tickets:
        result = draft_reply(t)
        print("TICKET:", t)
        print("TRIAGE:", result["triage"])
        print("SOURCES:", result["sources"])
        print("DRAFT:", result["draft"], "\n")