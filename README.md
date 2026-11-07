# Lex30

This repository currently contains a browser-based Lex30 data collection page and
a research-oriented scoring CLI.

For the current pilot-readiness plan, see
`docs/pilot_readiness_roadmap.md`.
For administration, use `docs/pilot_administration_protocol.md`.
For pilot data-collection design, use
`docs/pilot_data_collection_design.md`.
For batch notes and deviation tracking, copy
`docs/pilot_batch_notes_template.md` into protected study storage.
For pilot scoring and manual-review rules, use `docs/scoring_policy.md`.

## Run A Versioned Session

Use `researcher.html` to choose an experiment version and generate a participant
URL. For GitHub Pages deployment from `Ryuya-dot-com/Lex30`, the expected
researcher page is:

```text
https://ryuya-dot-com.github.io/Lex30/researcher.html
```

For local testing, serve the repository root and open:

```text
http://127.0.0.1:8000/researcher.html
```

Before sharing the participant URL, click `Run Preflight Check` on the researcher
page. The browser checks that the selected config loads, the freeze manifest
matches the selected version, and all audio files are reachable. On GitHub Pages
or localhost it also verifies MP3 SHA-256 hashes when the browser exposes Web
Crypto. `Copy URL` and `Open Participant Page` remain locked until preflight
passes for the selected version. The researcher page also shows the matching
analysis command for the selected version and the expected Excel workbook output
path.

Do not publish `.env` files or API keys through GitHub Pages. GPT annotation, if
used, is a local CLI analysis option only; it is not part of the browser app.

The participant URL looks like this:

```text
index.html?experiment=lex30-original-written-v1
```

Experiment definitions live in `experiments.json`, with detailed settings under
`configs/`. The current recommended administration version is
`updated-listening-easycue-posbalanced-followup-pilot-v0.4`. The original
written Lex30 baseline, `lex30-original-written-v1`, remains registered for
comparison and preserves the existing 30 written cue words, 4 responses per cue,
and 30 seconds per cue. Updated Lex30 versions are also registered:

- `updated-written-pilot-v0.1`
- `updated-listening-pilot-v0.1`
- `updated-written-easycue-pilot-v0.2`
- `updated-listening-easycue-pilot-v0.2`
- `updated-written-easycue-posbalanced-pilot-v0.3`
- `updated-listening-easycue-posbalanced-pilot-v0.3`
- `updated-listening-easycue-posbalanced-followup-pilot-v0.4`
- `updated-written-spoken-continuous-pilot-v0.5`
- `updated-written-spoken-discrete-pilot-v0.5`
- `updated-listening-spoken-continuous-pilot-v0.5`
- `updated-listening-spoken-discrete-pilot-v0.5`

The listening POS-balanced follow-up v0.4 pilot is the current default for
administration. It keeps the 30-cue Lex30 free-association core and adds
post-association recognition, Japanese-meaning, confidence-slider, and receptive
semantic probe fields. The earlier listening POS-balanced v0.3 pilot remains
registered as the no-follow-up listening form with the same approved Matilda
American English audio. The four v0.5 spoken pilots reuse the same 30 cues across
written (`text`) and listening (`audio`) stimulus presentation and compare
continuous 4-word spoken production (`continuous_4`) against word-by-word
discrete naming (`discrete_naming`). On `researcher.html`, researchers can filter
by stimulus/response modality, choose `vad_and_key` vs `key_only` slot advance
for discrete naming, choose `free` vs `star_no_chaining` association
instructions, configure un-scored practice warm-up items (`?practice=2|0`, using
`audio/practice/` for listening forms; default `2` for spoken modes and `0` for
written modes), select POS- and psycholinguistically matched 15-cue parallel
split-half forms (`?subset=form_a|form_b`, defined in
`tools/data/parallel_split_halves.json`) or counterbalanced presentation order
(`?order=counterbalanced_ba|random|fixed`), set or lock the participant UI
language (`?lang=ja|en`, plus `&langLock=1` to hide the participant language
toggle in controlled sessions), and test microphone permission before
sharing a link. None of these
forms is a psychometrically validated final test.

The v0.4 listening follow-up freeze file is:

```text
configs/updated-listening-easycue-posbalanced-followup-pilot-v0.4.freeze.json
```

It records the config hash, stimulus profile hash, and all 30 MP3 hashes. To
regenerate this reproducibility lock file after an intentional config or audio
change:

```bash
python3 tools/freeze_experiment.py updated-listening-easycue-posbalanced-followup-pilot-v0.4
```

To verify that the frozen config and audio files still match the lock file:

```bash
python3 tools/freeze_experiment.py updated-listening-easycue-posbalanced-followup-pilot-v0.4 --verify
```

Before a formal pilot batch, run the broader release-readiness check:

```bash
python3 tools/validate_release.py
```

This checks the default v0.4 registry entry, config invariants, freeze manifest,
audio file presence, one-at-a-time participant UI wiring, bilingual English-only
instructions, automatic-download wiring, researcher preflight wiring, and
follow-up probe coverage.

Downloaded CSV files include experiment metadata columns such as `ExperimentId`,
`ExperimentVersion`, `Mode`, `InterfaceLanguage`, `StimulusSetId`,
`AudioVersion`, `StimulusOrder`, `StartedAt`, `CompletedAt`,
`ParticipantSessionId`, item-level start/end
timestamps, advance trigger, audio file path, audio play count, audio ended
count, audio load/playability/error states, autoplay-blocked state, and the
audio-mode timer-start marker. Listening v0.4 also records
`CompletedAssociationBreakOrders` for the mid-task break. The original
`Participant`, `Stimulus`, `Answer1`-`Answer4`, and
`ReactionTime(ms)` columns are still present, so the scoring CLI remains
compatible. The v0.4 CSV also includes follow-up recognition, confidence,
Japanese-meaning, and receptive semantic-probe columns. The browser also exports
JSON with `schemaVersion: lex30-browser-results-v3`; use JSON as the fuller raw
archive and CSV as the spreadsheet/scoring input.

All three browser views (`index.html`, `researcher.html`, and
`review_spoken.html`) can be switched between English and Japanese from the
top-right `English / 日本語` toggle (synced via `localStorage` under
`lex30_interface_language`, with automatic browser-locale detection and URL
overrides `?lang=ja|en` and `?langLock=1`). Display localization never alters
frozen JSON configs or exported CSV/JSON column names and option values. In
both languages, the association task explicitly
instructs participants to enter English words only. On completion, the browser
automatically starts CSV and JSON downloads; the result screen keeps manual
download buttons as a fallback if the browser blocks one of the downloads.

During a test session, the browser also writes a local JSON autosave after each
item, audio-play event, and answer edit. This is stored only in that browser's
`localStorage`; it is not uploaded to a server. Participants can download a
current backup during the test, and a saved backup remains available on the
participant start screen if they reopen the same version URL on the same device.
Saved backups include a 14-day retention timestamp. On shared devices, use
`Clear Saved Backup` on the result screen or participant start screen after
confirming that CSV and JSON files were collected; the clear action requires the
matching Participant ID.

If only a browser JSON backup is available, recover scoring-compatible CSV rows
with:

```bash
python3 tools/recover_browser_backup.py path/to/backup.json \
  --output-csv results/raw_exports/recovered_PARTICIPANT.csv
```

The recovery tool writes completed items to the recovered CSV. If the backup
contains a currently open unfinished item, that row is written separately as
`recovered_draft_review.csv` and should be treated as researcher-review data, not
as a primary scored response row.

## Spoken Mode Archive And Offline Transcription

In `v0.5` spoken modes, the browser records raw 16 kHz mono 16-bit PCM WAV files
with `echoCancellation`, `noiseSuppression`, and `autoGainControl` disabled to
avoid clipping word-initial consonants, autosaves item WAV blobs to `IndexedDB`,
and downloads a single `.zip` bundle (`results.csv`, `results.json` with
`lex30-browser-results-v4`, and `audio/*.wav`). Convert spoken `.zip` bundles or
extracted folders into ASR-transcribed + acoustic voice-onset CSVs before scoring:

```bash
python3 tools/transcribe_spoken_lex30.py results/spoken_zips \
  --output-dir results/raw_exports/transcribed
```

The CLI computes deterministic 2 ms-hop energy + ZCR voice-onset latency
(`AcousticRT1(ms)`), masks cue-playback bleed on listening items, extracts
up to four words when `faster-whisper` or `openai-whisper` is installed (or runs
with `--acoustic-only` using stdlib `wave` only), strips English/Japanese
hesitations, flags homophone-ambiguous forms (`knight:night`), and writes
`spoken_transcription_review.csv`. Open `review_spoken.html` (also linked from
`researcher.html`) and drop the participant `.zip` bundles plus optional
`spoken_transcription_review.csv` to inspect waveforms, cue-bleed masks, and
`AcousticRT1(ms)` markers locally in the browser (`Alt+Space` to replay,
one-click homophone chips, `Ctrl/Cmd+Enter` to accept and advance), then export
the updated `spoken_transcription_review.csv` and apply corrections with
`--apply-review-csv path/to/spoken_transcription_review.csv`.

## Score Existing CSV Exports

The browser app downloads raw CSV files with four answer columns per stimulus.
Use `tools/score_lex30.py` to convert those raw exports into scored CSV/JSON.

```bash
python3 tools/score_lex30.py lex30_results_PARTICIPANT.csv
```

For a pilot batch, put browser-downloaded CSV files under:

```text
results/raw_exports/
```

Then run the full no-GPT analysis pipeline. `researcher.html` shows this command
for the selected version, including the appropriate `--experiment-id`:

```bash
python3 tools/run_pilot_analysis.py results/raw_exports \
  --experiment-id updated-listening-easycue-posbalanced-followup-pilot-v0.4
```

By default, the pipeline stops if raw CSV metadata or stimulus words do not
match the selected `--experiment-id` (15-cue `form_a` / `form_b` split-half runs
are auto-detected from `StimulusSubset` or can be locked explicitly with
`--stimulus-subset form_a|form_b`). Use `--allow-mixed-experiments` only for
diagnostic runs with legacy/sample files. If you intentionally reuse an existing
`--output-dir`, pass `--force` only after preserving any human-entered workbook
decision notes.

It writes a timestamped folder under `results/analysis/` with:

- `pilot_scored.csv`: one row per scored response token.
- `pilot_summary.csv`: participant-level NJ8/BNC-COCA/NGSL scores.
- `pilot_review.csv`: off-list and list-disagreement items for human review.
- `item_summary.csv`: stimulus-level response, timing, and audio-play QC.
- `participant_qc.csv`: participant/session-level completeness and audio QC.
- `score_diagnostics.csv`: score-distribution floor/ceiling and sparse-response
  diagnostics for complete sessions.
- `multiword_sensitivity.csv`: all-token vs first-token-per-slot scoring
  sensitivity for participants with multiword answer slots.
- `multifaceted_summary.csv`: secondary 6-dimension productive vocabulary
  profile (frequency sophistication including polytomous type/clang-filtered/EB-smoothed
  indices, retrieval fluency/time-cutoff sensitivity, phonological/clang &
  homophone bounds, lexical network diversity/chaining, psycholinguistic
  depth/derivational richness, and v0.4 receptive–productive bottleneck
  diagnostics). See `python3 tools/simulate_lex30_scoring.py` for the 4-scenario
  Japanese EFL psychometric simulation benchmark comparing binary vs. secondary
  indices.
- `external_criteria_linked.csv`, if `--external-criteria` is supplied:
  participant/session summaries linked to the supplied external criterion CSV.
- `external_criteria_correlations.csv`, if `--external-criteria` is supplied:
  descriptive Pearson correlations between Lex30 score fields and numeric
  external criterion fields.
- `cue_score_matrix.csv`: session-by-cue token-score matrix for pilot item and
  reliability diagnostics.
- `psychometrics_summary.csv`: descriptive pilot reliability/distribution
  diagnostics, including Cronbach alpha, split-half reliability, bootstrap CIs,
  and lowest item-total/item-rest summaries; not validation evidence by itself.
- `item_diagnostics.csv`: cue-level item score, item-total correlation,
  item-rest correlation, and bootstrap item-score diagnostics for pilot
  item-retention review.
- `pilot_report.md`: research-facing QC and scoring report with participant
  exclusion candidates, stimulus recheck candidates, review-token summaries, and
  recommended next decisions.
- `pilot_workbook.xlsx`: multi-sheet Excel workbook bundling a first-view
  `Decision_Summary`, `Data_Dictionary`, the report, participant QC, review
  items, score diagnostics, multiword sensitivity, item summary, psychometrics,
  item diagnostics, cue score matrix, participant summary, scored tokens, and
  analysis manifest.
  The QC sheets add status and action-hint columns to support human review; they
  are not automatic exclusion decisions. Blue Excel columns are optional
  researcher decision notes and do not alter the machine-generated CSV outputs.
- `analysis_manifest.json`: input/output paths, input hashes, freeze-check
  status, script/data hashes, Python version, and key package versions.

To link an external vocabulary/proficiency criterion, prepare a CSV with a join
key such as `participant_id`, `Participant`, `participant_session_id`, or
`analysis_session_key`. See:

```text
examples/external_criteria_template.csv
```

Then run:

```bash
python3 tools/run_pilot_analysis.py results/raw_exports \
  --experiment-id updated-listening-easycue-posbalanced-followup-pilot-v0.4 \
  --external-criteria path/to/external_criteria.csv
```

External-criteria outputs are descriptive criterion/convergent diagnostics only.
They do not alter primary deterministic scoring.

For reviewer calibration and listening-audio QC, use:

```text
docs/reviewer_calibration_protocol.md
docs/audio_perceptual_qc_checklist.md
examples/reviewer_calibration_decisions_template.csv
examples/audio_perceptual_qc_template.csv
```

To use manual spelling overrides without GPT:

```bash
python3 tools/run_pilot_analysis.py results/raw_exports \
  --manual-overrides examples/manual_overrides.csv
```

GPT annotation remains optional and should be treated only as review metadata:

```bash
python3 tools/run_pilot_analysis.py results/raw_exports --with-gpt
```

The scorer writes:

- `*_scored.csv`: one row per response token, including NJ8 and BNC/COCA ranks.
- `*_summary.csv`: participant-level scores for quick checking or spreadsheet use.
- `*_review.csv`: aggregated items for human review, including off-list forms and
  NJ8/BNC-COCA disagreements.
- `*_scored.json`: metadata, participant summary, review items, and detailed
  scored rows.

To score a folder of raw exports in one batch:

```bash
python3 tools/score_lex30.py path/to/raw_results_folder
```

Generated files such as `*_scored.csv`, `*_summary.csv`, `*_review.csv`, and
`manual_overrides.csv` are skipped when a folder is used as input.

By default it uses:

- New JACET 8000 from `tools/data/NJ8/NJ8.csv`.
- Nation's BNC/COCA word-family spreadsheet from
  `tools/data/bnc_coca/BNC_COCA_lists.xlsx`.
- NGSL 1.2 from `tools/data/ngsl/`.
- AntBNC fallback normalization from
  `tools/data/antbnc/antbnc_lemmas_ver_004.txt`.
- Brysbaert et al. (2014) concreteness norms from
  `tools/data/Brysbaert et al. (2014)/`.
- SUBTLEX-US from `tools/data/SUBTLEXus/`.
- `wordfreq` Zipf frequency as a Python-package frequency/familiarity proxy.
- NLTK WordNet as a POS-review proxy for stimulus selection.

Primary rule scoring is deterministic:

```text
K1 = 0
K2+ = 1
off-list = review
stimulus repetition = 0
```

Spelling is not automatically corrected. A misspelled response is scored exactly
as typed; if it does not match NJ8 or BNC/COCA after normalization, it remains a
review item. This keeps API cost at zero and avoids silently changing learner
responses. The `*_review.csv` file gives a compact list of forms to inspect
before deciding whether any manual override is justified.

The CLI reports both token and type scores for NJ8 and BNC/COCA. Type scores
count the first occurrence of a normalized response for a participant; repeated
responses remain visible in the detailed rows but do not add type-score points.
NGSL ranks and scores are also reported as an auxiliary open-list comparison,
not as the primary Lex30 scoring rule.
Summaries are keyed by `analysis_session_key` so retakes or recovered sessions
from the same participant ID are not silently merged.
Concreteness, SUBTLEX-US, `wordfreq`, and WordNet POS fields do not alter primary
binary `K1=0, K2+=1` scores; they are reported separately in secondary
multifaceted profile columns (`*_summary.csv`, `multifaceted_summary.csv`, and
the workbook `Multifaceted` sheet) as well as stimulus-profile outputs.

At this stage, every lexical token inside an answer slot is tokenized and scored.
The outputs therefore include `multiword_response_slots` and
`extra_tokens_in_response_slots` so researchers can inspect possible score
inflation before deciding a final policy. The full analysis pipeline also writes
`multiword_sensitivity.csv` and a workbook `Sensitivity` sheet comparing the
current all-token rule with a first-token-per-slot rule. Percent columns are
explicit about their denominators: `*_percent_of_lexical_tokens` uses produced
lexical tokens, whereas `*_percent_of_response_slots` uses answer slots.

List coverage is reported separately. A response may be `nj8_only`,
`bnc_coca_only`, `both_in_list`, or `both_off_list_review`. This is intentional:
NJ8 is useful for the Japanese EFL context, while Nation's BNC/COCA word-family
list connects the results to a broader vocabulary-assessment literature.

If a researcher wants to correct obvious spelling errors after review, use an
optional manual override CSV:

```bash
python3 tools/score_lex30.py examples/sample_results.csv \
  --manual-overrides examples/manual_overrides.csv
```

Override format:

```csv
token,corrected_form,note
carbohydrat,carbohydrate,clear spelling error
```

An optional `stimulus` column can scope an override to one cue word. Without this
file, no spelling correction is applied. When overrides are used, the detailed
CSV records both the original response and the lookup form, so the learner's
typed answer remains recoverable.

## Optional GPT Annotation

GPT can be used as an annotation and review aid, not as the primary scorer:

```bash
python3 tools/score_lex30.py lex30_results_PARTICIPANT.csv --with-gpt
```

The script reads `OPENAI_API_KEY` from `.env` in the repository root (falling
back to `~/Desktop/.env` if present) or environment variables. GPT annotations classify response validity and cue-response relation
type, using categories such as `lexical_set`, `collocation`, `form_based`, and
`erratic`. These annotations are written separately from the rule scores.

## Profile Stimulus Sets

Use `tools/profile_stimuli.py` to inspect a stimulus set against NJ8, BNC/COCA,
NGSL, psycholinguistic norms, and WordNet POS:

```bash
python3 tools/profile_stimuli.py configs/lex30-original-written-v1.json
```

The script writes `*_profile.csv` and `*_profile.json` next to the config. For
the current baseline, 28 of the 30 cues appear in all three bundled lists; the
two NGSL off-list cues are still retained because this file profiles, not
revises, the original Lex30.

To build a broad candidate pool for an Updated Lex30 pilot:

```bash
python3 tools/build_stimulus_candidates.py
```

This writes `tools/generated/stimulus_candidates.csv`, with NJ8, BNC/COCA, and
NGSL ranks, Brysbaert concreteness, SUBTLEX-US frequency/contextual diversity,
`wordfreq` Zipf frequency, WordNet primary/possible POS fields, and conservative
exclusion flags. The output is a review pool, not an automatically validated
final stimulus set.

To regenerate the original v0.1 draft Updated Lex30 written/listening configs
from that candidate pool:

```bash
python3 tools/generate_pilot_configs.py
python3 tools/profile_stimuli.py configs/updated-written-pilot-v0.1.json
python3 tools/profile_stimuli.py configs/updated-listening-pilot-v0.1.json
```

The generated v0.1 pilot set matches the original Lex30 NJ8 response-cue band profile
(`K1=16`, `K2=8`, `K3=4`, `K4=2`), excludes the original Lex30 cues, excludes
clear function-word and pronunciation-risk items, and keeps all 30 cues inside
NJ8, BNC/COCA, and NGSL. Psycholinguistic variables are used conservatively:
low familiarity, low known-rate, and missing concreteness are lightly penalized
in automatic draft selection, while abstract/concrete extremes are retained as
review flags rather than hard exclusions.

To regenerate the easier v0.2 drafts, where every stimulus cue is NJ8 K1
(`nj8_rank <= 1000`):

```bash
python3 tools/generate_pilot_configs.py --easy-cue
python3 tools/profile_stimuli.py configs/updated-written-easycue-pilot-v0.2.json
python3 tools/profile_stimuli.py configs/updated-listening-easycue-pilot-v0.2.json
```

The v0.2 `easycue` set is better aligned with the idea that Lex30 stimulus cues
should be easy and familiar, while difficulty should be reflected in the
participant's responses.

To regenerate the POS-balanced v0.3 drafts, where cues are still easy
(`NJ8 K1`, `nj8_rank <= 1000`) but WordNet primary-POS counts match the original
Lex30 baseline:

```bash
python3 tools/generate_pilot_configs.py --pos-balanced-easy-cue
python3 tools/profile_stimuli.py configs/updated-written-easycue-posbalanced-pilot-v0.3.json
python3 tools/profile_stimuli.py configs/updated-listening-easycue-posbalanced-pilot-v0.3.json
```

WordNet POS should be treated as a stimulus-review proxy rather than a
context-sensitive POS tag. It is useful for checking whether the stimulus set is
overly noun-heavy, but final cue approval still requires researcher review.

MRC familiarity/imageability norms are not currently part of the pipeline,
because the public MRC access point is unavailable. Familiarity is therefore
approximated with SUBTLEX-US contextual diversity and `wordfreq` Zipf frequency.

## Audio Stimuli

The current v0.4 listening follow-up form reuses the approved v0.3 audio files
under:

```text
audio/updated-listening-easycue-posbalanced-pilot-v0.3/
```

The expected filenames are deterministic, such as `01-center.mp3`. Preview the
audio-generation plan without calling the API:

```bash
python3 tools/generate_audio_stimuli.py
```

To actually call ElevenLabs and write the files, use `--execute`:

```bash
python3 tools/generate_audio_stimuli.py --execute
```

The script reads `ELEVENLABS_API_KEY`, voice IDs, model ID, and output format
from `/Users/tohokusla/Desktop/.env` by default. It is dry-run by default to
avoid accidental API cost.
