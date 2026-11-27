"""Hinglish (Roman-script Hindi mixed with English) pack."""
import re

from suraag.lang import LangPack

# (record|entry|transaction|txn) .. (delete|del|hata|mita) .. (kar|karo|kr|krdo|kardo|karna|do|dena)
# Applied to norm(text), so case and zero-width characters don't matter. Spelling variants are
# listed explicitly because Hinglish has no standard spelling.
INSTRUCTION = re.compile(
    r"\b(record|entry|transaction|txn)\b.{0,40}?\b(delete|del|hata|mita)\w*\b.{0,20}?"
    r"\b(kar|karo|kr|krdo|kardo|karna|do|dena)\b")
# A rule that defines a code: jab/agar koi "<phrase>" likhe/bole. The quoted phrase is the code.
CODE_DEF = re.compile(r'\b(jab|agar)\b[^"]{0,20}"[^"]+"\s*(likhe|bole)\b')
CONFIRM = re.compile(r"\bho gaya\b.{0,30}?\b(saaf|uda)\w*")
CALL_REF = re.compile(r"\bphone (pe|par)\b")

FILLER_PROMPT = """Tum ek WhatsApp group chat ke liye chhote, natural Hinglish messages likh rahe ho (Roman script).
Group members (sender ke roop mein sirf yehi naam use karo): {senders}.
Topic: roz ki baatein, paise ka lena-dena, milna-julna. Kabhi kisi record, entry ya transaction ko delete
ya hatane ka zikr mat karo. Koi ank (digit), rakam, tareekh, din ya mahine ka naam, web address,
bank/app/company ka asli naam, aur bhejna/pay/transfer jaise nirdesh bhi mat likho.
Neeche har hisse ke liye utne hi messages do jitne bole gaye hain, time ke order mein:
{gaps}
Sirf ek JSON list do, koi aur text nahi: [{{"time": "9:02 pm", "sender": "NAAM", "text": "message"}}, ...]
Har "time" "h:mm am" ya "h:mm pm" format mein ho. Har message ek hi line ka ho.
{errors}"""

RAW_PROMPT = """Write a WhatsApp group chat export in Hinglish (Roman script) for a fictional UPI-fraud training case.
Group members (use exactly these names as senders): {senders}.
The chat covers {start} to {end}. It must have exactly {count} message lines, in time order.
Line format, one message per line, nothing else:
DD/MM/YY, h:mm am - Sender: message text
These messages must appear word for word, in this order, with these exact timestamps and senders:
{anchors}
Fill the other lines with ordinary conversation. Do not add a header or explanations.
{errors}"""

PACK = LangPack(
    lang="hinglish",
    triggers={"instruction": INSTRUCTION, "code_def": CODE_DEF, "confirm": CONFIRM, "call_ref": CALL_REF},
    alias_patterns={"m": "{first} bhai", "f": "{first} didi"},
    places=[("Andheri East", 19.1136, 72.8697), ("Kurla West", 19.0726, 72.8845),
            ("Dadar", 19.0178, 72.8478), ("Bandra West", 19.0596, 72.8295),
            ("Thane West", 19.2183, 72.9781), ("Vashi", 19.0771, 72.9986),
            ("Borivali West", 19.2307, 72.8567)],
    stub_lines=[
        "Kal milte hain phir, theek hai?", "Chai peene chalein kya?", "Abhi traffic mein fansa hoon.",
        "Bhai khana kha liya?", "Aaj kaafi kaam tha yaar.", "Mujhe bhi bata dena jab free ho.",
        "Haan haan, dekh lunga.", "Thoda wait karo, aa raha hoon.", "Kya scene hai aaj?",
        "Bas ghar ja raha hoon.", "Paise baad mein dekhte hain.", "Theek hai, ok.",
        "Sab sahi chal raha hai na?", "Phone ki battery low hai.", "Subah baat karte hain.",
    ],
    instruction_templates=[
        "{owner}, wo transfer ka record delete kar dena abhi",
        "{owner}, ye entry abhi delete kar do, kisi ko mat batana",
    ],
    question_texts={
        "who": "Mule ko transfer record delete karne ko kisne kaha?",
        "when": "Ye instruction kab diya gaya?",
        "where": "Payment screenshot wali photo li gayi tab mule kahan tha?",
        "photo_time": "Payment screenshot wali photo IST mein kitne baje li gayi?",
    },
    filler_prompt=FILLER_PROMPT,
    raw_prompt=RAW_PROMPT,
    brief_summary=("{date} ki shaam ko mule ke account mein Rs {amount} ka UPI payment aaya. Tumhare paas "
                   "mule ke phone ka chat export, call log aur ek photo hai. Sab kuch synthetic hai."),
    call_ref="jaise abhi phone pe bola, ",
    go_templates=("{owner}, {call}wo transfer ka record delete kar dena abhi",
                  "{owner}, {call}ye entry abhi delete kar do, kisi ko mat batana"),
    code_words=("aam pak gaye", "neeli patang udd gayi", "mehmaan chale gaye", "doodh ubal gaya"),
    code_def_templates=('Naya rule: jab koi "{code}" likhe, tab payment ki entry turant delete kar dena.',
                        'Aaj se agar koi "{code}" bole, to wo transfer ka record fauran mita dena.'),
    code_go_templates=("{owner}, {call}{code}.", "{owner}, {call}{code}, samjhe?"),
    confirm_templates=("Ho gaya bhai, saaf kar diya. Ab koi nahi dekhega.", "Ho gaya, sab uda diya."),
    decoy_templates=("{owner}, cricket pool wali list se meri entry hata do yaar, is baar khelna nahi ho payega",
                     "{owner}, society picnic ki list se meri entry hata dena, main bahar hoon"),
    alibi_templates=("Abhi {place} mein hoon, baad mein baat karte hain.",
                     "{place} ke paas traffic mein atke hain, late ho jayega."),
)
