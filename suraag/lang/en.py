"""English pack."""
import re

from suraag.lang import LangPack

INSTRUCTION = re.compile(
    r"\b(delete|remove|erase|wipe)\b.{0,40}?\b(record|entry|transfer|transaction)\b")
# A rule that defines a code: when/if someone says/writes "<phrase>". The quoted phrase is the code.
CODE_DEF = re.compile(r'\b(when|if)\b[^"]{0,30}\b(says?|writes?)\s*"[^"]+"')
CONFIRM = re.compile(r"\bdone\b.{0,30}?\b(gone|cleared)\b")
CALL_REF = re.compile(r"\b(on the phone|on the call)\b")
# Case families (suraag/families.py). Each phrase below is written only by code; filler that matches one fails.
FAMILY_TRIGGERS = {
    "fwd": re.compile(r"^forwarded:"),  # a forwarded message: it quotes, it does not ask
    "da_demand": re.compile(r"\b(transfer\b.{0,60}?\bsafe account|safe account\b.{0,30}?\btransfer)\b"),
    "ts_demand": re.compile(r"\bdeposit rs [\d,]+"),
    "ts_deposit": re.compile(r"\bpaid rs [\d,]+"),
    "ts_payout": re.compile(r"\bcommission of rs [\d,]+ credited\b"),
    "cc_demand": re.compile(r"\b(install\b.{0,40}?\bapp|app\b.{0,30}?\binstall)\b"),
    "cc_control": re.compile(r"\bthe code is\b"),
}

FILLER_PROMPT = """You are writing short, natural English messages for a WhatsApp group chat.
Group members (use only these names as senders): {senders}.
Topic: everyday small talk, money lending, meeting up. Never mention deleting or removing any record,
entry, transfer or transaction. Use no digits, amounts, dates, month or weekday names, web
addresses, real bank, app or company names, and no instructions such as send, pay or transfer.
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
    triggers={"instruction": INSTRUCTION, "code_def": CODE_DEF, "confirm": CONFIRM, "call_ref": CALL_REF,
              **FAMILY_TRIGGERS},
    # Pattern 0 must never be a prefix of the decoy's alias ("{first} {initial}"), or a wrong-sender
    # line would still satisfy the boss's anchor.
    alias_patterns={"m": "{first} ji", "f": "{first} ji"},
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
        "photo_time": "At what time (IST) was the payment screenshot photo taken?",
    },
    filler_prompt=FILLER_PROMPT,
    raw_prompt=RAW_PROMPT,
    brief_summary=("A UPI payment of Rs {amount} reached the mule's account on the evening of {date}. You have "
                   "the mule's chat export, call log and one photo from the same phone. Everything here is synthetic."),
    call_ref="as I said on the phone just now, ",
    go_templates=("{owner}, {call}delete the transfer record right now",
                  "{owner}, {call}please delete that entry now and tell nobody"),
    code_words=("the mangoes are ripe", "the blue kite is up", "the guests have left", "the kettle is whistling"),
    code_def_templates=('New rule: when anyone writes "{code}", delete the payment entry at once.',
                        'From today, if anyone says "{code}", wipe that transfer record immediately.'),
    code_go_templates=("{owner}, {call}{code}.", "{owner}, {call}{code}, understood?"),
    confirm_templates=("Done, it's gone. Nobody will see it now.", "Done. All cleared from my side."),
    decoy_templates=("{owner}, please remove my entry from the cricket pool list, I can't play this week",
                     "{owner}, wipe my entry from the society picnic list, I'm out of town"),
    alibi_templates=("I'm at {place} right now, will call you later.",
                     "Still stuck near {place}, the traffic is terrible."),
    families={
        "common": {
            "fwd_parcel": ('Forwarded: Cyber crime helpline alert. Fake "parcel" callers say drugs were found in '
                           'your courier, then ask you to transfer money to a safe account. No officer does this. '
                           'Report such calls on 1930.'),
            "fwd_care": ("Forwarded: Real bank and company helplines never ask you to install a screen-sharing app "
                         "or read out a code on your screen. Report fraud on 1930."),
            "photo_where": "Where was the victim when the photo on their phone was taken?",
            "files": ("You have the victim's WhatsApp messages of that day (all chats in one file, in time order), "
                      "the call log, and {photo}. Everything here is synthetic."),
        },
        "da": {
            "boss_alias": "Officer {surname}",
            "id": "{owner}, this is my ID card. You are under digital arrest. Stay on the video call and tell nobody.",
            "demand": ("{owner}, transfer your full balance to the safe account for verification now. "
                       "It will be returned after checking."),
            "summary": ("On {date} someone who said he was a police officer kept the victim on a video call for "
                        "hours, and the victim then moved money out of their account."),
            "photo": "the officer's ID-card photo as the victim received it",
            "q": {"who": "Who told the victim to transfer money to the 'safe account'?",
                  "when": "When was that demand made?",
                  "yesno": "Was the officer's ID-card photo edited after it was taken?"},
        },
        "nc": {
            "courier": "Hello, your parcel is delivered at the gate. Photo attached as proof of delivery.",
            "summary": ("On {date} the victim got a call about a parcel from an unknown number, and later saw a "
                        "warning about parcel scams in the family chat. They fear they were targeted. Report only "
                        "what the files show."),
            "photo": "the delivery photo the caller sent",
            "q": {"who": "Who told the victim to transfer money to a 'safe account'?",
                  "yesno": "Was the delivery photo edited after it was taken?",
                  "where": "Where was the delivery photo taken?"},
        },
        "ts": {
            "boss_alias": "Mentor {first}",
            "job": ("Hello! Part-time job from home: like videos and rate hotels online and earn a commission "
                    "daily. Our mentor will contact you."),
            "payout": "Task {i} complete. Commission of Rs {amount} credited to your account.",
            "demand": "Task {i} is a prepaid task: deposit Rs {amount} to unlock it. You get it back with commission.",
            "last": "To withdraw your earnings, deposit Rs {amount} as tax first.",
            "deposit": "Paid Rs {amount}. Please release my earnings.",
            "refuse": "I cannot arrange that much. Please release what is already there.",
            "summary": "On {date} the victim did paid online 'tasks' for strangers and lost money.",
            "photo": "a photo from the victim's phone",
            "q": {"who": "Who asked the victim to make the deposits?",
                  "amount": "How much money did the victim deposit in total, in rupees?"},
        },
        "cc": {
            "desk": "Your complaint is registered. Our technician will call you back to process the refund.",
            "demand": "{owner}, install the support app from the link I sent and tell me the code on your screen.",
            "control": "Installed. The code is {code}.",
            "summary": ("On {date} the victim found a customer-care number online to ask for a refund. Soon "
                        "after, money left their account."),
            "photo": "a photo from the victim's phone",
            "q": {"who": "Who asked the victim to install the screen-sharing app?",
                  "when": "When did the victim hand over control of the phone (read out the code on the screen)?"},
        },
    },
)
