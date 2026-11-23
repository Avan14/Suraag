# Suraag (सुराग)

Fictional Indian forensic practice cases, **proved solvable by plain code**, with a grader that scores a
student on the answer **and on the exact evidence line they cite for it**.

> **All data is synthetic and for teaching only.** Names, phone numbers (`+91-5xxxx-xxxxx`, a range that
> is never a valid Indian mobile number), UPI handles and accounts are invented. Nothing here is
> court-validated or legal advice. SHA-256 hashes show a file is unchanged since generation; they do **not**
> prove it is authentic.

## What it does

- **Generates** a UPI-fraud case from a seed: a WhatsApp-style chat export (English or Hinglish), a call-log
  CSV, and a photo with EXIF metadata. Code builds the world model and writes the key evidence lines
  *verbatim*; an LLM (Gemini) writes only the filler around them.
- **Verifies** every case with deterministic code before it ships: anchors, traceability, contradictions
  (time order, one person per alias, cause before effect), solvability (a rule-based solver reproduces the
  answer key from the files and the student brief alone), a plausible distractor, and sealed SHA-256 hashes.
  A failing artifact is regenerated with the error message as input (up to 3 tries); a case that cannot be
  repaired is discarded and logged.
- **Grades** students per question on two points: the answer, and the evidence. A cited line is *valid* if it
  contains every string the claim needs (it need not be the designated anchor), *partial* if it has some,
  *wrong* if none. Explanations come from the verifier's own data, e.g.
  `chat.txt:3 contains neither "9:14 pm" nor "Raju bhai". A supporting line is chat.txt:12.` The same input
  always gives the same score. An LLM "overclaim" check is **advisory only** and never changes a score.
- **Teaches in two languages:** the interface and every grader/verifier message in English and हिन्दी;
  case content in English and Hinglish. Hints are tiered (file → rows → exact lines), built in code from the
  case model, never by the LLM, and never contain the culprit or the evidence text.

## Try it

```bash
python -m venv .venv && .venv/Scripts/activate        # or source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Five pre-generated cases are in `cases/`, so the app works with no API key. To generate with a live LLM,
put `GEMINI_API_KEY`, `SURAAG_MODEL_FILLER` and `SURAAG_MODEL_SOLVER` in `.env` (see `.env.example`); on
Streamlit Community Cloud put them in the app's secrets. With no key, or when the LLM is unavailable, the
pipeline falls back to deterministic stub filler and the manifest says `"model": "stub"`.

```bash
python -m suraag.pipeline --seed 7 --lang hinglish --out out/demo --defect timestamp_clash   # watch it catch and repair
python -m pytest                                                                             # 158 offline tests
```

## Results so far (all on synthetic cases; sample sizes beside every figure)

| Experiment | Result | n | Notes |
|---|---|---|---|
| Defect detection | 20 of 20 planted defects caught by the check meant for them | 20 (5 per type) | The defects are planted by our own code, so this shows the checks work, not how often real generators err. 0 of 5 clean cases flagged. |
| Raw LLM vs hybrid + verifier | **not usable yet.** A 10-sample raw pilot on `gemini-3.5-flash-lite` completed only 3 samples (the API returned overload errors for the rest); all 3 passed the chat checks | 3 of 10 | Raw mode is judged on chat checks only, so expect it to look better than the plain-chat baseline. `python -m eval.run_generator` is the full comparison and still needs the API. |
| Plain-chat baseline | 8 of 10 flagged by a model first pass; **3 clear-cut** (wrong cited lines, a range instead of a time, a self-contradicting key); human confirmation pending | 10 | One chat app, one prompt, `eval/plain_baseline/`. The other 5 flags rest on a strict reading. Not yet a person's check. |
| Grader agreement with manual grading | **not run yet** | 20 drafted | Needs human labels: `eval/grader_worksheet.md` |
| Blind solve by a second model | **not run yet** | | `python -m eval.run_blind_solve` |

## Limits (please read)

- Synthetic data, small samples, **one case family** (a UPI-fraud ring), not court-validated.
- In hybrid mode the anchored lines are written by code, so the anchor check passes *by construction*; the
  planted-defect experiment shows the checks fire, not that real LLM filler needs them. The raw-vs-hybrid
  experiment is the one that measures that.
- The rule-based solver proves a case is consistent with its templates. Whether a *person* can solve it is
  what the blind solve and a human playtest are for; neither is done yet.
- The Hindi strings are a first draft and **need a native reader's review**.
- The hash is an integrity record, not proof of authenticity.
- The exported-file artifacts (`chat.txt`, `calls.csv`, `photo.jpg`) are less realistic than full device
  images from emulation-based generators.

## Prior art we build on

Synthetic forensic scenarios with ground truth already exist: **EvidenceForge** (Cisco Talos), the
**DFRWS EU 2026** work on LLM-driven scenario generation (Plankl et al.), **hystck / ForTrace**, and
**EviPlant**, mostly for tool testing and DFIR practice. Solver-checked generation is established for LLM
logic puzzles. We claim only the *combination*, aimed at teaching: a verifier that checks a case's answer key
is derivable from its evidence, grading by the evidence a student cites, and Hindi/Hinglish Indian-context
artifacts. We do not claim to be first.

## Responsible use

Fictional data only; educational use only; a human instructor has the last word (free-text reasoning the
grader cannot match is marked *could not verify* and flagged for the instructor, never silently scored);
nothing here gives legal advice.

## Layout

`suraag/` the engine (`model`, `skeleton`, `render`, `verify`, `repair`, `solver`, `grade`, `hints`, `i18n`,
`pipeline`) · `suraag/components/` the evidence board and read-aloud · `app.py` the Streamlit app ·
`docs/RULES.md` the rules register (each rule traced to a source, a test and a status; 13 Implemented, 18 Partial) · `docs/research/` the research it rests on · `eval/` the experiments · `cases/` pre-generated cases (each folder includes `case.json`, the instructor's
answer key) · `tests/`.
