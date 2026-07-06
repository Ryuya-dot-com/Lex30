# Updated Lex30 Pilot Administration Protocol

Status: protocol for low-stakes pilot administration.

Default version:
`updated-listening-easycue-posbalanced-followup-pilot-v0.4`

This protocol is for researchers and teachers who administer the current pilot
form. The form is frozen for administration and descriptive QC, but it is not a
validated final test and must not be used for placement, grading, or other
high-stakes decisions.

## Roles

- Lead researcher: owns the version choice, study design, consent process, data
  storage, and analysis decisions.
- Administrator/teacher: runs the participant session, checks audio, collects
  downloads, and records deviations.
- Reviewer: applies `docs/scoring_policy.md` to review items and manual
  overrides.

One person may fill multiple roles, but the role boundaries should be explicit
in the study notes.

## Before The Session

1. Choose the hosting mode.

   For GitHub Pages deployment from `Ryuya-dot-com/Lex30`, use:

   ```text
   https://ryuya-dot-com.github.io/Lex30/researcher.html
   ```

   For local testing, start a local web server from the repository root:

   ```bash
   python3 -m http.server 8000
   ```

   Then open:

   ```text
   http://127.0.0.1:8000/researcher.html
   ```

2. Select the administration version:

   ```text
   updated-listening-easycue-posbalanced-followup-pilot-v0.4
   ```

3. Click `Run Preflight Check`.

   The session should not begin until the selected config, freeze manifest, and
   all audio files pass preflight on the actual administration device/server.
   The researcher page locks `Copy URL` and `Open Participant Page` until
   preflight passes for the selected version.

4. Verify the freeze from the command line when preparing a formal pilot batch:

   ```bash
   python3 tools/freeze_experiment.py updated-listening-easycue-posbalanced-followup-pilot-v0.4 --verify
   ```

5. Complete and confirm the pilot data-collection design for larger batches:

   ```text
   docs/pilot_data_collection_design.md
   ```

   Prepare a protected batch-specific copy of:

   ```text
   docs/pilot_batch_notes_template.md
   ```

6. Prepare participant IDs before administration.

   Use IDs that do not expose names or student numbers unless your ethics/data
   plan explicitly allows them.

7. Prepare the device.

   Use the same browser and audio setup throughout a batch when possible. Check
   headphones or speakers, volume, and browser permissions. Avoid shared browser
   profiles when sensitive data could remain visible. For a formal listening
   batch, complete the perceptual audio QC checklist:

   ```text
   docs/audio_perceptual_qc_checklist.md
   examples/audio_perceptual_qc_template.csv
   ```

8. Protect secrets and analysis files.

   GitHub Pages is public static hosting. Do not place `.env` files, OpenAI API
   keys, ElevenLabs API keys, raw participant exports, or analysis workbooks in
   the published repository. GPT annotation, if used, must be run locally through
   the CLI and treated as optional review metadata.

9. Prepare the storage location.

   Browser-downloaded CSV files should be collected under:

   ```text
   results/raw_exports/
   ```

   Keep JSON downloads as raw archives in a separate protected folder.

## Participant Instructions

Use a consistent spoken or written instruction such as:

```text
You will hear 30 English words. For each word, type up to 4 English words that
come to your mind. Try to type one word in each box. You may leave boxes blank.
The timer starts when the audio begins. Press Next or Space when you are ready,
or the page will move on automatically. After the 30 words, answer short
follow-up questions about the same cue words.
```

Participants may switch the interface between English and Japanese with the
top-right language toggle, but association responses must still be English words.

Do not coach participants on spelling, word choice, list membership, or whether a
response is good. If the task is used in class, present it as a low-stakes pilot
activity or research tool, not as a test of grades.

## Running A Participant

1. From `researcher.html`, copy or open the participant URL.

2. Ask the participant to enter their assigned Participant ID.

3. Confirm that the participant can hear audio before starting the test.

4. Start the test.

5. For listening mode, the response timer starts when the audio begins playing,
   not merely when the item page appears.

6. If autoplay is blocked, the participant should press the audio play control.
   This is acceptable and is logged.

7. If an audio file is unavailable or sounds wrong, stop the session and record a
   deviation. Do not treat that session as primary complete-case evidence without
   review.

8. The listening v0.4 task offers a short break after association item 15. The
   participant can continue when ready; do not rush or coach responses during the
   break.

9. After the free-association task, the participant completes the follow-up
   questions. Do not coach answers to the recognition, meaning, confidence, or
   receptive probe items.

10. If the browser is closed or refreshed, download the saved browser backup if
   possible. The backup is stored only in that browser's `localStorage`.

## After Each Participant

1. Confirm that the CSV result file downloaded automatically. If it did not,
   press the manual CSV download button on the result screen.

2. Confirm that the JSON result file downloaded automatically as the raw archive.
   If it did not, press the manual JSON download button on the result screen.

3. Confirm that both filenames include the experiment ID, participant ID, and
   participant session ID.

4. Move or copy the CSV file into:

   ```text
   results/raw_exports/
   ```

5. Store JSON raw archives according to the study data plan.

6. On shared devices, clear the saved browser backup after confirming that CSV
   and JSON files were collected. The result screen and participant start screen
   provide `Clear Saved Backup`; it requires the matching Participant ID.
   Browser backups expire after 14 days, but this TTL is a recovery aid, not a
   privacy guarantee.

7. Record deviations, for example:

   - audio problem,
   - browser refresh,
   - participant interruption,
   - wrong version opened,
   - missing CSV or JSON,
   - nonstandard instruction,
   - shared-device recovery used.

## Batch Analysis

Run the default no-GPT analysis from the repository root:

```bash
python3 tools/run_pilot_analysis.py results/raw_exports \
  --experiment-id updated-listening-easycue-posbalanced-followup-pilot-v0.4
```

Use `--allow-mixed-experiments` only for diagnostic runs. Do not use mixed raw
exports for primary pilot analysis.

The analysis writes a timestamped folder under:

```text
results/analysis/
```

Open `pilot_workbook.xlsx` first. Review these sheets in order:

1. `Decision_Summary`
2. `Participant_QC`
3. `Score_Diagnostics`
4. `Sensitivity`
5. `Review_Items`
6. `Item_Summary`
7. `Psychometrics`
8. `Cue_Score_Matrix`
9. `Summary`
10. `Scored_Tokens`
11. `Manifest`

Blue workbook columns are for human notes and decisions. They do not alter the
machine-generated CSV outputs. Preserve the workbook before rerunning analysis
into the same output folder.

## Scoring And Review

Use `docs/scoring_policy.md` as the scoring authority for the current pilot.

Key boundaries:

- Spelling is not automatically corrected.
- GPT annotation is optional review metadata only.
- Manual overrides require a recorded decision and rationale.
- v0.4 administration blocks multiword answer slots in the browser. Legacy or
  recovered multiword rows are still reported in `Sensitivity` if present.
- v0.4 scores and follow-up probe outputs are descriptive pilot outputs, not
  validation evidence by
  themselves.

For two-reviewer calibration, use:

```text
docs/reviewer_calibration_protocol.md
examples/reviewer_calibration_decisions_template.csv
```

If manual spelling overrides are needed, run:

```bash
python3 tools/run_pilot_analysis.py results/raw_exports \
  --experiment-id updated-listening-easycue-posbalanced-followup-pilot-v0.4 \
  --manual-overrides examples/manual_overrides.csv
```

Use GPT only when the research plan explicitly calls for optional annotation:

```bash
python3 tools/run_pilot_analysis.py results/raw_exports \
  --experiment-id updated-listening-easycue-posbalanced-followup-pilot-v0.4 \
  --with-gpt
```

Do not report GPT output as the score.

If an external vocabulary/proficiency criterion is collected, link it with:

```bash
python3 tools/run_pilot_analysis.py results/raw_exports \
  --experiment-id updated-listening-easycue-posbalanced-followup-pilot-v0.4 \
  --external-criteria path/to/external_criteria.csv
```

Review `External_Criteria` and `Criterion_Correlations` after participant QC and
manual review decisions. These sheets are descriptive criterion/convergent
diagnostics only; they do not validate the form by themselves.

## Minimum Pilot Batch Notes

For each pilot batch, keep a short record with:

- date and location,
- administrator,
- device/browser,
- version ID,
- preflight result,
- participant ID list,
- deviations,
- analysis output folder,
- whether manual overrides were used,
- whether GPT metadata was used.
- reviewer calibration file, if used,
- audio perceptual QC file.

As a working target, collect at least 50 complete sessions for early item review
and preferably 100+ complete sessions before treating reliability estimates as
stable enough for stronger interpretation.

## Stop Conditions

Stop administration and resolve the issue before continuing if:

- preflight fails,
- the wrong version is selected,
- audio files are missing or audibly defective,
- CSV downloads cannot be collected,
- participant IDs are wrong or duplicated unexpectedly,
- the browser falls back to `?devFallback=1` in a real session.

## Deliverables Checklist

For a complete low-stakes pilot administration batch, retain:

- raw participant CSV files,
- raw participant JSON files,
- study deviation notes,
- analysis output folder,
- `pilot_workbook.xlsx`,
- any `manual_overrides.csv`,
- scoring/reviewer notes,
- and the experiment freeze verification result.
