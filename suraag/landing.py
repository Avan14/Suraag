"""The landing view: what Suraag is, a two-minute interactive taste of citing a line and of the verifier, and the
honest numbers. Rendered as inline HTML (st.html with JS), so it inherits the case-desk styles in suraag/ui/app.css.

The demo lines come from the shipped case upi-ring-001-en, so what a visitor clicks here is real evidence text.
The Hindi strings are a first draft and need a native reader's review, like the rest of i18n.py.
"""
from html import escape as esc

S = {
    "en": {
        "eyebrow": "Forensic teaching tool · synthetic data",
        "title": "Practice cases that are checked before students see them.",
        "lede": "Suraag builds fictional Indian UPI-fraud cases (a WhatsApp chat, a call log and a photo), proves each one "
                "can be solved from the files alone, and grades students on the exact line they cite.",
        "steps": [
            ("Generate", "Code builds the case and plants the clues. An LLM writes only the small talk around them."),
            ("Verify", "Six plain-code checks run on every case. A case that fails is repaired or thrown away, never shipped."),
            ("Cite", "Students answer and click the line that proves it. The grader names the line behind every point."),
        ],
        "try_label": "Try it",
        "try_q": "Who told the mule to delete the transfer record? Click the line you would cite.",
        "verdict_holds": "Holds",
        "verdict_snapped": "Snapped",
        "why": {
            "chat:13": "This line has the instruction and who gave it: Prakash ji.",
            "chat:14": "Nothing here is about deleting a record. And careful: Prakash V. is not Prakash ji.",
            "calls:4": "One minute earlier, the number of Prakash ji called the mule. The call log backs up the chat.",
        },
        "pick": "Pick a line to see how the grader reads it.",
        "watch_label": "Watch the verifier",
        "watch_text": "A recorded run of this case with a planted clash: the instruction line moved 6 minutes, so it no longer "
                      "agrees with the call. The checks catch it, the chat is rewritten, and only then is the case sealed.",
        "watch_btn": "Replay a recorded run",
        "watch_again": "Run again",
        "log": [
            ("", "[A1] initial"),
            ("bad", "✕ F1: chat.txt:13 at 7:04 pm vs calls.csv row 4 at 18:57 differs by 7 min (tolerance 2)"),
            ("", "[A2] regenerate chat (LLM)"),
            ("ok", "✓ every check passes"),
            ("ok", "→ manifest.json sealed"),
        ],
        "verified": "VERIFIED",
        "numbers_label": "What we measured",
        "numbers": [
            ("20 / 20", "planted defects caught by the check meant for them"),
            ("20 / 20", "hybrid cases shipped, against 8 of 19 when the LLM writes the whole chat"),
            ("30 / 30", "answers a second model got right from the files alone"),
        ],
        "limits": "Synthetic cases, one case family, small samples. Hashes show a file has not changed; they do not show "
                  "it is genuine. Not court-validated.",
    },
    "hi": {
        "eyebrow": "फ़ॉरेंसिक शिक्षण टूल · काल्पनिक डेटा",
        "title": "अभ्यास केस, जो छात्रों तक पहुँचने से पहले जाँचे जाते हैं।",
        "lede": "सुराग काल्पनिक भारतीय UPI-धोखाधड़ी के केस बनाता है (एक WhatsApp चैट, एक कॉल लॉग और एक फ़ोटो), साबित करता है "
                "कि हर केस सिर्फ़ फ़ाइलों से हल हो सकता है, और छात्रों को उसी पंक्ति पर अंक देता है जिसका वे हवाला देते हैं।",
        "steps": [
            ("बनाइए", "कोड केस बनाता है और सुराग रखता है। LLM सिर्फ़ उनके आसपास की आम बातचीत लिखता है।"),
            ("जाँचिए", "हर केस पर छह जाँचें चलती हैं। जो केस फ़ेल हो, वह ठीक किया जाता है या हटा दिया जाता है, कभी जारी नहीं होता।"),
            ("हवाला दीजिए", "छात्र उत्तर देते हैं और उसे साबित करने वाली पंक्ति पर क्लिक करते हैं। हर अंक के पीछे की पंक्ति बताई जाती है।"),
        ],
        "try_label": "आज़माइए",
        "try_q": "म्यूल को ट्रांसफ़र रिकॉर्ड मिटाने को किसने कहा? वह पंक्ति चुनिए जिसका आप हवाला देंगे।",
        "verdict_holds": "सही बैठता है",
        "verdict_snapped": "नहीं टिकता",
        "why": {
            "chat:13": "इस पंक्ति में निर्देश है और यह भी कि किसने दिया: Prakash ji।",
            "chat:14": "यहाँ रिकॉर्ड मिटाने की कोई बात नहीं। और ध्यान दें: Prakash V. और Prakash ji अलग लोग हैं।",
            "calls:4": "एक मिनट पहले Prakash ji के नंबर से म्यूल को कॉल आया। कॉल लॉग चैट की पुष्टि करता है।",
        },
        "pick": "कोई पंक्ति चुनिए और देखिए कि ग्रेडर उसे कैसे पढ़ता है।",
        "watch_label": "जाँचकर्ता को काम करते देखिए",
        "watch_text": "इसी केस का एक दर्ज रन, जिसमें टकराव डाला गया: निर्देश वाली पंक्ति 6 मिनट खिसकाई गई, इसलिए वह कॉल से मेल नहीं "
                      "खाती। जाँचें उसे पकड़ती हैं, चैट फिर से लिखी जाती है, और तभी केस सील होता है।",
        "watch_btn": "दर्ज किया गया रन दोबारा देखिए",
        "watch_again": "फिर से चलाइए",
        "log": [
            ("", "[A1] पहला प्रयास"),
            ("bad", "✕ F1: chat.txt:13 पर 7:04 pm बनाम calls.csv रो 4 पर 18:57; अंतर 7 मिनट (सहनसीमा 2)"),
            ("", "[A2] चैट फिर से लिखी (LLM)"),
            ("ok", "✓ हर जाँच पास"),
            ("ok", "→ manifest.json सील हुआ"),
        ],
        "verified": "सत्यापित",
        "numbers_label": "हमने क्या मापा",
        "numbers": [
            ("20 / 20", "डाले गए दोष, जिन्हें उनके लिए बनी जाँच ने पकड़ा"),
            ("20 / 20", "हाइब्रिड केस जारी हुए; जब LLM पूरी चैट लिखता है तो 19 में से 8"),
            ("30 / 30", "उत्तर, जो दूसरे मॉडल ने सिर्फ़ फ़ाइलों से सही दिए"),
        ],
        "limits": "काल्पनिक केस, एक ही तरह के केस, छोटे नमूने। हैश बताता है कि फ़ाइल बदली नहीं; यह नहीं कि वह असली है। "
                  "अदालत में जाँचा नहीं गया।",
    },
}

# Real lines from the shipped case upi-ring-001-en (evidence text is never translated).
DEMO = [
    ("chat:13", "chat.txt:13", "16/04/26, 6:58 pm - Prakash ji: Mahesh ji, delete the transfer record right now", True),
    ("chat:14", "chat.txt:14", "16/04/26, 6:59 pm - Prakash V.: Great, I am leaving my house now.", False),
    ("calls:4", "calls.csv:4", "2026-04-16T18:57:00+05:30, incoming, +91-57297-34908, Prakash ji, 47", True),
]


def hero_html(lang: str) -> str:
    s = S.get(lang, S["en"])
    return (f'<section class="land-hero"><div class="land-eyebrow">{esc(s["eyebrow"])}</div>'
            f'<div class="land-title" role="heading" aria-level="1">{esc(s["title"])}</div>'
            f'<p class="land-lede">{esc(s["lede"])}</p></section>')


def body_html(lang: str) -> str:
    s = S.get(lang, S["en"])
    steps = "".join(f'<li class="land-step"><span class="land-num">{i}</span><div><div class="land-step-title">{esc(t)}</div>'
                    f'<p>{esc(d)}</p></div></li>' for i, (t, d) in enumerate(s["steps"], 1))
    rows = "".join(f'<button type="button" class="demo-row" data-key="{k}" data-holds="{str(ok).lower()}" '
                   f'data-why="{esc(s["why"][k])}" aria-pressed="false">'
                   f'<span class="demo-loc">{esc(loc)}</span><span class="demo-text">{esc(text)}</span></button>'
                   for k, loc, text, ok in DEMO)
    log = "".join(f'<div class="ln {k}">{esc(x)}</div>' for k, x in s["log"])
    nums = "".join(f'<div class="land-stat"><div class="land-stat-n">{esc(n)}</div><p>{esc(d)}</p></div>' for n, d in s["numbers"])
    return f'''
<section class="land">
  <ol class="land-steps">{steps}</ol>

  <div class="land-grid">
    <section class="land-card" id="demo">
      <div class="land-card-label">{esc(s["try_label"])}</div>
      <p class="land-q">{esc(s["try_q"])}</p>
      <div class="demo-rows" role="group" aria-label="{esc(s["try_label"])}">{rows}</div>
      <div class="demo-verdict" aria-live="polite" data-holds="{esc(s["verdict_holds"])}" data-snapped="{esc(s["verdict_snapped"])}"><p class="demo-hint">{esc(s["pick"])}</p></div>
    </section>

    <section class="land-card" id="watch">
      <div class="land-card-label">{esc(s["watch_label"])}</div>
      <p class="land-q">{esc(s["watch_text"])}</p>
      <div class="watch-log log" aria-live="polite">{log}</div>
      <div class="watch-foot">
        <button type="button" class="land-btn" data-again="{esc(s["watch_again"])}">{esc(s["watch_btn"])}</button>
        <span class="stamp ok big watch-stamp" aria-hidden="true">{esc(s["verified"])}</span>
      </div>
    </section>
  </div>

  <section class="land-numbers">
    <div class="land-card-label">{esc(s["numbers_label"])}</div>
    <div class="land-stats">{nums}</div>
    <p class="land-limits">{esc(s["limits"])}</p>
  </section>
</section>
<script>
/* No less-than sign anywhere in this script: Streamlit's sanitiser drops a script whose text has one before a letter or slash. */
/* One document-level listener, installed once: Streamlit may draw this HTML before or after the script runs, */
/* and redraws it on every rerun, so nothing is bound to particular elements. */
if (!window.__suraagLanding) {{
  window.__suraagLanding = true;
  document.addEventListener("click", (e) => {{
    const row = e.target.closest(".demo-row");
    if (row) {{
      /* Try it: show how the grader reads the line. Feedback only; transitions, so rapid clicks retarget. */
      const land = row.closest(".land");
      land.querySelectorAll(".demo-row").forEach((r) => {{ r.classList.remove("is-holds", "is-snapped"); r.setAttribute("aria-pressed", "false"); }});
      const holds = row.dataset.holds === "true";
      row.classList.add(holds ? "is-holds" : "is-snapped");
      row.setAttribute("aria-pressed", "true");
      const v = land.querySelector(".demo-verdict");
      const stamp = document.createElement("span");
      stamp.className = "stamp " + (holds ? "ok" : "bad") + " demo-stamp";
      stamp.textContent = (holds ? "✓ " : "✕ ") + (holds ? v.dataset.holds : v.dataset.snapped);
      const why = document.createElement("p");
      why.className = "demo-why";
      why.textContent = row.dataset.why;
      v.replaceChildren(stamp, why);
      return;
    }}
    const btn = e.target.closest(".land-btn");
    if (btn) {{
      /* Watch the verifier: an explanation, so it plays at reading pace, and only when asked. */
      const watch = btn.closest("#watch");
      watch.classList.remove("playing");
      void watch.offsetWidth;            /* restart the CSS animations from the first line */
      watch.classList.add("playing");
      btn.textContent = btn.dataset.again;
    }}
  }});
}}
</script>'''
