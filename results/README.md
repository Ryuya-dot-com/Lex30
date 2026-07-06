# Lex30 Results Workspace

Use this folder for local pilot data and analysis outputs.

```text
results/raw_exports/
```

Place browser-downloaded participant CSV files there. Keep the JSON downloads as
raw archives too if you collect them, but the scoring pipeline reads the CSV
files.

Run the default v0.4 pilot analysis with:

```bash
python3 tools/run_pilot_analysis.py
```

Outputs are written under:

```text
results/analysis/YYYYMMDD-HHMMSS/
```

The pipeline writes a multi-sheet Excel workbook (`pilot_workbook.xlsx`) with a
first-view `Decision_Summary`, a `Data_Dictionary`, scored token rows,
participant summaries, human-review items, item-level timing/audio QC,
participant-level QC, score-distribution floor/ceiling and sparse-response
diagnostics, optional external-criteria linkage/correlation diagnostics,
cue-level score matrices, descriptive psychometric diagnostics, item-total and
item-rest diagnostics, a Markdown report, and an analysis manifest with input hashes,
script/data hashes, and runtime metadata.
Blue columns in workbook QC sheets are optional researcher decision notes.
