"""Suraag: verified Indian forensic practice cases, graded on the exact evidence a student cites.

Three views. Lecturer: generate a case, plant a defect and watch the verifier catch and repair it, then
read the certificate. Student: read the files, click lines to cite them, answer, and see the deterministic
grader explain each point. Evaluation: the numbers, with sample sizes. All data is synthetic.
"""
import base64
import csv
import datetime as dt
import io
import json
import os
import tempfile
import zipfile
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from suraag import filler as filler_module
from suraag.defects import EXPECTED
from suraag.grade import Citation, Claim, grade_all
from suraag.hints import PERSONAS, SPEECH, TIERS, hint
from suraag.i18n import render_expl, render_failure, t
from suraag.model import Brief, Case
from suraag.parse import Artifacts, load_calls, load_chat, load_exif
from suraag.pipeline import generate_case
from suraag.verify import verify

ROOT = Path(__file__).parent
CASES = ROOT / "cases"
DAILY_CAP = 20
CHECKS = ["anchor", "traceability", "contradiction", "solvability", "distractor"]

canvas = components.declare_component("suraag_canvas", path=str(ROOT / "suraag" / "components" / "canvas"))
speak = components.declare_component("suraag_speak", path=str(ROOT / "suraag" / "components" / "speak"))

st.set_page_config(page_title="Suraag", page_icon=None, layout="wide")

# On Streamlit Community Cloud the key lives in secrets; mirror it into the environment for llm.py.
try:
    for _k in ("GEMINI_API_KEY", "SURAAG_MODEL_FILLER", "SURAAG_MODEL_SOLVER"):
        if _k in st.secrets and _k not in os.environ:
            os.environ[_k] = str(st.secrets[_k])
except Exception:
    pass


@st.cache_resource
def _live_counter() -> dict:
    return {"day": dt.date.today().isoformat(), "n": 0}  # per process; resets on restart, which is fine


def _take_generation() -> bool:
    c = _live_counter()
    if c["day"] != dt.date.today().isoformat():
        c.update(day=dt.date.today().isoformat(), n=0)
    if c["n"] >= DAILY_CAP:
        return False
    c["n"] += 1
    return True


# ---------------------------------------------------------------------------------------- style
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600&family=Noto+Serif+Devanagari:wght@600;700&display=swap');
:root { --ink-1:#1B1D21; --ink-2:#3B3F47; --ink-3:#6B6F78; --border-1:#E2E0DA; --success:#2E7D52; --success-tint:#EEF6F0; --danger:#C2412F; --danger-tint:#FCF1EF; }
.stApp, .stApp p, .stApp label, .stApp button, .stApp input, .stApp textarea, .stApp [data-baseweb] { font-family: 'IBM Plex Sans','Noto Sans Devanagari',system-ui,sans-serif; }
/* Never override Streamlit's icon font: its icons are ligatures, and a text font turns them into the words ("arrow_down"). */
[data-testid="stIconMaterial"], .material-symbols-rounded, [class*="material-symbols"] { font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important; }
.block-container { padding-top: 1rem; max-width: 1500px; }
/* The Deploy toolbar would sit on top of our top bar, and a public demo does not need it. */
header[data-testid="stHeader"], [data-testid="stAppToolbar"], [data-testid="stToolbar"] { display: none; }
.topbar { display:flex; align-items:center; gap:14px; height:56px; padding:0 4px; border-bottom:1px solid var(--border-1); margin-bottom:6px; background:#fff; }
.topbar .wordmark { font-family:'Noto Serif Devanagari',Georgia,serif; font-weight:700; font-size:24px; color:var(--ink-1); }
.topbar .brand { font-weight:700; letter-spacing:.14em; font-size:13px; color:var(--ink-2); }
.topbar .tagline { color:var(--ink-3); font-size:13px; }
.synthetic { display:inline-block; border:1px solid var(--danger); color:var(--danger); border-radius:4px; padding:2px 8px; font:600 11px/1.4 'IBM Plex Sans',sans-serif; letter-spacing:.06em; margin:2px 0 8px; }
.stTabs [data-baseweb="tab-list"] { gap:4px; border-bottom:1px solid var(--border-1); }
.stTabs [aria-selected="true"] { border-bottom:2px solid var(--danger) !important; color:var(--ink-1) !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color:var(--danger) !important; }
.stButton > button, .stDownloadButton > button { border-radius:6px; border:1px solid var(--border-1); transition:background-color .12s ease-out, border-color .12s ease-out; }
.stButton > button[kind="primary"] { background:#1B1D21; color:#fff; border-color:#1B1D21; }
.stButton > button[kind="primary"]:hover { background:#33363C; }
table.lab { border-collapse:collapse; width:100%; font-size:13px; background:#fff; }
table.lab th, table.lab td { border:1px solid var(--border-1); padding:6px 10px; text-align:left; vertical-align:top; }
table.lab th { background:#F7F6F3; font-weight:600; letter-spacing:.04em; }
.ok { color:var(--success); font-weight:600; } .bad { color:var(--danger); font-weight:600; } .dim { color:var(--ink-3); }
.msg { font-family:'IBM Plex Mono',monospace; font-size:12.5px; background:var(--danger-tint); border-left:3px solid var(--danger); padding:6px 10px; margin:4px 0; border-radius:4px; }
.msg.pass { background:var(--success-tint); border-left-color:var(--success); }
.cert { background:#fff; border:1px solid var(--border-1); border-radius:8px; padding:14px 16px; box-shadow:0 1px 2px rgba(60,40,15,.08), 0 3px 6px -2px rgba(60,40,15,.08); }
.cert code { font-family:'IBM Plex Mono',monospace; font-size:12px; word-break:break-all; }
.score { font-size:44px; font-weight:600; line-height:1; }
.pt { font-size:13px; } .expl { font-size:13px; color:var(--ink-2); margin:2px 0; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------------------- helpers
# Read the language switch first: the top bar is drawn before the radio itself is.
st.session_state["lang"] = "hi" if st.session_state.get("lang_choice") == "हिन्दी" else "en"


def L(key: str, **kw) -> str:
    return t(key, st.session_state["lang"], **kw)


def available_cases() -> dict[str, Path]:
    found = {p.parent.name: p.parent for p in sorted(CASES.glob("*/manifest.json"))}
    found.update(st.session_state.get("live_cases", {}))
    return found


@st.cache_data(show_spinner=False)
def load_dir(path: str):
    p = Path(path)
    case = Case.model_validate_json((p / "case.json").read_text("utf-8"))
    return case, Artifacts.from_dir(p), json.loads((p / "manifest.json").read_text("utf-8"))


def lab_table(attempts, sealed: bool) -> str:
    cols = "".join(f"<th>A{a.n}</th>" for a in attempts)
    rows = []
    shown = [c for c in CHECKS + ["filler_count"] if c in CHECKS or any(f.check == c for a in attempts for f in a.failures)]
    for c in shown:
        cells = "".join(
            f'<td class="{"bad" if any(f.check == c for f in a.failures) else "ok"}">'
            f'{"✕ " + L("lec.fail") if any(f.check == c for f in a.failures) else "✓ " + L("lec.pass")}</td>' for a in attempts)
        rows.append(f"<tr><th>{L('check.' + c)}</th>{cells}</tr>")
    last = attempts[-1]
    cells = "".join(f'<td class="dim">–</td>' for _ in attempts[:-1])
    cells += f'<td class="{"ok" if sealed else "dim"}">{"✓ " + L("lec.pass") if sealed else "–"}</td>'
    rows.append(f"<tr><th>{L('check.integrity')}</th>{cells}</tr>")
    return f'<table class="lab"><tr><th></th>{cols}</tr>{"".join(rows)}</table>'


def attempt_html(a) -> str:
    head = f"<b>{L('lec.attempt', n=a.n, action=a.action)}</b>"
    if not a.failures:
        return f'{head}<div class="msg pass">✓ {L("lec.pass")}</div>'
    return head + "".join(f'<div class="msg">✕ {render_failure(f, st.session_state["lang"])}</div>' for f in a.failures)


def make_zip(path: Path, student: bool) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name in (("chat.txt", "calls.csv", "photo.jpg", "manifest.json", "brief.md") if student else ("case.json",)):
            if (path / name).exists():
                z.write(path / name, name)
    return buf.getvalue()


def certificate(manifest: dict, path: Path, key: str) -> None:
    files = "".join(f"<div><b>{n}</b><br><code>{h}</code></div>" for n, h in manifest["files"].items())
    stub = f'<div class="msg">{L("lec.stub_notice")}</div>' if manifest.get("model") == "stub" else ""
    st.markdown(
        f'<div class="cert"><b>{L("lec.certificate")}</b>: {manifest["case_id"]} ({manifest["lang"]}, {manifest["mode"]}), '
        f'seed {manifest["seed"]}, model <code>{manifest["model"]}</code><br><br><b>{L("lec.hashes")}</b>{files}'
        f'<p class="dim" style="margin-top:10px">{L("lec.hash_note")}</p>{stub}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.download_button(L("lec.zip_student"), make_zip(path, True), f"{path.name}-student.zip", key=f"zs-{key}")
    c2.download_button(L("lec.zip_key"), make_zip(path, False), f"{path.name}-key.zip", key=f"zk-{key}")


# ---------------------------------------------------------------------------------------- header
hc1, hc2 = st.columns([5, 1])
hc1.markdown(f'<div class="topbar"><span class="wordmark">सुराग</span><span class="brand">SURAAG</span>'
             f'<span class="tagline">{L("app.tagline")}</span></div>', unsafe_allow_html=True)
hc2.radio(L("ui.language"), ["EN", "हिन्दी"], horizontal=True, key="lang_choice")
st.markdown(f'<span class="synthetic">{L("ui.synthetic")}</span>', unsafe_allow_html=True)

tab_lec, tab_stu, tab_eval = st.tabs([L("ui.tab_lecturer"), L("ui.tab_student"), L("ui.tab_eval")])

# ---------------------------------------------------------------------------------------- lecturer
with tab_lec:
    left, right = st.columns([1, 1.6])
    with left:
        st.subheader(L("lec.generate"))
        seed = st.number_input(L("lec.seed"), 1, 9999, 7, key="gen_seed")
        case_lang = st.selectbox(L("lec.mode"), ["hinglish", "en"], key="gen_lang")
        plant = st.checkbox(L("lec.plant"), value=True, key="gen_plant", help=L("lec.defects_help"))
        defect = target = None
        if plant:
            defect = st.selectbox(L("lec.defect"), list(EXPECTED), key="gen_defect")
            target = "calls" if defect == "unsolvable_question" else st.selectbox(L("lec.defect_target"), ["chat", "calls"], key="gen_target")
        go = st.button(L("lec.run"), type="primary", key="gen_go")
    with right:
        log_box = st.container()
        if go:
            if not _take_generation():
                st.warning(L("lec.cap", cap=DAILY_CAP))
            else:
                out = Path(tempfile.mkdtemp(prefix="suraag-")) / f"upi-ring-{int(seed):03d}-{case_lang}"
                attempts = []
                with log_box:
                    st.subheader(L("lec.log"))
                    holders = []

                    def on_attempt(a):
                        attempts.append(a)
                        h = st.empty()
                        h.markdown(attempt_html(a), unsafe_allow_html=True)
                        holders.append(h)

                    res = generate_case(int(seed), case_lang, "hybrid", out, defect=defect, defect_target=target or "chat",
                                        on_attempt=on_attempt, log_path=ROOT / "logs" / "failures.jsonl")
                st.session_state["last_run"] = {"attempts": attempts, "ok": res.ok, "path": str(out), "seed": int(seed),
                                                "manifest": res.manifest}
                if res.ok:
                    st.session_state.setdefault("live_cases", {})[out.name] = out
                    load_dir.clear()
        run = st.session_state.get("last_run")
        if run and not go:
            with log_box:
                st.subheader(L("lec.log"))
                for a in run["attempts"]:
                    st.markdown(attempt_html(a), unsafe_allow_html=True)
        if run:
            st.subheader(L("lec.lab_sheet"))
            st.markdown(lab_table(run["attempts"], run["ok"]), unsafe_allow_html=True)
            if run["ok"]:
                n = len(run["attempts"])
                st.success(L("lec.repaired", n=n) if n > 1 else L("lec.pass"))
                certificate(run["manifest"], Path(run["path"]), "run")
            else:
                st.error(L("lec.discarded", n=len(run["attempts"])))
    st.divider()
    st.subheader(L("ui.case"))
    cases = available_cases()
    if cases:
        pick = st.selectbox(L("ui.case"), list(cases), key="lec_pick", label_visibility="collapsed")
        case, arts, manifest = load_dir(str(cases[pick]))
        fails = verify(case, arts)
        st.markdown(lab_table([type("A", (), {"n": 1, "failures": fails})()], not fails), unsafe_allow_html=True)
        certificate(manifest, cases[pick], "pick")
    else:
        st.info(L("ui.no_cases"))

# ---------------------------------------------------------------------------------------- student
with tab_stu:
    cases = available_cases()
    if not cases:
        st.info(L("ui.no_cases"))
    else:
        name = st.selectbox(L("ui.case"), list(cases), key="stu_pick")
        case, arts, manifest = load_dir(str(cases[name]))
        brief: Brief = case.brief
        ck, gk = f"cites::{name}", f"graded::{name}"
        st.session_state.setdefault(ck, {})
        graded = st.session_state.get(gk)

        with st.expander(L("ui.case") + f": {case.case_id}", expanded=True):
            st.write(brief.summary)
            st.caption(f"{L('stu.lab')}: " + ", ".join(brief.lab_cast))
            c1, c2 = st.columns(2)
            c1.markdown(f"**{L('stu.suspects')}**")
            c1.table({"": [s.name for s in brief.suspects], " ": [s.phone for s in brief.suspects]})
            c2.markdown(f"**{L('stu.places')}**")
            c2.table({"": [p.name for p in brief.places], " ": [f"{p.lat:.4f}, {p.lon:.4f}" for p in brief.places]})

        board, inspector = st.columns([3.4, 1.0])
        qs = brief.questions
        with inspector:
            active_i = st.radio(L("stu.question", n=""), range(len(qs)), key=f"active::{name}",
                                format_func=lambda i: f"{L('stu.question', n=i + 1)}: {qs[i].text}")
            answers, rationales = {}, {}
            for i, q in enumerate(qs):
                st.markdown(f"**{L('stu.question', n=i + 1)}**")
                if q.kind == "who":
                    ids = [s.id for s in brief.suspects]
                    answers[q.id] = st.selectbox(L("stu.answer_person"), ids, key=f"a::{name}::{q.id}", index=None,
                                                 format_func=lambda x: next(s.name for s in brief.suspects if s.id == x))
                elif q.kind == "where":
                    ids = [p.id for p in brief.places]
                    answers[q.id] = st.selectbox(L("stu.answer_place"), ids, key=f"a::{name}::{q.id}", index=None,
                                                 format_func=lambda x: next(p.name for p in brief.places if p.id == x))
                else:
                    answers[q.id] = st.text_input(L("stu.answer_time"), key=f"a::{name}::{q.id}")
                rationales[q.id] = st.text_input(L("stu.rationale"), key=f"r::{name}::{q.id}")
                st.caption(L("stu.cited", n=len(st.session_state[ck].get(q.id, []))))

            st.markdown(f"**{L('hint.title')}**")
            persona = st.selectbox(L("hint.persona"), PERSONAS, key="persona", format_func=lambda p: L(f"persona.{p}"))
            hk = f"hints::{name}::{qs[active_i].id}"
            st.session_state.setdefault(hk, 0)
            if st.button(L("hint.next"), key=f"hint-btn::{name}"):
                st.session_state[hk] = min(st.session_state[hk] + 1, TIERS)
            shown = st.session_state[hk]
            for tier in range(1, shown + 1):
                st.info(hint(case, qs[active_i].id, tier, st.session_state["lang"], persona))
            if shown:
                if shown >= TIERS:
                    st.caption(L("hint.none_left"))
                speak(text=hint(case, qs[active_i].id, shown, st.session_state["lang"], persona),
                      lang=st.session_state["lang"], rate=SPEECH[persona]["rate"], pitch=SPEECH[persona]["pitch"],
                      labels={"read": L("speak.read"), "mute": L("speak.mute"), "no_voice": L("speak.no_voice")},
                      key=f"speak::{name}", default=None)

            s1, s2 = st.columns(2)
            submit = s1.button(L("stu.submit"), type="primary", key=f"submit::{name}")
            if graded and s2.button("↑", key=f"reset::{name}", help="reset"):
                st.session_state.pop(gk, None)
                st.rerun()

        # grading ---------------------------------------------------------------------------
        if submit:
            claims = []
            for q in qs:
                cs = []
                for k in st.session_state[ck].get(q.id, []):
                    kind, _, loc = k.partition(":")
                    cs.append(Citation("chat", line=int(loc)) if kind == "chat" else
                              Citation("calls", row=int(loc)) if kind == "calls" else Citation("photo", exif_tag=loc))
                claims.append(Claim(q.id, answers.get(q.id) or "", tuple(cs), rationales.get(q.id, "")))
            st.session_state[gk] = grade_all(case, arts, claims)
            st.rerun()

        marks, needles = [], {}
        if graded:
            for r in graded:
                q = next(x for x in case.questions if x.id == r.question_id)
                for m in r.marks:
                    key = {"chat": f"chat:{m.citation.line}", "calls": f"calls:{m.citation.row}",
                           "photo": f"photo:{m.citation.exif_tag}"}[m.citation.artifact]
                    marks.append({"qid": q.id, "key": key, "label": m.label})
                    for fid in q.answer_facts:
                        for a in case.fact(fid).anchors:
                            if a.artifact == m.citation.artifact:
                                needles.setdefault(key, [])
                                needles[key] += [s for s in a.must_contain if s not in needles[key]]

        chat_rows = [{"n": ln.line, "text": ln.raw} for ln in load_chat(arts.chat)]
        call_rows = [{"row": r.row, "text": f"{r.t:%Y-%m-%d %H:%M:%S},{r.direction},{r.number},{r.contact_name},{r.duration_s}"}
                     for r in load_calls(arts.calls)]
        exif_rows = [{"tag": k, "value": v} for k, v in load_exif(arts.photo).items()]
        with board:
            val = canvas(chat=chat_rows, calls=call_rows, exif=exif_rows, key=f"canvas::{name}", default=None,
                         photo="data:image/jpeg;base64," + base64.b64encode(arts.photo).decode(),
                         active={"id": qs[active_i].id, "label": L("stu.question", n=active_i + 1)},
                         cites=st.session_state[ck], marks=marks, needles=needles, locked=bool(graded),
                         labels={"holds": L("stu.holds"), "snapped": L("stu.snapped"), "partial": L("stu.partial"),
                                 "tray": L("stu.cited", n="").strip(), "empty": L("stu.cite")})
            if val and "cites" in val and val["cites"] != st.session_state[ck]:
                st.session_state[ck] = val["cites"]
                st.rerun()

        if graded:
            total, possible = sum(r.points for r in graded), 2 * len(graded)
            with board:
                st.markdown(f'<div class="score">{total}<span class="dim" style="font-size:18px"> / {possible}</span></div>'
                            f'<div class="dim">{L("stu.score")}: {L("stu.points", n=total, m=possible)}</div>', unsafe_allow_html=True)
                for r in graded:
                    q = next(x for x in qs if x.id == r.question_id)
                    st.markdown(f"**{q.text}**")
                    a_ok = f'<span class="ok">✓ {L("stu.earned")}</span>' if r.answer_correct else f'<span class="bad">✕ {L("stu.lost")}</span>'
                    e_ok = f'<span class="ok">✓ {L("stu.earned")}</span>' if r.citation_valid else f'<span class="bad">✕ {L("stu.lost")}</span>'
                    st.markdown(f'<div class="pt">{L("stu.answer_point")}: {a_ok} &nbsp;|&nbsp; {L("stu.evidence_point")}: {e_ok}</div>',
                                unsafe_allow_html=True)
                    for e in r.explanations:
                        st.markdown(f'<div class="expl">{render_expl(e, st.session_state["lang"])}</div>', unsafe_allow_html=True)
                    if r.rationale_flag:
                        st.caption({"could_not_verify": L("stu.flagged"), "overclaim": L("stu.flag_overclaim"),
                                    "ok": L("stu.flag_ok")}[r.rationale_flag])

# ---------------------------------------------------------------------------------------- evaluation
with tab_eval:
    st.subheader(L("eval.title"))
    st.caption(L("eval.note"))
    res_path = ROOT / "eval" / "results.json"
    results = json.loads(res_path.read_text("utf-8")) if res_path.exists() else {}
    if not results:
        st.info(L("eval.empty"))
    dd = results.get("defect_detection")
    if dd:
        st.markdown(f"**Defect detection** ({L('eval.n', n=dd['n_defects'])})")
        st.table({"defect": list(dd["per_type"]),
                  "n": [v["n"] for v in dd["per_type"].values()],
                  "caught by the intended check": [v["caught_by_intended_check"] for v in dd["per_type"].values()],
                  "caught by any check": [v["caught_by_any_check"] for v in dd["per_type"].values()]})
        st.caption(f"False positives on clean cases: {dd['false_positives']} of {dd['clean_cases_checked']} ({L('eval.n', n=dd['clean_cases_checked'])}). {dd['note']}")
    gq = results.get("generator_quality")
    if gq:
        st.markdown("**Generator quality: raw LLM vs hybrid + verifier**")
        rows = []
        for lang in [k for k in gq if k != "note"]:
            for mode, r in gq[lang].items():
                rows.append({"language": lang, "mode": mode, "n completed": r["completed"],
                             "first-try pass": r["first_try_pass"], "pass after repair": r["pass_after_repair"],
                             "excluded (LLM unavailable)": r["llm_unavailable_excluded"]})
        st.table(rows)
        st.caption(gq["note"])
    bs = results.get("blind_solve")
    if bs:
        st.markdown(f"**Blind solve by {bs['model']}** ({L('eval.n', n=bs['completed'])}, unscored)")
        st.table({"question kind": list(bs["agreement_with_key"]),
                  "agrees with key": [f"{v['agree']} of {v['of']}" for v in bs["agreement_with_key"].values()]})
    ga = results.get("grader_agreement")
    if ga:
        st.markdown(f"**Grader agreement with manual grading** ({L('eval.n', n=ga['n_labelled'])})")
        st.table({"check": list(ga["agreement"]), "agree": [f"{v} of {ga['n_labelled']}" for v in ga["agreement"].values()]})
    pilot = ROOT / "eval" / "raw_pilot.json"
    if pilot.exists():
        rp = json.loads(pilot.read_text("utf-8"))
        st.markdown(f"**Raw LLM pilot** ({L('eval.n', n=rp['completed'])}): {rp['failed']} of {rp['completed']} chats failed a check. {rp['note']}.")
    sc = ROOT / "eval" / "plain_baseline" / "scores.csv"
    if sc.exists():
        rows = [r for r in csv.DictReader(sc.open(encoding="utf-8")) if r.get("broken") in ("y", "n")]
        if rows:
            broken = sum(r["broken"] == "y" for r in rows)
            first_pass = any("claude" in r.get("checker", "") for r in rows)
            how = "flagged by a first-pass model check, not yet confirmed by a person (some on a strict reading)" if first_pass else "hand-checked cases had at least one defect"
            st.markdown(f"**Plain-chat baseline** ({L('eval.n', n=len(rows))}): {broken} of {len(rows)} {how}.")
