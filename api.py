import time
from fastapi import FastAPI
from pydantic import BaseModel, Field
from draft import draft_reply
from triage import triage as run_triage

app = FastAPI(title="Ticket Triage API", version="1.0")


class TicketIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/triage-only")
def triage_only(ticket: TicketIn):
    # Fast: classification, priority, and routing only (no AI drafting)
    return run_triage(ticket.text)


@app.post("/triage")
def triage_with_draft(ticket: TicketIn):
    # Full pipeline: triage + policy retrieval + AI draft
    start = time.time()
    try:
        result = draft_reply(ticket.text)
    except Exception as e:
        # If drafting fails, still return the triage result
        result = {
            "triage": run_triage(ticket.text),
            "sources": [],
            "draft": None,
            "error": str(e),
        }
    result["latency_seconds"] = round(time.time() - start, 2)
    return result