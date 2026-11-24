"""Suraag: verified Indian forensic practice cases, graded on the exact evidence a student cites.

Three views. Lecturer: generate a case, plant a defect and watch the verifier catch and repair it, then
read the certificate. Student: read the files, click lines to cite them, answer, and see the deterministic
grader explain each point. Evaluation: the numbers, with sample sizes. All data is synthetic.

Only the active view runs on each interaction, and the student bench is a fragment, so citing a line reruns
the bench alone. Styles come from the Case Canvas kit tokens in suraag/ui/.
"""
import base64
import csv
import datetime as dt
import html
import io
import json
import os
import tempfile
import zipfile
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from suraag import filler as filler_module  # noqa: F401  (kept: the filler records its source for the UI)
from suraag.defects import EXPECTED
from suraag.grade import Citation, Claim, grade_all
from suraag.hints import PERSONAS, SPEECH, TIERS, hint
from suraag.i18n import render_expl, render_failure, t
from suraag.model import Brief, Case
from suraag.parse import Artifacts, load_calls, load_chat, load_exif, text_at
from suraag.pipeline import generate_case
from suraag.verify import verify

ROOT = Path(__file__).parent
CASES = ROOT / "cases"
UI = ROOT / "suraag" / "ui"
DAILY_CAP = 20
CHECKS = ["anchor", "traceability", "contradiction", "solvability", "distractor"]
VIEWS = ["lecturer", "student", "eval"]

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
def _css() -> str:  # four small files; read each run so CSS edits show up without a restart
    # The token files are the kit's, verbatim. One <style> with the font @import first: a style-only st.html body
    # takes no space in the layout (a <link> beside it would add an empty row above the top bar).
    tokens = "\n".join((UI / "tokens" / f).read_text("utf-8") for f in ("colors.css", "spacing.css", "typography.css"))
    tokens = "\n".join(ln for ln in tokens.splitlines() if not ln.startswith("@import"))
    fonts = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700"
             "&family=Noto+Sans+Devanagari:wght@400;500;600&family=Noto+Serif+Devanagari:wght@600;700&display=swap")
    return f'<style>@import url("{fonts}");\n{tokens}\n{(UI / "app.css").read_text("utf-8")}</style>'


st.html(_css())

# ---------------------------------------------------------------------------------------- helpers
# Widget values are already current when the script starts, so read the language before the header draws.
st.session_state["lang"] = st.session_state.get("lang_choice") or "en"


def L(key: str, **kw) -> str:
    return t(key, st.session_state["lang"], **kw)


def esc(s) -> str:
    return html.escape(str(s))


def note(text: str, kind: str = "") -> None:
    """Kit feedback block: tint + 3px bar + words (never colour alone). kind: '', 'ok' or 'bad'."""
    glyph = {"ok": "✓ ", "bad": "✕ "}.get(kind, "")
    st.markdown(f'<div class="note {kind}">{glyph}{esc(text)}</div>', unsafe_allow_html=True)


def html_table(header: list[str], rows: list[list]) -> str:
    head = ("<tr>" + "".join(f"<th>{esc(h)}</th>" for h in header) + "</tr>") if header else ""
    body = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="lab">{head}{body}</table>'


def available_cases() -> dict[str, Path]:
    found = {p.parent.name: p.parent for p in sorted(CASES.glob("*/manifest.json"))}
    found.update(st.session_state.get("live_cases", {}))
    return found


@st.cache_data(show_spinner=False)
def load_dir(path: str):
    p = Path(path)
    case = Case.model_validate_json((p / "case.json").read_text("utf-8"))
    arts = Artifacts.from_dir(p)
    photo = "data:image/jpeg;base64," + base64.b64encode(arts.photo).decode()
    return case, arts, json.loads((p / "manifest.json").read_text("utf-8")), photo


@st.cache_data(show_spinner=False)
def verify_dir(path: str) -> list:
    case, arts, _, _ = load_dir(path)
    return verify(case, arts)


@st.cache_data(show_spinner=False)
def make_zip(path: str, student: bool) -> bytes:
    buf, p = io.BytesIO(), Path(path)
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name in (("chat.txt", "calls.csv", "photo.jpg", "manifest.json", "brief.md") if student else ("case.json",)):
            if (p / name).exists():
                z.write(p / name, name)
    return buf.getvalue()


def lab_table(attempts, sealed: bool) -> str:
    cols = "".join(f"<th>A{a.n}</th>" for a in attempts)
    rows = []
    shown = [c for c in CHECKS + ["filler_count"] if c in CHECKS or any(f.check == c for a in attempts for f in a.failures)]
    for c in shown:
        cells = "".join(
            f'<td class="{"bad" if any(f.check == c for f in a.failures) else "ok"}">'
            f'{"✕ " + L("lec.fail") if any(f.check == c for f in a.failures) else "✓ " + L("lec.pass")}</td>' for a in attempts)
        rows.append(f"<tr><th>{L('check.' + c)}</th>{cells}</tr>")
    cells = "".join('<td class="dim">–</td>' for _ in attempts[:-1])
    cells += f'<td class="{"ok" if sealed else "dim"}">{"✓ " + L("lec.pass") if sealed else "–"}</td>'
    rows.append(f"<tr><th>{L('check.integrity')}</th>{cells}</tr>")
    return f'<table class="lab"><tr><th></th>{cols}</tr>{"".join(rows)}</table>'


def attempt_html(a) -> str:
    head = f'<div class="attempt">{esc(L("lec.attempt", n=a.n, action=a.action))}</div>'
    if not a.failures:
        return f'{head}<div class="msg pass">✓ {L("lec.pass")}</div>'
    return head + "".join(f'<div class="msg">✕ {esc(render_failure(f, st.session_state["lang"]))}</div>' for f in a.failures)


def certificate(manifest: dict, path: Path, key: str) -> None:
    files = "".join(f'<div class="file"><b>{esc(n)}</b><br><code>{esc(h)}</code></div>' for n, h in manifest["files"].items())
    stub = f'<div class="msg">{esc(L("lec.stub_notice"))}</div>' if manifest.get("model") == "stub" else ""
    st.markdown(
        f'<div class="cert"><b>{esc(L("lec.certificate"))}</b>: <span class="mono">{esc(manifest["case_id"])}</span> '
        f'({esc(manifest["lang"])}, {esc(manifest["mode"])}), seed {manifest["seed"]}, model <code>{esc(manifest["model"])}</code>'
        f'<div class="label" style="margin-top:12px">{esc(L("lec.hashes"))}</div>{files}'
        f'<p class="dim" style="margin-top:10px">{esc(L("lec.hash_note"))}</p>{stub}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.download_button(L("lec.zip_student"), make_zip(str(path), True), f"{path.name}-student.zip", key=f"zs-{key}")
    c2.download_button(L("lec.zip_key"), make_zip(str(path), False), f"{path.name}-key.zip", key=f"zk-{key}")


# ---------------------------------------------------------------------------------------- header
cases_now = available_cases()
view = st.session_state.get("view") or "lecturer"
pill_case = {"lecturer": st.session_state.get("lec_pick"), "student": st.session_state.get("stu_pick")}.get(view)
if view != "eval" and not pill_case and cases_now:
    pill_case = next(iter(cases_now))

with st.container(key="topbar", horizontal=True, vertical_alignment="center"):
    st.html('<div class="brand"><span class="wm" lang="hi">सुराग</span><span class="name">SURAAG</span></div>', width="content")
    if pill_case:
        st.html(f'<span class="pill">{esc(pill_case)}</span>', width="content")
    st.segmented_control(L("ui.view"), VIEWS, key="view", default="lecturer", required=True, label_visibility="collapsed",
                         format_func=lambda v: L({"lecturer": "ui.tab_lecturer", "student": "ui.tab_student", "eval": "ui.tab_eval"}[v]))
    st.html(f'<span class="tag-synth" title="{esc(L("ui.synthetic"))}" aria-label="{esc(L("ui.synthetic"))}">'
            f'{esc(L("ui.synthetic_tag"))}</span>', width="content")
    st.segmented_control(L("ui.language"), ["hi", "en"], key="lang_choice", default="en", required=True,
                         label_visibility="collapsed", format_func=lambda x: "हिं" if x == "hi" else "EN")


# ---------------------------------------------------------------------------------------- lecturer
def lecturer_view() -> None:
    left, right = st.columns([1, 1.6], gap="large")
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
        if go:
            if not _take_generation():
                note(L("lec.cap", cap=DAILY_CAP), "bad")
            else:
                out = Path(tempfile.mkdtemp(prefix="suraag-")) / f"upi-ring-{int(seed):03d}-{case_lang}"
                attempts = []
                st.subheader(L("lec.log"))
                with st.status(L("lec.generating"), expanded=True) as status:
                    def on_attempt(a):
                        attempts.append(a)
                        st.markdown(attempt_html(a), unsafe_allow_html=True)

                    res = generate_case(int(seed), case_lang, "hybrid", out, defect=defect, defect_target=target or "chat",
                                        on_attempt=on_attempt, log_path=ROOT / "logs" / "failures.jsonl")
                    status.update(label=L("lec.log"), state="complete" if res.ok else "error")
                st.session_state["last_run"] = {"attempts": attempts, "ok": res.ok, "path": str(out), "manifest": res.manifest}
                if res.ok:
                    st.session_state.setdefault("live_cases", {})[out.name] = out
                st.rerun()  # redraw once so the header pill and the case list include the new case
        run = st.session_state.get("last_run")
        if run:
            st.subheader(L("lec.log"))
            st.markdown("".join(attempt_html(a) for a in run["attempts"]), unsafe_allow_html=True)
            st.subheader(L("lec.lab_sheet"))
            st.markdown(lab_table(run["attempts"], run["ok"]), unsafe_allow_html=True)
            if run["ok"]:
                n = len(run["attempts"])
                note(L("lec.repaired", n=n) if n > 1 else L("lec.pass"), "ok")
                certificate(run["manifest"], Path(run["path"]), "run")
            else:
                note(L("lec.discarded", n=len(run["attempts"])), "bad")
    st.divider()
    st.subheader(L("ui.case"))
    if not cases_now:
        note(L("ui.no_cases"))
        return
    pick = st.selectbox(L("ui.case"), list(cases_now), key="lec_pick", label_visibility="collapsed")
    fails = verify_dir(str(cases_now[pick]))
    st.markdown(lab_table([type("A", (), {"n": 1, "failures": fails})()], not fails), unsafe_allow_html=True)
    certificate(load_dir(str(cases_now[pick]))[2], cases_now[pick], "pick")


# ---------------------------------------------------------------------------------------- student
@st.fragment
def student_bench(name: str, path: str) -> None:
    case, arts, _, photo = load_dir(path)
    brief: Brief = case.brief
    qs = brief.questions
    ck, gk, canvas_key = f"cites::{name}", f"graded::{name}", f"canvas::{name}"
    st.session_state.setdefault(ck, {})
    # The board reports clicks as its widget value; take it before drawing so the board and the counts agree
    # without a second rerun.
    val = st.session_state.get(canvas_key)
    if val and "cites" in val and not st.session_state.get(gk):
        st.session_state[ck] = val["cites"]
    graded = st.session_state.get(gk)
    active_i = st.session_state.get(f"active::{name}") or 0

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

    with st.container(key="bench"):
        board, inspector_col = st.columns([3.3, 1.0])
    with board:
        canvas(chat=[{"n": ln.line, "text": ln.raw} for ln in load_chat(arts.chat)],
               calls=[{"row": r.row, "text": text_at(arts, "calls", row=r.row)} for r in load_calls(arts.calls)],
               exif=[{"tag": k, "value": v} for k, v in load_exif(arts.photo).items()],
               key=canvas_key, default=None, photo=photo,
               active={"id": qs[active_i].id, "label": L("stu.question", n=active_i + 1)},
               cites=st.session_state[ck], marks=marks, needles=needles, locked=bool(graded),
               labels={"holds": L("stu.holds"), "snapped": L("stu.snapped"), "partial": L("stu.partial"),
                       "tray": L("stu.cited", n="").strip(), "empty": L("stu.cite")})

    with inspector_col, st.container(key="inspector"):
        # A fixed, hidden label: Streamlit resets a widget whose label changes, which would drop the choice on a language switch.
        st.markdown(f'<div class="label">{esc(L("stu.question", n=""))}</div>', unsafe_allow_html=True)
        st.radio("question", range(len(qs)), key=f"active::{name}", label_visibility="collapsed",
                 format_func=lambda i: f"{L('stu.question', n=i + 1)}: {qs[i].text}")
        answers, rationales = {}, {}
        for i, q in enumerate(qs):
            st.markdown(f'<div class="label" style="margin-top:14px">{esc(L("stu.question", n=i + 1))}</div>', unsafe_allow_html=True)
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

        st.markdown(f'<div class="label" style="margin-top:18px">{esc(L("hint.title"))}</div>', unsafe_allow_html=True)
        persona = st.selectbox(L("hint.persona"), PERSONAS, key="persona", format_func=lambda p: L(f"persona.{p}"))
        hk = f"hints::{name}::{qs[active_i].id}"
        st.session_state.setdefault(hk, 0)
        if st.button(L("hint.next"), key=f"hint-btn::{name}"):
            st.session_state[hk] = min(st.session_state[hk] + 1, TIERS)
        shown = st.session_state[hk]
        for tier in range(1, shown + 1):
            st.markdown(f'<div class="hint">{esc(hint(case, qs[active_i].id, tier, st.session_state["lang"], persona))}</div>',
                        unsafe_allow_html=True)
        if shown:
            if shown >= TIERS:
                st.caption(L("hint.none_left"))
            speak(text=hint(case, qs[active_i].id, shown, st.session_state["lang"], persona),
                  lang=st.session_state["lang"], rate=SPEECH[persona]["rate"], pitch=SPEECH[persona]["pitch"],
                  labels={"read": L("speak.read"), "mute": L("speak.mute"), "no_voice": L("speak.no_voice")},
                  key=f"speak::{name}", default=None)

        s1, s2 = st.columns(2)
        if s1.button(L("stu.submit"), type="primary", key=f"submit::{name}"):
            claims = []
            for q in qs:
                cs = []
                for k in st.session_state[ck].get(q.id, []):
                    kind, _, loc = k.partition(":")
                    cs.append(Citation("chat", line=int(loc)) if kind == "chat" else
                              Citation("calls", row=int(loc)) if kind == "calls" else Citation("photo", exif_tag=loc))
                claims.append(Claim(q.id, answers.get(q.id) or "", tuple(cs), rationales.get(q.id, "")))
            st.session_state[gk] = grade_all(case, arts, claims)
            st.rerun(scope="fragment")
        if graded and s2.button("↑", key=f"reset::{name}", help="reset"):
            st.session_state.pop(gk, None)
            st.rerun(scope="fragment")

    if graded:
        total, possible = sum(r.points for r in graded), 2 * len(graded)
        with board:
            st.markdown(f'<div class="score">{total}<span class="dim" style="font-size:18px"> / {possible}</span></div>'
                        f'<div class="dim">{esc(L("stu.score"))}: {esc(L("stu.points", n=total, m=possible))}</div>', unsafe_allow_html=True)
            for r in graded:
                q = next(x for x in qs if x.id == r.question_id)
                st.markdown(f"**{q.text}**")
                a_ok = f'<span class="ok">✓ {L("stu.earned")}</span>' if r.answer_correct else f'<span class="bad">✕ {L("stu.lost")}</span>'
                e_ok = f'<span class="ok">✓ {L("stu.earned")}</span>' if r.citation_valid else f'<span class="bad">✕ {L("stu.lost")}</span>'
                st.markdown(f'<div class="pt">{L("stu.answer_point")}: {a_ok} &nbsp;|&nbsp; {L("stu.evidence_point")}: {e_ok}</div>',
                            unsafe_allow_html=True)
                for e in r.explanations:
                    st.markdown(f'<div class="expl">{esc(render_expl(e, st.session_state["lang"]))}</div>', unsafe_allow_html=True)
                if r.rationale_flag:
                    st.caption({"could_not_verify": L("stu.flagged"), "overclaim": L("stu.flag_overclaim"),
                                "ok": L("stu.flag_ok")}[r.rationale_flag])


def student_view() -> None:
    if not cases_now:
        note(L("ui.no_cases"))
        return
    name = st.selectbox(L("ui.case"), list(cases_now), key="stu_pick")
    case = load_dir(str(cases_now[name]))[0]
    brief = case.brief
    with st.expander(L("ui.case") + f": {case.case_id}", expanded=True):
        st.write(brief.summary)
        st.caption(f"{L('stu.lab')}: " + ", ".join(brief.lab_cast))
        c1, c2 = st.columns(2)
        c1.markdown(f'<div class="label">{esc(L("stu.suspects"))}</div>' +
                    html_table([], [[s.name, s.phone] for s in brief.suspects]), unsafe_allow_html=True)
        c2.markdown(f'<div class="label">{esc(L("stu.places"))}</div>' +
                    html_table([], [[p.name, f"{p.lat:.4f}, {p.lon:.4f}"] for p in brief.places]),
                    unsafe_allow_html=True)
    student_bench(name, str(cases_now[name]))


# ---------------------------------------------------------------------------------------- evaluation
def eval_view() -> None:
    st.subheader(L("eval.title"))
    st.caption(L("eval.note"))
    res_path = ROOT / "eval" / "results.json"
    results = json.loads(res_path.read_text("utf-8")) if res_path.exists() else {}
    if not results:
        note(L("eval.empty"))

    def block(title: str, header, rows, caption: str = "") -> None:
        st.markdown(f'<div class="label" style="margin-top:22px">{esc(title)}</div>' + html_table(header, rows), unsafe_allow_html=True)
        if caption:
            st.caption(caption)

    dd = results.get("defect_detection")
    if dd:
        block(f"Defect detection ({L('eval.n', n=dd['n_defects'])})",
              ["defect", "n", "caught by the intended check", "caught by any check"],
              [[k, v["n"], v["caught_by_intended_check"], v["caught_by_any_check"]] for k, v in dd["per_type"].items()],
              f"False positives on clean cases: {dd['false_positives']} of {dd['clean_cases_checked']} "
              f"({L('eval.n', n=dd['clean_cases_checked'])}). {dd['note']}")
    gq = results.get("generator_quality")
    if gq:
        block("Generator quality: raw LLM vs hybrid + verifier",
              ["language", "mode", "n completed", "first-try pass", "pass after repair", "excluded (LLM unavailable)"],
              [[lang, mode, r["completed"], r["first_try_pass"], r["pass_after_repair"], r["llm_unavailable_excluded"]]
               for lang in [k for k in gq if k != "note"] for mode, r in gq[lang].items()], gq["note"])
    for key, label in (("blind_solve", "stub filler"), ("blind_solve_real", "real LLM filler")):
        bs = results.get(key)
        if bs:
            block(f"Blind solve by {bs['model']}, {label} ({L('eval.n', n=bs['completed'])}, unscored)",
                  ["question kind", "agrees with key"],
                  [[k, f"{v['agree']} of {v['of']}"] for k, v in bs["agreement_with_key"].items()])
    ga = results.get("grader_agreement")
    if ga:
        block(f"Grader agreement with manual grading ({L('eval.n', n=ga['n_labelled'])})",
              ["check", "agree"], [[k, f"{v} of {ga['n_labelled']}"] for k, v in ga["agreement"].items()])
    sc = ROOT / "eval" / "plain_baseline" / "scores.csv"
    if sc.exists():
        rows = [r for r in csv.DictReader(sc.open(encoding="utf-8")) if r.get("broken") in ("y", "n")]
        if rows:
            broken = sum(r["broken"] == "y" for r in rows)
            first_pass = any("claude" in r.get("checker", "") for r in rows)
            how = ("flagged by a first-pass model check, not yet confirmed by a person (some on a strict reading)"
                   if first_pass else "hand-checked cases had at least one defect")
            st.markdown(f'<div class="label" style="margin-top:22px">Plain-chat baseline ({esc(L("eval.n", n=len(rows)))})</div>'
                        f'<div class="note">{broken} of {len(rows)} {esc(how)}.</div>', unsafe_allow_html=True)


{"lecturer": lecturer_view, "student": student_view, "eval": eval_view}[view]()
