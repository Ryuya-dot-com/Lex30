# Analysis Outputs

`tools/run_pilot_analysis.py` writes timestamped analysis folders here. Each
folder includes `pilot_workbook.xlsx`, a multi-sheet Excel workbook bundling a
first-view `Decision_Summary`, a `Data_Dictionary`, the main report, participant
QC, review items, item summary, psychometrics, item diagnostics, cue score
matrix, participant summary, scored token rows, and analysis manifest.

These generated folders can be removed and regenerated from the raw CSV exports
and the current scoring scripts.

Each analysis folder includes `score_diagnostics.csv` and a matching
`Score_Diagnostics` workbook sheet for floor/ceiling concentration,
sparse-response concentration, and token/type score-distribution review.
When `--external-criteria` is supplied, the folder also includes
`external_criteria_linked.csv`, `external_criteria_correlations.csv`, and
matching workbook sheets for descriptive criterion/convergent diagnostics.

Do not rerun analysis into a folder where researchers have entered workbook
decisions unless those decisions have been preserved. The analysis command
requires `--force` before writing into a non-empty explicit `--output-dir`.
