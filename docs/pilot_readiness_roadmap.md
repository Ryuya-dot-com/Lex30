# Updated Lex30 Pilot Readiness Roadmap

This roadmap separates construct/form decisions, administration readiness,
scoring-policy decisions, reviewer calibration, pilot psychometrics, and
final-form validation. The current v0.4 listening follow-up form is suitable for
frozen pilot administration and descriptive QC, not for consequential placement,
grading, or final-form claims.

## Current Status

Implemented and usable now:

- Frozen v0.4 listening follow-up administration with config/audio hashes.
- Researcher preflight for config, freeze metadata, and audio availability.
- Browser CSV/JSON exports with session, timing, audio-play, autosave, and
  follow-up data.
- Participant export filenames include session IDs.
- Participant page fails closed when config loading fails, except explicit
  `?devFallback=1` development runs.
- Batch analysis workbook with `Decision_Summary`, `Data_Dictionary`, QC sheets,
  review items, psychometrics, cue-level score matrix, token-level scoring, and
  manifest.
- Workbook-only manual decision columns for researcher notes.
- Raw-batch validation against selected experiment metadata/stimuli.
- Output-directory overwrite protection unless `--force` is explicitly used.
- Session-level scoring summaries through `analysis_session_key`.
- v0.4 browser blocking for multiword answer slots, with legacy/recovery
  multiword QC and response-slot denominator score percentages retained.
- Analysis manifest script/data hashes and runtime metadata.
- Cue score matrix, descriptive Cronbach-alpha diagnostics, split-half
  reliability, bootstrap CIs, and item-total/item-rest diagnostics for complete
  sessions.
- Score-distribution floor/ceiling and sparse-response diagnostics through
  `score_diagnostics.csv` and the workbook `Score_Diagnostics` sheet.
- Optional external-criteria linkage and descriptive criterion/convergent
  correlation outputs through `--external-criteria`.
- Audio-mode response timer starts after the first audio `play` event, with
  exported load/playable/failure/autoplay-blocked/error/timer-start fields.
- Saved browser backups include a 14-day retention timestamp and visible clear
  controls that require the matching Participant ID.
- Researcher page locks participant URL copy/open actions until preflight passes
  for the selected version.
- Pilot scoring policy is documented in `docs/scoring_policy.md`.
- Researcher/teacher administration protocol is documented in
  `docs/pilot_administration_protocol.md`.
- Pilot data-collection working design is documented in
  `docs/pilot_data_collection_design.md`.
- Batch notes and deviation tracking template is documented in
  `docs/pilot_batch_notes_template.md`.

Current interpretation boundary:

- Use current outputs for administration checks, descriptive pilot review, item
  review, and researcher workflow decisions.
- Do not use current scores for placement, grading, or final-form claims.
- GPT annotation remains optional review metadata and is not part of primary
  scoring.
- Spelling is preserved as typed unless a documented manual override is applied.

## Phase 0: Construct And Form Decision

Goal: define what Updated Lex30 is measuring and which form is being piloted
before adding more implementation or collecting larger samples.

Working decision for the next pilot:

- Treat `updated-listening-easycue-posbalanced-followup-pilot-v0.4` as the
  default administration form because its config and audio/follow-up layout are
  frozen.
- Treat `updated-written-easycue-posbalanced-pilot-v0.3` as a comparison or
  development form until its own status, administration design, and validation
  plan are documented.
- Treat the original `lex30-original-written-v1` as a baseline/comparison form,
  not as evidence that the updated listening form is already validated.

Decisions to document:

1. Intended use.
   State whether the tool is for research, classroom diagnostic feedback,
   low-stakes formative assessment, or a later validated test candidate.

2. Primary interpretation.
   Decide whether the primary construct is written lexical association,
   listening-triggered lexical association, or modality comparison.

3. Target population.
   Specify learner population, age/education context, L1 background if relevant,
   and expected proficiency range.

4. Cue-selection rationale.
   v0.3 intentionally keeps all cues in NJ8 K1 / BNC-COCA K1 / NGSL K1 and
   approximates the original Lex30 POS profile. Document whether the priority is
   accessibility for Japanese EFL learners, comparability to original Lex30 cue
   structure, response dispersion, or parallel written/listening forms.

5. Modality plan.
   If written and listening forms are compared, specify within-subject vs
   between-subject design, modality order, washout interval, counterbalancing,
   and whether identical cue reuse is acceptable.

Gate to administration hardening:

- Default pilot form and comparison forms are named.
- Target population and use boundary are written.
- Written/listening relationship is explicit.
- Fixed-order vs randomized/counterbalanced administration is decided for the
  pilot sample.

## Phase 1: Administration Hardening

Goal: reduce data-loss, timing, audio, and device-context risks before collecting
a larger pilot sample.

Implemented hardening:

1. Audio timing.
   The response timer starts only after the first audio `play` event in audio
   mode. Exports log loaded, playable, play failure, autoplay-blocked,
   audio-error, and timer-start states.

2. Shared-device recovery.
   Keep saved backups available, but add clearer shared-device handling:
   matching participant ID is required for saved-backup download and clearing;
   backups now carry a 14-day retention timestamp.

3. Pilot administration checklist.
   Required browser/server setup, preflight pass, headphone/audio check,
   CSV+JSON collection, backup handling, and data-storage procedure are
   documented in `docs/pilot_administration_protocol.md`.

4. Researcher preflight enforcement.
   `Copy URL` and `Open Participant Page` are locked until preflight passes for
   the selected version. The check requires HTTP(S) serving, config/freeze
   consistency, and audio availability for audio-presented versions.

Remaining tasks:

1. Audio perceptual QC gate.
   Preserve the current human-approved Matilda American English audio, but make
   the acceptance criteria explicit: target accent, intelligibility, absence of
   misleading stress or vowel quality, device/headphone listen-through, and any
   pronunciation-risk notes. The number/early replacement history should remain
   auditable through the audio manifest and QC folders.

Gate to larger pilot:

- Preflight passes on the actual administration device/server.
- Audio timing logs distinguish loaded/played/failed/autoplay-blocked states.
- Timer starts after audible cue onset in listening mode.
- Export filenames, session IDs, and backup procedure are confirmed.
- Researchers can recover or archive data without exposing prior participants on
  shared devices.
- Researchers have a short administration protocol they can follow without
  reading the codebase.

## Phase 2: Scoring Policy Freeze

Goal: write a stable scoring specification before interpreting pilot scores.

Pilot policy now documented in `docs/scoring_policy.md`:

1. Multiword answer slots.
   The current v0.4 browser asks for one English word per box and blocks
   multiword advance. The scorer still reports `multiword_response_slots` and
   `extra_tokens_in_response_slots` for legacy/recovered rows.

2. Spelling and typo handling.
   Typed responses are preserved. Automatic GPT correction is outside the
   primary scoring path. Manual overrides require a recorded reviewer decision
   and rationale.

3. Proper nouns, non-English forms, abbreviations, and compounds.
   These are review categories unless the study protocol explicitly allows
   another treatment.

4. Stimulus repetition.
   Current repetition detection is lemma-based through AntBNC normalization.
   Repetitions receive zero score credit under the current machine rule.

5. Primary list hierarchy.
   NJ8 is the current primary Japanese EFL pilot reference; BNC/COCA and NGSL
   remain secondary/auxiliary comparisons.

Final-form pending decisions:

- Compare the all-token pilot rule with first-token or other multiword-slot
  policies before final validation.
- Decide whether final repetition handling should use exact form, lemma, or word
  family.
- Calibrate reviewer agreement on spelling, off-list forms, compounds, proper
  nouns, and non-English responses.

Gate to score reporting:

- A scoring-policy document exists.
- Manual override rules are documented.
- Multiword slots have a fixed primary-score rule.
- Review categories are stable enough for two researchers to apply consistently.
- GPT/LLM use is explicitly limited to optional annotation or reviewer support.

## Phase 3: Reviewer Calibration

Goal: make human review reliable enough that manual decisions do not become an
uncontrolled scoring variable.

Tasks:

1. Calibration set.
   Use a small batch of real or sample responses containing spelling errors,
   off-list forms, compounds, proper nouns, non-English responses, and multiword
   slots. Use `docs/reviewer_calibration_protocol.md` and
   `examples/reviewer_calibration_decisions_template.csv`.

2. Independent coding.
   Have at least two researchers apply the scoring policy independently before
   comparing decisions.

3. Disagreement resolution.
   Record disagreement types and revise the scoring policy if the rules are not
   operational enough.

4. Audit trail.
   Preserve final decisions in workbook decision columns or a manual override
   CSV before rerunning analysis.

Gate to primary pilot scoring:

- Reviewer agreement is acceptable for the intended low-stakes use, or
  disagreements are explicitly reported.
- All manual override categories have examples.
- Manual decisions can be reproduced from the saved workbook/CSV trail.

## Phase 4: Pilot Data Collection Design

Goal: collect data that can support item-retention and reliability decisions.

Design tasks:

1. Sample plan.
   Specify target participant groups, proficiency range, minimum sample size,
   exclusion rules, and whether incomplete sessions are analyzed descriptively or
   excluded from primary summaries. As a working planning target, aim for at
   least 50 complete sessions for early item review and preferably 100+ complete
   sessions before treating reliability estimates as stable. Use
   `docs/pilot_data_collection_design.md` to record the final plan before
   collecting a larger batch.

2. External criteria.
   Collect at least one linkable external criterion when feasible: vocabulary
   size/level test, course placement, TOEIC/CEFR proxy, teacher rating, or an
   existing lexical association measure. If no criterion is collected, label the
   pilot as item/QC evidence only.

3. Order effects.
   v0.3 currently uses fixed order. Decide whether fixed order is part of the
   standard administration or whether a randomized/counterbalanced pilot version
   is needed for item-retention evidence. At minimum, analyze `StimulusOrder`
   effects.

4. Modality comparison.
   If the listening version is intended as a parallel form, collect written and
   listening data from a subset of participants with a documented order and
   washout plan.

Gate to psychometric analysis:

- Batch contains only the intended experiment/version.
- Complete-case count meets the stated pilot threshold.
- External criteria, if used, are cleanly linked by participant/session ID.
- Manual review decisions are preserved before rerunning analysis.
- Modality/order design is known rather than inferred after collection.

## Phase 5: Pilot Psychometrics

Goal: turn pilot data into evidence for item retention and score interpretation.

Implemented diagnostics:

- Cue-by-session score matrix.
- Descriptive Cronbach-alpha diagnostics for complete sessions.
- Odd/even split-half reliability with Spearman-Brown adjustment.
- Random-split and bootstrap split-half reliability intervals.
- Bootstrap CIs for mean total score and alpha.
- Cue-level `item_diagnostics.csv` with item-total and item-rest correlations.
- Score distribution fields and QC summaries in the workbook.
- Floor/ceiling and sparse-response diagnostics for token/type score fields in
  `score_diagnostics.csv` and the workbook `Score_Diagnostics` sheet.
- All-token vs first-token-per-slot multiword sensitivity in
  `multiword_sensitivity.csv` and the workbook `Sensitivity` sheet.
- Optional external-criteria linkage with `external_criteria_linked.csv`,
  `external_criteria_correlations.csv`, and matching workbook sheets when
  `--external-criteria` is supplied.

Next diagnostics:

1. Sensitivity analyses.
   Compare scores before and after manual spelling decisions. Use the implemented
   multiword sensitivity output to decide whether the all-token pilot rule
   materially affects interpretation.

2. Criterion/convergent interpretation.
   If external vocabulary/proficiency data exist, review linkage quality,
   missingness, sample size, and correlations before making any criterion
   validity claim.

Gate to final-form candidate:

- Item-retention decisions are documented.
- Reliability and score-distribution diagnostics are acceptable for the intended
  research use.
- Manual review sensitivity does not materially change interpretation, or the
  dependency is explicitly reported.
- Listening-specific issues do not cluster around particular cues or devices.
- Cue-level decisions are traceable to evidence, not only researcher intuition.

## Phase 6: Final-Form Candidate

Goal: create a candidate that can be frozen and then validated in a new sample.

Tasks:

1. Form revision decision record.
   For every retained, revised, replaced, or dropped cue, record evidence from
   response productivity, item-rest correlation, modality effects, audio QC,
   POS/ambiguity review, and review-token burden.

2. Revise or retain stimuli.
   Use item QC, response productivity, timing, audio issues, POS/ambiguity
   review, and review-token burden.

3. Freeze candidate config and audio.
   Generate a new freeze manifest after any stimulus/audio/config change.

4. Prepare administration documentation.
   Include participant instructions, researcher checklist, data-handling notes,
   scoring-policy document, and interpretation limits.

5. Validation study.
   Collect a new sample for validation rather than validating only on the item
   selection pilot.

Gate to consequential use:

- Final form is validated on a fresh sample.
- Reliability, validity, and scoring policy are documented.
- Score interpretation is tied to the validated population and use case.
- Limitations of the listening modality and GPT review metadata are explicit.

## Immediate Next Sprint

Recommended next implementation order:

1. Confirm the `TBD` fields in `docs/pilot_data_collection_design.md` for the
   actual participant batch.
2. Complete perceptual audio QC with `docs/audio_perceptual_qc_checklist.md`.
3. Run a reviewer-calibration pass using `docs/scoring_policy.md` and
   `docs/reviewer_calibration_protocol.md`.
4. Inspect `Sensitivity` before finalizing the multiword-slot policy.
5. If external criteria are collected, inspect `External_Criteria` and
   `Criterion_Correlations` after participant QC decisions.

## Operational Rules

- Do not mix raw CSV exports from different experiment IDs in primary analysis.
- Preserve workbook decisions before rerunning analysis into an existing output
  folder.
- Keep browser JSON files as raw archives; use CSV as the primary batch-analysis
  input.
- Treat LLM/GPT output as optional review metadata, not primary scoring.
- Treat v0.3 as a frozen pilot, not a validated final form.
- Treat written/listening comparisons as a design question, not as an automatic
  consequence of sharing the same cue list.
