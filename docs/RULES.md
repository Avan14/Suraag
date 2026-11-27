# Suraag RULES.md: rules register for fictional forensic training cases

## 1. Purpose and status

Suraag (SLAY HACKS 2026) generates fictional Indian forensic training cases and proves they are solvable. Code builds a world model and writes the anchored evidence lines verbatim; an LLM (a Gemini model through google-genai; the model id is set in `.env`) writes only the filler chat; a verifier with six checks (anchor, traceability, contradiction, solvability, distractor, integrity) and a bounded repair loop decides whether a case ships; a deterministic grader scores student answers. A "raw" mode, where the LLM writes everything, is the baseline for comparison.

This file is a rules register. Each rule says what it checks, why it exists, where it comes from, how strong that source is, how it is tested and what state it is in, so that a judge or a forensic lecturer can audit any rule from the rule back to its source.

**Research current as of 23 November 2026.**

**Not legal advice.** This is training-project documentation, not legal advice. Statute wording was read through bare-act reproduction sites, not the official India Code or Gazette text, so verify any statute wording against the official India Code text before relying on it or hard-coding it.

Every case, file and screen produced by Suraag is labelled SYNTHETIC. Hashes show that a file is unchanged; they do not by themselves prove the file is authentic.

**Status as of 28 November 2026.** Statuses reflect the repository. *Implemented* means the named tests in `tests/` pass (15 rules); *Partial* means part of the rule is built and tested and the Status line says what is not (16 rules); every other rule is still Planned, Open or awaiting expert review. Module and test names in rules not yet built are proposals.

## 2. How to read this file

**Rule IDs.** The letter gives the family; the number is stable and is never reused.

| Prefix | Family | Covers |
|---|---|---|
| L | Logic and verification | The six checks, the repair loop, and generation rules that keep the LLM from changing facts |
| H | Handling and integrity | Hashing, copies, the practice certificate, chain of custody, isolation, what a hash shows |
| F | File formats | chat.txt, calls.csv, photo.jpg EXIF, phone numbers, languages |
| S | Scenario realism | UPI fraud facts, typologies, offence labels, tracing facts |
| R | Responsible use and fairness | SYNTHETIC labelling, names, bias audit, respectful portrayal |
| G | Grading and assessment | Deterministic grading, citations, scoring, difficulty, hints |
| E | Evaluation and claims | Baseline gate, reporting, claims that may and may not be made |

**Strength labels.**

| Label | Meaning |
|---|---|
| REQUIRED BY LAW OR STANDARD | The behaviour the rule reproduces is required by the cited law or standard in real practice (for example, fields of a real certificate). The project itself is not legally bound, and the label does not upgrade a weak source |
| GOOD PRACTICE | Recommended by standards bodies, guides, papers or consistent police or court documents, but not mandatory |
| PROJECT CONVENTION | A decision of this project. If no external source supports it the rule says "PROJECT CONVENTION: no external source" and cites nothing. Where sources are shown only as context, they do not justify the rule |

**Source quality tags** (carried over from the notes; they apply to the document, not to the rule). PRIMARY: official text or court order read directly. SECONDARY: legal publisher, bare-act reproduction, law firm, news report, open-source parser code, academic paper summary or tool documentation. WEAK: blog, vendor page, forum post or opinion piece. Only the legal note used these three tags on its sources (the UPI note flagged vendor, blog and secondary sources in words); for the other notes the tag was assigned here, on the same scale, from each note's own description of the source, and the register shows any caveat the note gave (for example "read through a summariser"). A PRIMARY tag does not mean the full text was checked.

**Status labels.**

| Label | Meaning |
|---|---|
| Planned | Designed and testable; not yet built or not yet shown passing |
| Partial | Part of the rule is built and tested; the Status line says what is missing |
| Implemented | Built and its named test passes |
| Needs expert review | A forensic lecturer should confirm the rule or its wording before it is relied on |
| Open | A decision or fact is unresolved; see section 6 |

**Checked by.** Checks live in `verify.py` as `check_anchor`, `check_traceability`, `check_contradiction`, `check_solvability`, `check_distractor` and `check_integrity`. A "planted defect" is a deliberately broken fixture case under `tests/fixtures/defects/` that the named check must reject. Test names are given as `file::test_name`.

**Citations.** `[S12]` points to the source register in section 7. A Caveat line appears only where the notes flag a conflict, a gap, a weak source or an inference.

## 3. Index of rules

| ID | Short name | Strength | Status |
|---|---|---|---|
| L-01 | Anchor check | GOOD PRACTICE | Implemented |
| L-02 | Traceability check | GOOD PRACTICE | Partial |
| L-03 | Contradiction check (time, entity, numeric) | GOOD PRACTICE | Partial |
| L-04 | Solvability check | PROJECT CONVENTION | Implemented |
| L-05 | Distractor check | GOOD PRACTICE | Implemented |
| L-06 | Integrity (sealing) check | GOOD PRACTICE | Implemented |
| L-07 | Repair loop and failure log | PROJECT CONVENTION | Implemented |
| L-08 | Code writes every concrete value; symbolic ground truth first | GOOD PRACTICE | Implemented |
| L-09 | Filler adds no facts | GOOD PRACTICE | Partial |
| L-10 | Causal prerequisites in timelines | GOOD PRACTICE | Partial |
| L-11 | Facts carry validity intervals | GOOD PRACTICE | Planned |
| H-01 | Manifest with a SHA-256 per file | PROJECT CONVENTION | Partial |
| H-02 | Hash before and after every copy; work on copies | GOOD PRACTICE | Planned |
| H-03 | Practice "Section 63 style" certificate (optional) | REQUIRED BY LAW OR STANDARD | Needs expert review |
| H-04 | Certificate defects are planted, labelled and not hard-coded to one signatory rule | GOOD PRACTICE | Needs expert review |
| H-05 | Chain-of-custody record has the consolidated fields | GOOD PRACTICE | Needs expert review |
| H-06 | Custody continuity | GOOD PRACTICE | Planned |
| H-07 | Isolation is documented, power state is not mandated | GOOD PRACTICE | Needs expert review |
| H-08 | Hash disclaimer wording and provenance labels | GOOD PRACTICE | Partial |
| F-01 | WhatsApp Android line grammar | GOOD PRACTICE | Implemented |
| F-02 | One date order per case | GOOD PRACTICE | Partial |
| F-03 | Line types the generator emits | GOOD PRACTICE | Partial |
| F-04 | Variants without a source are not emitted | GOOD PRACTICE | Open |
| F-05 | calls.csv columns and types | GOOD PRACTICE | Partial |
| F-06 | calls.csv encoding | GOOD PRACTICE | Implemented |
| F-07 | calls.csv date format (project decision) | PROJECT CONVENTION | Implemented |
| F-08 | EXIF base tags | GOOD PRACTICE | Partial |
| F-09 | EXIF tamper markers appear only when planted | GOOD PRACTICE | Planned |
| F-10 | photo.jpg is a camera original, not a forwarded copy | GOOD PRACTICE | Planned |
| F-11 | Phone-number policy (open) | PROJECT CONVENTION | Open |
| F-12 | Languages and Unicode | PROJECT CONVENTION | Implemented |
| S-01 | UPI reference and address formats | GOOD PRACTICE | Planned |
| S-02 | Amounts and timing plausible | PROJECT CONVENTION | Needs expert review |
| S-03 | Typologies and ring roles | GOOD PRACTICE | Needs expert review |
| S-04 | Withdrawn collect request is not a current mechanism | GOOD PRACTICE | Planned |
| S-05 | Evidence artefacts in a case | GOOD PRACTICE | Partial |
| S-06 | Offence labels | GOOD PRACTICE | Needs expert review |
| S-07 | Reporting, freezing and tracing facts only as sourced | GOOD PRACTICE | Needs expert review |
| S-08 | Anomaly patterns are labelled as inference | PROJECT CONVENTION | Planned |
| R-01 | SYNTHETIC label everywhere | PROJECT CONVENTION | Partial |
| R-02 | Fictional names, numbers and institutions | PROJECT CONVENTION | Partial |
| R-03 | Random guilt and a bias audit | PROJECT CONVENTION | Implemented |
| R-04 | Respectful, non-operational portrayal | GOOD PRACTICE | Needs expert review |
| R-05 | Not legal advice; practice certificate is not a legal form | PROJECT CONVENTION | Planned |
| G-01 | Deterministic grading; the overclaim check is advisory | PROJECT CONVENTION | Implemented |
| G-02 | Citation validity | PROJECT CONVENTION | Implemented |
| G-03 | Scoring rule | PROJECT CONVENTION | Implemented |
| G-04 | Distractor and difficulty design | GOOD PRACTICE | Planned |
| G-05 | Per-student variants | GOOD PRACTICE | Partial |
| G-06 | Tiered hints built in code | PROJECT CONVENTION | Implemented |
| E-01 | Baseline gate | PROJECT CONVENTION | Partial |
| E-02 | Report per language and per check | PROJECT CONVENTION | Partial |
| E-03 | No invented numbers | PROJECT CONVENTION | Planned |
| E-04 | The claims table is binding | GOOD PRACTICE | Planned |

54 rules in total (L 11, H 8, F 12, S 8, R 5, G 6, E 4).

## 4. Rules

Each rule uses one block format. Each Rule is one testable sentence (some are long because they list the required items); Why is one or two sentences.

## 4.1 Family L: Logic and verification

The six verifier checks (L-01 to L-06), the repair loop (L-07) and the generation rules that keep the LLM from damaging the facts (L-08 to L-11). Check functions are in `verify.py`: `check_anchor`, `check_traceability`, `check_contradiction`, `check_solvability`, `check_distractor`, `check_integrity`.

### L-01. Anchor check
- **Rule:** For every anchored fact in the world model, a line containing all of the fact's must_contain values exists verbatim in the file and at the line position the model recorded.
- **Why:** Code writes the anchor lines; if filler regeneration or a re-render drops or changes one, the case can no longer be solved or graded.
- **Source:** [S90] PRIMARY (related practice only: MuSR checks that each gold fact is entailed by the narrative; the method differs).
- **Strength:** GOOD PRACTICE
- **Checked by:** `suraag/verify.py::check_anchors`; `tests/test_verify_chat.py::test_anchor_text_removed_gives_anchor_missing`, `::test_raw_mode_finds_the_anchor_wherever_it_is`; `tests/test_defects.py` (missing_anchor and timestamp_clash defects).
- **Status:** Implemented

### L-02. Traceability check
- **Rule:** Every fact in the answer key lists at least one evidence line (file and line number), every listed line exists and contains that fact's must_contain values, and every anchor line maps back to exactly one world-model fact id.
- **Why:** The grader accepts a citation on the same test (G-02), so a fact that cannot be traced cannot be graded.
- **Source:** [S100] PRIMARY (pattern only: cite the evidence for each claim, then audit for uncited claims).
- **Strength:** GOOD PRACTICE
- **Checked by:** `suraag/verify.py::check_traceability`; `tests/test_verify.py::test_traceability_fails_for_unanchored_fact_and_unmapped_question`.
- **Status:** Partial. Not built yet: the check that every anchor line maps back to exactly one world-model fact (orphan anchors).
- **Caveat:** VeriScene is about crime-scene reconstruction from physical and legal evidence, not digital artefacts, and is a preprint of unknown peer-review status. Only the audit pattern is borrowed.

### L-03. Contradiction check (time, entity, numeric)
- **Rule:** After parsing chat.txt, calls.csv and the photo EXIF back from the shipped files, no value conflicts with the world model or with another file in any of three classes: time (order, date, zone), entity (every nickname in chat and every contact_name in calls.csv resolves to exactly one roster person; names, numbers and devices do not point to two people) and numeric (amounts, counts, durations, 12-digit references).
- **Why:** In long LLM text, timeline and fact errors dominate, and absolute-time errors sit furthest from the fact they contradict, so the check compares distant lines, not only neighbours. Rule-based checks are preferred because LLM checkers miss many errors.
- **Source:** [S94] PRIMARY; [S89] PRIMARY (automated checks of temporal coverage, counts and thresholds).
- **Strength:** GOOD PRACTICE
- **Checked by:** `suraag/verify.py::check_chat_consistency`, `::check_cross_time`, `::check_causality`; `tests/test_verify_chat.py::test_unknown_sender_gives_alias_unresolved_with_count`, `::test_swapped_filler_times_give_time_order`; `tests/test_verify.py::test_cross_time_fails_when_chat_and_calls_disagree`, `::test_cross_time_works_across_midnight`.
- **Status:** Partial. Not built yet: the numeric class (amounts, references) and the check that every calls.csv contact_name resolves to exactly one person.
- **Caveat:** No source measured contradiction rates in LLM-generated chat or call logs. The three class names are this project's grouping of the notes' candidate rule families.

### L-04. Solvability check
- **Rule:** A rule-based solver that reads only the shipped files (never the world model) returns the ground-truth answer, and returns no answer or a different one when every anchor line is removed.
- **Why:** This shows the case is solvable from the evidence given, not just claimed to be. An LLM blind solve on about 10 cases is run for information only and never enters a score or a pass/fail.
- **Source:** PROJECT CONVENTION: no external source.
- **Strength:** PROJECT CONVENTION
- **Checked by:** `suraag/solver.py`; `suraag/verify.py::check_solvability`; `tests/test_solver.py::test_fixture_is_solved_from_the_artifacts_alone`, `::test_blank_contact_name_makes_who_unsolvable`, `::test_two_instruction_lines_make_who_and_when_unsolvable`; `tests/test_defects.py` (unsolvable_question); `tests/test_levels.py` (every practice level). The blind solve (`eval/run_blind_solve.py`, `gemini-3.6-flash`, unscored) has been run three times: 30 of 30 answers on 10 stub-filler cases, 30 of 30 on 10 real-filler cases, and on the 14 shipped cases per level 15 of 15, 9 of 9, 8 of 12 and 12 of 12 (`eval/results.json`).
- **Status:** Implemented
- **Caveat:** The notes found no tool that checks solvability formally; implicit solvability comes from planting artefacts. A generator-side check that each ground-truth item is derivable from the output is, by the notes' own inference, a novel contribution and not established practice. It proves solvability for this project's solver, not that a student finds it easy.

### L-05. Distractor check
- **Rule:** Every distractor is recorded in the world model with an id, is rendered into the files, and is insufficient alone: the solver given every line except the anchor lines returns no unique answer.
- **Why:** A distractor should look relevant without deciding the case; a decisive one makes the answer key wrong or the case trivial.
- **Source:** [S97] PRIMARY (over-specific clues make a case trivial); [S90] PRIMARY (a rule-based baseline at chance level shows the narrative does not leak the answer).
- **Strength:** GOOD PRACTICE
- **Checked by:** `suraag/verify.py::check_distractor`; `tests/test_verify.py::test_distractor_checks`.
- **Status:** Implemented. The 'insufficient alone' test is `suraag/verify.py::check_insufficient_alone`: with every chat line and call row a who/when answer is anchored in removed, the solver must not reach the key (`tests/test_insufficient_alone.py`, all 14 shipped cases pass). Photo questions rest on single EXIF tags and are not part of this test.
- **Caveat:** The notes found no educator source that discusses distractors in forensic cases specifically; the minimum distractor count per difficulty is a project setting.

### L-06. Integrity (sealing) check
- **Rule:** The SHA-256 of each shipped file's bytes equals its entry in manifest.json, and this check runs last, after any repair, on the exact bytes that will be delivered.
- **Why:** Sealing after repair means the manifest describes what the student receives. A match shows the files are unchanged since sealing; it shows nothing else (see H-08).
- **Source:** [S24] PRIMARY (hash at acquisition, verification hash before analysis, rehash at the end); [S2] SECONDARY (a hash report is enclosed with the certificate).
- **Strength:** GOOD PRACTICE
- **Checked by:** `suraag/repair.py::seal`; `tests/test_repair.py::test_clean_case_seals_with_matching_hashes`.
- **Status:** Implemented. A loaded case is re-verified and its hashes compared with its manifest before the lecturer view shows it as verified (`app.py`, `lecturer_view`); `tests/test_levels.py::test_every_shipped_case_verifies_and_matches_its_hashes` does the same for every shipped case.

### L-07. Repair loop and failure log
- **Rule:** A case that fails a check is repaired at most 3 times (regenerate the LLM filler, or re-render the CSV or EXIF from the clean model), all six checks run again from scratch after each repair, every failure is appended to logs/failures.jsonl with the failing check's name, and a case still failing after the third repair is rejected and not shipped.
- **Why:** A bounded loop caps cost; re-running everything catches repairs that break another check; the log supplies the per-check failure counts used in E-02.
- **Source:** PROJECT CONVENTION: no external source for the limit of 3. (A retry-then-prune step also appears in MuSR [S90] PRIMARY; it is not used to justify the number.)
- **Strength:** PROJECT CONVENTION
- **Checked by:** `suraag/repair.py::run`; `tests/test_repair.py::test_chat_clash_is_flagged_then_repaired_by_regenerating_the_chat`, `::test_calls_clash_is_repaired_by_rerendering_calls_only`, `::test_unrepairable_filler_is_discarded_logged_and_writes_no_files`.
- **Status:** Implemented

### L-08. Code writes every concrete value; symbolic ground truth first
- **Rule:** Every date, time, duration, amount, reference number, phone number and count in any file is produced by code from the world model, which is built first (as structured data, from a fixed seed) and rendered into files afterwards, and no LLM prompt asks for such a value.
- **Why:** LLMs are weakest at date and duration arithmetic and default to years from their training data, so deterministic work goes to code. The same seed gives the same bytes, which makes a case auditable.
- **Source:** [S83] PRIMARY (deterministic tasks go to code; models defaulted to 2023 or 2025 dates); [S91] PRIMARY (duration arithmetic as low as about 13.5% for the models tested); [S90] PRIMARY (symbolic tree built first, then rendered to prose); [S80] SECONDARY (EvidenceForge keeps the LLM out of record generation and is seed-reproducible); [S95] PRIMARY (on forensic timelines ChatGPT-4o mis-ordered events and did worse than a rule-based approach).
- **Strength:** GOOD PRACTICE
- **Checked by:** `suraag/skeleton.py`, `suraag/render.py`; `tests/test_render.py::test_render_is_byte_for_byte_repeatable`; `tests/test_skeleton.py::test_build_case_is_deterministic_and_seeds_differ`; `tests/test_filler_rules.py`.
- **Status:** Implemented
- **Caveat:** The benchmarks used other models (for example GPT-4o, Claude-3-Sonnet, Gemini 1.5 Pro), not the Gemini model this project uses, and none tested Hinglish chat. The rule rests on the pattern, not on a measurement of this project's model.

### L-09. Filler adds no facts
- **Rule:** Every LLM filler line passes the filler constraint list: (a) no digit characters (ASCII or Devanagari) and no currency symbol or amount word; (b) no date, clock time, month name or weekday name; (c) no statement of who told whom to send, pay, delete, share or do anything; (d) speaker and any named person come only from the case roster; (e) no real brand, bank, app or agency name; (f) no URL; (g) Roman Hinglish or English only, within the configured length; and a failing line is regenerated, never patched by code.
- **Why:** Prompt-stated rules are enforced unreliably by LLMs, so they are checked by code after generation. Banning numbers and instruction claims keeps the solver's facts, and the answer key, entirely in the code-written lines.
- **Source:** [S83] PRIMARY (only the strongest model followed prompt-stated coherence rules; so check in code).
- **Strength:** GOOD PRACTICE
- **Checked by:** `suraag/fillerrules.py`; `suraag/verify.py::check_chat_consistency`; `tests/test_filler_rules.py::test_each_rule_catches_its_case`, `::test_a_bad_filler_line_fails_the_hybrid_check_with_a_clear_message`.
- **Status:** Partial. Not built yet: named persons inside filler text (only senders are checked), language and length limits, and a longer brand list.
- **Caveat:** Items (c) to (g) are project choices; only the principle "check in code, not just in the prompt" comes from the source. A word list for Hinglish instruction claims cannot be complete; an LLM overclaim check (G-01) could flag more, but none is wired in yet, and it could never change a score.

### L-10. Causal prerequisites in timelines
- **Rule:** Each world-model event lists the events that must come before it (for example the photo is taken before the chat line that sends it, a payment alert follows the debit, a call precedes any message saying "I called you"), and the rendered times satisfy every prerequisite.
- **Why:** Causal ordering is what makes a timeline believable and what a solver relies on; LLMs break it, and only the strongest tested model kept to stated ordering rules.
- **Source:** [S80] SECONDARY (prerequisite events inserted, for example DNS before connection); [S81] SECONDARY (causality and timing scored); [S83] PRIMARY (coherence rules such as browser open before visit).
- **Strength:** GOOD PRACTICE
- **Checked by:** `suraag/verify.py::check_causality`; `tests/test_verify.py::test_causality_fails_when_a_cause_comes_after_its_effect`.
- **Status:** Partial. Not built yet: prerequisites are depends_on links between world-model events; ordering of a chat line after the photo it sends is not modelled.
- **Caveat:** EvidenceForge covers security logs; the sources fetched do not mention chat or message artefacts, so applying the idea to chats is an analogy.

### L-11. Facts carry validity intervals
- **Rule:** State facts (who holds a phone or SIM, whose account it is, where a person is) have a start and an end time in the world model, and no two incompatible states of one entity overlap.
- **Why:** An entity cannot be in two states at once; interval overlap is a simple symbolic test for the contradictions LLMs introduce.
- **Source:** [S92] PRIMARY (atomic pre- and post-facts with validity intervals; contradiction when a later pre-fact conflicts with an earlier post-fact); [S93] PRIMARY (static and dynamic memory, commit only if validation passes).
- **Strength:** GOOD PRACTICE
- **Checked by:** `world.py::check_state_overlap` (called by `check_contradiction`); `tests/test_world.py::test_two_holders_of_one_phone_overlap_fails`, `::test_back_to_back_states_pass`.
- **Status:** Planned
- **Caveat:** FactTrack uses an NLI model and GPT-4 scores as a proxy and finds only binary contradictions; ConWriter was evaluated on 20 cases. Both are preprints on non-forensic text. This project applies the idea symbolically.

## 4.2 Family H: Handling and integrity

These rules model how evidence is hashed, copied, certified and passed on. The custody record and the practice certificate belong to an optional handling exercise; they are not among the four case files (chat.txt, calls.csv, photo.jpg, manifest.json).

**Schedule fields as recorded in the research notes** (reproduction of the Gazette text, [S2] SECONDARY; verify against India Code):

| Part | Fields recorded |
|---|---|
| A (party or person in control) | Declarant name; son/daughter/spouse of; residing or employed at; solemn affirmation; source tick-box (Computer/Storage Media, DVR, Mobile, Flash Drive, CD/DVD, Server, Cloud, Other); make and model; colour; serial number; IMEI/UIN/UID/MAC/Cloud ID; declarations of lawful control and regular use, proper working, regular feeding of information; tick Owned / Maintained / Managed / Operated; hash value and algorithm (SHA1, SHA256, MD5, Other "legally acceptable standard"); "hash report to be enclosed"; name and signature; Date (DD/MM/YYYY); Time (IST, 24-hour); Place |
| B (expert) | Same identity block; same source tick-box and make, model, colour, serial, IMEI/UIN/UID/MAC/Cloud ID (the source the record was "obtained from"); same hash statement and algorithm options; hash report enclosed; name, designation and signature; same date, time and place. No regular-use or proper-working declarations |

### H-01. Manifest with a SHA-256 per file
- **Rule:** manifest.json lists every case file with its byte size and SHA-256 as 64 lowercase hex characters, does not list itself, and the hash report printed from it shows the tool name and version, the algorithm, then one line per file with hash, size and name.
- **Why:** A per-file hash list lets anyone detect later change and mirrors the hash report the Schedule says to enclose. SHA-256 is a project convention: the Schedule names SHA1, SHA256, MD5 or Other and no source found makes one mandatory. SWGDE asks for SHA-2 or SHA-3 where a match is relied on as evidence, and the Council of Europe guide warns against using MD5 or SHA-1 alone.
- **Source:** PROJECT CONVENTION for the choice of SHA-256 and the layout. Context only: [S2] SECONDARY (algorithm options, hash report enclosed, no format given); [S25] PRIMARY; [S28] PRIMARY; [S26] PRIMARY (SHA-1 retired by 31 Dec 2030).
- **Strength:** PROJECT CONVENTION
- **Checked by:** `suraag/repair.py::seal`, `suraag/parse.py::Artifacts.sha256`; `tests/test_repair.py::test_clean_case_seals_with_matching_hashes`; `tests/test_parse.py::test_sha256_matches_bytes_and_uses_bom_for_csv`.
- **Status:** Partial. Not built yet: byte size per file and the printed hash report.
- **Caveat:** No source says how a hash must be formatted (case, spacing, one per file or combined). The Schedule still allows MD5 and SHA1, so this rule is stricter than Indian law. The Supreme Court order says nothing about algorithms, and press reports of it add none ([S4] PRIMARY; [S5] SECONDARY).

### H-02. Hash before and after every copy; work on copies
- **Rule:** Every copy made by the app or an exercise is hashed before and after copying with equal results, the solver and any student exercise read only the copy, and the original case folder is read-only.
- **Why:** NIST asks for message digests of original and copy to be compared and for examination of copies only; ACPO's first principle is not to change original data; a Delhi High Court order told a department to copy phone data with a hash and return the devices.
- **Source:** [S22] PRIMARY; [S24] PRIMARY; [S27] PRIMARY; [S33] PRIMARY; [S30] PRIMARY.
- **Strength:** GOOD PRACTICE
- **Checked by:** `copyutil.py::copy_with_hashes`; `tests/test_copy.py::test_hash_before_equals_after`, `::test_solver_never_opens_original` (patch `open`), `::test_original_folder_is_read_only`.
- **Status:** Planned
- **Caveat:** SWGDE notes that two separate extractions of a live phone can give different hashes, so the comparison must be between the same image before and after, never between two extractions. Project case files are static, but the rule keeps like-with-like. NIST SP 800-86 was read only in part.

### H-03. Practice "Section 63 style" certificate (optional)
- **Rule:** When the practice certificate exercise is on, the form has Part A and Part B with the fields in the table above, shows Date as DD/MM/YYYY and Time as 24-hour IST, carries the same hash and algorithm in both parts as the manifest, and is titled "PRACTICE FORM - NOT A LEGAL FORM - SYNTHETIC".
- **Why:** Students meet the real certificate in court work; the exercise lets them practise reading the fields without implying that the form is valid.
- **Source:** [S2] SECONDARY; [S4] PRIMARY (Part A requires hash disclosure; Part B is an expert declaration); [S3] SECONDARY.
- **Strength:** REQUIRED BY LAW OR STANDARD
- **Checked by:** `certificate.py::render_practice_certificate`; `tests/test_certificate.py::test_has_part_a_and_part_b_fields`, `::test_date_and_time_formats`, `::test_title_has_practice_label`, `::test_hash_equal_in_both_parts_and_manifest`; planted defect `certificate_hash_mismatch` (extends `check_integrity`).
- **Status:** Needs expert review
- **Caveat:** "Required" here means the Schedule requires these fields on a real certificate; the project is not bound by it and the exercise is optional. The Schedule text was read only through a bare-act reproduction, not India Code, and two reproductions differ by a typo in s.63(1). The Supreme Court order mentions the hash only for Part A while the reproduced Schedule has it in both parts; carrying the same hash in both and flagging a mismatch is this project's conservative choice (an inference in the notes). Bar & Bench places the hash only in Part B and is contradicted by the Schedule text ([S14] WEAK). No source says whether the date and time format is enforced.

### H-04. Certificate defects are planted, labelled and not hard-coded to one signatory rule
- **Rule:** Practice certificates with deliberate defects (hash not equal to the manifest, algorithm not ticked, hash report not enclosed, Part A or Part B missing, Part B signatory credentials not shown) exist only as variants listed in the case answer key as planted defects, and no validator in the code requires the Part B signatory to be a notified s.79A examiner.
- **Why:** The Supreme Court left open who may sign Part B, so hard-coding "only s.79A examiners" would teach a rule the Court did not make. Labelled defects give students something to find.
- **Source:** [S4] PRIMARY (Madras High Court view not binding; question left open); [S6] SECONDARY; [S7] SECONDARY; [S8] PRIMARY (21 notified labs, context for access).
- **Strength:** GOOD PRACTICE
- **Checked by:** `certificate.py::make_defect_variant`; `tests/test_certificate_defects.py::test_each_defect_is_listed_in_answer_key`, `::test_no_validator_requires_79a_only`, `::test_each_defect_is_caught_by_check_integrity`.
- **Status:** Needs expert review
- **Caveat:** The order is an admission-stage order with short reasoning; it says it is "possible to hold" that a person with special skill may sign and keeps the question open. Verdictum's headline says an expert "is competent", which overstates the order. Anything after mid-2026 (a review petition, a fuller hearing, MeitY adding examiners) was not checked.

### H-05. Chain-of-custody record has the consolidated fields
- **Rule:** Every custody entry has case or FIR id, exhibit id, description (make, model, serial or IMEI), collected-by name and role, collection date, time and place, giver and receiver names with a signature marker, transfer date and time, reason for transfer, storage location between transfers, seal or tamper-tape number, and hash value(s); a seizure may also carry a seizure-recording reference and independent witness names.
- **Why:** Authorities converge on what, who, when, where, why, each transfer and storage; courts discount forensic reports when custody is not shown.
- **Source:** [S23] PRIMARY; [S22] PRIMARY; [S30] PRIMARY; [S29] PRIMARY; [S31] PRIMARY; [S28] PRIMARY; [S21] PRIMARY (headings only); [S13] SECONDARY; [S15] SECONDARY and [S32] SECONDARY (the optional seizure fields).
- **Strength:** GOOD PRACTICE
- **Checked by:** `custody.py::validate_custody_record`; `tests/test_custody.py::test_entry_missing_each_field_fails` (parametrised over the fields).
- **Status:** Needs expert review
- **Caveat:** ISO/IEC 27037 clause 6.1 and Annex B text was not readable, so its minimum fields are unknown ([S20] PRIMARY). No source names seal number or hash value as a mandatory custody column; they are common practice that the Indian documents imply. The UP SOP, Bihar order and Sikkim deck are undated or of unclear authorship. The field list is a synthesis. For BNSS only ss.94, 105 and 176(3) were confirmed, from secondary sources.

### H-06. Custody continuity
- **Rule:** In every custody record each receiver is the next entry's giver, transfer times never decrease, no handler appears in the storage trail without an entry, and the seal number recorded at opening equals the one recorded at sealing.
- **Why:** These are the continuity tests the notes derive from the sources; a break is what makes custody evidence weak.
- **Source:** [S22] PRIMARY (log of everyone with custody); [S31] PRIMARY (every transfer signed, no time gaps); [S28] PRIMARY (check seals on opening, reseal after examination).
- **Strength:** GOOD PRACTICE
- **Checked by:** `custody.py::check_continuity`; `tests/test_custody.py::test_receiver_not_next_giver_fails`, `::test_decreasing_time_fails`, `::test_missing_handler_entry_fails`, `::test_seal_number_mismatch_fails`.
- **Status:** Planned
- **Caveat:** The continuity checks are the notes' inference, not wording found in any single source.

### H-07. Isolation is documented, power state is not mandated
- **Rule:** Every custody entry for a phone records the isolation method (flight mode, Faraday bag or foil, RF-shielded enclosure, powered off) and the power state when found, and the verifier accepts both powered-on and powered-off phones.
- **Why:** ACPO says power a live phone off (Faraday only on advice); SWGDE says keep it powered and isolated and does not rely on airplane mode alone; Indian police and judicial-academy documents mostly say isolate and keep the state. The one point they share is isolation from the network.
- **Source:** [S27] PRIMARY; [S23] PRIMARY; [S30] PRIMARY; [S29] PRIMARY; [S31] PRIMARY.
- **Strength:** GOOD PRACTICE
- **Checked by:** `custody.py::validate_custody_record`; `tests/test_custody.py::test_phone_entry_without_isolation_fails`, `::test_powered_on_and_powered_off_both_pass`.
- **Status:** Needs expert review
- **Caveat:** This is the largest cross-source conflict in the notes. The Indian documents are police or training documents; no Indian lab document was found. Bihar adds that a phone that is off should have its battery removed and IMEI and SIM recorded.

### H-08. Hash disclaimer wording and provenance labels
- **Rule:** Every screen, report and manifest field that shows a hash carries the sentence "A matching hash shows this file has not changed since the hash was computed; it does not show who made the file or that its content is genuine" (with a Hindi version in the Hindi UI) and no text says a hash proves a chat, call log or photo is authentic; and the case card labels chat.txt as an in-app text export (weak provenance: no signature or checksum inside; corroborate), calls.csv as an exported copy and photo.jpg as an original image file, and no file as a device extraction.
- **Why:** SWGDE treats hashing as an integrity check only, and a chat export has no signature or checksum inside it, so it can be edited before the first hash. The Supreme Court, by contrast, describes the hash and the Part B expert in terms of authenticity and integrity. Forensic sources favour acquiring from the device, so an in-app export should be called weak.
- **Source:** [S24] PRIMARY (integrity only); [S29] PRIMARY (the certificate addresses admissibility, not authenticity); [S4] PRIMARY (hash as an "electronic fingerprint" serving authenticity and integrity); [S34] PRIMARY; [S35] SECONDARY (exported chat can be edited without visible signs); [S28] PRIMARY (physical and file-system copies preferred; for chat apps, change the app, not the message database).
- **Strength:** GOOD PRACTICE
- **Checked by:** `tests/test_repair.py::test_manifest_carries_the_synthetic_flag_the_hash_note_and_the_date_order`, `::test_the_ui_hash_note_is_the_same_sentence_as_the_manifests`; `tests/test_i18n.py::test_both_languages_have_exactly_the_same_keys` (Hindi version).
- **Status:** Partial. Not built yet: case-card provenance labels (chat as a weak text export) and the scan for forbidden phrases such as 'proves authentic'.
- **Caveat:** No source states the limit in one sentence; the wording is this project's synthesis. Two positions exist (SWGDE and Bihar on one side, the Supreme Court's looser language on the other) and the app should teach both. The strong, moderate and weak tiering of provenance (device extraction with hash and tool log, backup with key, text export or screenshot) is the notes' inference; no standard, SWGDE document, NIST publication or Indian SOP found addresses "Export chat". The IJERT review is from a lower-tier journal and was read through a summariser.

## 4.3 Family F: File formats

All example lines are synthetic. There is no official WhatsApp export specification: the grammar comes from what widely used open-source parsers accept, so every WhatsApp rule below is SECONDARY at best.

### F-01. WhatsApp Android line grammar
- **Rule:** Every message line in chat.txt matches `DD/MM/YY, h:mm am|pm - Sender: text` (two-digit day, month and year; 12-hour clock with unpadded hour and lower-case am or pm; no seconds; no brackets; " - " before the sender), for example `04/03/26, 9:14 pm - Raju bhai: Chai pe aa ja`, and the file is UTF-8.
- **Why:** This is the Android style most plausible for Indian users and the one the parsers document; the verifier uses a tolerant parser (optional marks, brackets, seconds, 4-digit years) while the generator emits only the strict form.
- **Source:** [S36] SECONDARY (Android example `12/08/2016, 16:20 - username:`); [S37] SECONDARY (shared header regex; README example `06/03/2017, 00:45 - Sample User: ...`); [S40] SECONDARY (Android indicator); [S38] SECONDARY; [S39] SECONDARY (reads UTF-8).
- **Strength:** GOOD PRACTICE
- **Checked by:** `suraag/render.py::render_chat`; `tests/test_render.py::test_chat_layout_and_anchor_line`; `tests/test_parse.py::test_chat_text_with_syntax_chars`; `tests/test_timefmt.py::test_formats_match_the_documented_examples`.
- **Status:** Implemented
- **Caveat:** Grammar is reverse-engineered from third-party parsers; no changelog by app version was found. No source describes en-IN output (am/pm case, 2 or 4 digit years), so lower-case am/pm and 2-digit years follow the project example and parser samples. The notes give no source on whether WhatsApp writes a BOM, so none is written (project choice).

### F-02. One date order per case
- **Rule:** Every case fixes DD/MM order, records it as `chat_date_order = "DMY"` in manifest.json, the verifier parses with that order and never guesses, and any case spanning more than one day has at least one chat date with a day number above 12.
- **Why:** Parsers cannot read day-month order from the file; they infer it from values above 12 or default to days first. A line like `04/03/26` is ambiguous (4 March or 3 April) without the metadata.
- **Source:** [S37] SECONDARY (inference from values above 12; days-first default); [S36] SECONDARY.
- **Strength:** GOOD PRACTICE
- **Checked by:** `tests/test_repair.py::test_manifest_carries_the_synthetic_flag_the_hash_note_and_the_date_order` (chat_date_order is DMY in the manifest).
- **Status:** Partial. Not built yet: the rule that a multi-day case has a chat date with a day above 12, and the parser's refusal to guess.

### F-03. Line types the generator emits
- **Rule:** chat.txt contains only these line types: a message; a continuation line with no header (joined to the previous message with a newline); a system line with a header and no sender (for example `04/03/26, 9:00 pm - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.`); and message lines whose text is `<Media omitted>`, `IMG-YYYYMMDD-WAnnnn.jpg (file attached)` or `This message was deleted`.
- **Why:** These are the line types the parsers recognise; any line that fails the header regex is treated as part of the previous message.
- **Source:** [S37] SECONDARY (system events have no author; continuation lines); [S38] SECONDARY (multi-line messages preserved; English system phrases); [S40] SECONDARY (`<media omitted>`, `(file attached)`); [S41] WEAK (encryption notice text, deleted string); [S42] WEAK (attachment line example).
- **Strength:** GOOD PRACTICE
- **Checked by:** `tests/test_render.py::test_extra_filler_is_dropped_and_newlines_flattened`.
- **Status:** Partial. Not built yet: continuation, system and media lines are never emitted; the SYNTHETIC header is a plain first line, not a timestamped system line.
- **Caveat:** The encryption text and deleted string come from a WEAK mirror of a loader; system text is localised to the phone language, so English is the only wording used. File naming: an Android export is named like `WhatsApp Chat with <Contact>.txt` per a vendor blog (WEAK); the project file is chat.txt.

### F-04. Variants without a source are not emitted
- **Rule:** The generator never writes iOS bracket lines, U+200E or U+200F marks, a narrow no-break space (U+202F) before am or pm, an edited-message marker, or "You deleted this message"; the iOS bracket form (`[DD/MM/YY, HH:MM:SS] Name: text`) is a documented stretch with its own renderer and fixtures, accepted by the verifier only when the case metadata says platform is ios.
- **Why:** The notes could not confirm these variants from a WhatsApp-specific source, and emitting them would present guesses as realism.
- **Source:** [S37] SECONDARY and [S40] SECONDARY (iOS brackets, seconds, optional U+200E); [S36] SECONDARY.
- **Strength:** GOOD PRACTICE
- **Checked by:** `tests/test_whatsapp.py::test_android_output_has_no_lrm_or_u202f`, `::test_no_edited_marker`, `::test_ios_fixture_parses_when_platform_ios` (stretch).
- **Status:** Open
- **Caveat:** U+202F before am or pm in newer exports, the edited-message marker, "You deleted this message", iOS system-line rendering and iOS omitted-media wording are unconfirmed in the notes. Message-cap numbers come only from a vendor blog.

### F-05. calls.csv columns and types
- **Rule:** calls.csv has exactly the columns row, datetime, direction, number, contact_name, duration_s; row is a 1-based integer in file order; direction is one of incoming, outgoing, missed or rejected (Android types 1, 2, 3 and 5); number matches the F-11 pattern; contact_name resolves to exactly one roster person; duration_s is a non-negative whole number of seconds, 0 for missed and rejected calls.
- **Why:** This is a handset-style call log using the documented Android vocabulary (duration in seconds). A real handset stores the date as epoch milliseconds, and an operator CDR is a different, richer artefact; calls.csv is neither, and the case card says so.
- **Source:** [S43] PRIMARY (columns, type values 1-7, date in epoch milliseconds, duration in seconds); [S44] SECONDARY (operator CDR fields and varying formats).
- **Strength:** GOOD PRACTICE
- **Checked by:** `tests/test_render.py::test_calls_roundtrip_and_header`.
- **Status:** Partial. Not built yet: the 'rejected' direction is unused, no test for zero duration on missed calls, and contact_name uniqueness is unchecked (see L-03).
- **Caveat:** The project columns are a renaming and subset of the Android columns. No official Indian CDR schema was found; the CDR field list is assembled from one academic paper, training slides and commercial commentary, and operator column names rest on a low-reliability blog. The CDR code vocabulary (MOC, MTC) is an assumption and is not used. Zero duration for missed calls is a project convention.

### F-06. calls.csv encoding
- **Rule:** calls.csv is UTF-8 with a BOM (bytes EF BB BF), uses CRLF line ends, has the header row first, and double-quotes every text field.
- **Why:** Excel recognises UTF-8 only when a BOM is present, so a BOM-less file with Devanagari names shows as garbled text.
- **Source:** [S57] PRIMARY; [S58] WEAK; [S45] SECONDARY (UK comparison spec: comma-delimited, double-quoted, CRLF).
- **Strength:** GOOD PRACTICE
- **Checked by:** `suraag/render.py::render_calls`, `suraag/parse.py::Artifacts.calls_bytes`; `tests/test_render.py::test_calls_roundtrip_and_header`, `::test_written_files_roundtrip_and_csv_has_a_bom`.
- **Status:** Implemented
- **Caveat:** No source covers Indian police or lab practice on CSV encoding or delimiter, and Excel's day-month behaviour on en-IN settings was not verified. The UK spec is not Indian.

### F-07. calls.csv date format (project decision)
- **Rule:** The datetime column is ISO 8601 local time with an explicit offset, `YYYY-MM-DDTHH:MM:SS+05:30`, and the verifier parses it with the standard library, never by guessing.
- **Why:** ISO removes the day-month ambiguity, and the explicit offset removes the time-zone trap. That the chat uses DD/MM/YY with a 12-hour clock and no zone while the CSV uses ISO with an offset is realistic, because Indian CDR deliveries vary in date and time styles by provider; the solver must reconcile the two.
- **Source:** PROJECT CONVENTION for the format. Context only: [S44] SECONDARY (date and time formats vary by provider; 24-hour or AM/PM); [S58] WEAK (Excel recognises YYYY-MM-DD).
- **Strength:** PROJECT CONVENTION
- **Checked by:** `suraag/timefmt.py::csv_ts`; `tests/test_timefmt.py::test_formats_match_the_documented_examples`; `tests/test_verify.py::test_cross_time_works_across_midnight`.
- **Status:** Implemented
- **Caveat:** No source states how time zones appear in Indian CDRs; the UK spec and the Kanpur paper both give bare local times. The notes did not test Excel on the `T` and offset form.

### F-08. EXIF base tags
- **Rule:** photo.jpg EXIF holds DateTimeOriginal and CreateDate with equal values in `YYYY:MM:DD HH:MM:SS` form; OffsetTime, OffsetTimeOriginal and OffsetTimeDigitized are `+05:30`; the time equals the capture time in the world model; in a clean photo ModifyDate equals DateTimeOriginal or is at most 5 seconds later (never earlier); no Software tag is written; ImageDescription carries the SYNTHETIC label (R-01); and Make and Model come from `device_profiles.json`, where every entry is marked `sourced: false`.
- **Why:** EXIF date strings carry no zone, so the OffsetTime tags are the only zone information inside the file; a clean camera original has a modify time equal to or within seconds of its capture time.
- **Source:** [S50] SECONDARY (tag names and IDs); [S51] SECONDARY (OffsetTime tags arrived with Exif 2.31; date strings are naked local time); [S52] SECONDARY; [S53] SECONDARY.
- **Strength:** GOOD PRACTICE
- **Checked by:** `tests/test_photo.py::test_exif_fields_round_trip`, `::test_clean_photo_has_the_full_date_and_offset_tag_set`.
- **Status:** Partial. Not built yet: Make and Model come from a short list in skeleton.py, not device_profiles.json.
- **Caveat:** The CIPA DC-008 standard itself was not read; the year Exif 2.31 appeared is inconsistent on the Wikipedia page (2013 or 2016). Make and Model values are unsourced assumptions; no source gives typical values for Indian-market phones. Real phone photos usually carry a firmware build string in Software, so writing none is a simplification. The 5-second threshold is a project choice. No GPS tags are written (project choice); if added later, GPS UTC time should equal DateTimeOriginal minus 05:30 (the notes' inference; that GPSTimeStamp is UTC was not confirmed by a fetched source).

### F-09. EXIF tamper markers appear only when planted
- **Rule:** A Software tag naming an editor, a ModifyDate earlier than DateTimeOriginal or later by more than 5 seconds, or a dropped or inconsistent OffsetTime tag appears only in photos planted as tampered, and each such case lists the marker in its answer key.
- **Why:** These are the editing indicators the forensic guides name, so a case that shows them without a plan would give a false clue.
- **Source:** [S52] SECONDARY (Software tag; capture date not matching modification date; EXIF can be forged); [S53] SECONDARY (editors leave fingerprints; correlate with file-system metadata).
- **Strength:** GOOD PRACTICE
- **Checked by:** `render/exif.py::apply_tamper`; `tests/test_exif.py::test_markers_only_in_planted_tamper_cases`, `::test_tamper_marker_listed_in_answer_key`; planted defect `exif_modified_after_capture`.
- **Status:** Planned
- **Caveat:** EXIF is easy to forge, so a clean EXIF is not proof of authenticity. The thumbnail-mismatch cue is well known but no fetched source supports it, so it is not generated.

### F-10. photo.jpg is a camera original, not a forwarded copy
- **Rule:** photo.jpg has full camera-style EXIF and a recorded camera-style name `IMG_YYYYMMDD_HHMMSS.jpg` whose timestamp matches DateTimeOriginal within 2 seconds, and any chat line showing a WhatsApp-style name `IMG-YYYYMMDD-WAnnnn.jpg` uses the date of that chat line and never claims the file carries Make, Model or GPS.
- **Why:** WhatsApp standard-quality sends compress the image and strip most EXIF, and the WA name carries the send or receive date, not the capture date. A photo that is a forwarded copy could not also carry a camera model.
- **Source:** [S54] WEAK; [S55] WEAK; [S56] SECONDARY (IMG_ and PXL_ camera names); [S42] WEAK.
- **Strength:** GOOD PRACTICE
- **Checked by:** `tests/test_photo.py::test_camera_name_matches_exif_time`, `::test_wa_filename_date_equals_chat_line_date`; verified by `check_contradiction`.
- **Status:** Planned
- **Caveat:** The strongest sources here are WEAK (a blog and forum observations). Naming for Samsung, Xiaomi, Oppo, Vivo and Realme was not sourced; whether Pixel names carry milliseconds, and whether the WA counter resets daily, are unconfirmed. Sending a photo as a document keeps EXIF (blog claim).

### F-11. Phone-number policy (open)
- **Rule:** Every fictional number in every file matches `^\+91-5\d{4}-\d{5}$`, no case uses a number starting 6, 7, 8 or 9, a `1xxxxxxxxx` special-service number or a short code, the UI never renders a number as a clickable call link, and every case carries the SYNTHETIC label (R-01).
- **Why:** The notes confirm a leading 5 is not a mobile range (mobile numbers are levels 6 to 9). They do not confirm it is unreachable: level 5 is used for some fixed lines and five-digit short codes, and STD codes beginning with 5 exist (0522, 0542), so a number could match a real landline.
- **Source:** PROJECT CONVENTION for the pattern. Context: [S46] PRIMARY; [S47] PRIMARY; [S48] SECONDARY; [S49] WEAK.
- **Strength:** PROJECT CONVENTION
- **Checked by:** Proposed, not built yet: `numbers.py::fictional_number`; `tests/test_numbers.py::test_pattern`, `::test_no_mobile_prefix`, `::test_no_special_service_numbers`, `::test_ui_has_no_tel_links`.
- **Status:** Open
- **Caveat:** No official reserved range for fictional or drama numbers was found (not proven not to exist). The 5xxxx convention means "clearly not a mobile", not "guaranteed unassigned". Recommended mitigation: the visible SYNTHETIC marker plus no clickable numbers, and a decision by the forensic lecturer on whether to keep the convention. Current numbering allocations after 2025 were not checked.

### F-12. Languages and Unicode
- **Rule:** UI strings exist in English and Hindi; case content is English or Roman Hinglish; names are stored with Devanagari spellings in NFC form; Devanagari case content is a stretch goal and is not generated by default.
- **Why:** Mixed Unicode forms of the same name break matching, and the nickname and contact_name uniqueness test in L-03 needs one canonical spelling.
- **Source:** PROJECT CONVENTION: no external source.
- **Strength:** PROJECT CONVENTION
- **Checked by:** `suraag/names.py`, `suraag/i18n.py`; `tests/test_skeleton.py::test_names_are_nfc_and_draws_are_reproducible`; `tests/test_i18n.py::test_both_languages_have_exactly_the_same_keys`.
- **Status:** Implemented

## 4.4 Family S: Scenario realism

All scenario content is fictional. Where the notes found only secondary or weak sources, the rule says so.

### S-01. UPI reference and address formats
- **Rule:** Every UPI reference in any file is 12 numeric digits with no letters and no date-based prefix, generated by code, unique within the case, and identical wherever the same payment appears; UPI addresses have the form `username@handle` with a fictional handle; no app-specific long transaction-ID prefix is invented as if real.
- **Why:** The 12-digit number is the key that links an app screen, a bank alert and a statement line. NPCI changed how it is built in April 2024, so recent references should not be expected to encode a date.
- **Source:** [S70] SECONDARY (12 numeric digits; UTR and UPI Ref No are labels for it); [S71] SECONDARY (the YDDD prefix was replaced and its validation removed by 31 May 2024); [S72] SECONDARY (address form).
- **Strength:** GOOD PRACTICE
- **Checked by:** `scenario/ids.py::upi_reference`; `tests/test_scenario_ids.py::test_reference_is_12_digits`, `::test_reference_does_not_start_with_yddd_of_payment_date`, `::test_same_payment_same_reference_everywhere`, `::test_vpa_handle_is_fictional`.
- **Status:** Planned
- **Caveat:** The NPCI primary circular could not be read; the format is confirmed by secondary sources only. The format of app-specific long transaction IDs was not verified, so none are invented. No official specification of bank SMS wording exists in the notes.

### S-02. Amounts and timing plausible
- **Rule:** Amounts are whole rupees within the per-typology range set in `scenario_config.json`; an onward transfer never precedes the victim's payment (L-10) and follows it within the configured minutes-to-hours range; any reply time from a bank or telecom stated in a case stays within the sourced figures (bank gives police the requested information within 2 calendar days under the SOP; private-bank data took 6 to 10 days in one police account) unless the case marks the delay as deliberate.
- **Why:** Implausible sums or instant bank replies are cues that a case is invented and give students a false lesson about process.
- **Source:** PROJECT CONVENTION for the ranges. Sourced points only: [S65] SECONDARY (task scams: early payouts of Rs 50 to Rs 500, then larger transfers); [S74] PRIMARY (2-day response); [S67] SECONDARY (6 to 10 days).
- **Strength:** PROJECT CONVENTION
- **Checked by:** `scenario/config.py`; `tests/test_scenario_ranges.py::test_amounts_are_whole_rupees_in_range`, `::test_onward_transfer_after_victim_payment`, `::test_reply_time_within_sourced_bounds`.
- **Status:** Needs expert review
- **Caveat:** The notes found no source for typical UPI fraud amounts or transfer timing, and no official RBI or NPCI statistics by method. The ranges need lecturer review.

### S-03. Typologies and ring roles
- **Rule:** Cases are drawn only from the configured typologies (task or part-time job scam, mule-account layering, SIM swap, remote-access-app misuse, fake customer-care call, investment-style lure, digital-arrest-style impersonation of an unnamed agency), and ring roles (operator, recruiter, mule account holder, handler, cash-out agent) are shown in the answer key and teacher view as a project synthesis, not an official taxonomy.
- **Why:** Most typologies are documented in the sources (the fake customer-care call has no fetched official source); the roles are a reasonable reading of police descriptions but no official body defines them.
- **Source:** [S59] SECONDARY (2025 shares); [S62] SECONDARY (remote access); [S63] SECONDARY (SIM swap); [S64] SECONDARY (digital arrest); [S65] SECONDARY; [S66] SECONDARY; [S67] SECONDARY; [S68] WEAK (qualitative roles only).
- **Strength:** GOOD PRACTICE
- **Checked by:** `scenario/typologies.py`; `tests/test_typologies.py::test_typology_in_allowed_list`, `::test_role_labels_marked_synthesis`.
- **Status:** Needs expert review
- **Caveat:** The notes found no official source that defines these roles and no peer-reviewed study of ring structure; the CyberPeace figures looked inconsistent, so only its qualitative descriptions are used. No fetched official source covers fake KYC or phishing-link scams, so that typology is limited to a generic fake customer-care call. Headline counts differ between sources (28.15 lakh cases in ThePrint against over 24 lakh complaints in the Free Press Journal), so no count is quoted. Weighting typologies by real base rates was left open.

### S-04. Withdrawn collect request is not a current mechanism
- **Rule:** A P2P collect (pull) request is never shown as a way fraud works today; it may appear only in a case whose labelled date is before 1 October 2025, and remote-access-app misuse is labelled "legacy pattern" in the teacher view.
- **Why:** NPCI directed that P2P collect requests stop from 1 October 2025, so showing one as current would teach something out of date.
- **Source:** [S61] SECONDARY (NPCI directed banks, apps and PSPs not to initiate, route or process P2P collect requests after 1 Oct 2025); [S62] SECONDARY (the AnyDesk warning dates from 2019).
- **Strength:** GOOD PRACTICE
- **Checked by:** `scenario/typologies.py`; `tests/test_typologies.py::test_collect_request_only_before_cutoff`, `::test_remote_access_labelled_legacy`.
- **Status:** Planned
- **Caveat:** The NPCI primary circular was not read, only a press report. Labelling remote-access scenes as legacy is the notes' inference (the warning dates from 2019). Merchant collect is a separate flow, and the notes do not say what remains of it.

### S-05. Evidence artefacts in a case
- **Rule:** Every case's evidence is the three case files (chat export, call log, photo with EXIF); identifiers they share (amount, 12-digit reference, address, times) agree across files; other artefacts (bank SMS, statement line, app screenshot, operator CDR, CCTV) are not generated in this version and are mentioned only as "not in the pack".
- **Why:** Real investigations use many artefact types; the project keeps to three so every item can be verified by code, and says plainly what is left out.
- **Source:** [S73] WEAK (artefact catalogue; vendor blog); [S66] SECONDARY (CDR, IMEI and money-trail analysis in a Delhi case); [S74] PRIMARY (notice fields: account number, UTR or transaction id, amount, date); [S44] SECONDARY.
- **Strength:** GOOD PRACTICE
- **Checked by:** `tests/test_pipeline.py::test_generate_case_writes_every_file`.
- **Status:** Partial. Not built yet: a case folder also holds case.json, brief.json and brief.md beside the three case files and the manifest.
- **Caveat:** The artefact catalogue is a vendor blog and the pack shape is the notes' inference. Bank SMS wording varies by bank and has no official specification.

### S-06. Offence labels
- **Rule:** A case that names offences uses only these labels: BNS s.318(4) (cheating), BNS s.319 (cheating by personation), IT Act s.66C (identity theft) and IT Act s.66D (cheating by personation using a computer resource), each followed by "training label; check the official text"; the UI shows no BNS punishment or sub-section lettering for s.319 until verified against India Code.
- **Why:** The BNS details in the notes come from a weak source, so the app avoids stating them.
- **Source:** [S17] WEAK (BNS 318, 319; punishments); [S18] SECONDARY (s.318 and s.319 labels); [S19] SECONDARY (s.66C and s.66D: up to three years and fine up to one lakh rupees).
- **Strength:** GOOD PRACTICE
- **Checked by:** `scenario/offences.py`; `tests/test_offences.py::test_labels_in_whitelist`, `::test_every_label_has_verify_note`, `::test_no_bns_punishment_text`.
- **Status:** Needs expert review
- **Caveat:** BNS punishments and cognizability came from a WEAK blog; nothing was verified on India Code or the Gazette. That s.318(4) engages BNSS s.176(3) (seven years or more) is the notes' own inference ([S16] SECONDARY), as is the lettering of s.319(1) and (2). Whether IT Act and BNS charges can coexist for the same act was not researched. Other BNS and IT Act sections were not checked.

### S-07. Reporting, freezing and tracing facts only as sourced
- **Rule:** Any text describing reporting, freezing or tracing uses only facts on an allow-list: report through 1930 or cybercrime.gov.in and receive a Complaint ID; a designated officer verifies and asks the bank to block the money; the hold is limited to the disputed amount, may sit on a first-layer account, and may be empty if funds already moved; the bank gives police requested information within 2 calendar days; and the "first hour" and the Rs 10 lakh e-Zero FIR threshold are never stated as fact.
- **Why:** The freezing SOP of 2 January 2026 changed practice, so older descriptions would mislead; the two unofficial claims have no official source.
- **Source:** [S77] PRIMARY; [S76] SECONDARY; [S74] PRIMARY; [S75] SECONDARY; [S78] WEAK (the source of the unverified claims, not used for any fact).
- **Strength:** GOOD PRACTICE
- **Checked by:** `scenario/process_facts.py`; `tests/test_process_facts.py::test_text_uses_only_allow_listed_facts`, `::test_no_first_hour_claim`, `::test_no_ten_lakh_threshold_claim`.
- **Status:** Needs expert review
- **Caveat:** The MHA SOP was read only through a bank-hosted copy and a LiveLaw analysis; section numbers and timelines need checking against the primary PDF before any is quoted. Telecom CDR request formats and retention, and WhatsApp or Telegram legal-request processes, were not confirmed from official sources.

### S-08. Anomaly patterns are labelled as inference
- **Rule:** Each planted anomaly (a timing gap, a reference mismatch, a statement-versus-log contradiction, a deleted-record pattern, clustered credits) carries `basis: inference` in the answer key and the teacher view, and never `basis: documented`.
- **Why:** The notes found no official or academic catalogue of evidence anomalies in UPI fraud; the patterns are scenario-design ideas, and students should not be told they are documented findings.
- **Source:** PROJECT CONVENTION: no external source.
- **Strength:** PROJECT CONVENTION
- **Checked by:** `scenario/anomalies.py`; `tests/test_anomalies.py::test_every_anomaly_has_basis_inference`, `::test_no_anomaly_marked_documented`.
- **Status:** Planned
- **Caveat:** The notes record only that investigators compare transaction timestamps with bank statements and suspects' statements with logs; no source lists these anomaly patterns. Recoverability of deleted WhatsApp or UPI app data is not documented in the accessible sources.

## 4.5 Family R: Responsible use and fairness

The notes found no India-specific teaching guideline on portraying fraud scenarios. Most rules here are project conventions; where a source exists it is named.

### R-01. SYNTHETIC label everywhere
- **Rule:** The word SYNTHETIC appears on every Streamlit screen, as `synthetic: true` plus a label string in manifest.json, in a system line near the top of chat.txt (for example `04/03/26, 9:00 pm - SYNTHETIC CASE - fictional training data, no real people`, written without a colon so a parser does not read it as a sender), in the photo's EXIF ImageDescription, and in the case folder and download file names; calls.csv carries it only through its manifest entry and folder name, because its six-column schema has no free-text column.
- **Why:** A case, file or screen must never be mistakable for a real record or case. The label also backs the phone-number mitigation in F-11.
- **Source:** PROJECT CONVENTION: no external source.
- **Strength:** PROJECT CONVENTION
- **Checked by:** `tests/test_repair.py::test_manifest_carries_the_synthetic_flag_the_hash_note_and_the_date_order`; `tests/test_photo.py::test_exif_fields_round_trip` (ImageDescription).
- **Status:** Partial. Not built yet: no automated check of the app banner, download names do not carry SYNTHETIC, and the chat label is a plain first line.
- **Caveat:** The notes only suggest marking everything synthetic as an inference; no guideline requires it. Labelling the chat and photo inside the files is a project choice that slightly changes realism; the labelling of calls.csv is a decision to confirm.

### R-02. Fictional names, numbers and institutions
- **Rule:** Every person name comes from the regional pools in names.json by seeded draw, no name matches the blocklist of real public figures and copyrighted characters, and every bank, UPI handle, app, telecom operator and agency in a case text is fictional or generic (for example "a caller posing as an investigative agency").
- **Why:** Cases must not point at real people or institutions. Where a scenario involves impersonation, real agencies are impersonated by scammers, not complicit, and a bank insider must be an individual and fictional.
- **Source:** PROJECT CONVENTION: no external source. Context only: [S64] SECONDARY (impersonated agencies are not complicit).
- **Strength:** PROJECT CONVENTION
- **Checked by:** `tests/test_skeleton.py::test_blocklisted_names_are_never_drawn`, `::test_names_are_nfc_and_draws_are_reproducible`; `tests/test_filler_rules.py`.
- **Status:** Partial. Not built yet: no scan of every output for real bank, app or operator names beyond the filler brand list.
- **Caveat:** The notes found no source on legal or ethical limits for fictional cases that resemble real ones; that is left to the team's and lecturer's review. A blocklist can never be complete.

### R-03. Random guilt and a bias audit
- **Rule:** The culprit and every other role are assigned by a seeded random draw that does not use the name pool's region or community, and an audit test over at least 1,000 seeded world models (no LLM calls) fails if any pool's share of culprits differs from its share of draws by more than the tolerance set in the test (chi-square test at p < 0.01).
- **Why:** If guilt followed region or community the generator would teach a stereotype. Indian official framing treats digital arrest as an organised cross-border crime and does not attribute it to a community, and mule holders may themselves be exploited.
- **Source:** PROJECT CONVENTION for the audit design. Context only: [S64] SECONDARY; [S67] SECONDARY; [S69] SECONDARY.
- **Strength:** PROJECT CONVENTION
- **Checked by:** `suraag/skeleton.py`; `tests/test_bias_audit.py::test_culprit_region_share_matches_the_draw_share_over_1000_seeds`, `::test_every_role_is_equally_likely_for_each_gender`.
- **Status:** Implemented
- **Caveat:** The sample size and the p-value are the team's choices.

### R-04. Respectful, non-operational portrayal
- **Rule:** No case text, hint or UI string ties wrongdoing to a state, city, language, religion, caste or community; places are neutral and unattributed; victims are described as targets of deliberate deception and never with blame wording such as "duped" or "fell for"; and cases and hints contain no URL, working script or step-by-step instruction for committing fraud.
- **Why:** Stereotyping and victim-blaming are the main harms in how scams are talked about, and training material must not double as a manual. The offender's deliberate action is named with active verbs.
- **Source:** [S79] SECONDARY (avoid victim-blaming words, shame, stereotypes and sensationalism); [S64] SECONDARY (no community attribution). The ban on how-to content is PROJECT CONVENTION: no external source.
- **Strength:** GOOD PRACTICE
- **Checked by:** Built: `tests/test_portrayal.py::test_learner_page_links_1930_and_cybercrime_portal` (the footer on every page). Proposed, not built yet: `::test_no_blame_lexicon_in_english_or_hinglish`, `::test_no_place_names_in_case_text`, `::test_no_urls_in_case_files`, `::test_known_scam_script_phrases_rejected`.
- **Status:** Needs expert review
- **Caveat:** The only guidance found is an Australian communications guide whose publisher and date could not be confirmed on the page; no Indian guideline was found. The word lists are project-made and incomplete, and the lecturer should review them. The one-line pointer to 1930 and cybercrime.gov.in follows the guide's advice to include support options and is an inference. The notes make the how-to ban an inference, not a cited guideline.

### R-05. Not legal advice; practice certificate is not a legal form
- **Rule:** Every screen that shows law or procedure text (offence labels, certificate, custody, hash help) carries the line "Training material, not legal advice. Check the official India Code text.", the practice certificate has the title required in H-03, and no screen calls a fictional outcome a legal finding of guilt.
- **Why:** Statute wording was read through reproductions, not India Code, and the Part B question is open.
- **Source:** PROJECT CONVENTION: no external source.
- **Strength:** PROJECT CONVENTION
- **Checked by:** `tests/test_ui_strings.py::test_law_screens_have_notice`, `::test_notice_has_hindi_version`, `::test_no_guilt_finding_wording`.
- **Status:** Planned

## 4.6 Family G: Grading and assessment

Grading is deterministic. The LLM overclaim check is advisory only, and no classifier is wired in yet.

### G-01. Deterministic grading; the overclaim check is advisory
- **Rule:** The grade is a pure function of the submitted structured answer (culprit id, mechanism code, key fact values, cited lines) and the case answer key, the same input gives the same score on every run, grading makes no LLM or network call, and the LLM overclaim check writes only to an advisory field shown to a teacher and can never change a score, a hint tier or pass or fail.
- **Why:** Students and judges must be able to reproduce any score; LLM checkers miss many errors and can themselves err, so a deterministic grader must not depend on one.
- **Source:** PROJECT CONVENTION: no external source. Context only: [S94] PRIMARY (an LLM checker reached recall 0.55 on injected errors).
- **Strength:** PROJECT CONVENTION
- **Checked by:** `suraag/grade.py`; `tests/test_grade.py::test_same_input_always_gives_the_same_score`, `::test_rationale_is_advisory_and_never_changes_the_score`, `::test_overclaim_classifier_is_optional_and_failures_fall_back_safely`.
- **Status:** Implemented
- **Caveat:** No source was found that describes grading students on cited evidence references. The closest are grading of reports and documentation ([S97] PRIMARY), generator ground-truth files that help instructors grade ([S85] PRIMARY) and per-student solution sheets for marking ([S99] SECONDARY, abstract only). No overclaim classifier is wired in yet: `grade_all` is called without one, so every free-text reason is flagged "could not verify" for the instructor.

### G-02. Citation validity
- **Rule:** A citation (file and line) is valid if and only if the cited line contains every must_contain value of the fact it supports; extra supporting lines are allowed and not penalised; a cited line that contains none of the fact's values is wrong; a line with some but not all values is neither valid nor wrong.
- **Why:** The same test the verifier uses for traceability (L-02) makes citations auto-checkable, and allowing extra lines avoids punishing a student for citing context.
- **Source:** PROJECT CONVENTION: no external source.
- **Strength:** PROJECT CONVENTION
- **Checked by:** `suraag/grade.py::grade_claim`; `tests/test_grade.py::test_an_extra_supporting_line_is_allowed_even_if_it_is_not_the_anchor`, `::test_a_partial_line_neither_earns_nor_costs_and_says_what_is_missing`, `::test_right_answer_wrong_line_loses_only_the_citation_point_and_names_the_support`.
- **Status:** Implemented
- **Caveat:** The project brief does not say how a line with only some values is treated; "neither valid nor wrong" is this file's proposal and needs confirming.

### G-03. Scoring rule
- **Rule:** A submission scores out of 2: 1 point if the structured answer matches the key, and 1 point for citations, awarded all-or-nothing only if every key fact in the answer has at least one valid cited line and none of the cited lines is wrong.
- **Why:** The brief left the all-or-nothing question open; a two-part score keeps the answer and the evidence visible separately and is easy to explain. It can be refined to partial credit after lecturer feedback.
- **Source:** PROJECT CONVENTION: no external source.
- **Strength:** PROJECT CONVENTION
- **Checked by:** `suraag/grade.py::grade_claim`; `tests/test_grade.py::test_right_answer_with_right_lines_scores_two`, `::test_wrong_answer_right_lines_loses_only_the_answer_point`, `::test_a_required_artifact_with_no_citation_fails_the_citation_point`. The all-or-nothing rule was chosen by the project owner during design.
- **Status:** Implemented
- **Caveat:** This is a recommendation, marked PROJECT CONVENTION to confirm; no source prescribes a scoring scheme. Whether the citation point is per fact or overall is part of what to confirm.

### G-04. Distractor and difficulty design
- **Rule:** Difficulty is set only by the number of distractors and the number of steps from anchor lines to the culprit; no single line names both the culprit and the mechanism; and no obstacle makes a needed fact unrecoverable from the files provided (for example, content that needs a key the case does not contain).
- **Why:** Over-specific clues make a case trivial; unrecoverable obstacles make it unfair.
- **Source:** [S97] PRIMARY (overly specific clues make a case trivial; encryption without a key in the data is too hard); [S86] PRIMARY (difficulty varied by what data a case needs); [S88] SECONDARY (trivial bulk files plus hidden secrets); [S81] SECONDARY (background noise).
- **Strength:** GOOD PRACTICE
- **Checked by:** `verify.py::check_distractor` and `::check_solvability`; `tests/test_difficulty.py::test_levels_differ_in_distractors_and_steps`, `::test_no_single_line_names_culprit_and_mechanism`, `::test_no_unrecoverable_obstacle`.
- **Status:** Planned
- **Caveat:** The notes found no educator source that discusses distractors in forensic cases or grading rubrics for cited evidence. The "steps" measure is a project choice.

### G-05. Per-student variants
- **Rule:** The generator takes a seed, the app can issue a differently seeded case to each student, and the seed and answer key are stored so an instructor can regenerate and grade any student's case.
- **Why:** Papers argue that shared static cases let students collaborate or pass on finished solutions and that seedable generation gives each student a distinct case with known answers. The project does not claim that variants reduce cheating.
- **Source:** [S98] PRIMARY; [S87] PRIMARY (proposed as a future possibility, not built); [S99] SECONDARY; [S96] PRIMARY.
- **Strength:** GOOD PRACTICE
- **Checked by:** `tests/test_skeleton.py::test_build_case_is_deterministic_and_seeds_differ`; `tests/test_render.py::test_render_is_byte_for_byte_repeatable`.
- **Status:** Partial. Not built yet: the app issues the same case to everyone; there is no per-student issue flow.
- **Caveat:** The notes found no empirical study of cheating or solution-sharing in digital-forensics courses, and no study of outcomes from per-student datasets. The case rests on design rationale in the papers cited, not measured results; Russell et al. give no year in the fetched text, and Murphy et al. was read as an abstract only.

### G-06. Tiered hints built in code
- **Rule:** Hints are built by code from the world model in tiers (each reveals more than the one before), may be wrapped by a persona (Vetaal, Birbal or Plain) that changes wording only, no hint at any tier or persona contains the culprit's name or an anchor line verbatim, optional read-aloud speaks exactly the displayed hint, and the LLM never writes a hint.
- **Why:** An LLM-written hint could leak the answer or invent a fact; a code-built hint is testable.
- **Source:** PROJECT CONVENTION: no external source. Context only: [S97] PRIMARY (a case should be investigable "with some hints").
- **Strength:** PROJECT CONVENTION
- **Checked by:** `suraag/hints.py`; `tests/test_hints.py::test_no_hint_leaks_the_culprit_the_evidence_or_a_line_verbatim`, `::test_a_hint_never_contains_the_text_of_any_chat_line`, `::test_plain_is_the_bare_hint_and_other_personas_only_wrap_it`.
- **Status:** Implemented

## 4.7 Family E: Evaluation and claims

### E-01. Baseline gate
- **Rule:** Before any claim about the hybrid generator, 10 raw-mode cases are checked by hand against the six checks and the results are recorded in `docs/baseline_check.csv`; if 3 or more are broken, the report and slides lead with that result.
- **Why:** The comparison is only honest if the baseline is examined first. The threshold of 3 of 10 is the team's own and is not taken from any source.
- **Source:** PROJECT CONVENTION: no external source.
- **Strength:** PROJECT CONVENTION
- **Checked by:** `eval/plain_baseline/scores.csv`, `eval/notes.md`.
- **Status:** Partial. Not built yet: the plain-chat baseline (8 of 10 flagged, 3 clear-cut) is a model first pass awaiting human confirmation. The raw-mode run is done through `eval/run_generator.py` (19 of 20 cases completed; results in `eval/results.json`).
- **Caveat:** Ten cases is a small sample; any rate must be stated with its sample size (E-03).

### E-02. Report per language and per check
- **Rule:** Results are reported separately for English and Hinglish cases, hybrid and raw side by side, with failures counted per check from logs/failures.jsonl and cases counted separately from repair attempts.
- **Why:** A single pooled number would hide where the generator fails and would mix cases with attempts.
- **Source:** PROJECT CONVENTION: no external source.
- **Strength:** PROJECT CONVENTION
- **Checked by:** `eval/run_generator.py`; the failure log written by `suraag/repair.py` records the check and code per failure.
- **Status:** Partial. Not built yet: failure counts come from `eval/results.json` (per language, per code), not yet from a per-check breakdown of `logs/failures.jsonl`. Run for English (10 hybrid, 10 raw) and Hinglish (10 hybrid, 9 raw).
- **Caveat:** The notes found no source measuring contradiction rates in generated chat logs, so there is no external figure to compare against.

### E-03. No invented numbers
- **Rule:** Every number in the README, slides and demo script appears in `docs/claims_ledger.csv` with its origin (a run log, a test output or a source id from this register), and every rate is shown with its sample size.
- **Why:** Judges and a lecturer will audit the claims; an unmeasured number is the quickest way to lose trust.
- **Source:** PROJECT CONVENTION: no external source.
- **Strength:** PROJECT CONVENTION
- **Checked by:** Proposed, not built yet: `scripts/check_claims.py`; `tests/test_claims.py::test_every_readme_number_is_in_ledger`, `::test_every_rate_has_sample_size`.
- **Status:** Planned

### E-04. The claims table is binding
- **Rule:** Statements about prior art, benchmarks and novelty follow the "Claims you may and may not make" table in section 5, and README, slides and the demo script are scanned for the banned wordings.
- **Why:** Several figures and names in earlier drafts were wrong; the table records the corrections so they do not return.
- **Source:** [S90] PRIMARY; [S91] PRIMARY; [S83] PRIMARY; [S80] SECONDARY; [S100] PRIMARY; [S101] PRIMARY.
- **Strength:** GOOD PRACTICE
- **Checked by:** Proposed, not built yet: `scripts/check_claims.py`; `tests/test_claims.py::test_no_banned_phrases_in_docs` (banned: "62%" near GPT-4 or MuSR, "13-36%", "Re-Imagen" or "Re-imagen" as a source, "EvidenceForge (SANS)", "first ever", "world's first").
- **Status:** Planned

## 5. Claims you may and may not make

Corrections carried over from the research notes. Rule E-04 enforces this table.

| Topic | You may say | You may not say | Why |
|---|---|---|---|
| MuSR | MuSR is real (arXiv 2310.16049, ICLR 2024). It builds narratives from a symbolic reasoning tree. With the best prompt reported (CoT+, Table 5), GPT-4 scored 80.4 on murder mysteries, against 50.0 for chance and 94.1 for a human majority | "GPT-4 scored 62%" on MuSR | 62 matches GPT-3.5 (61.6, and 62.0 in a separate table) and an unrelated 62% fact-entailment figure; only Tables 5 and 8 were seen, so other GPT-4 settings are unchecked [S90] |
| Test of Time | Test of Time is real (arXiv 2406.09170, ICLR 2025). Date and duration arithmetic is a weak area: as low as about 13.5% on duration arithmetic for the models tested | "13-36%" as a stated range | The range appears nowhere; 13.5% is the lowest arithmetic category and 24 to 36% are Timeline question scores in one table [S91] |
| Plankl et al. 2026 | The paper is real (DFRWS EU 2026; FSI: Digital Investigation vol. 56, art. 302053). It recommends giving deterministic tasks to code and reports models defaulting to 2023 or 2025 dates | That it benchmarks scenario quality or proves the approach works | It is essentially one case study with no quantitative benchmark [S83] [S84] |
| Re-Imagen | Nothing | Citing "Re-Imagen" for anything forensic | It is an unrelated text-to-image paper (arXiv 2209.14491); no forensic work with that name was found [S101] |
| EvidenceForge | It is a Cisco Talos open-source project (author David J. Bianco, MIT licence), listed on the SANS tools page; its engine makes no LLM calls | "A SANS project" or "EvidenceForge (SANS)" | The code is Cisco's; the SANS link is a listing and the author's role as instructor [S80] [S82] |
| VeriScene | Its evidence-citing audit loop is a pattern we borrowed | That it is a digital-forensics tool | It concerns physical and legal evidence, and its peer-review status is unknown [S100] |
| Prior-art validation | The generators surveyed validate by construction and by spot checks; only EvidenceForge reports an `eval` score | That prior generators measure scenario quality | The notes found no quantitative scenario-quality metrics apart from EvidenceForge's `eval` [S80] [S81] |
| Novelty | Each ingredient exists in prior work (code-controlled values, LLM text with a deterministic back end, symbolic-first narratives, evidence-citing audits). In the searches run, we did not find a published tool combining them for chat, call-log and photo cases in an Indian setting with a rule-based solvability check | "First", "novel generator", "no one has done this", or that solvability checking is new to the field | Only the combination can be claimed, and only as "not found in our search"; the notes call a generator-side solvability check a novel contribution by inference, and found no paper on LLM-generated forensic chat datasets in the searches run [S83] [S80] [S90] [S100] |
| Hashes | A matching hash shows a file is unchanged since the hash was computed | That a hash proves a chat, call log or photo is authentic | See H-08; the Supreme Court describes hash and Part B in authenticity terms, SWGDE and the Bihar order do not [S4] [S24] [S29] |
| Hash algorithm | SHA-256 is this project's convention; the Schedule offers SHA1, SHA256, MD5 or Other | "The law requires SHA-256" | No source found mandates an algorithm; the Supreme Court order is silent on algorithms [S2] [S4] |
| Part B signatory | The Supreme Court left open who may sign Part B and said it is possible that a person with special expertise could, if the court is satisfied on unimpeachable material | "Only s.79A examiners may sign" or "any cyber expert may sign" | Admission-stage order; question kept open [S4] |
| Phone numbers | Numbers starting with 5 are not in any mobile series | That +91-5xxxx-xxxxx numbers cannot reach a real phone | Level 5 includes some fixed lines and short codes; STD codes starting with 5 exist [S47] [S49] |
| Fraud statistics | A named statistic with its date and source | One headline cyber-fraud count without its source and date | ThePrint (28.15 lakh cases) and the Free Press Journal (over 24 lakh complaints) differ for the same year [S59] [S60] |
| LLM blind solve | It was run on 10 + 10 generated cases and the 14 shipped cases, one model, and is reported as unscored context | That it measures solvability or accuracy, or how a person would do | It is unscored by design (L-04); one model, small n |

## 6. Open issues and questions for a forensic lecturer

Built from the Gaps sections of the five research notes. Tick an item when a decision is recorded and the affected rule's status is updated.

- [ ] 1. **Part B signatory.** The Supreme Court left open who may sign Part B and kept the Madras High Court view from binding anyone [S4]. Which approach should the practice certificate teach, and should it show a signatory profile? (H-03, H-04)
- [ ] 2. **Primary legal text not read.** s.63 and the Schedule were read through bare-act reproductions, not India Code or the Gazette; the commencement notification number is unconfirmed; no check was made for amendments after mid-2026 [S1] [S2]. Please check the wording of the Schedule fields in H-03.
- [ ] 3. **No official hash format or algorithm list.** No source says how a hash value must be written or which algorithms are "legally acceptable"; the Supreme Court order is silent [S4]. Is lower-case SHA-256 hex an acceptable teaching choice? (H-01)
- [ ] 4. **Certificate for original records.** Whether s.63(4) applies to primary electronic records is contested: one commentator reads s.61 with s.63 as requiring it even for originals [S11], while Arjun Panditrao (old Act) exempted a produced original device [S12]; s.57 Explanations 4 to 7 matter [S10]. No BSA-era ruling was found. The practice exercise includes a certificate in both situations. Is that the right default?
- [ ] 5. **Hash and authenticity wording.** No source states "integrity, not authenticity" in one sentence, and the Supreme Court speaks of hash and Part B in authenticity terms. Please review the sentence in H-08 for both accuracy and tone.
- [ ] 6. **Phone-number policy.** Keep `+91-5xxxx-xxxxx` with a visible SYNTHETIC marker, or choose another approach? No official reserved range was found, and a 5-leading number may match a landline. (F-11)
- [ ] 7. **Unsourced WhatsApp details.** U+202F before am or pm, the edited-message marker, "You deleted this message", en-IN specifics (am/pm case, year digits), iOS system-line and omitted-media wording, Android and iOS version thresholds, and the vendor-blog message cap are all unconfirmed. Can the lecturer confirm any from real exports? (F-03, F-04)
- [ ] 8. **Indian CDR schema.** No official national schema was found; operator layouts and code vocabularies differ and are only weakly sourced. calls.csv is a handset-style log, not a CDR. Is a CDR artefact wanted in a later version? (F-05, S-05)
- [ ] 9. **Photo metadata values.** Make, Model and typical Software strings for Indian-market phones are unsourced; the thumbnail-mismatch cue is unsupported; the year Exif 2.31 was released is inconsistent; the CIPA standard was not read. (F-08, F-09)
- [ ] 10. **Power-state conflict.** ACPO says power a live phone off; SWGDE and Indian documents say keep it powered and isolated. The verifier requires only documented isolation. Is that acceptable for teaching? (H-07)
- [ ] 11. **ISO/IEC 27037 text.** The standard is paywalled; clause numbers come from a table of contents, Annex B minimum fields are unknown, and the three widely quoted principles (relevance, reliability, sufficiency) were not verified [S20] [S21]. (H-05)
- [ ] 12. **BNSS provisions.** Only ss.94, 105 and 176(3) were confirmed, from secondary sources; s.176(3) applies State by State [S16]; no provision on preserving devices was confirmed; section numbers in the freezing SOP need rechecking. (H-05, S-07)
- [ ] 13. **BNS and IT Act labels.** BNS punishments came from a weak blog; sub-section lettering of s.319 is inferred; the double-jeopardy question was not researched. (S-06)
- [ ] 14. **MHA freezing SOP.** The primary PDF was not read; the "first hour" advice and the Rs 10 lakh e-Zero FIR threshold come only from an unofficial blog. (S-07)
- [ ] 15. **NPCI circulars.** Neither the collect-request withdrawal nor the RRN change was read from NPCI; both rest on press and law-firm summaries. (S-01, S-04)
- [ ] 16. **Amounts and timing ranges.** No source gives typical UPI fraud amounts or transfer timing; the ranges in S-02 are placeholders for lecturer review.
- [ ] 17. **Respectful portrayal.** The only guidance is an Australian guide of unconfirmed publisher; no Indian teaching guideline exists in the notes. Please review the blame lexicon and place-name rules. (R-04)
- [ ] 18. **Scoring rule.** Confirm the 2-point scheme, whether the citation point is per fact or overall, and how a line with only some must_contain values is treated. (G-02, G-03)
- [ ] 19. **No evidence on cheating or outcomes.** No empirical study of solution-sharing, or of per-student datasets, was found; the project makes no such claim. (G-05)
- [ ] 20. **Anomaly patterns.** No official or academic catalogue exists; every anomaly is labelled inference. Does the lecturer recognise these patterns from practice? (S-08)
- [ ] 21. **Indian practice for chat evidence.** No Indian SOP for WhatsApp export was found and no official description of how CFSL or RFSL labs run mobile examinations; several state documents are undated. (H-05, H-08)
- [ ] 22. **Developments after mid-2026.** Later High Court rulings, a review of the Part B order, additions to the notified examiner list, new State s.176(3) notifications or official hash guidance may exist and were not exhaustively checked; most case law still applies the old s.65B because pending matters continue under the 1872 Act [S9].
- [ ] 23. **Prior-art gaps.** No paper on LLM-generated forensic chat datasets was found, and no formal solvability check exists in any tool surveyed; novelty claims are limited accordingly (E-04).

## 7. Source register

Quality tags: PRIMARY, SECONDARY, WEAK (see section 2). URLs are copied from the research notes. Entries are grouped by family and numbered in the order shown.

### A. Indian law and court material

| ID | Title | Publisher or author | Date | URL | Quality | Used for |
|---|---|---|---|---|---|---|
| [S1] | Bharatiya Sakshya Adhiniyam 2023, section 63 (bare-act reproduction) | AdvocateKhoj | not stated in notes | https://www.advocatekhoj.com/library/bareacts/bharatiyaaakshya2023/63.php | SECONDARY | Text of s.63(1)-(5); not the India Code original. |
| [S2] | BSA 2023 Schedule: certificate, Part A and Part B (reproduction of the Gazette text) | AdvocateKhoj | not stated in notes | https://www.advocatekhoj.com/library/bareacts/bharatiyaaakshya2023/b.php | SECONDARY | Certificate fields, hash algorithm options (SHA1, SHA256, MD5, Other), hash report, DD/MM/YYYY and 24-hour IST. |
| [S3] | BSA s.63 admissibility of electronic records | AapTaxLaw | not stated in notes | https://aaptaxlaw.com/bsa/63-bsa-admissibility-of-electronic-records-63-bsa-2023.html | SECONDARY | Cross-check of s.63 text; says the Schedule has hash and algorithm fields and a hash report. |
| [S4] | Order, Pune Bar Association v. Union of India, WP(C) 599 of 2026 | Supreme Court of India (PDF hosted by LiveLaw) | 22 May 2026 | https://www.livelaw.in/pdf_upload/2026/05/27/pune-bar-association-v-union-of-india-676590.pdf | PRIMARY | Upholds s.63(4) and Schedule at admission stage; hash described as electronic fingerprint; Part B signatory left open; no algorithm guidance. |
| [S5] | SC upholds admissibility of electronic evidence under section 63(4) BSA | SCC Online blog | 8 Jul 2026 | https://www.scconline.com/blog/post/2026/07/08/sc-upholds-admissibility-of-electronic-evidence-under-section-63-4-bsa/ | SECONDARY | Secondary report of the Pune order; reports no algorithm guidance. |
| [S6] | JSA Prism note on the Part B ruling | JSA (law firm) | June 2026 | https://www.jsalaw.com/?p=58355 | SECONDARY | Says the signatory question stays open and may be revisited. |
| [S7] | Verdictum report on who may sign Part B | Verdictum | not stated in notes | https://www.verdictum.in/supreme-court/qualification-section-39-bsa-not-restricted-section-79a-it-act-examiners-forensics-sign-part-b-certificate-1614860 | SECONDARY | Headline says an expert is competent to sign; the order itself leaves the question open (a documented disagreement). |
| [S8] | Delhi High Court Circular No. 186/Rules/DHC (MeitY letter on notified s.79A examiners) | Delhi High Court | 8 Jul 2026 | https://delhihighcourt.nic.in/files/2026-07/notifications-and-practice-directions/circular_no._186_dated_08.07.2026.pdf | PRIMARY | 21 digital forensic labs notified as Examiners of Electronic Evidence (context for Part B access). |
| [S9] | BSA 2023, section 170 (repeal and savings) | AdvocateKhoj | not stated in notes | https://www.advocatekhoj.com/library/bareacts/bharatiyaaakshya2023/170.php | SECONDARY | Pending matters continue under the 1872 Act, so much case law still applies s.65B. |
| [S10] | BSA 2023, section 57 (primary evidence, Explanations 4-7) | AdvocateKhoj | not stated in notes | https://www.advocatekhoj.com/library/bareacts/bharatiyaaakshya2023/57.php | SECONDARY | When electronic records count as primary evidence. |
| [S11] | Bharatiya Sakshya Adhiniyam transformed digital evidence (article) | LiveLaw | 2026 | https://www.livelaw.in/articles/bharatiya-sakshya-adhiniyam-transformed-digital-evidence-552681 | SECONDARY (Opinion piece; no case cited that decides the point.) | Opinion that s.61 with s.63 requires a certificate even for originals. |
| [S12] | Supreme Court: certificate a pre-requisite for producing electronic records (Anvar, Arjun Panditrao) | Nishith Desai Associates | not stated in notes | https://www.nishithdesai.com/research-and-articles/hotline/dispute-resolution-hotline/supreme-court-requirement-of-certificate-pre-requisite-for-producing-electronic-records-4334 | SECONDARY | Arjun Panditrao: no certificate needed if the original device is produced (old Act). |
| [S13] | Call detail records not admissible without s.65B certificate (Pooranmal v. State of Rajasthan) | LiveLaw | 10 Mar 2026 (judgment) | https://www.livelaw.in/supreme-court/call-detail-records-not-admissible-with-s65-evidence-act-certificate-supreme-court-525988 | SECONDARY | Court discounted an FSL report for broken chain of custody; supports a custody log. |
| [S14] | Tech-savvy evidence system: step-by-step guide to hash function and value (SS Rana & Co) | Bar & Bench | 13 Aug 2024 | https://www.barandbench.com/law-firms/view-point/tech-savvy-evidence-system-step-by-step-guide-hash-function-value-electronic-evidence | WEAK | Names MD5 and SHA-256; shows no approved hash list existed; wrongly places the hash only in Part B. |
| [S15] | BNSS s.105 recording of search and seizure through audio-video means (bare-act reproduction) | AapTaxLaw | not stated in notes | https://aaptaxlaw.com/bnss/105-bnss-recording-of-search-and-seizure-through-audio-video-electronic-means-105-bnss-2023.html | SECONDARY | Seizure recording and seizure list; shape for the optional seizure fields in a custody record. |
| [S16] | Section 176 BNSS (forensic expert visit, offences of seven years or more) | WritingLaw | not stated in notes | https://www.writinglaw.com/section-176-bnss/ | SECONDARY | s.176(3) language; State-by-State phase-in. |
| [S17] | Section 420 BNS: cheating (BNS 318) | iPleaders blog | 'last verified' 22 Jun 2026 | https://blog.ipleaders.in/section-420-bns-cheating-318/ | WEAK | BNS s.318 gradations and punishments; s.319 personation; s.316. |
| [S18] | SCC Online blog on cyber frauds and BNS provisions | SCC Online blog | not stated in notes | https://www.scconline.com/blog/?p=365805 | SECONDARY | s.318 cheating and s.319 cheating by personation; only a snippet-level extract was read. |
| [S19] | IT Act 2000 sections 66C and 66D (UNODC SHERLOC legislation database) | UNODC SHERLOC | not stated in notes | https://sherloc.unodc.org/cld/fr/legislation/ind/the_information_technology_act_2000/chapter_xi/sections_66c66d/sections_66c-66d.html | SECONDARY | s.66C and s.66D wording; up to three years and fine up to one lakh rupees. |

### B. Forensic standards, good practice and Indian police documents

| ID | Title | Publisher or author | Date | URL | Quality | Used for |
|---|---|---|---|---|---|---|
| [S20] | ISO/IEC 27037:2012 catalogue page | ISO | published Oct 2012; reviewed 2018 | https://www.iso.org/standard/44381.html | PRIMARY (Catalogue page only.) | Standard is listed as current; only the catalogue page was read, not the body text. |
| [S21] | INCITS/ISO/IEC 27037:2012 (R2019) preview | ANSI webstore | R2019 | https://webstore.ansi.org/preview-pages/INCITS/preview_INCITS+ISO+IEC+27037+2012+(R2019).pdf | PRIMARY (Table of contents only.) | Clause headings only (chain of custody 6.1, Annex B minimum documentation); body paywalled. |
| [S22] | NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response | NIST | not stated in notes | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-86.pdf | PRIMARY (Read through a summariser; first 100,000 of 386,000 characters.) | Compare digests of original and copy; examine only copies; custody log. |
| [S23] | SWGDE 18-F-003-2.0 Best Practices for Mobile Device Evidence Collection, Preservation, Handling and Acquisition | SWGDE | 2025 version | https://www.swgde.org/wp-content/uploads/2025/09/2025-08-21-Best-Practices-for-Mobile-Device-Evidence-Collection-Preservation-Handling-and-Acquisition-18-F-003-2.0.pdf | PRIMARY (Read through a summariser; wording and section numbers indicative.) | Seizure documentation, chain-of-custody fields, isolation and power state; no hash algorithm prescribed. |
| [S24] | SWGDE 06-F-001 Data Integrity within Computer Forensics | SWGDE | older document; currency unsure | https://www.swgde.org/documents/published-complete-listing/06-f-001-swgde-data-integrity-within-computer-forensics/ | PRIMARY | Acquisition hash, verification hash before analysis, rehash at the end; hash addresses integrity only. |
| [S25] | SWGDE position on the use of MD5 and SHA1 hash algorithms in digital and multimedia forensics | SWGDE | v1.0, 29 Sep 2019 (per fetch summary) | https://www.swgde.org/documents/published-complete-listing/swgde-position-on-the-use-of-md5-and-sha1-hash-algorithms-in-digital-and-multimedia-forensics/ | PRIMARY (The fetched page gave a conflicting document number, so cite by title and URL only.) | MD5 and SHA-1 acceptable for integrity checks; SHA-2 or SHA-3 where a match is relied on as evidence. |
| [S26] | NIST transitioning away from SHA-1 for all applications | NIST CSRC | 2022 | https://csrc.nist.gov/news/2022/nist-transitioning-away-from-sha-1-for-all-apps | PRIMARY | SHA-1 to be retired by 31 Dec 2030. |
| [S27] | ACPO Good Practice Guide for Digital Evidence, v5 (EPPO-hosted PDF) | ACPO (UK) | Oct 2011 / cover Mar 2012 | https://training-on-eppo.era.int/EPPO/kiosk/pdf/ACPO_Good_Practice_Guide.pdf | PRIMARY (Read through a summariser. No successor document found.) | Four principles; power a live phone off (Faraday exception); documentation list. |
| [S28] | Council of Europe electronic evidence guide | Council of Europe | Sep 2019 | https://rm.coe.int/090000168097d7cb | PRIMARY | Hash of copy must match original; MD5 and SHA-1 never used exclusively; seals and labels; chat apps: change the app, not the database. |
| [S29] | Police order on electronic evidence and s.65B/63(4) certificates | Bihar Police (issuer inferred) | undated | https://police.bihar.gov.in/misc/Officer_Orders/65B_Police_order_En.pdf | PRIMARY (Undated; issuer inferred.) | Isolation, imaging with hash, chain-of-custody form, seals; says the certificate addresses admissibility, not authenticity. |
| [S30] | Collective SOPs for Crime Scene Investigation | UP State FSL and Technical Services | undated | https://uppolice.gov.in/site/writereaddata/siteContent/TRAININGDIROCTORATE/202410211032196102Collective%20SOPs%20For%20Crime%20Scence%20Investigation.pdf | PRIMARY (Undated.) | Chain-of-custody content, phone isolation, hash of original and image. |
| [S31] | Digital Crime Scene Investigation (training deck) | Sikkim Judicial Academy | not stated | https://sikkimjudicialacademy.nic.in/sites/default/files/PPTs/Digital%20Crime%20Scene%20Investigation.pdf | PRIMARY (Author and date not stated.) | Keep a powered phone on and isolated; custody log with no time gaps; hash and custody called non-negotiable. |
| [S32] | Bytes and Rights: search and seizure of electronic evidence under India's legal framework | NFSU Journal of Forensic Justice | not stated in notes | https://jfj.nfsu.ac.in/Uploads/EJournal/4/7/(32-44)%20BYTES%20AND%20RIGHTS%20UNPACKING%20SEARCH%20AND%20SEIZURE%20OF%20THE%20ELECTRONIC%20EVIDENCE%20UNDER%20INDIA%E2%80%99S%20LEGAL%20FRAMEWORK.pdf | SECONDARY (The CBI manual itself was not read.) | Describes the CBI manual (2020): independent witnesses, hash at seizure, itemised seizure memo. |
| [S33] | Rakesh Kumar Gupta v. Directorate of Revenue Intelligence, W.P.(C) 11518/2024 | Delhi High Court | 20 Mar 2025 | https://delhihighcourt.nic.in/app/showFileJudgment/68920032025CW115182024_113532.pdf | PRIMARY | Copy phone data with a hash value, let the other side verify, return the devices. |
| [S34] | WhatsApp FAQ: exporting chat history (Android) | WhatsApp | not stated in notes | https://whatsapp.com/faq/en/android/23756533 | PRIMARY | Export gives a text file, with or without media; cannot be re-imported. |
| [S35] | Evidence from WhatsApp conversations under manipulation: a systematic review of forensic techniques | IJERT, vol. 15, issue 6 | 2026 | https://www.ijert.org/research/evidence-from-whatsapp-conversations-under-manipulation-a-systematic-review-of-forensic-techniques-c-IJERTV15IS061193.pdf | SECONDARY (Lower-tier journal; read through a summariser.) | Export format has no signature or checksum, so it can be edited unnoticed. |

### C. File formats and numbering

| ID | Title | Publisher or author | Date | URL | Quality | Used for |
|---|---|---|---|---|---|---|
| [S36] | whatstk parser source (header-format syntax) | whatstk (open-source library) | v0.7.0 | https://whatstk.readthedocs.io/en/v0.7.0/_modules/whatstk/whatsapp/parser.html | SECONDARY (No official WhatsApp spec exists; all grammar sources are third-party parsers.) | Reverse-engineered Android line grammar; continuation lines. |
| [S37] | whatsapp-chat-parser v4.0.2 (source map and README) | whatsapp-chat-parser (open-source, npm) | v4.0.2 | https://cdn.jsdelivr.net/npm/whatsapp-chat-parser@4.0.2/dist/index.cjs.map<br>https://unpkg.com/whatsapp-chat-parser@4.0.2/README.md | SECONDARY | Header regex, system events with no author, attachment regex, days-first default. |
| [S38] | chatpack 0.6.0 (whatsapp.rs and EXPORT_GUIDE) | chatpack (open-source, Rust) | v0.6.0 | https://docs.rs/crate/chatpack/0.6.0/source/src/parsing/whatsapp.rs<br>https://docs.rs/crate/chatpack/0.6.0/source/docs/EXPORT_GUIDE.md | SECONDARY | Five locale variants; English system phrases; multi-line messages preserved. |
| [S39] | chat-miner chatparsers.py | chat-miner (open-source, Python) | not stated in notes | https://raw.githubusercontent.com/joweich/chat-miner/main/chatminer/chatparsers.py | SECONDARY | Reads UTF-8, strips U+200E. |
| [S40] | WhatsR parse_android and parse_ios | WhatsR (R package) | not stated in notes | https://search.r-project.org/CRAN/refmans/WhatsR/html/parse_android.html<br>https://search.r-project.org/CRAN/refmans/WhatsR/html/parse_ios.html | SECONDARY | Separate Android and iOS grammars; media-omitted marker; (file attached) marker; iOS attached-file marker. |
| [S41] | LangChain WhatsApp chat loader (mirror) | LangChain code, mirrored on a Hugging Face space | not stated in notes | https://huggingface.co/spaces/zhangyi617/webui/blame/main/langchain/chat_loaders/whatsapp.py | WEAK | Encryption notice text; 'This message was deleted'. |
| [S42] | WhatsApp chat export complete guide | ChatToPDF (vendor blog on dev.to) | 2026 | https://dev.to/chattopdf/whatsapp-chat-export-complete-guide-iphone-android-zip-pdf-2026-10lo | WEAK (Vendor blog; message-cap numbers unverified.) | Android file name pattern; IMG-...-WA####.jpg (file attached); UTF-8. |
| [S43] | android.provider.CallLog (CallLog.java) | Android Open Source Project | not stated in notes | https://android.googlesource.com/platform/frameworks/base/+/refs/heads/main/core/java/android/provider/CallLog.java?format=TEXT | PRIMARY | Call-log columns; type values 1-7; date in epoch milliseconds; duration in seconds. |
| [S44] | Using Telecom Data for COVID-19 Contact Tracing | IIT Kanpur | not stated in notes | https://ccjr.cse.iitk.ac.in/opapers/Using%20Telecom%20for%20Covid%20Tracing.pdf | SECONDARY | Indian operator CDR fields; date and time formats vary by provider. |
| [S45] | Call-record file specification (UK) | FCS (UK) | not stated in notes | https://www.fcs.org.uk/?p=17975 | SECONDARY (Not Indian.) | UK comparison: comma-delimited, quoted, CRLF, DD/MM/YYYY. |
| [S46] | National Numbering Plan 2003 | DoT (C-DOT hosted PDF) | 2003 | https://dotws.cdot.in/sites/default/files/nnp2003_0_0.pdf?download=1 | PRIMARY | Level allocation; 10-digit national numbers. |
| [S47] | TRAI Recommendations on numbering | TRAI | 29 May 2020 | https://www.trai.gov.in/sites/default/files/2024-09/Recommendations_29052020.pdf | PRIMARY | Mobile numbers are levels 6-9; level 5 used for some fixed lines and five-digit short codes. |
| [S48] | Mobile telephone numbering in India | Wikipedia | not stated in notes | https://en.wikipedia.org/wiki/Mobile_telephone_numbering_in_India | SECONDARY | Mobile numbers start with 6-9 (its code table is flagged as uncited). |
| [S49] | Lucknow and Varanasi STD code pages | nativeplanet.com | not stated in notes | https://nativeplanet.com/lucknow-std-code-0522.html<br>https://nativeplanet.com/varanasi-std-code-0542.html | WEAK (Identified from search-result titles; page text not fetched.) | STD codes beginning with 5 exist (0522, 0542). |
| [S50] | ExifTool EXIF tag names | ExifTool | not stated in notes | https://exiftool.org/TagNames/EXIF.html | SECONDARY (Tool reference, not the CIPA DC-008 standard.) | Tag IDs: DateTimeOriginal, CreateDate, ModifyDate, OffsetTime tags, Software, Make, Model. |
| [S51] | Exif | Wikipedia | not stated in notes | https://en.wikipedia.org/wiki/Exif | SECONDARY | OffsetTime tags arrived with Exif 2.31 (year inconsistent on the page); date strings are naked local time. |
| [S52] | Detecting forged and altered images | Forensic Focus | not stated in notes | https://www.forensicfocus.com/articles/detecting-forged-altered-images/ | SECONDARY | Software tag, capture date vs modification date, EXIF easily forged. |
| [S53] | Photo forensics | Belkasoft | not stated in notes | https://belkasoft.com/photo-forensics | SECONDARY | Software fingerprints; correlate EXIF with file-system metadata. |
| [S54] | WhatsApp, Telegram, Signal photo metadata preservation | Fast.io (blog) | not stated in notes | https://fast.io/resources/whatsapp-telegram-signal-photo-metadata-preservation/ | WEAK | WhatsApp standard-quality sends strip most EXIF. |
| [S55] | WhatsApp media file naming convention (forum thread) | Forensic Focus forum | not stated in notes | https://www.forensicfocus.com/forums/general/whatsapp-media-file-naming-convention/ | WEAK | IMG-YYYYMMDD-WAnnnn.jpg uses send or receive date; user observations only. |
| [S56] | Google Camera on Android 11 changes Pixel image file name | MobileSyrup | 20 Aug 2020 | https://mobilesyrup.com/2020/08/20/google-camera-android-11-pixel-image-file-name/ | SECONDARY | IMG_ date-time names vs PXL_ camera names. |
| [S57] | Opening CSV UTF-8 files correctly in Excel | Microsoft Support | not stated in notes | https://support.microsoft.com/Excel/opening-csv-utf-8-files-correctly-in-excel | PRIMARY | Excel opens UTF-8 CSV normally only if saved with a BOM. |
| [S58] | CSV and Excel | Peter Hilton (blog) | not stated in notes | https://hilton.org.uk/blog/csv-excel | WEAK | Excel recognises UTF-8 only with a BOM; recognises YYYY-MM-DD. |

### D. UPI fraud scenarios and responsible use

| ID | Title | Publisher or author | Date | URL | Quality | Used for |
|---|---|---|---|---|---|---|
| [S59] | Cybercrime saw 24% spike in 2025; Indians lost Rs 22,495 crore | ThePrint | 21 Feb 2026 | https://theprint.in/india/cybercrime-saw-24-spike-in-2025-indians-lost-rs-22495-crore-mainly-in-investment-scams/2859930 | SECONDARY | Typology shares for 2025 (MHA data): investment fraud dominates by value. |
| [S60] | Over 24 lakh cyber complaints, Rs 22,495 crore fraud reported in 2025 | Free Press Journal | 18 Feb 2026 | https://www.freepressjournal.in/mumbai/over-24-lakh-cyber-complaints-22495-crore-fraud-reported-in-2025 | SECONDARY | A second 2025 count (24 lakh complaints) that conflicts with ThePrint's 28.15 lakh. |
| [S61] | NPCI to end P2P collect requests on UPI by October | YourStory | Aug 2025 | https://yourstory.com/2025/08/npci-to-ends-p2p-collect-requests-on-upi-by-october-amid-fraud-concerns | SECONDARY | P2P collect requests stop from 1 Oct 2025; the NPCI circular itself was not read. |
| [S62] | NPCI cautions consumers against downloading AnyDesk app | Outlook Business | 2019 | https://www.outlookbusiness.com/personal-finance-news/npci-cautions-consumers-against-downloading-anydesk-app-2886 | SECONDARY | Remote-access app fraud sequence (2019 warning). |
| [S63] | SIM swap fraud (awareness page) | Axis Bank | not stated in notes | https://axisbank.com/fraud-awarness/sim-swap-fraud | SECONDARY | SIM swap sequence and victim-side signs. |
| [S64] | MHA alert on fraudsters calling citizens as CBI, NCB officials | The Statesman | not stated in notes | https://www.thestatesman.com/india/mha-alert-on-fraudsters-calling-citizens-as-cbi-ncb-officials-1503300277.html | SECONDARY | Digital arrest as an organised cross-border crime; real agencies are impersonated, not complicit. |
| [S65] | Cyber police warn against task-based earning scams | Free Press Journal | 3 Nov 2025 | https://www.freepressjournal.in/amp/mumbai/cyber-police-warn-citizens-against-task-based-earning-scams-promising-easy-money | SECONDARY | Task scam pattern: early payouts of Rs 50 to Rs 500, then larger UPI transfers. |
| [S66] | Delhi Police busts interstate gangs supplying mule bank accounts | ThePrint | not stated in notes | https://theprint.in/india/delhi-police-busts-interstate-gangs-supplying-mule-bank-accounts-to-cybercrooks-9-arrested/2808326 | SECONDARY | Roles in an account-supply ring; CDR, IMEI and money-trail analysis. |
| [S67] | Mule accounts play crucial role in cyber crime, Bengaluru police | Deccan Herald | not stated in notes | https://www.deccanherald.com/india/karnataka/bengaluru/mule-accounts-play-crucial-role-in-cyber-crime-bengaluru-police-2774243 | SECONDARY | Payment splitting; mule holders recruited from poor or rural groups; private-bank data takes 6-10 days. |
| [S68] | Inside India's cyber fraud economy: bank insiders, crypto and mule accounts | CyberPeace (blog) | 24 Oct 2026 | https://cyberpeace.org/resources/blogs/inside-indias-cyber-fraud-economy-bank-insiders-crypto-and-mule-accounts | WEAK | Qualitative role descriptions only; its figures looked inconsistent. |
| [S69] | Explained: RBI's MuleHunter.AI | Business Standard | 9 Dec 2024 | https://www.business-standard.com/amp/finance/personal-finance/explained-rbi-has-a-new-ai-tool-mulehunter-ai-to-reduce-digital-frauds-124120900250_1.html | SECONDARY | Mule recruitment can exploit people as well as implicate them. |
| [S70] | RRN (retrieval reference number) explainer | Xflow (payments company blog) | not stated in notes | https://www.xflowpay.com/blog/rrn-retrieval-reference-number | SECONDARY | UPI RRN is 12 numeric digits; app labels differ (UTR, UPI Ref No). |
| [S71] | NPCI revises RRN in UPI (summary of NPCI circular) | Lexplosion | circular 24 Apr 2024 | https://lexplosion.in/npci-revises-retrieval-reference-number-in-upi-to-avoid-duplicates-psps-and-banks-to-implement-revised-rrn-and-remove-validation-of-yddd-by-31st-may-2024/ | SECONDARY (NPCI circular itself not fetched.) | Date-based YDDD prefix replaced; validation removed by 31 May 2024. |
| [S72] | UPI payment methods (docs) | Razorpay | not stated in notes | https://razorpay.com/docs/payments/payment-methods/upi.md | SECONDARY | VPA form username@handle (limited example). |
| [S73] | Vendor blog post (title not recorded in notes) | Hawkeye Forensic (vendor) | not stated in notes | https://hawkeyeforensic.com/?p=4562 | WEAK | Catalogue of phone, bank, network and telecom artefacts. |
| [S74] | SOP for NCRP and CFCFRMS account freezing (MHA SOP, bank-hosted copy) | MHA SOP as hosted by Zoroastrian Co-operative Bank | SOP dated 2 Jan 2026 | https://www.zoroastrianbank.bank.in/download/SOP-NCRP.pdf | PRIMARY (Bank-hosted copy; about 100,000 of 134,602 characters read; section numbers need rechecking.) | Bank-side steps and timelines; notice annexures; first-layer account. |
| [S75] | CFCFRMS: reading the MHA new account freeze SOP | LiveLaw | not stated in notes | https://www.livelaw.in/articles/cfcfrms-reading-mha-new-account-freeze-sop-537503 | SECONDARY | Freeze limited to the disputed amount; critiques of the SOP. |
| [S76] | Cyber fraud: Rs 11,158 crore saved; how to report on the cybercrime portal | Outlook Money | 13 Aug 2026 | https://www.outlookmoney.com/amp/story/retirement/cyber-fraud-rs-11158-crore-saved-across-328-million-complaints-how-to-report-financial-fraud-on-cybercrime-portal | SECONDARY | Portal reporting steps; Complaint ID; officer verifies and asks the bank to block. |
| [S77] | PIB press release on cyber fraud measures (1930, NCRP, CFCFRMS) | PIB (Government of India) | 12 Mar 2025 | https://pib.gov.in/PressReleasePage.aspx?PRID=2110809 | PRIMARY | 1930 helpline, cybercrime.gov.in, CFCFRMS; policing is a state subject. |
| [S78] | How law enforcement investigates cyber scams in India | ScamDekho (blog) | not stated in notes | https://scamdekho.in/blog/how-law-enforcement-investigates-cyber-scams-in-india-the-complete-process | WEAK | Source of the unverified 'first hour' and Rs 10 lakh e-Zero FIR claims, which the project does not state as fact. |
| [S79] | Language guide: scams communication for industry | Scamwatch (Australian government-linked guide); publisher and date not confirmed on the page | appears 2025 | https://www.scamwatch.gov.au/system/files/language-guide-scams-communication-for-industry.pdf | SECONDARY (Australian; no Indian equivalent found.) | Avoid victim-blaming words, stereotypes and sensationalism. |

### E. Prior art, benchmarks and forensic education

| ID | Title | Publisher or author | Date | URL | Quality | Used for |
|---|---|---|---|---|---|---|
| [S80] | Introducing EvidenceForge: synthetic security logs that don't look as fake | Cisco Talos (author David J. Bianco) | 27 May 2026 | https://blog.talosintelligence.com/introducing-evidenceforge-synthetic-security-logs-that-dont-look-as-fake/ | SECONDARY (Project author's own blog.) | LLM stays out of record generation; prerequisite events; ground truth files. |
| [S81] | EvidenceForge README (fork) | THORCollective fork of Cisco-Talos/EvidenceForge | not stated in notes | https://github.com/THORCollective/EvidenceForge | SECONDARY | Eval pillars; schema and cross-reference checks; seed-reproducible engine. |
| [S82] | EvidenceForge on the SANS tools page | SANS | not stated in notes | https://www.sans.org/tools/evidenceforge | SECONDARY | Shows the tool is SANS-listed; the code is Cisco's. |
| [S83] | Addressing the dataset gap problem with Generative AI: towards LLM-driven forensic scenarios for dataset generation (Plankl, Göbel, Baier) | Forensic Science International: Digital Investigation vol. 56, art. 302053 (DFRWS EU 2026) | 2026 | https://dfrws.org/wp-content/uploads/2026/03/Addressing-the-dataset-gap-problem-with-Generati_2026_Forensic-Science-Inter.pdf | PRIMARY (Essentially one case study; no quantitative benchmark.) | LLM storylines with a deterministic back end; deterministic tasks to code; default-year and coherence-rule failures. |
| [S84] | DFRWS EU 2026: 2 papers accepted | UniBW Munich digital forensics group | not stated in notes | https://www.unibw.de/digfor/news/dfrws-eu-2026-2-papers-accepted | SECONDARY | Confirms the Plankl et al. paper was accepted at DFRWS EU 2026. |
| [S85] | hystck: a novel approach for generating synthetic datasets for digital forensics | Göbel et al., Advances in Digital Forensics XVI (Springer) | 2020 | https://www.rz.unibw-muenchen.de/digfor/publikationen/pdf/goebel2020hystck.pdf | PRIMARY | Ground-truth reporter; XML could help instructors grade; one base image, many variants. |
| [S86] | ForTrace: a holistic forensic data set synthesis framework | Göbel et al., FSI: Digital Investigation 40 | 2022 | https://www.rz.unibw-muenchen.de/digfor/publikationen/pdf/2022-03-dfrws-eu-goebel.pdf | PRIMARY | Difficulty varied by what data a case needs; chat modules were still planned. |
| [S87] | EviPlant (Scanlon, Du, Lillis) | arXiv 1704.08990; Digital Investigation, DFRWS EU 2017 | 2017 | https://arxiv.org/pdf/1704.08990 | PRIMARY | Per-student unique images proposed as a future possibility only. |
| [S88] | ForGe computer forensic test image generator | Forensic Focus | not stated in notes | https://www.forensicfocus.com/articles/forge-computer-forensic-test-image-generator/ | SECONDARY | Trivial bulk files plus hidden secrets; answer-key cheat sheet. |
| [S89] | Towards a Quality Assessment Framework for LLM-Based Decision Support in Digital Forensics | Galvan et al., WDF 2026, CEUR Vol-4329 | Feb 2026 | https://ceur-ws.org/Vol-4329/paper3.pdf | PRIMARY | Synthetic fraud case with automated checks of temporal coverage, counts and thresholds, plus SHA-256 hashes and manifests. |
| [S90] | MuSR: Testing the Limits of Chain-of-thought with Multistep Soft Reasoning (arXiv 2310.16049) | Sprague, Ye, Bostrom, Chaudhuri, Durrett; ICLR 2024 | Oct 2023 (v2 Mar 2024) | https://arxiv.org/abs/2310.16049<br>https://arxiv.org/pdf/2310.16049 | PRIMARY (Only Tables 5 and 8 were seen; page truncated.) | Symbolic tree first, then narrative; validators; GPT-4 80.4 (Table 5, CoT+) vs chance 50.0 and humans 94.1. |
| [S91] | Test of Time: a benchmark for evaluating LLMs on temporal reasoning (arXiv 2406.09170) | Fatemi et al. (Google); ICLR 2025 | Jun 2024 | https://arxiv.org/abs/2406.09170<br>https://proceedings.iclr.cc/paper_files/paper/2025/file/eb7295a8bc613b375726659c2ecd6f14-Paper-Conference.pdf<br>https://arxiv.org/html/2406.09170v1 | PRIMARY | Duration arithmetic as low as 13.5% for tested models; no '13-36%' range stated. |
| [S92] | FactTrack (arXiv 2407.16347v2) | Lyu, Yang, Kong, Klein | not stated in notes | https://arxiv.org/html/2407.16347v2 | PRIMARY (Preprint; judged by an NLI model; binary contradictions only.) | Facts with validity intervals; contradiction when a later pre-fact conflicts with an earlier post-fact. |
| [S93] | ConWriter (arXiv 2608.05169) | Li et al., HKUST-GZ | 2026 | https://arxiv.org/pdf/2608.05169 | PRIMARY (Preprint; 20-case evaluation.) | Static and dynamic memory; commit to memory only if validation passes. |
| [S94] | ConStory-Bench: Lost in Stories (arXiv 2603.05890) | Li et al. | Mar 2026 | https://arxiv.org/html/2603.05890 | PRIMARY (Preprint; English fiction only.) | Timeline and fact errors dominate; absolute-time errors have the largest distance; LLM checker recall 0.55. |
| [S95] | Towards a standardized methodology and dataset for evaluating LLM-based digital forensic timeline analysis (arXiv 2505.03100) | Studiawan, Breitinger, Scanlon | May 2025 | https://arxiv.org/html/2505.03100v1 | PRIMARY | ChatGPT-4o mis-ordered events and did worse than a rule-based approach. |
| [S96] | Paper on realism of synthetic forensic data (title not recorded in notes) | Göbel, Baier, Breitinger, Digital Threats: Research and Practice 4(3), art. 38 | Oct 2023 | https://opus.bibliothek.uni-augsburg.de/opus4/files/117557/117557.pdf | PRIMARY | Seedable generation so each student can get a distinct case; no quantitative quality metrics proposed. |
| [S97] | Student-built forensic case design paper (title not recorded in notes) | Wang, Bai, Goda, SIGITE 2019 | 2019 | https://faculty.washington.edu/godab/Pubs/p33-wangA.pdf | PRIMARY | Over-specific clues make a case trivial; encryption without a key is too hard; grading of report and documentation. |
| [S98] | Forensic Image Description Language (Russell, Macfarlane, Ludwiniak) | Edinburgh Napier University repository | year not stated (about 2012 by inference) | https://napier-repository.worktribe.com/OutputFile/195555 | PRIMARY | Shared static images let students bypass individual work; per-student unique images proposed (design rationale, not measured). |
| [S99] | Authentic Assessment Challenges in Forensic Computing: a tool to enable individualised practical assessment (INTED2025) | Murphy, Krasniewicz, Cox | 2025 | https://library.iated.org/view/MURPHY2025AUN | SECONDARY (Abstract only; integrity purpose not confirmed.) | Generated per-student question and solution sheets for marking. |
| [S100] | VeriScene: Reconstructing Crime Scenes from Legal Evidence via World-Model Agent (arXiv 2609.08342) | Fu, Zheng, Lam, Yeong | Sep 2026 (arXiv ID implies) | https://arxiv.org/pdf/2609.08342 | PRIMARY (Preprint; peer-review status unknown.) | Cite-the-evidence-for-each-claim audit loop; it is NOT a digital-forensics tool. |
| [S101] | Re-Imagen: Retrieval-Augmented Text-to-Image Generator (arXiv 2209.14491) | Chen, Hu, Saharia, Cohen | Sep 2022 | https://arxiv.org/abs/2209.14491 | PRIMARY | Registered only to record that it is an unrelated text-to-image paper and must not be cited. |


## 8. Change log

| Date | Change |
|---|---|
| 24 November 2026 | Statuses updated against the code: 13 Implemented, 18 Partial. Added a Partial label. Replaced the model name. calls.csv now follows F-06 and F-07 (CRLF, quoted text, ISO time with offset); EXIF writes the F-08 tag set; manifest.json carries the synthetic flag, hash note and date order (R-01, H-08, F-02); filler content rules (L-09) and the bias audit (R-03) were added. |
| 23 November 2026 | First version of RULES.md, written from the five research notes (Indian electronic evidence law, forensic standards and procedures, file-format realism, UPI fraud scenarios, case-generation prior art). All rules start as Planned, Needs expert review or Open; none is marked Implemented. |
