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
from types import SimpleNamespace
import zipfile
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from suraag import filler as filler_module  # noqa: F401  (kept: the filler records its source for the UI)
from suraag.defects import EXPECTED
from suraag.grade import Citation, Claim, grade_all
from suraag.hints import PERSONAS, SPEECH, TIERS, hint
from suraag.i18n import EN, render_expl, render_failure, t
from suraag.landing import body_html, hero_html
from suraag.model import Brief, Case
from suraag.parse import Artifacts, load_calls, load_chat, load_exif, text_at
from suraag.pipeline import generate_case
from suraag.verify import verify

ROOT = Path(__file__).parent
CASES = ROOT / "cases"
UI = ROOT / "suraag" / "ui"
DAILY_CAP = 20
CHECKS = ["anchor", "traceability", "contradiction", "solvability", "distractor"]
VIEWS = ["home", "lecturer", "student", "eval"]

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
def _css() -> str:  # read each run so CSS edits show up without a restart
    # One style-only st.html body (font @import first) takes no space in the layout.
    fonts = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+Devanagari:wght@400;500;600;700"
             "&family=Tiro+Devanagari+Hindi:ital@0;1&display=swap")
    return f'<style>@import url("{fonts}");\n{(UI / "app.css").read_text("utf-8")}</style>'

st.html(_css())

# ---------------------------------------------------------------------------------------- helpers
# View and language live in session_state and are set by button callbacks, which run before the script does.
st.session_state.setdefault("lang", "en")
st.session_state.setdefault("view", "home")


def _set(key: str, value: str) -> None:
    st.session_state[key] = value


def L(key: str, **kw) -> str:
    return t(key, st.session_state.get("lang", "en"), **kw)  # .get: format_func can run outside a script run


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


def page_intro(view: str, title: str | None = None) -> None:
    st.markdown(f'<section class="intro"><div class="eyebrow">{esc(L(f"page.{view}.eyebrow"))}</div>'
                f'<div class="display" role="heading" aria-level="1">{esc(title or L(f"page.{view}.title"))}</div>'
                f'<p class="lede">{esc(L(f"page.{view}.lede"))}</p></section>', unsafe_allow_html=True)


TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>')
CROSS = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" '
         'aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>')


def stamp(kind: str, text: str, big: bool = False) -> str:
    glyph = {"ok": TICK, "bad": CROSS}.get(kind, "")
    return f'<span class="stamp {kind}{" big" if big else ""}">{glyph}{esc(text)}</span>'


def action_text(action: str) -> str:
    return " + ".join(L(f"act.{p}") if f"act.{p}" in EN else p for p in action.split(" + "))


def lab_sheet(attempts, sealed: bool) -> str:
    """One row per check: how it ended (passed, failed then repaired, failed) and the first error it caught."""
    first, last, lang = attempts[0], attempts[-1], st.session_state["lang"]
    shown = CHECKS + [c for c in ("filler_count",) if any(f.check == c for a in attempts for f in a.failures)]
    rows = []
    for i, c in enumerate(shown + ["integrity"], 1):
        name, _, desc = L("check." + c).partition(": ")
        desc = desc[:1].upper() + desc[1:]
        if c == "integrity":
            mark = stamp("ok", L("lec.stamp_pass")) if sealed else stamp("mute", L("lec.stamp_unsealed"))
            detail = ""
        else:
            f1 = [f for f in first.failures if f.check == c]
            fl = [f for f in last.failures if f.check == c]
            mark = (stamp("bad", L("lec.stamp_fail")) if fl else stamp("bad", L("lec.stamp_repaired")) if f1
                    else stamp("ok", L("lec.stamp_pass")))
            detail = f'<div class="detail">{esc(render_failure((fl or f1)[0], lang))}</div>' if (fl or f1) else ""
        rows.append(f'<div class="check"><span class="num">{i}</span><div class="body"><div class="name">{esc(name)}</div>'
                    f'<div class="desc">{esc(desc)}</div>{detail}</div>{mark}</div>')
    return (f'<section class="sheet"><div class="sheet-head"><span>{esc(L("lec.sheet"))}</span>'
            f'<span class="mono">{esc(L("lec.repairs_used", n=len(attempts) - 1))}</span></div>{"".join(rows)}</section>')


def run_log(attempts, sealed: bool) -> str:
    lang, lines = st.session_state["lang"], []
    for a in attempts:
        lines.append(("", f"[A{a.n}] {action_text(a.action)}"))
        if a.failures:
            lines += [("bad indent", f"✕ {render_failure(f, lang)}") for f in a.failures]
        else:
            lines.append(("ok indent", f"✓ {L('lec.verify_line')}"))
    lines.append(("ok", f"→ {L('lec.sealed_line')}") if sealed else ("bad", f"✕ {L('lec.discarded', n=len(attempts))}"))
    body = "".join(f'<div class="ln {k}" style="animation-delay:{i * 45}ms">{esc(x)}</div>' for i, (k, x) in enumerate(lines))
    return f'<section class="log"><div class="title">{esc(L("lec.log"))}</div>{body}</section>'


def certificate(manifest: dict | None, path: Path, key: str, sealed: bool, fresh: bool) -> None:
    with st.container(key="certbox"):
        head = (f'<div class="cert-head"><div class="panel-title" role="heading" aria-level="2">{esc(L("lec.certificate"))}</div>'
                f'{stamp("ok" if sealed else "bad", L("lec.verified") if sealed else L("lec.discarded_stamp"), big=True)}</div>')
        wrap = "fresh" if fresh else ""
        if not sealed or not manifest:  # a discarded run has no manifest; a pre-generated case that fails keeps one
            why = L("lec.not_shipped") if key == "run" else L("lec.pick_failed")
            st.markdown(f'<div class="{wrap}">{head}<p class="fine">{esc(why)}</p></div>', unsafe_allow_html=True)
            return
        kv = list(manifest["files"].items())
        kv += [(L("lec.k_case"), manifest["case_id"]), (L("lec.k_seed"), f'{manifest["seed"]:03d} / {manifest["mode"]}'),
               (L("lec.k_lang"), manifest["lang"]), (L("lec.k_model"), manifest["model"]),
               (L("lec.k_prompt"), (manifest.get("prompt_hashes") or {}).get("filler", "–"))]
        dl = "".join(f'<dt>{esc(k)}</dt><dd title="{esc(v)}">{esc(v)}</dd>' for k, v in kv)
        stub = f'<div class="note bad">{esc(L("lec.stub_notice"))}</div>' if manifest.get("model") == "stub" else ""
        st.markdown(f'<div class="{wrap}">{head}<dl class="kv">{dl}</dl>'
                    f'<p class="fine">{esc(L("lec.hash_note"))} {esc(L("lec.not_real"))}</p>{stub}</div>', unsafe_allow_html=True)
        with st.container(horizontal=True, gap="small"):
            st.download_button(L("lec.zip_student"), make_zip(str(path), True), f"{path.name}-student.zip", key=f"zs-{key}")
            st.download_button(L("lec.zip_key"), make_zip(str(path), False), f"{path.name}-key.zip", key=f"zk-{key}")


# ---------------------------------------------------------------------------------------- header
cases_now = available_cases()
view, lang = st.session_state["view"], st.session_state["lang"]

# Only the active view runs, and Streamlit forgets the value of any widget that was not drawn in a run. Re-own the
# keys of the views that are not drawn, so a student's typed answers and the lecturer's choices survive a view switch.
# (Only keys whose widgets pass no explicit default; their defaults are set here instead.)
st.session_state.setdefault("gen_seed", 7)
st.session_state.setdefault("gen_plant", True)
_hidden = (("gen_", "lec_pick") if view != "lecturer" else ()) + (("a::", "r::", "stu_pick", "persona") if view != "student" else ())
for _k in [k for k in st.session_state if isinstance(k, str) and k.startswith(_hidden)]:
    st.session_state[_k] = st.session_state[_k]

# Plain buttons, not st.segmented_control: its active option draws side borders that CSS cannot remove.
with st.container(key="topbar", horizontal=True, vertical_alignment="center"):
    st.html(f'<div class="brand"><span class="wm" lang="hi">सुराग</span><span class="latin">Suraag</span>'
            f'<span class="tagline">{esc(L("app.tagline"))}</span></div>', width="content")
    with st.container(key="nav", horizontal=True, gap=None, width="content", vertical_alignment="center"):
        for v, k in (("home", "ui.tab_home"), ("lecturer", "ui.tab_lecturer"), ("student", "ui.tab_student"), ("eval", "ui.tab_eval")):
            st.button(L(k), key=f"nav_{v}", type="tertiary", on_click=_set, args=("view", v))
    st.html(f'<span class="tag-synth" title="{esc(L("ui.synthetic"))}" aria-label="{esc(L("ui.synthetic"))}">'
            f'{esc(L("ui.synthetic_tag"))}</span>', width="content")
    with st.container(key="langsw", horizontal=True, gap=None, width="content", vertical_alignment="center"):
        st.button("हिं", key="lang_hi", type="tertiary", on_click=_set, args=("lang", "hi"))
        st.button("EN", key="lang_en", type="tertiary", on_click=_set, args=("lang", "en"))
# The active nav pill, language and case language are filled with ink (style-only, so it takes no space).
st.html(f"<style>.st-key-nav_{view} button, .st-key-lang_{lang} button, "
        f".st-key-genlang_{st.session_state.get('gen_lang', 'hinglish')} button "
        f"{{ background: var(--ink) !important; color: var(--paper) !important; }}</style>")


# ---------------------------------------------------------------------------------------- lecturer
def lecturer_view() -> None:
    page_intro("lec")
    st.session_state.setdefault("gen_lang", "hinglish")
    left, right = st.columns([1, 1.75], gap="large")
    with left, st.container(key="aside"):
        st.markdown(f'<div class="panel-title" role="heading" aria-level="2">{esc(L("lec.generate"))}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="label">{esc(L("lec.mode"))}</div>', unsafe_allow_html=True)
        with st.container(key="genlang", horizontal=True, gap=None):
            for code, label in (("en", "English"), ("hinglish", "Hinglish")):
                st.button(label, key=f"genlang_{code}", type="tertiary", on_click=_set, args=("gen_lang", code))
        seed = st.number_input(L("lec.seed"), 1, 9999, key="gen_seed")
        plant = st.toggle(L("lec.plant"), key="gen_plant", help=L("lec.defects_help"))
        defect = target = None
        if plant:
            defect = st.selectbox(L("lec.defect"), list(EXPECTED), key="gen_defect")
            target = ("calls" if defect == "unsolvable_question"
                      else st.selectbox(L("lec.defect_target"), ["chat", "calls"], key="gen_target"))
        with st.container(horizontal=True, vertical_alignment="center"):
            go = st.button(L("lec.run"), type="primary", key="gen_go")
            st.markdown(f'<span class="seedline">seed {int(seed):03d} · hybrid</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="fine ruled">{esc(L("lec.cap_note", cap=DAILY_CAP))}</div>', unsafe_allow_html=True)
        if cases_now:
            st.selectbox(L("lec.open_case"), list(cases_now), key="lec_pick", on_change=_set, args=("show", "pick"))

    with right:
        if go:
            if not _take_generation():
                note(L("lec.cap", cap=DAILY_CAP), "bad")
            else:
                case_lang = st.session_state["gen_lang"]
                out = Path(tempfile.mkdtemp(prefix="suraag-")) / f"upi-ring-{int(seed):03d}-{case_lang}-live"
                attempts = []
                with st.status(L("lec.generating"), expanded=True) as status:
                    def on_attempt(a):
                        attempts.append(a)
                        lines = [f"**{esc(L('lec.attempt', n=a.n, action=action_text(a.action)))}**"]
                        lines += ["✕ " + esc(render_failure(f, st.session_state["lang"])) for f in a.failures] or ["✓ " + L("lec.pass")]
                        st.markdown("  \n".join(lines))

                    res = generate_case(int(seed), case_lang, "hybrid", out, defect=defect, defect_target=target or "chat",
                                        on_attempt=on_attempt, log_path=ROOT / "logs" / "failures.jsonl")
                    status.update(label=L("lec.log"), state="complete" if res.ok else "error")
                st.session_state["last_run"] = {"attempts": attempts, "ok": res.ok, "path": str(out), "manifest": res.manifest}
                if res.ok:
                    st.session_state.setdefault("live_cases", {})[out.name] = out
                st.session_state.update(show="run", fresh=True)
                st.rerun()

        fresh = st.session_state.pop("fresh", False)
        run = st.session_state.get("last_run")
        if run and st.session_state.get("show") == "run":
            attempts, sealed, path, manifest, key = run["attempts"], run["ok"], Path(run["path"]), run["manifest"], "run"
        elif cases_now:
            path = cases_now[st.session_state.get("lec_pick") or next(iter(cases_now))]
            fails = verify_dir(str(path))
            attempts = [SimpleNamespace(n=1, failures=fails, action="initial")]
            _, arts, manifest, _ = load_dir(str(path))
            sealed, key = not fails and arts.sha256() == manifest["files"], "pick"
        else:
            note(L("ui.no_cases"))
            return
        st.markdown(f'<div class="{"fresh" if fresh else ""}">{lab_sheet(attempts, sealed)}<div style="height:24px"></div>'
                    f'{run_log(attempts, sealed)}</div>', unsafe_allow_html=True)
        certificate(manifest, path, key, sealed, fresh)


# ---------------------------------------------------------------------------------------- student
def _grade(name: str, path: str) -> None:
    """Submit callback: build the claims from session state and grade them before the bench redraws."""
    case, arts, _, _ = load_dir(path)
    cites = st.session_state.get(f"cites::{name}", {})
    claims = []
    for q in case.brief.questions:
        cs = []
        for k in cites.get(q.id, []):
            kind, _, loc = k.partition(":")
            cs.append(Citation("chat", line=int(loc)) if kind == "chat" else
                      Citation("calls", row=int(loc)) if kind == "calls" else Citation("photo", exif_tag=loc))
        answer = st.session_state.get(f"a::{name}::{q.id}") or ""
        claims.append(Claim(q.id, str(answer), tuple(cs), st.session_state.get(f"r::{name}::{q.id}") or ""))
    st.session_state[f"graded::{name}"] = grade_all(case, arts, claims)


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
    # The chosen question is kept under its own key: read before the radio is drawn, a widget's stored value can
    # come back in its serialised form (the label text), not the option.
    active_i = st.session_state.get(f"q::{name}", 0)

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
        # Streamlit stores a radio's choice as its label text, so a language switch would leave nothing selected;
        # write the choice back from our own key before drawing it.
        st.session_state[f"active::{name}"] = active_i
        st.radio("question", range(len(qs)), key=f"active::{name}", label_visibility="collapsed",
                 format_func=lambda i: f"{L('stu.question', n=i + 1)}: {qs[i].text}",
                 on_change=lambda: _set(f"q::{name}", st.session_state[f"active::{name}"]))
        for i, q in enumerate(qs):
            st.markdown(f'<div class="label" style="margin-top:14px">{esc(L("stu.question", n=i + 1))}</div>', unsafe_allow_html=True)
            if q.kind == "who":
                ids = [s.id for s in brief.suspects]
                st.selectbox(L("stu.answer_person"), ids, key=f"a::{name}::{q.id}", index=None, placeholder=L("ui.choose"),
                                             format_func=lambda x: next(s.name for s in brief.suspects if s.id == x))
            elif q.kind == "where":
                ids = [p.id for p in brief.places]
                st.selectbox(L("stu.answer_place"), ids, key=f"a::{name}::{q.id}", index=None, placeholder=L("ui.choose"),
                                             format_func=lambda x: next(p.name for p in brief.places if p.id == x))
            else:
                st.text_input(L("stu.answer_time"), key=f"a::{name}::{q.id}")
            st.text_input(L("stu.rationale"), key=f"r::{name}::{q.id}")
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
        s1.button(L("stu.submit"), type="primary", key=f"submit::{name}", on_click=_grade, args=(name, path))
        if graded:
            s2.button(L("stu.reset"), key=f"reset::{name}", on_click=lambda: st.session_state.pop(gk, None))

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
    page_intro("stu")
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
    page_intro("eval", L("eval.title"))
    res_path = ROOT / "eval" / "results.json"
    results = json.loads(res_path.read_text("utf-8")) if res_path.exists() else {}
    if not results:
        note(L("eval.empty"))

    def block(title: str, header, rows, caption: str = "") -> None:
        st.markdown(f'<div class="sub">{esc(title)}</div>' + html_table(header, rows), unsafe_allow_html=True)
        if caption:
            st.caption(caption)

    dd = results.get("defect_detection")
    if dd:
        block(f"Defect detection ({L('eval.n', n=dd['n_defects'])})",
              ["defect", "n", "caught by the intended check", "caught by any check"],
              [[k, v["n"], v["caught_by_intended_check"], v["caught_by_any_check"]] for k, v in dd["per_type"].items()],
              f"False positives on clean cases: {dd['false_positives']} of {dd['clean_cases_checked']} "
              f"({L('eval.n', n=dd['clean_cases_checked'])}). {dd['note'][:1].upper() + dd['note'][1:]}.")
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
            st.markdown(f'<div class="sub">Plain-chat baseline ({esc(L("eval.n", n=len(rows)))})</div>'
                        f'<div class="note">{broken} of {len(rows)} {esc(how)}.</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------------------- home
def home_view() -> None:
    st.html(hero_html(st.session_state["lang"]))
    with st.container(key="cta", horizontal=True):
        st.button(L("home.cta_lecturer"), type="primary", key="cta_lec", on_click=_set, args=("view", "lecturer"))
        st.button(L("home.cta_student"), key="cta_stu", on_click=_set, args=("view", "student"))
    st.html(body_html(st.session_state["lang"]), unsafe_allow_javascript=True)


{"home": home_view, "lecturer": lecturer_view, "student": student_view, "eval": eval_view}[view]()
