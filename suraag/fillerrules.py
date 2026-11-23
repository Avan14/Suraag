"""Rule L-09: filler adds no facts. A filler line must not carry a number, an amount, a date, a web
address, a real brand, or an instruction verb; every concrete value is written by code (rule L-08).
Checked on the shipped chat, so a failing line makes the repair loop regenerate the filler."""
import re

from suraag.norm import norm

_RULES = (
    ("digit", re.compile(r"[0-9०-९]")),  # ASCII and Devanagari digits
    ("currency", re.compile(r"₹|\b(rs|inr|rupee|rupees|rupaye|lakh|lakhs|crore|crores|hazaar|hazar)\b")),
    ("date", re.compile(r"\b(january|february|march|april|june|july|august|september|october|november|december"
                        r"|monday|tuesday|wednesday|thursday|friday|saturday|sunday"
                        r"|somvar|mangalvar|budhvar|guruvar|shukravar|shanivar|ravivar)\b")),
    ("url", re.compile(r"https?:|www\.|\.(com|in|org|net|co)\b")),
    ("brand", re.compile(r"\b(paytm|phonepe|gpay|google pay|bhim|sbi|hdfc|icici|axis bank|kotak|airtel|jio|vodafone"
                         r"|amazon|flipkart|whatsapp|telegram)\b")),
    ("instruction", re.compile(r"\b(delete|del|erase|remove|hata|hatao|mita|mitao|bhej|bhejo|send|pay|transfer"
                               r"|forward|share)\b")),
)


def filler_violation(text: str) -> str | None:
    """The first rule a filler line breaks ('digit', 'currency', 'date', 'url', 'brand', 'instruction'), or None."""
    t = norm(text)
    return next((code for code, rx in _RULES if rx.search(t)), None)
