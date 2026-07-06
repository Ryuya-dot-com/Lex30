# Lex30 Audio Perceptual QC Checklist

Status: checklist for listening-pilot audio review.

Use this checklist before a larger listening batch and whenever `Item_Summary`
or participant notes suggest cue-level audio problems. Browser preflight confirms
that files exist and can be loaded; this checklist confirms that the audio is
perceptually suitable for the intended listeners.

## Review Setup

- Use the same file version named in the frozen experiment config.
- Review through the same hosting mode and browser used for administration when
  possible.
- Use the target classroom or lab audio setup, or a comparable headset.
- Set volume to a normal participant level before reviewing.
- Record decisions in:

  ```text
  examples/audio_perceptual_qc_template.csv
  ```

## Per-Cue Checks

For each cue, record:

- cue word and audio file path
- reviewer ID and review date
- device, browser, and headphone/speaker setup
- pass/fail for file loading
- pass/fail for intelligibility
- pass/fail for target pronunciation
- pass/fail for clipping/noise
- whether stress, vowel quality, or consonants could bias responses
- whether the cue should be retained, rerecorded, or replaced

Use `review_decision` values:

```text
retain
rerecord
replace
drop
uncertain
```

## Minimum Pass Rule

Do not administer a formal listening batch if any cue has:

- missing or failed audio,
- unclear onset,
- severe clipping or background noise,
- pronunciation that makes the intended word ambiguous,
- mismatch between config stimulus text and spoken cue,
- or reviewer uncertainty that has not been resolved.

## Link To Analysis

After collecting pilot data, compare audio QC notes with:

- `Item_Summary`
- `Participant_QC`
- `Score_Diagnostics`
- `Item_Diagnostics`
- administration deviation notes

If a cue has weak response productivity or unusual timing, check whether the
audio QC record provides a plausible explanation before making an item-retention
decision.
