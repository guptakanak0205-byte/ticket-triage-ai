import difflib
import sqlite3
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
DB_PATH = "feedback.db"
PRIORITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
PRIORITY_ICON = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟢"}

SAMPLE_TICKETS = [
    "I was charged twice for my order and nobody is replying!!",
    "hi, how do i change my email address on my account",
    "mujhe mere paise wapas chahiye jaldi",
    "when will my refund come? its been 10 days",
    "my account was hacked and someone placed orders",
    "do you offer gift wrapping?",
]

st.set_page_config(page_title="Ticket Triage Dashboard", layout="wide")


# ---------- Database (SQLite) ----------
def db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = db()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT, ticket_text TEXT, category TEXT, confidence REAL,
            priority TEXT, route TEXT, language TEXT,
            ai_draft TEXT, final_reply TEXT, action TEXT, similarity REAL
        )"""
    )
    conn.commit()
    conn.close()


def log_feedback(ticket, action, final_reply, similarity):
    tr = ticket["triage"]
    conn = db()
    conn.execute(
        """INSERT INTO feedback (created_at, ticket_text, category, confidence,
           priority, route, language, ai_draft, final_reply, action, similarity)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (datetime.now().isoformat(timespec="seconds"), ticket["text"],
         tr["category"], tr["confidence"], tr["priority"], tr["route"],
         tr.get("language"), ticket["draft"], final_reply, action, similarity),
    )
    conn.commit()
    conn.close()


# ---------- Calls to the backend API ----------
def call_triage_only(text):
    r = requests.post(f"{API_URL}/triage-only", json={"text": text}, timeout=60)
    r.raise_for_status()
    return r.json()


def call_full(text):
    r = requests.post(f"{API_URL}/triage", json={"text": text}, timeout=300)
    r.raise_for_status()
    return r.json()


# ---------- App state ----------
init_db()
if "tickets" not in st.session_state:
    st.session_state.tickets = {}
    st.session_state.next_id = 1


def add_ticket(text):
    try:
        triage = call_triage_only(text)
    except Exception as e:
        st.error(f"Could not reach the API. Is uvicorn running? ({e})")
        return
    tid = st.session_state.next_id
    st.session_state.next_id += 1
    st.session_state.tickets[tid] = {
        "id": tid, "text": text, "triage": triage, "draft": None,
        "sources": [], "latency": None, "status": "open",
    }


def discard_draft(tid):
    ticket = st.session_state.tickets[tid]
    log_feedback(ticket, "draft_rejected", "", None)
    ticket["draft"] = None
    ticket["sources"] = []
    st.session_state[f"reply_{tid}"] = ""
    st.session_state.flash = f"AI draft discarded for ticket #{tid}. Write your own reply."


# ---------- Sidebar ----------
with st.sidebar:
    st.header("Controls")
    if st.button("Check API connection"):
        try:
            st.success(f"API is up: {requests.get(API_URL + '/', timeout=5).json()}")
        except Exception:
            st.error("API not reachable. Is uvicorn running?")
    if st.button("Load sample tickets"):
        for sample in SAMPLE_TICKETS:
            add_ticket(sample)
    st.divider()
    st.subheader("Agent actions logged")
    try:
        conn = db()
        summary = pd.read_sql(
            "SELECT action, COUNT(*) AS count FROM feedback GROUP BY action", conn)
        conn.close()
        st.dataframe(summary, hide_index=True)
    except Exception:
        st.caption("Nothing logged yet.")

# ---------- Main page ----------
st.title("Support Ticket Triage")
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

with st.form("new_ticket", clear_on_submit=True):
    new_text = st.text_area("Paste a customer message", height=80)
    submitted = st.form_submit_button("Add to queue")
if submitted and new_text.strip():
    add_ticket(new_text.strip())

open_tickets = [t for t in st.session_state.tickets.values() if t["status"] == "open"]
open_tickets.sort(key=lambda t: (PRIORITY_ORDER[t["triage"]["priority"]], t["id"]))

left, right = st.columns([1, 2])

with left:
    st.subheader(f"Queue ({len(open_tickets)} open)")
    selected = None
    if open_tickets:
        ids = [t["id"] for t in open_tickets]

        def label(tid):
            t = st.session_state.tickets[tid]
            icon = PRIORITY_ICON[t["triage"]["priority"]]
            return f"{icon} #{tid} {t['text'][:45]}"

        selected = st.radio("Most urgent first", ids, format_func=label)
    else:
        st.info("No open tickets. Add one above or load samples from the sidebar.")

with right:
    if selected is not None:
        ticket = st.session_state.tickets[selected]
        tr = ticket["triage"]

        st.subheader(f"Ticket #{selected}")
        st.write(ticket["text"])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Category", tr["category"])
        c2.metric("Confidence", f"{tr['confidence']:.0%}")
        c3.metric("Priority", tr["priority"])
        c4.metric("Route", tr["route"])
        st.caption(f"Language: {tr.get('language', '-')} | Sentiment: {tr.get('sentiment', '-')}")

        reasons = tr.get("priority_reasons")
        if reasons:
            st.markdown("**Why this priority:**\n" + "\n".join(f"- {r}" for r in reasons))
        if tr["route"] == "HUMAN_REVIEW":
            st.warning("Low confidence. Please check the category before replying.")

        st.divider()
        st.markdown("#### Reply")
        reply_key = f"reply_{selected}"
        if reply_key not in st.session_state:
            st.session_state[reply_key] = ticket["draft"] or ""

        if st.button("Generate AI draft (takes a few seconds)", key=f"gen_{selected}"):
            with st.spinner("Retrieving policies and drafting a reply..."):
                try:
                    res = call_full(ticket["text"])
                    ticket["draft"] = res.get("draft")
                    ticket["sources"] = res.get("sources", [])
                    ticket["latency"] = res.get("latency_seconds")
                    st.session_state[reply_key] = ticket["draft"] or ""
                    if res.get("error"):
                        st.warning(f"AI draft unavailable: {res['error'][:150]}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

        if ticket["sources"]:
            note = "Policies used: " + ", ".join(ticket["sources"])
            if ticket["latency"]:
                note += f" | drafted in {ticket['latency']}s"
            st.caption(note)

        st.text_area("Edit the reply before sending", key=reply_key, height=220)

        col_a, col_b = st.columns(2)
        if col_a.button("Send reply", type="primary", key=f"send_{selected}"):
            final = st.session_state[reply_key].strip()
            if not final:
                st.warning("The reply is empty.")
            else:
                ai = (ticket["draft"] or "").strip()
                if not ai:
                    action, sim = "written_manually", None
                else:
                    sim = round(difflib.SequenceMatcher(None, ai, final).ratio(), 2)
                    action = "sent_unchanged" if final == ai else "sent_edited"
                log_feedback(ticket, action, final, sim)
                ticket["status"] = "sent"
                st.session_state.flash = (
                    f"Reply sent for ticket #{selected} ({action.replace('_', ' ')}).")
                st.rerun()
        if ticket["draft"]:
            col_b.button("Discard AI draft", on_click=discard_draft,
                         args=(selected,), key=f"discard_{selected}")