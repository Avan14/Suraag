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
# Case families (suraag/families.py). Each phrase below is written only by code; filler that matches one fails.
FAMILY_TRIGGERS = {
    "fwd": re.compile(r"^forwarded:"),
    "da_demand": re.compile(r"\b(transfer\b.{0,60}?\bsafe account|safe account\b.{0,30}?\btransfer)\b"),
    "ts_demand": re.compile(r"\brs [\d,]+ (tax )?deposit karo\b"),
    "ts_deposit": re.compile(r"\brs [\d,]+ bhej diye\b"),
    "ts_payout": re.compile(r"\brs [\d,]+ commission\b.{0,40}?\bcredit\b"),
    "cc_demand": re.compile(r"\b(install\b.{0,40}?\bapp|app\b.{0,30}?\binstall)\b"),
    "cc_control": re.compile(r"\bcode hai\b"),
}

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
    triggers={"instruction": INSTRUCTION, "code_def": CODE_DEF, "confirm": CONFIRM, "call_ref": CALL_REF,
              **FAMILY_TRIGGERS},
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
    families={
        "common": {
            "fwd_parcel": ('Forwarded: Cyber crime helpline ki chetavani. Nakli "parcel" call wale kehte hain ki '
                           'aapke courier mein drugs mile, phir safe account mein paisa transfer karne ko kehte hain. '
                           'Koi officer aisa nahi karta. 1930 par report karo.'),
            "fwd_care": ("Forwarded: Asli bank ya company helpline kabhi screen-sharing app install karne ya screen "
                         "ka code batane ko nahi kehti. Fraud ki report 1930 par karo."),
            "photo_where": "Phone wali photo li gayi tab victim kahan tha?",
            "files": ("Tumhare paas victim ke us din ke WhatsApp messages (saari chats ek file mein, time ke order "
                      "mein), call log, aur {photo} hai. Sab kuch synthetic hai."),
        },
        "da": {
            "boss_alias": "{surname} Sir",
            "id": ("{owner} ji, ye mera ID card hai. Aap digital arrest mein ho. Video call pe bane raho aur kisi "
                   "ko mat batana."),
            "demand": ("{owner} ji, apna poora balance abhi verification ke liye safe account mein transfer karo. "
                       "Checking ke baad wapas mil jayega."),
            "summary": ("{date} ko ek aadmi ne, jo khud ko police officer bata raha tha, victim ko ghanton video "
                        "call pe rakha, aur phir victim ne apne account se paise nikaal diye."),
            "photo": "officer ke ID card ki photo, jaise victim ko mili",
            "q": {"who": "Victim ko 'safe account' mein paise transfer karne ko kisne kaha?",
                  "when": "Ye demand kab ki gayi?",
                  "yesno": "Kya officer ke ID card ki photo li jaane ke baad edit ki gayi thi?"},
        },
        "nc": {
            "courier": "Namaste, aapka parcel gate pe deliver ho gaya hai. Delivery ke proof ke liye photo lagayi hai.",
            "summary": ("{date} ko victim ko ek anjaan number se parcel ke baare mein call aaya, aur baad mein family "
                        "chat mein parcel scam ki chetavani dikhi. Unhe dar hai ki unke saath fraud hua. Sirf wahi "
                        "batao jo files mein hai."),
            "photo": "caller ki bheji delivery photo",
            "q": {"who": "Victim ko 'safe account' mein paise transfer karne ko kisne kaha?",
                  "yesno": "Kya delivery wali photo li jaane ke baad edit ki gayi thi?",
                  "where": "Delivery wali photo kahan li gayi thi?"},
        },
        "ts": {
            "boss_alias": "Mentor {first}",
            "job": ("Hello! Ghar baithe part-time job: videos like karo, hotels ko rating do, roz commission kamao. "
                    "Hamare mentor aapse contact karenge."),
            "payout": "Task {i} complete. Rs {amount} commission aapke account mein credit ho gaya.",
            "demand": ("Task {i} prepaid task hai: unlock karne ke liye Rs {amount} deposit karo. Commission ke saath "
                       "wapas milega."),
            "last": "Earning withdraw karne ke liye pehle Rs {amount} tax deposit karo.",
            "deposit": "Rs {amount} bhej diye. Meri earning release karo.",
            "refuse": "Itna intezaam nahi ho payega. Jo pehle se hai wahi release karo.",
            "summary": "{date} ko victim ne anjaan logon ke liye online paid 'tasks' kiye aur paise gawaye.",
            "photo": "victim ke phone ki ek photo",
            "q": {"who": "Victim ko deposit karne ko kisne kaha?",
                  "amount": "Victim ne kul kitne rupaye deposit kiye?"},
        },
        "cc": {
            "desk": "Aapki complaint register ho gayi hai. Refund ke liye hamara technician aapko call karega.",
            "demand": "{owner} ji, maine jo link bheja usse support app install karo aur screen pe jo code aaye wo batao.",
            "control": "Install ho gaya. Code hai {code}.",
            "summary": ("{date} ko victim ne refund ke liye online customer care ka number dhoondha. Thodi der baad "
                        "unke account se paise nikal gaye."),
            "photo": "victim ke phone ki ek photo",
            "q": {"who": "Victim ko screen-sharing app install karne ko kisne kaha?",
                  "when": "Victim ne phone ka control kab saunpa (screen ka code kab bataya)?"},
        },
    },
)
