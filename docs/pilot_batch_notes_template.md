# Lex30 Pilot Batch Notes Template

Use one copy of this file per pilot batch. Store completed notes with the
protected study materials, not in public GitHub Pages content.

## Batch Identity

- Batch ID:
- Collection date(s):
- Location:
- Lead researcher:
- Administrator(s):
- Reviewer(s):
- Experiment ID: `updated-listening-easycue-posbalanced-followup-pilot-v0.4`
- Analysis output folder:

## Design Confirmation

- Data-collection design file:
  `docs/pilot_data_collection_design.md`
- Intended use:
- Target population:
- Participant group labels:
- Target complete sessions:
- External criterion collected: yes / no
- External criterion source, if any:
- Follow-up recognition/semantic probes collected: yes / no
- Written/listening comparison planned: yes / no
- GPT metadata used: no by default / yes with rationale

## Administration Setup

- Hosting mode:
- Researcher URL:
- Participant URL:
- Device type:
- Browser and version:
- Audio setup:
- Headphone/speaker check completed:
- Perceptual audio QC file:
  `examples/audio_perceptual_qc_template.csv`
- Perceptual audio QC completed:
- Researcher preflight passed:
- Command-line freeze verification passed:
- Participant instructions used verbatim:

Freeze verification command:

```bash
python3 tools/freeze_experiment.py updated-listening-easycue-posbalanced-followup-pilot-v0.4 --verify
```

## Participant Tracking

Use anonymous IDs only.

| Participant ID | Session ID | CSV Collected | JSON Archived | Backup Cleared | Notes |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Deviations

Record every nonstandard event, even if the session is still included.

| Time | Participant ID | Deviation Type | Description | Immediate Action | Primary Analysis Decision |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

Deviation types:

- audio problem,
- browser refresh or closure,
- participant interruption,
- wrong version opened,
- missing CSV or JSON,
- duplicate participant/session ID,
- nonstandard instruction,
- shared-device recovery used,
- backup not cleared,
- other.

## Analysis Notes

- Analysis command:

  ```bash
  python3 tools/run_pilot_analysis.py results/raw_exports \
    --experiment-id updated-listening-easycue-posbalanced-followup-pilot-v0.4
  ```

- External criterion analysis command, if used:

  ```bash
  python3 tools/run_pilot_analysis.py results/raw_exports \
    --experiment-id updated-listening-easycue-posbalanced-followup-pilot-v0.4 \
    --external-criteria path/to/external_criteria.csv
  ```

- Manual override CSV used:
- GPT metadata used:
- `Decision_Summary` reviewed:
- `Participant_QC` decisions preserved:
- `Score_Diagnostics` reviewed:
- `Sensitivity` reviewed:
- `Review_Items` decisions preserved:
- `Item_Summary` decisions preserved:
- Follow-up completion and probe columns reviewed:
- External criterion merge/correlation performed:
- Reviewer calibration file, if used:
  `examples/reviewer_calibration_decisions_template.csv`
- Reviewer calibration decision:

## Batch Decision Summary

| Date | Decision | Rationale | Decided By | Evidence/File |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
