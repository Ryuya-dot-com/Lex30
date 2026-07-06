# Updated Lex30 Pilot Data Collection Design

Status: working design for low-stakes v0.4 pilot data collection. Items marked
`TBD` must be confirmed for the actual batch before administration.

Default administration version:
`updated-listening-easycue-posbalanced-followup-pilot-v0.4`

Use this design before collecting a larger pilot batch. The goal is to make the
sample, inclusion rules, external criteria, and modality/order design known
before the analysis workbook is interpreted.

## Working Decisions For The Next Batch

| Decision Area | Working Decision |
| --- | --- |
| Primary form | Use `updated-listening-easycue-posbalanced-followup-pilot-v0.4`. |
| Primary interpretation | Listening-triggered lexical association for descriptive pilot evidence; follow-up probes are diagnostic covariates and QC evidence. |
| Primary score reference | NJ8, with BNC/COCA and NGSL retained as secondary diagnostics. |
| Sample target | At least 50 complete sessions for early item review; prefer 100+ complete sessions before stronger reliability interpretation. |
| Stimulus order | Use the frozen fixed order for the first larger v0.4 listening batch; analyze `StimulusOrder` descriptively. |
| Modality comparison | Do not treat this batch as a written/listening parallel-form validation unless a separate counterbalanced design is added. |
| External criterion | Prefer UVLT CAT Stage 1 or another linkable vocabulary/proficiency criterion if feasible; otherwise report the batch as item/QC evidence only. |
| GPT metadata | Disabled by default; optional review metadata only if explicitly planned. |

## Study Boundary

- Intended use: low-stakes research, classroom diagnostic feedback, descriptive
  QC, and item-retention review.
- Primary interpretation: listening-triggered lexical association, not a
  validated placement or grading score.
- Target population: Japanese EFL learners; exact class, institution, and age or
  education level `TBD`.
- Setting: supervised classroom, lab, or researcher-managed session with a
  controlled browser/audio setup; exact site `TBD`.
- Expected proficiency range: `TBD`; avoid collecting only from a group expected
  to produce near-zero responses or only from a group expected to be near ceiling.
- L1 background, if relevant: expected Japanese L1 or Japan-based EFL context;
  record mixed-L1 participation if present.
- Administrator: `TBD`.
- Collection dates: `TBD`.

Required statement:

```text
The current v0.4 listening follow-up form is a frozen pilot form for descriptive
QC, item-retention review, and low-stakes research or classroom feedback. It is
not a validated final test and must not be used for placement, grading, or other
high-stakes decisions.
```

## Version And Administration

- Experiment ID: `updated-listening-easycue-posbalanced-followup-pilot-v0.4`
- Hosting mode: GitHub Pages for formal administration, or localhost for
  rehearsal only; exact URL/server `TBD`.
- Administration device/browser: use the same browser family and device type
  throughout a batch when possible; record exact browser and device in batch
  notes.
- Audio setup: headphones or quiet speaker setup required; run an audible
  listen check before the participant starts.
- Preflight completed on the administration device/server: required before each
  collection session.
- Command-line freeze verification completed: required before each formal batch.
- Participant instructions used exactly as written in
  `docs/pilot_administration_protocol.md`: required.
- Deviations log location: use a protected batch-specific copy of
  `docs/pilot_batch_notes_template.md`; exact completed-note path `TBD`.

Pre-administration checks:

```bash
python3 tools/freeze_experiment.py updated-listening-easycue-posbalanced-followup-pilot-v0.4 --verify
```

Open `researcher.html`, select the same experiment ID, and run the browser
preflight before copying or opening the participant URL.

## Sample Plan

- Planned participant groups: one or more intact Japanese EFL classes or
  researcher-recruited learner groups; group labels `TBD`.
- Target complete sessions: 50 minimum for early item review; 100+ preferred.
- Minimum complete sessions for early item review: 50.
- Recruitment source: `TBD`.
- Inclusion criteria: assigned anonymous participant ID, correct experiment ID,
  complete 30-item session, audio check passed, CSV collected, JSON archive
  collected when required by the study plan, and consent/ethics requirements met.
- Exclusion criteria for primary complete-case analysis: wrong experiment ID,
  `?devFallback=1`, failed or missing preflight, missing CSV, unresolved duplicate
  ID/session problem, known defective audio, or major nonstandard administration.
- Treatment of incomplete sessions: retain for workflow/QC review, but exclude
  from primary complete-case psychometrics unless a partial-session analysis is
  explicitly planned.
- Treatment of duplicate participant/session IDs: do not merge rows across
  sessions. Resolve from session IDs and deviation notes; include only one
  session in primary analysis when a documented retake rule exists.
- Treatment of audio/playback deviations: review before inclusion. Exclude from
  primary listening-form evidence when the participant did not hear the cue or
  when an audio file was missing or audibly defective.
- Treatment of high auto-advance or low filled-slot sessions: review before
  inclusion. Use `Participant_QC` and `Score_Diagnostics`; include in sensitivity
  analysis only unless the researcher documents a reason for primary inclusion.

Working target:

- Collect at least 50 complete sessions for early item review.
- Prefer 100+ complete sessions before treating reliability estimates as stable.
- If complete sessions are below the stated threshold, label outputs as workflow
  and QC evidence only.

## External Criteria

Collect at least one linkable external criterion when feasible.

- External criterion name: `TBD`; recommended first choice for the current plan
  is UVLT CAT Stage 1 when available. Other acceptable criteria are an existing
  course placement level, vocabulary size/level test, teacher rating, or
  TOEIC/CEFR proxy.
- Source: `TBD`.
- Collection date: `TBD`.
- Linkage key: anonymous participant ID used in Lex30 exports.
- Scale/range: `TBD`.
- Missing-data rule: report missing criterion data; do not impute for the first
  pilot pass.
- Expected relationship with Lex30 score: positive association with NJ8 token and
  type scores, after participant QC and manual review decisions.
- Whether the criterion can be stored with Lex30 results: `TBD`; store outside
  public GitHub Pages content unless explicitly approved.

Candidate criteria:

- UVLT CAT Stage 1,
- vocabulary size or vocabulary level test,
- course placement level,
- TOEIC/CEFR proxy,
- teacher rating,
- existing lexical association measure.

If no external criterion is collected, report the pilot as item/QC evidence only
and do not make criterion-validity claims.

## Order And Modality Design

This working plan treats the current fixed stimulus order as the standard
administration for the first larger v0.4 listening batch. Treat order effects as
a limitation to inspect, not as something already ruled out.

- Stimulus order design: fixed for the first larger v0.4 listening batch.
- Rationale: preserves the frozen administration form and avoids creating a new
  variant before initial item/QC evidence is collected.
- Planned `StimulusOrder` analysis: inspect response completion, auto-advance,
  reaction time, and cue scores by `StimulusOrder` in `Item_Summary`,
  `Cue_Score_Matrix`, and downstream analysis.
- Written form collected: no by default for the first listening-focused batch.
- Listening form collected: yes.
- If both modalities are collected, design: `TBD`; use a separately documented
  counterbalanced subset rather than treating shared cues as automatic parallel
  forms.
- Modality order: not applicable unless a written/listening subset is added.
- Washout interval: not applicable unless a written/listening subset is added.
- Counterbalancing rule: not applicable unless a written/listening subset is
  added.
- Whether identical cue reuse is acceptable: not assumed; must be justified if a
  modality comparison is added.

If no written/listening comparison is planned, state that the listening form is
being piloted on its own and do not interpret it as a validated parallel form.

## Raw Data Handling

- CSV collection folder:
  `results/raw_exports/`
- JSON archive location: protected storage outside public GitHub Pages content;
  exact folder `TBD`.
- Participant ID format: anonymous IDs such as `L30-<group>-###`; do not use
  participant names or raw student numbers unless the ethics/data plan explicitly
  allows it.
- File naming check completed: required after each participant.
- Shared-device backup clearing procedure followed: required on shared devices
  after CSV and JSON collection are confirmed.
- Manual override CSV location, if used: protected batch-specific file; exact
  path `TBD`.
- Whether GPT metadata is used: no by default.

Rules:

- Do not edit raw CSV exports in place.
- Keep JSON downloads as raw archives.
- Use manual override CSV files only after human review.
- Treat GPT output as optional review metadata, not primary scoring.

## Analysis Plan

Default no-GPT analysis:

```bash
python3 tools/run_pilot_analysis.py results/raw_exports \
  --experiment-id updated-listening-easycue-posbalanced-followup-pilot-v0.4
```

Primary review order:

1. `Decision_Summary`
2. `Participant_QC`
3. `Score_Diagnostics`
4. `Sensitivity`
5. `Review_Items`
6. `Item_Summary`
7. `Psychometrics`
8. `Item_Diagnostics`
9. `Cue_Score_Matrix`
10. `Summary`
11. `Scored_Tokens`
12. `Manifest`

Score-distribution checks:

- Inspect floor concentration before interpreting low mean scores.
- Inspect ceiling concentration before claiming the form differentiates stronger
  participants.
- Inspect sparse-response concentration before interpreting low scores as only
  vocabulary knowledge.
- Compare token/type scores and response-slot denominator percentages.
- Treat multiword answer slots as a score-inflation review issue.
- v0.4 browser administration blocks multiword answer slots. Use `Sensitivity`
  and `multiword_sensitivity.csv` to inspect legacy/recovered multiword rows if
  any appear.

Follow-up checks:

- Confirm that follow-up completion is near complete before using the follow-up
  fields in item-level interpretation.
- Treat recognition confidence and typed heard word as cue-perception QC, not as
  the primary score.
- Treat Japanese meaning, semantic confidence, response confidence, and
  receptive probe correctness as diagnostic covariates for explaining cue-level
  association output.

External-criteria analysis, if available:

- Confirm the linkage key before merging data.
- Preserve the unmerged raw criterion file.
- Report missing criterion data.
- Correlate Lex30 scores with the external criterion only after participant QC
  and manual review decisions are documented.

External criterion CSV template:

```text
examples/external_criteria_template.csv
examples/uvlt_cat_external_criteria_template.csv
```

Reviewer calibration and audio QC templates:

```text
docs/reviewer_calibration_protocol.md
docs/audio_perceptual_qc_checklist.md
examples/reviewer_calibration_decisions_template.csv
examples/audio_perceptual_qc_template.csv
```

External criterion command:

```bash
python3 tools/run_pilot_analysis.py results/raw_exports \
  --experiment-id updated-listening-easycue-posbalanced-followup-pilot-v0.4 \
  --external-criteria path/to/external_criteria.csv
```

## Decision Log

Record decisions before rerunning analysis into an existing output folder.

| Date | Decision | Rationale | Decided By | Evidence/File |
| --- | --- | --- | --- | --- |
| 2026-07-06 | Use v0.4 listening follow-up as the next primary administration form. | Keeps the Lex30 free-association core, reuses frozen v0.3 audio, and adds post-association recognition/semantic diagnostics; not final validation evidence. | Working plan | `configs/updated-listening-easycue-posbalanced-followup-pilot-v0.4.freeze.json` |
| 2026-07-06 | Keep fixed stimulus order for the first larger listening batch. | Avoids introducing a new variant before initial item/QC evidence; analyze order effects descriptively. | Working plan | `StimulusOrder` export and `Item_Summary` |
| 2026-07-06 | Target 50 complete sessions minimum, 100+ preferred. | Supports early item review while avoiding overinterpretation of unstable reliability estimates. | Working plan | `docs/pilot_readiness_roadmap.md` |
| 2026-07-06 | Disable GPT metadata by default. | Primary scoring remains deterministic and auditable. | Working plan | `docs/scoring_policy.md` |

## Stop Conditions

Stop collection and resolve the issue before continuing if:

- researcher preflight fails,
- command-line freeze verification fails,
- the wrong experiment ID is opened,
- audio is missing or audibly defective,
- participant IDs are wrong or duplicated unexpectedly,
- CSV downloads cannot be collected,
- JSON archives are missing when the study plan requires them,
- the browser uses `?devFallback=1` in a real session.
