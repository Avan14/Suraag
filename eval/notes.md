
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
