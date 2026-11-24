"""t(key, lang) for the English/Hindi UI, plus renderers for verifier failures and grader explanations.

Rules: sentence case, no emoji (only the glyphs ✓ ✕ → ↑), name exact evidence (`chat.txt:5`), the grader
states facts and never praise or blame. Evidence text (chat lines, CSV rows, EXIF values) is never
translated. The Hindi strings are a first draft and NEED A NATIVE READER'S REVIEW before release.
"""
from typing import Literal

Lang = Literal["en", "hi"]

EN: dict[str, str] = {
    # app chrome
    "app.tagline": "Verified forensic practice cases. Cite the exact line.",
    "ui.language": "Language",
    "ui.tab_lecturer": "Lecturer",
    "ui.tab_student": "Student",
    "ui.tab_eval": "Evaluation",
    "ui.synthetic": "SYNTHETIC CASE: fictional, for teaching only. Not real data.",
    "ui.synthetic_tag": "SYNTHETIC",
    "ui.view": "View",
    "ui.choose": "Choose an option",
    "act.initial": "initial",
    "act.regenerate chat (LLM)": "regenerate chat (LLM)",
    "act.re-render calls": "re-render calls",
    "act.re-render photo": "re-render photo",
    "act.re-render": "re-render",
    "lec.generating": "Generating and checking the case",
    "ui.case": "Case",
    "ui.no_cases": "No cases found. Generate one in the Lecturer tab.",
    # lecturer
    "lec.generate": "Generate a new case",
    "lec.seed": "Seed",
    "lec.mode": "Language of the case",
    "lec.plant": "Plant a defect (demo)",
    "lec.defect": "Defect type",
    "lec.defect_target": "Plant it in",
    "lec.run": "Generate and verify",
    "lec.lab_sheet": "Lab sheet: six checks",
    "lec.log": "Run log",
    "lec.attempt": "Attempt {n}: {action}",
    "lec.pass": "pass",
    "lec.fail": "fail",
    "lec.repaired": "Repaired and passed after {n} attempts.",
    "lec.discarded": "Discarded: it could not be repaired in {n} attempts. The failure is logged.",
    "lec.certificate": "Case certificate",
    "lec.hashes": "SHA-256 of each file",
    "lec.hash_note": "A matching hash shows this file has not changed since the hash was computed; it does not show who made the file or that its content is genuine.",
    "lec.zip_student": "Download student files (ZIP)",
    "lec.zip_key": "Download answer key (JSON)",
    "lec.stub_notice": "The LLM was unavailable, so offline stub filler was used.",
    "lec.cap": "Daily generation limit reached ({cap}). Open a pre-generated case instead.",
    "lec.defects_help": "A planted defect shows the verifier catching a contradiction and repairing it.",
    "lec.override": "Instructor override: an unverified rationale is flagged here, never scored silently.",
    # the six checks
    "check.anchor": "Anchors: each evidence string is at its stated line, row or tag",
    "check.traceability": "Traceability: every fact has an anchor, every question has facts",
    "check.contradiction": "Contradictions: times agree, each alias is one person, causes come first",
    "check.solvability": "Solvability: a solver reproduces the key from the files alone",
    "check.distractor": "Distractor: a plausible wrong suspect exists and does not fool the solver",
    "check.integrity": "Integrity: file hashes sealed after every check passed",
    "check.filler_count": "Filler: the chat has the right number of lines",
    # student
    "stu.question": "Question {n}",
    "stu.answer": "Your answer",
    "stu.answer_person": "Pick a person",
    "stu.answer_place": "Pick a place",
    "stu.answer_time": "Time (for example 9:14 pm or 21:14)",
    "stu.cite": "Click lines in the files to cite them as evidence for this question.",
    "stu.cited": "Cited: {n}",
    "stu.rationale": "Your reasoning (optional)",
    "stu.submit": "Submit answers",
    "stu.score": "Score",
    "stu.points": "{n} of {m} points",
    "stu.answer_point": "Answer",
    "stu.evidence_point": "Evidence",
    "stu.earned": "earned",
    "stu.lost": "not earned",
    "stu.holds": "✓ holds",
    "stu.snapped": "✕ does not support",
    "stu.partial": "partly supports",
    "stu.flagged": "Could not verify: flagged for the instructor.",
    "stu.flag_overclaim": "Advisory: the conclusion may go further than the cited evidence. Not scored.",
    "stu.flag_ok": "Advisory: the conclusion stays within the cited evidence. Not scored.",
    "stu.suspects": "Suspects",
    "stu.places": "Places",
    "stu.lab": "Lab team",
    "stu.files": "Evidence files",
    # hints and read-aloud
    "hint.title": "Hint",
    "hint.next": "Show the next hint",
    "hint.persona": "Hint style",
    "hint.none_left": "No more hints for this question.",
    "persona.plain": "Plain",
    "persona.vetaal": "Vetaal",
    "persona.birbal": "Birbal",
    "speak.read": "Read aloud",
    "speak.mute": "Mute read-aloud",
    "speak.no_voice": "No Hindi voice is installed on this device, so the hint is shown as text only.",
    # hint text, by tier
    "hint.t1": "The evidence for this question is in {files}.",
    "hint.t2": "Look at {where}.",
    "hint.t3": "Check {locs}.",
    "hint.where.chat": "chat.txt lines {a} to {b}",
    "hint.where.calls": "calls.csv rows {a} to {b}",
    "hint.where.photo": "photo.jpg tags {tags}",
    "hint.persona.plain.pre": "",
    "hint.persona.plain.post": "",
    "hint.persona.vetaal.pre": "Listen, king, here is a riddle with a clue: ",
    "hint.persona.vetaal.post": " Now answer, or your head will split!",
    "hint.persona.birbal.pre": "Your Majesty, a wise man looks at the proof first: ",
    "hint.persona.birbal.post": " Judge by evidence, not by suspicion.",
    # evaluation
    "eval.title": "Evaluation",
    "eval.note": "All data is synthetic. Sample sizes are shown next to every figure. Limits: small n, one case family, not court-validated.",
    "eval.n": "n = {n}",
    "eval.empty": "No results yet. Run the evaluation scripts in eval/.",
    # verifier failures
    "fail.anchor_missing": "{loc} does not contain {needle!r}",
    "fail.anchor_nonexistent": "{loc} does not exist",
    "fail.anchor_missing_raw": "{file}: no line contains {wanted}",
    "fail.time_order": "chat.txt:{line} time {t} is earlier than chat.txt:{prev} time {prev_t}",
    "fail.alias_unresolved": "chat.txt:{line} sender {sender!r} resolves to {count} people",
    "fail.trigger_in_filler": "chat.txt:{line} matches the instruction phrase but is not the instruction line",
    "fail.filler_content": "chat.txt:{line} filler contains {reason_text}",
    "filler.reason.digit": "a digit",
    "filler.reason.currency": "a currency or amount word",
    "filler.reason.date": "a month or weekday name",
    "filler.reason.url": "a web address",
    "filler.reason.brand": "a real brand, bank or app name",
    "filler.reason.instruction": "an instruction verb (delete, send, pay, transfer ...)",
    "fail.fact_no_anchor": "{fact} has no anchor in any artifact",
    "fail.question_no_fact": "{question} does not map to any fact",
    "fail.cross_time": "{fact}: chat.txt:{chat_line} at {chat_t} vs calls.csv row {row} at {call_t} differs by {diff:g} min (tolerance {tol})",
    "fail.cause_after_effect": "{event} happens before its cause {cause}",
    "fail.solver_mismatch": "{question}: solver answered {got}, key is {key}",
    "fail.no_distractor": "the case has no distractor fact",
    "fail.distractor_implausible": "{fact} is not plausible: far from the key event and no similar alias",
    "fail.solver_picked_distractor": "the solver picked the distractor {actor} for {question}",
    "fail.filler_short": "chat.txt: filler has {got} messages, {needed} needed",
    "fail.llm_unavailable": "chat.txt: the LLM is unavailable ({reason})",
    # grader explanations
    "expl.answer_ok": "{question}: your answer is consistent with the evidence.",
    "expl.answer_wrong": "{question}: your answer does not match what the evidence supports.",
    "expl.cite_valid": "{loc} contains the evidence for this claim.",
    "expl.cite_partial": "{loc} contains {has_and} but not {missing_and}. A supporting line is {support}.",
    "expl.cite_wrong": "{loc} contains neither {needles_nor}. A supporting line is {support}.",
    "expl.cite_nonexistent": "{loc} does not exist in this case's files.",
    "expl.cite_irrelevant": "{artifact} holds no evidence for this question.",
    "expl.cite_missing_artifact": "You cited no valid line in {artifact}. A supporting line is {support}.",
}

HI: dict[str, str] = {
    "app.tagline": "सत्यापित फ़ॉरेंसिक अभ्यास केस। सटीक पंक्ति का हवाला दें।",
    "ui.language": "भाषा",
    "ui.tab_lecturer": "प्राध्यापक",
    "ui.tab_student": "छात्र",
    "ui.tab_eval": "मूल्यांकन",
    "ui.synthetic": "काल्पनिक केस: केवल शिक्षण के लिए। असली डेटा नहीं।",
    "ui.synthetic_tag": "काल्पनिक",
    "ui.view": "दृश्य",
    "ui.choose": "एक विकल्प चुनें",
    "act.initial": "पहला प्रयास",
    "act.regenerate chat (LLM)": "चैट फिर से लिखी (LLM)",
    "act.re-render calls": "कॉल लॉग फिर से बनाया",
    "act.re-render photo": "फ़ोटो फिर से बनाई",
    "act.re-render": "फिर से बनाया",
    "lec.generating": "केस बनाया और जाँचा जा रहा है",
    "ui.case": "केस",
    "ui.no_cases": "कोई केस नहीं मिला। प्राध्यापक टैब में नया बनाएँ।",
    "lec.generate": "नया केस बनाएँ",
    "lec.seed": "सीड",
    "lec.mode": "केस की भाषा",
    "lec.plant": "दोष डालें (डेमो)",
    "lec.defect": "दोष का प्रकार",
    "lec.defect_target": "इसमें डालें",
    "lec.run": "बनाएँ और जाँचें",
    "lec.lab_sheet": "लैब शीट: छह जाँचें",
    "lec.log": "रन लॉग",
    "lec.attempt": "प्रयास {n}: {action}",
    "lec.pass": "पास",
    "lec.fail": "फ़ेल",
    "lec.repaired": "{n} प्रयासों में मरम्मत हुई और जाँच पास हुई।",
    "lec.discarded": "रद्द: {n} प्रयासों में मरम्मत नहीं हो सकी। विफलता दर्ज है।",
    "lec.certificate": "केस प्रमाणपत्र",
    "lec.hashes": "हर फ़ाइल का SHA-256",
    "lec.hash_note": "मिलता हुआ हैश दिखाता है कि हैश बनने के बाद फ़ाइल बदली नहीं गई; यह नहीं दिखाता कि फ़ाइल किसने बनाई या उसकी सामग्री असली है।",
    "lec.zip_student": "छात्रों की फ़ाइलें डाउनलोड करें (ZIP)",
    "lec.zip_key": "उत्तर कुंजी डाउनलोड करें (JSON)",
    "lec.stub_notice": "LLM उपलब्ध नहीं था, इसलिए ऑफ़लाइन स्टब भराव इस्तेमाल हुआ।",
    "lec.cap": "रोज़ की सीमा ({cap}) पूरी हो गई। पहले से बना केस खोलें।",
    "lec.defects_help": "डाला गया दोष दिखाता है कि जाँच विरोधाभास पकड़कर उसकी मरम्मत करती है।",
    "lec.override": "प्राध्यापक का अधिकार: असत्यापित तर्क यहाँ चिह्नित होता है, चुपचाप अंक नहीं मिलते।",
    "check.anchor": "आधार: हर साक्ष्य-शब्द अपनी बताई पंक्ति, रो या टैग में है",
    "check.traceability": "पता लगाने योग्यता: हर तथ्य का आधार है, हर प्रश्न तथ्यों से जुड़ा है",
    "check.contradiction": "विरोधाभास: समय मेल खाते हैं, हर उपनाम एक ही व्यक्ति का है, कारण पहले आता है",
    "check.solvability": "हल होने की जाँच: सॉल्वर केवल फ़ाइलों से कुंजी दोहरा लेता है",
    "check.distractor": "भ्रामक तथ्य: एक विश्वसनीय ग़लत संदिग्ध है और सॉल्वर को भ्रमित नहीं करता",
    "check.integrity": "अखंडता: सभी जाँच पास होने के बाद फ़ाइलों के हैश सील हुए",
    "check.filler_count": "भराव: चैट में पंक्तियों की सही संख्या है",
    "stu.question": "प्रश्न {n}",
    "stu.answer": "आपका उत्तर",
    "stu.answer_person": "व्यक्ति चुनें",
    "stu.answer_place": "स्थान चुनें",
    "stu.answer_time": "समय (जैसे 9:14 pm या 21:14)",
    "stu.cite": "इस प्रश्न के साक्ष्य के रूप में फ़ाइलों की पंक्तियों पर क्लिक करें।",
    "stu.cited": "चुनी गईं: {n}",
    "stu.rationale": "आपका तर्क (वैकल्पिक)",
    "stu.submit": "उत्तर जमा करें",
    "stu.score": "अंक",
    "stu.points": "{m} में से {n} अंक",
    "stu.answer_point": "उत्तर",
    "stu.evidence_point": "साक्ष्य",
    "stu.earned": "मिला",
    "stu.lost": "नहीं मिला",
    "stu.holds": "✓ सही बैठता है",
    "stu.snapped": "✕ समर्थन नहीं करता",
    "stu.partial": "आंशिक समर्थन",
    "stu.flagged": "सत्यापित नहीं हो सका: प्राध्यापक के लिए चिह्नित।",
    "stu.flag_overclaim": "सलाह: निष्कर्ष चुने गए साक्ष्य से आगे जा सकता है। अंक नहीं जुड़ते।",
    "stu.flag_ok": "सलाह: निष्कर्ष चुने गए साक्ष्य के भीतर है। अंक नहीं जुड़ते।",
    "stu.suspects": "संदिग्ध",
    "stu.places": "स्थान",
    "stu.lab": "लैब टीम",
    "stu.files": "साक्ष्य फ़ाइलें",
    "hint.title": "संकेत",
    "hint.next": "अगला संकेत दिखाएँ",
    "hint.persona": "संकेत की शैली",
    "hint.none_left": "इस प्रश्न के लिए और संकेत नहीं हैं।",
    "persona.plain": "सादा",
    "persona.vetaal": "बेताल",
    "persona.birbal": "बीरबल",
    "speak.read": "ज़ोर से पढ़ें",
    "speak.mute": "आवाज़ बंद करें",
    "speak.no_voice": "इस डिवाइस पर हिंदी आवाज़ नहीं है, इसलिए संकेत केवल लिखित दिखाया गया है।",
    "hint.t1": "इस प्रश्न का साक्ष्य {files} में है।",
    "hint.t2": "{where} देखें।",
    "hint.t3": "{locs} जाँचें।",
    "hint.where.chat": "chat.txt की पंक्तियाँ {a} से {b}",
    "hint.where.calls": "calls.csv की रो {a} से {b}",
    "hint.where.photo": "photo.jpg के टैग {tags}",
    "hint.persona.plain.pre": "",
    "hint.persona.plain.post": "",
    "hint.persona.vetaal.pre": "सुनो राजा, एक पहेली और एक सुराग: ",
    "hint.persona.vetaal.post": " अब उत्तर दो, वरना सिर के टुकड़े हो जाएँगे!",
    "hint.persona.birbal.pre": "जहाँपनाह, समझदार पहले सबूत देखता है: ",
    "hint.persona.birbal.post": " फ़ैसला सबूत से कीजिए, शक से नहीं।",
    "eval.title": "मूल्यांकन",
    "eval.note": "सारा डेटा काल्पनिक है। हर आँकड़े के साथ नमूने का आकार दिया गया है। सीमाएँ: छोटा n, एक केस-परिवार, अदालत में मान्य नहीं।",
    "eval.n": "n = {n}",
    "eval.empty": "अभी कोई परिणाम नहीं। eval/ की स्क्रिप्ट चलाएँ।",
    "fail.anchor_missing": "{loc} में {needle!r} नहीं है",
    "fail.anchor_nonexistent": "{loc} मौजूद नहीं है",
    "fail.anchor_missing_raw": "{file}: किसी भी पंक्ति में {wanted} नहीं है",
    "fail.time_order": "chat.txt:{line} का समय {t}, chat.txt:{prev} के समय {prev_t} से पहले का है",
    "fail.alias_unresolved": "chat.txt:{line} का भेजने वाला {sender!r} {count} व्यक्तियों से मेल खाता है",
    "fail.trigger_in_filler": "chat.txt:{line} निर्देश वाले वाक्यांश से मेल खाती है, पर यह निर्देश वाली पंक्ति नहीं है",
    "fail.filler_content": "chat.txt:{line} के भराव में {reason_text} है",
    "filler.reason.digit": "कोई अंक",
    "filler.reason.currency": "मुद्रा या राशि का शब्द",
    "filler.reason.date": "महीने या सप्ताह के दिन का नाम",
    "filler.reason.url": "वेब पता",
    "filler.reason.brand": "किसी असली ब्रांड, बैंक या ऐप का नाम",
    "filler.reason.instruction": "निर्देश वाली क्रिया (delete, send, pay, transfer ...)",
    "fail.fact_no_anchor": "{fact} का किसी भी फ़ाइल में कोई आधार नहीं है",
    "fail.question_no_fact": "{question} किसी तथ्य से जुड़ा नहीं है",
    "fail.cross_time": "{fact}: chat.txt:{chat_line} पर {chat_t} बनाम calls.csv रो {row} पर {call_t}; अंतर {diff:g} मिनट (सहनसीमा {tol})",
    "fail.cause_after_effect": "{event} अपने कारण {cause} से पहले हो रहा है",
    "fail.solver_mismatch": "{question}: सॉल्वर का उत्तर {got}, कुंजी {key}",
    "fail.no_distractor": "केस में कोई भ्रामक तथ्य नहीं है",
    "fail.distractor_implausible": "{fact} विश्वसनीय नहीं है: मुख्य घटना से दूर और कोई मिलता-जुलता उपनाम नहीं",
    "fail.solver_picked_distractor": "सॉल्वर ने {question} के लिए भ्रामक व्यक्ति {actor} चुना",
    "fail.filler_short": "chat.txt: भराव में {got} संदेश हैं, {needed} चाहिए",
    "fail.llm_unavailable": "chat.txt: LLM उपलब्ध नहीं है ({reason})",
    "expl.answer_ok": "{question}: आपका उत्तर साक्ष्य से मेल खाता है।",
    "expl.answer_wrong": "{question}: आपका उत्तर साक्ष्य से समर्थित उत्तर से मेल नहीं खाता।",
    "expl.cite_valid": "{loc} में इस दावे का साक्ष्य मौजूद है।",
    "expl.cite_partial": "{loc} में {has_and} है, पर {missing_and} नहीं है। एक समर्थक पंक्ति {support} है।",
    "expl.cite_wrong": "{loc} में इनमें से कुछ भी नहीं है: {needles_slash}। एक समर्थक पंक्ति {support} है।",
    "expl.cite_nonexistent": "{loc} इस केस की फ़ाइलों में मौजूद नहीं है।",
    "expl.cite_irrelevant": "इस प्रश्न के लिए {artifact} में कोई साक्ष्य नहीं है।",
    "expl.cite_missing_artifact": "आपने {artifact} में कोई मान्य पंक्ति नहीं चुनी। एक समर्थक पंक्ति {support} है।",
}

STRINGS: dict[str, dict[str, str]] = {"en": EN, "hi": HI}


def t(key: str, lang: str = "en", /, **params) -> str:
    """Look a string up by key; unknown languages fall back to English; a missing key raises."""
    table = STRINGS.get(lang, EN)
    text = table[key] if key in table else EN[key]
    return text.format(**params) if params else text


def _fmt_lists(params: dict) -> dict:
    """Pre-format list params so templates can stay simple. Evidence strings are never translated."""
    out = dict(params)
    q = lambda xs: [f'"{x}"' for x in xs]  # noqa: E731
    if "needles" in out:
        out["needles_nor"] = " nor ".join(q(out["needles"]))
        out["needles_slash"] = " / ".join(q(out["needles"]))
    if "has" in out:
        out["has_and"] = " and ".join(q(out["has"]))
    if "missing" in out:
        out["missing_and"] = " and ".join(q(out["missing"]))
    return out


def render_failure(f, lang: str = "en") -> str:
    """A verifier Failure in the chosen language, from its code and params."""
    key = f"fail.{f.code}"
    if f.code == "anchor_missing":
        key = ("fail.anchor_missing" if "needle" in f.params else
               "fail.anchor_missing_raw" if "wanted" in f.params else "fail.anchor_nonexistent")
    params = dict(f.params)
    if f.code == "filler_content":
        params["reason_text"] = t(f"filler.reason.{params['reason']}", lang)
    return t(key, lang, **params)


def render_expl(e, lang: str = "en") -> str:
    """A grader Expl in the chosen language."""
    params = _fmt_lists(e.params)
    if lang == "hi" and "has" in params:  # Hindi joins with और
        params["has_and"] = " और ".join(f'"{x}"' for x in e.params["has"])
        params["missing_and"] = " और ".join(f'"{x}"' for x in e.params["missing"])
    return t(f"expl.{e.code}", lang, **params)
