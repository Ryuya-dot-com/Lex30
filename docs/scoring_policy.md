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

For the current v0.4 pilot, the browser asks for one English word per response
box and blocks multiword answer slots before advancing. The scorer still retains
the all-token reporting path for legacy CSVs, recovered backups, and auditability
if a multiword slot appears.

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
