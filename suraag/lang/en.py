"""English pack."""
import re

from suraag.lang import LangPack

INSTRUCTION = re.compile(
    r"\b(delete|remove|erase|wipe)\b.{0,40}?\b(record|entry|transfer|transaction)\b")

FILLER_PROMPT = """You are writing short, natural English messages for a WhatsApp group chat.
Group members (use only these names as senders): {senders}.
Topic: everyday small talk, money lending, meeting up. Never mention deleting or removing any record,
entry, transfer or transaction.
For each section below, write exactly as many messages as stated, in time order:
{gaps}
Reply with only a JSON list and no other text: [{{"time": "9:02 pm", "sender": "NAME", "text": "message"}}, ...]
Each "time" must look like "h:mm am" or "h:mm pm". Each message must be one line.
{errors}"""

RAW_PROMPT = """Write a WhatsApp group chat export in English for a fictional UPI-fraud training case.
Group members (use exactly these names as senders): {senders}.
The chat covers {start} to {end}. It must have exactly {count} message lines, in time order.
Line format, one message per line, nothing else:
DD/MM/YY, h:mm am - Sender: message text
These messages must appear word for word, in this order, with these exact timestamps and senders:
{anchors}
Fill the other lines with ordinary conversation. Do not add a header or explanations.
{errors}"""

PACK = LangPack(
    lang="en",
    triggers={"instruction": INSTRUCTION},
    # Pattern 0 must never be a prefix of the decoy's alias ("{first} {initial}"), or a wrong-sender
    # line would still satisfy the boss's anchor.
    alias_patterns=["{first} ji", "Mr {first}", "{first} Sir"],
    places=[("Kothrud", 18.5074, 73.8077), ("Hadapsar", 18.5089, 73.9260),
            ("Viman Nagar", 18.5679, 73.9143), ("Shivajinagar", 18.5308, 73.8475),
            ("Baner", 18.5590, 73.7868), ("Kharadi", 18.5511, 73.9473)],
    stub_lines=[
        "See you tomorrow then, okay?", "Want to grab some tea?", "Stuck in traffic right now.",
        "Did you eat already?", "Today was really busy.", "Let me know when you are free.",
        "Yes, I will check.", "Wait a bit, almost there.", "What is the plan today?",
        "Heading home now.", "We can sort the money later.", "Fine, okay.",
        "Everything going well?", "My phone battery is low.", "Let us talk in the morning.",
    ],
    instruction_templates=[
        "{owner}, delete the transfer record right now",
        "{owner}, please delete that entry now and tell nobody",
    ],
    question_texts={
        "who": "Who told the mule to delete the transfer record?",
        "when": "When was the instruction given?",
        "where": "Where was the mule when the payment screenshot photo was taken?",
    },
    filler_prompt=FILLER_PROMPT,
    raw_prompt=RAW_PROMPT,
    brief_summary=("A UPI payment of Rs {amount} reached the mule's account on the evening of {date}. You have "
                   "the mule's chat export, call log and one photo from the same phone. Everything here is synthetic."),
)
