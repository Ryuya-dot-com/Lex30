# Lex30 Reviewer Calibration Protocol

Status: working protocol for low-stakes pilot review.

Use this protocol before finalizing manual spelling overrides, excluding review
tokens, or interpreting off-list response patterns. The goal is to make human
review decisions reproducible enough that they do not become an undocumented
scoring variable.

## Materials

- `docs/scoring_policy.md`
- `pilot_workbook.xlsx` from the target analysis batch
- `Review_Items`, `Sensitivity`, and `Scored_Tokens` workbook sheets
- `examples/reviewer_calibration_decisions_template.csv`
- Any proposed `manual_overrides.csv`

## Calibration Set

Build a small set of rows that covers the decision types the pilot is likely to
need:

- spelling or typo candidates
- both-off-list forms
- NJ8/BNC-COCA list disagreements
- proper nouns
- non-English responses
- abbreviations
- hyphenated or open compounds
- multiword answer slots
- stimulus repetitions or near-repetitions

For the first pass, include all high-priority `Review_Items` rows plus a sample
of medium-priority rows. Add `Sensitivity` rows where first-token scoring changes
any participant score.

## Independent Review

1. Run the no-GPT analysis first.
2. Give each reviewer the same calibration set and the current scoring policy.
3. Reviewers work independently. Do not resolve cases during first coding.
4. Each reviewer records decisions in a separate copy of:

   ```text
   examples/reviewer_calibration_decisions_template.csv
   ```

5. Use only the allowed `decision` values unless the scoring policy is revised:

   ```text
   accept_as_typed
   correct_spelling
   exclude_invalid
   proper_noun
   non_english
   abbreviation
   compound_policy
   multiword_policy
   stimulus_repetition
   uncertain
   ```

## Compare Decisions

After independent coding, compare decisions by `analysis_session_key`,
`stimulus`, `response_token`, and `lookup_token`.

Record at minimum:

- number of rows reviewed
- exact-agreement count and percent
- disagreement categories
- rows requiring policy clarification
- final resolved decision
- whether a manual override is needed

Do not create or apply a manual override until the resolved decision is recorded.

## Resolution

For each disagreement:

1. Re-read the relevant section of `docs/scoring_policy.md`.
2. Decide whether the policy already answers the case.
3. If not, revise the policy before applying a one-off decision.
4. Record the final decision and rationale.
5. Add only justified spelling corrections to `manual_overrides.csv`.

If a decision changes scoring, rerun the analysis with the appropriate
`--manual-overrides` file and preserve the pre-rerun workbook.

## Reporting

In pilot reporting, state:

- number of reviewers
- number of calibration rows
- agreement rate or unresolved disagreement count
- number and type of manual overrides
- whether multiword sensitivity changed interpretation
- whether GPT metadata was used

GPT annotation may support review, but it is not an independent reviewer and
must not be counted as one.
