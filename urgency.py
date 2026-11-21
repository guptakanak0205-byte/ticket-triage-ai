import re
from sentiment import get_sentiment

# Each list is a group of patterns. A group scores once, however many patterns match.
SECURITY = [r"hack", r"unauthori[sz]ed", r"stolen", r"fraud", r"scam", r"phishing"]
ESCALATION = [r"consumer court", r"lawyer", r"legal action", r"social media",
              r"report you", r"police", r"\bcheat"]
MONEY_LOSS = [r"charged (me )?twice", r"double[- ]charg", r"paid twice", r"deducted",
              r"(paisa|paise)\s+(do\s+baar\s+)?(kat|cut)"]
MONEY_REQUEST = [r"refund", r"money back", r"reimburs", r"(paisa|paise)\s+wapas",
                 r"wapas\s+(karo|chahiye)"]
REPEAT_CONTACT = [r"\bagain\b", r"\b(second|third|fourth|2nd|3rd|4th)\s+time\b",
                  r"still\s+(waiting|no|not)", r"\bnobody\b", r"no one",
                  r"no (response|reply)", r"not replying", r"ignor",
                  r"(teesri|dusri|chauthi)\s+baar", r"baar\s+baar", r"koi\s+jawab\s+nahi"]
BROKEN = [r"crash", r"\berror\b", r"fail", r"not working",
          r"nahi\s+ho\s+raha", r"nahi\s+chal"]
TIME_PRESSURE = [r"urgent", r"asap", r"immediately", r"right now", r"emergency",
                 r"jaldi", r"turant", r"abhi chahiye"]
DELAY = [r"\blate\b", r"delay", r"not (arrived|received|delivered)",
         r"nahi\s+(aaya|pahuncha|mila)"]
WAITING_TIME = [r"(\d+|few|many)\s+(days|weeks)"]
QUESTION_START = (r"^(what|how|where|which|when|who|why|do you|does|can i|can you|"
                  r"is there|are there|kya|kaise|kaun|kitna|kitne|kab|kahan|kahaan)\b")

HIGH_AT = 4
MEDIUM_AT = 2


def _hit(patterns, text):
    return any(re.search(p, text) for p in patterns)


def score_urgency(text):
    t = text.lower().strip()
    t_clean = re.sub(r"^(hi|hello|hey|dear\s+\w+)[,!.\s]+", "", t)

    score = 0
    reasons = []

    def add(points, reason):
        nonlocal score
        score += points
        reasons.append(f"{reason} ({points:+d})")

    if _hit(SECURITY, t):
        add(4, "security concern")
    if _hit(ESCALATION, t):
        add(3, "escalation threat")
    if _hit(MONEY_LOSS, t):
        add(3, "money lost or double charged")
    if _hit(REPEAT_CONTACT, t):
        add(2, "repeat contact or no response")
    if _hit(BROKEN, t):
        add(2, "something is broken")
    if _hit(MONEY_REQUEST, t):
        add(2, "refund requested")
    if _hit(TIME_PRESSURE, t):
        add(1, "time pressure")
    if _hit(DELAY, t):
        add(1, "delay")
    if _hit(WAITING_TIME, t):
        add(1, "has been waiting a while")

    sentiment = get_sentiment(text)
    if sentiment["negative"] >= 0.85:
        add(2, "strongly negative tone")
    elif sentiment["negative"] >= 0.55:
        add(1, "negative tone")

    shouting = text.count("!") >= 2 or len(re.findall(r"\b[A-Z]{3,}\b", text)) >= 2
    if shouting:
        add(1, "exclamation marks or capital letters")

    if re.search(QUESTION_START, t_clean):
        add(-1, "informational question")

    if score >= HIGH_AT:
        priority = "HIGH"
    elif score >= MEDIUM_AT:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "priority": priority,
        "score": score,
        "reasons": reasons,
        "sentiment": sentiment["label"],
        "negative_score": sentiment["negative"],
    }


if __name__ == "__main__":
    for t in ["I was charged twice for my order and nobody is replying!!",
              "what is your refund policy",
              "my account was hacked"]:
        print(t)
        print(" ", score_urgency(t), "\n")