# Lex30 Pilot Scoring Policy

Status: pilot policy for `updated-listening-easycue-posbalanced-followup-pilot-v0.4`.

This policy supports administration checks, descriptive pilot review, classroom
diagnostic feedback, and item-retention decisions. It is not a validation claim
and does not justify placement, grading, or high-stakes decisions.

## Primary Principle

Scoring must remain deterministic and auditable. GPT/LLM output may be used only
as optional review metadata or reviewer support. GPT/LLM output must not change a
primary score unless a human reviewer records the same decision through a manual
override workflow.

## Primary List Hierarchy

For the current Japanese EFL pilot:

1. NJ8 is the primary score reference.
2. Nation BNC/COCA is a secondary vocabulary-family comparison.
3. NGSL is an auxiliary open-list comparison.

The browser and CLI should keep all three outputs because disagreements are
useful review evidence. Reports should name which list is being interpreted
rather than collapsing the lists into a single undocumented score.

## Current Machine-Scoring Rule

The current deterministic rule is:

```text
K1 = 0
K2+ = 1
off-list = review
stimulus repetition = 0
```

The scorer reports both token and type scores. Type scores count the first
normalized occurrence for a participant/session; repeated normalized responses
remain visible in token rows but do not add type-score points.

## Multiword Answer Slots

Lex30 administration asks for up to four responses per stimulus. A response slot
should normally contain one lexical response.

For the current v0.4 pilot, the browser asks participants to add one English
word at a time and blocks multiword responses before advancing. The scorer still
retains the all-token reporting path for legacy CSVs, recovered backups, and
auditability if a multiword slot appears.

Required safeguards:

- Report `multiword_response_slots` and `extra_tokens_in_response_slots`.
- Use response-slot denominator percentages when comparing participants.
- Treat sessions or items with frequent multiword slots as review cases before
  interpreting scores.
- Do not silently drop extra words in a slot.

Before any final-form validation, inspect the sensitivity analysis for any
legacy/recovered multiword rows. The full pilot pipeline writes this comparison
to `multiword_sensitivity.csv` and the workbook `Sensitivity` sheet.

## Spelling And Typos

Spelling is preserved as typed. The scorer must not automatically correct
responses, and GPT must not be used for automatic spelling correction in the
primary scoring path.

A manual spelling override is allowed only when all of the following are true:

- The intended English word is highly probable from the typed form.
- The correction does not change the response into a different plausible word.
- The decision is recorded in `manual_overrides.csv` or workbook decision
  columns.
- The reviewer records who made the decision and why.

Examples:

- `helth` may be reviewed as a likely spelling of `health`.
- `person` typed correctly must stay `person`.
- Ambiguous forms should remain as typed and be reported as review items.

## Proper Nouns, Non-English Forms, Abbreviations, And Compounds

Use these pilot rules unless a study protocol pre-registers a different rule:

- Proper nouns: review-only unless the study intentionally allows them.
- Non-English responses: review-only and normally excluded from primary English
  lexical scoring.
- Abbreviations: review-only unless they are listed lexical items or documented
  common English forms.
- Hyphenated compounds: score deterministically when recognized by the
  tokenizer/list pipeline; otherwise review.
- Open compounds entered as multiple words: follow the multiword slot rule and
  flag the slot.

## Stimulus Repetition

Stimulus repetition is currently detected through normalized/lemma-based
matching using the available AntBNC normalization fallback. A response that
repeats the stimulus does not receive lexical score credit.

Before final-form validation, decide whether repetition should be exact-form,
lemma-based, or word-family-based. The current pilot reports enough token detail
to audit this decision.

## Spoken Response Transcription And Homophone Sensitivity

For `v0.5` spoken forms (`continuous_4` and `discrete_naming`), raw `.zip`
archives are processed offline via `tools/transcribe_spoken_lex30.py`:

- ASR transcripts are researcher-review inputs, not unverified ground truth.
  Inspect `spoken_transcription_review.csv` (especially low-confidence segments,
  cue-bleed overlaps, and homophone-flagged items) and rerun with
  `--apply-review-csv` before final reporting.
- Spoken homophones (e.g., `night`/`knight`, `write`/`right`) cannot be
  disambiguated by phonology alone. The scorer flags homophone-group tokens and
  reports deterministic sensitivity bounds (`homophone_conservative_nj8_score`
  assigning the highest-frequency/lowest-credit homophone vs
  `homophone_lenient_nj8_score` assigning the lowest-frequency/highest-credit
  homophone) alongside the transcribed primary score.

## Secondary Multifaceted Diagnostics (6 Dimensions)

Alongside the unchanged primary deterministic binary score (`K1 = 0`, `K2+ = 1`),
`score_lex30.py` and `run_pilot_analysis.py` output secondary diagnostic indices
in `multifaceted_summary.csv` and the `Multifaceted` workbook sheet:

1. **Frequency Sophistication**: polytomous band totals (`K1=0, K2=1, K3=2, K4+=3`)
   and continuous log-rank, SUBTLEX-US `Lg10CD`, and `wordfreq` Zipf means.
2. **Retrieval Fluency**: slot-1 onset latency (`mean_rt1_onset_ms`,
   `median_rt1_onset_ms`), inter-response interval (`mean_iri_ms`), and 5s/10s
   time-cutoff K2+ scores.
3. **Phonological vs Semantic Processing**: cue-response form/clang ratio and
   homophone sensitivity bounds.
4. **Network Structure & Chaining**: lexical TTR, intra-item POS diversity,
   response-to-response chaining index (`sim(R_t, R_{t-1}) - sim(R_t, Cue)`),
   forward flow, and optional `--association-norms` stereotypy strength.
5. **Psycholinguistic & Morphological Depth**: Brysbaert concreteness mean,
   Shannon POS entropy, noun-bias ratio, derivational suffix ratio, and word length.
6. **Receptive–Productive Bottleneck (`v0.4` follow-up)**: cue perception accuracy,
   Japanese meaning dictionary match (`tools/data/cue_japanese_glosses.json`),
   conditional K2+ yield on receptively known cues, and productive retrieval gap.

These secondary indices are descriptive research profiles and never overwrite or
reweight primary binary Lex30 scores.

## Manual Review Workflow

1. Run the no-GPT analysis first.
2. Open `pilot_workbook.xlsx`.
3. Review `Decision_Summary`, `Participant_QC`, `Review_Items`, and
   `Item_Summary`. If multiword slots are present, also review `Sensitivity`.
4. For reviewer calibration, use `docs/reviewer_calibration_protocol.md` and
   `examples/reviewer_calibration_decisions_template.csv`.
5. Record optional decisions in blue workbook columns or in
   `manual_overrides.csv`.
6. Preserve the workbook or override CSV before rerunning analysis with
   `--force`.
7. If GPT annotation is used, treat it as reviewer-support metadata only.

For pilot score reporting, report:

- the deterministic score output,
- the number of review items,
- the number and type of manual overrides,
- multiword-slot counts,
- and whether GPT metadata was generated.

## Researcher Reporting Boundary

Reports should state:

- the experiment ID and version,
- whether the form was listening or written,
- the score reference list,
- whether manual overrides were used,
- whether GPT metadata was used,
- and that v0.3 is a pilot form, not a validated final test.
