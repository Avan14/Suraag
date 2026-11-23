# Plain-LLM baseline: do it by hand (free)

1. Open a free chat app (claude.ai or ChatGPT). For **each** of the 10 cases, start a **new chat** (so no case sees the others) and paste the prompt below, exactly as written.
2. Save the whole reply as `eval/plain_baseline/case_01.md` ... `case_10.md`. Note which app/model you used in `eval/notes.md`.
3. Score each case with `eval/baseline_rubric.md` into `eval/plain_baseline/scores.csv` (about 5-8 minutes per case).
4. Tell me the number of broken cases. 3 or more of 10 = lead with it; 0-2 = lead with citation grading and scale.

Report it honestly as "n=10, one chat app, hand-checked, synthetic".

## Prompt (copy everything in the block)

```
Create a fictional Indian UPI-fraud forensic training case for university students.
Include:
1. A WhatsApp-style group chat export in Hinglish, about 25 numbered lines, each with a date and time.
2. A call log as CSV with columns row,datetime,direction,number,contact_name,duration_s (about 6 rows).
3. The EXIF metadata of one photo: DateTimeOriginal and GPS coordinates.
4. A list of 3 candidate places with coordinates.
5. Three questions: who instructed deleting the transfer record, when, and where the mule was when the photo was taken.
6. An answer key that cites the exact chat line numbers and call-log rows supporting each answer.
Include at least one plausible wrong suspect. All names fictional; all phone numbers must start with +91-5.
```
