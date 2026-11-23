
## Gate 1: plain-chat baseline (recorded Nov 23)

Source: 10 replies from one free chat app (ChatGPT, logged out), same prompt each time, fresh chat each.
Checked against `eval/baseline_rubric.md` by a **model first pass** (`checker = claude-first-pass`), not yet by a person.

- Flagged broken: **8 of 10** (01, 02, 03, 04, 05, 08, 09, 10). Not flagged: 06, 07.
- **Clear-cut (3 of 10):** 02 (the key cites the wrong chat lines for the decoy suspect), 05 (the "when" answer is a
  range and the call log contradicts the chat order), 09 (the key corrects itself mid-answer and the case's own note
  is false about a call's timing).
- **Borderline (5 of 10), flagged only on a strict reading:** 01 and 03 (the key reads an OUTGOING call row as the
  suspect calling the device owner), 04 (two competing instruction times), 08 and 10 (a call said to come "shortly
  before" a message actually overlaps it).
- R7 (the chat mentions the photo before its EXIF capture time) is not in the rubric; it was noted per case only
  and is not counted.

**Decision (Gate 1):** 3 or more of 10 flagged, so the video leads with plain-LLM failures. Use the conservative
figure: "at least 3 of 10 hand-checked cases had a clear defect (n=10, one chat app, synthetic)", and only after a
person confirms cases 02, 05 and 09 against the lines quoted in `scores.csv`.
TODO (human): confirm 02, 05, 09; decide whether the borderline five count; change `checker` to your initials.

## Raw-mode pilot attempt (Nov 24)

`python -m eval.run_raw_pilot --n 10 --model gemini-3.5-flash-lite` (patient retry mode): **3 of 10 samples completed**;
the other 7 failed with API overload errors (503 and 504). All 3 completed samples passed the chat checks (0 failures).
This is not a failure rate: n is 3, one world model, chat checks only, a lite model (the stronger `gemini-3.5-flash` was
returning "high demand" errors at the time). Result file: `eval/raw_pilot_flash-lite.json`.
Reading: raw mode is judged on chat structure only (the calls come from our renderer), so it is likely to look better
than the plain-chat baseline, which tested whole cases including their own answer keys. Do not pitch raw mode as
"fails X of 10" unless `eval.run_generator` shows it.
