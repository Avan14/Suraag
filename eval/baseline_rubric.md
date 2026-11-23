# Plain-LLM baseline: hand-check rubric (Gate 1)

Check each `eval/plain_baseline/case_NN.md` by hand and fill one row of `scores.csv` with `y` or `n`.

| Check | Question | Counts toward "broken"? |
|---|---|---|
| R1 | Every citation in the answer key points to a chat line or call-log row that exists **and** says what the key claims. | yes |
| R2 | The chat time and the call-log time of the key event agree within 2 minutes, and the chat times are in order. | yes |
| R3 | Each name or alias refers to exactly one person throughout. | yes |
| R4 | Each question can be answered from the artifacts alone, with no fact that appears only in the answer key. | yes |
| R5 | A plausible wrong suspect exists. | no (reported separately) |
| R6 | The photo's EXIF time and GPS agree with the answer and with one of the candidate places. | yes |

- `broken` = `y` if **any** of R1, R2, R3, R4 or R6 is `n`.
- `checker` = your initials. If a second person checks, add their rows with their initials.
- `notes` = what exactly is wrong (e.g. "key cites line 14, which is about lunch").

**Gate 1 decision:** if 3 or more of 10 are broken, the video opens with the plain-LLM failure rate. If 0 to 2 are broken, it opens with citation grading and scale. Record the decision and n in `eval/notes.md`.

Data is synthetic. Report this as "n=10, hand-checked, synthetic", never as a general claim about LLMs.
