#!/usr/bin/env python3
"""Run a full Lex30 pilot-analysis pass from raw browser CSV exports."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import random
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from importlib import metadata as importlib_metadata
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOLS_ROOT = PROJECT_ROOT / "tools"
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

import freeze_experiment  # noqa: E402
import score_lex30  # noqa: E402


DEFAULT_RAW_DIR = PROJECT_ROOT / "results" / "raw_exports"
DEFAULT_ANALYSIS_ROOT = PROJECT_ROOT / "results" / "analysis"
DEFAULT_EXPERIMENT_ID = "updated-listening-easycue-posbalanced-followup-pilot-v0.4"
SCORE_FIELDS = ["nj8_token_score", "bnc_coca_token_score", "ngsl_token_score"]
BOOTSTRAP_ITERATIONS = 500
RANDOM_SPLIT_ITERATIONS = 500
BOOTSTRAP_SEED = 20260706
FLOOR_PERCENT_OF_RESPONSE_SLOTS = 10.0
CEILING_PERCENT_OF_RESPONSE_SLOTS = 90.0
SCORE_CONCENTRATION_REVIEW_PERCENT = 25.0
LOW_FILLED_SLOT_PERCENT = 50.0
LOW_FILLED_SLOT_REVIEW_PERCENT = 10.0
MIN_SCORE_DISTRIBUTION_SESSIONS = 10
WORD_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*")
ANSWER_RE = re.compile(r"^Answer(\d+)$")
REVIEW_EXTRA_FIELDS = ["review_priority_rank", "review_priority", "review_action_hint"]
SCORE_DIAGNOSTIC_FIELDS = [
    ("nj8_token_score", "NJ8 token score"),
    ("nj8_type_score", "NJ8 type score"),
    ("bnc_coca_token_score", "BNC/COCA token score"),
    ("bnc_coca_type_score", "BNC/COCA type score"),
    ("ngsl_token_score", "NGSL token score"),
    ("ngsl_type_score", "NGSL type score"),
]
EXTERNAL_SCORE_FIELDS = SCORE_DIAGNOSTIC_FIELDS
EXTERNAL_JOIN_KEY_ALIASES = [
    (
        "analysis_session_key",
        ["analysis_session_key", "AnalysisSessionKey", "analysis session key"],
    ),
    (
        "participant_session_id",
        ["participant_session_id", "ParticipantSessionId", "session_id", "SessionID", "session id"],
    ),
    (
        "participant_id",
        ["participant_id", "Participant", "ParticipantID", "participant", "participant id"],
    ),
]
MANUAL_DECISION_COLUMNS = {
    "Participant_QC": [
        "researcher_include",
        "researcher_decision",
        "decision_note",
        "decision_by",
        "decision_at",
    ],
    "Review_Items": [
        "final_action",
        "final_corrected_form",
        "count_in_final_score",
        "decision_note",
        "decision_by",
        "decision_at",
    ],
    "Item_Summary": [
        "item_decision",
        "stimulus_revision_note",
        "decision_by",
        "decision_at",
    ],
}
MANUAL_DECISION_VALIDATIONS = {
    "researcher_include": ["include", "exclude", "uncertain"],
    "researcher_decision": [
        "include_complete_case",
        "exclude_from_primary",
        "include_sensitivity_only",
        "needs_followup",
    ],
    "final_action": [
        "accept_as_typed",
        "correct_spelling",
        "exclude_invalid",
        "proper_noun",
        "uncertain",
    ],
    "count_in_final_score": ["yes", "no", "uncertain"],
    "item_decision": ["retain", "revise", "replace", "drop", "uncertain"],
}
EXCEL_NUMERIC_FIELDS = {
    "answer_slots",
    "auto_advanced_items",
    "auto_advanced_percent",
    "bnc_coca_band",
    "bnc_coca_rank",
    "bnc_coca_score_token",
    "bnc_coca_score_type",
    "bnc_coca_token_percent",
    "bnc_coca_token_percent_of_lexical_tokens",
    "bnc_coca_token_percent_of_response_slots",
    "bnc_coca_token_score",
    "bnc_coca_type_score",
    "both_off_list_review_tokens",
    "completion_percent",
    "complete_sessions_used",
    "criterion_mean",
    "cronbach_alpha_complete_sessions",
    "bootstrap_iterations",
    "random_split_iterations",
    "duplicate_stimulus_rows",
    "duplicate_token_count_so_far",
    "elapsedSinceTestStartMs",
    "extra_tokens_in_response_slots",
    "extra_tokens_in_slot",
    "filled_slot_percent",
    "filled_slots",
    "floor_band_percent",
    "floor_band_sessions",
    "floor_threshold_percent_of_response_slots",
    "followup_completed_items",
    "followup_completion_percent",
    "linked_external_rows",
    "matched_summary_rows",
    "items_missing_audio_play_log",
    "items_with_no_audio_play",
    "japanese_meaning_items",
    "lexical_tokens",
    "list_disagreement_tokens",
    "max_total_score",
    "max_percent_of_response_slots",
    "max_item_score",
    "max_score",
    "mean_extra_tokens_in_response_slots",
    "mean_filled_slot_percent",
    "mean_heard_confidence",
    "mean_item_score",
    "mean_item_score_ci95_high",
    "mean_item_score_ci95_low",
    "mean_lexical_tokens_observed",
    "mean_lexical_tokens",
    "mean_meaning_confidence",
    "mean_multiword_response_slots_observed",
    "mean_multiword_response_slots",
    "mean_no_response_slots",
    "mean_percent_of_response_slots",
    "median_percent_of_response_slots",
    "median_score",
    "mean_both_off_list_review_tokens_observed",
    "mean_audio_play_count",
    "mean_lexical_tokens_per_item",
    "mean_reaction_time_ms",
    "mean_response_confidence",
    "mean_score",
    "mean_total_score",
    "mean_total_score_ci95_high",
    "mean_total_score_ci95_low",
    "median_reaction_time_ms",
    "min_item_rest_correlation",
    "min_item_total_correlation",
    "min_percent_of_response_slots",
    "min_item_score",
    "min_score",
    "min_total_score",
    "multiword_response_slots",
    "multiword_session_percent",
    "multiword_sessions",
    "multiword_slot_percent",
    "first_token_bnc_coca_token_score",
    "first_token_bnc_coca_type_score",
    "first_token_extra_tokens_excluded",
    "first_token_lexical_tokens",
    "first_token_list_disagreement_tokens",
    "first_token_ngsl_token_score",
    "first_token_ngsl_type_score",
    "first_token_nj8_token_score",
    "first_token_nj8_type_score",
    "first_token_review_tokens",
    "first_token_score_delta_bnc_coca_token",
    "first_token_score_delta_bnc_coca_type",
    "first_token_score_delta_ngsl_token",
    "first_token_score_delta_ngsl_type",
    "first_token_score_delta_nj8_token",
    "first_token_score_delta_nj8_type",
    "ngsl_band",
    "ngsl_off_list_tokens",
    "ngsl_rank",
    "ngsl_score_token",
    "ngsl_score_type",
    "ngsl_token_percent",
    "ngsl_token_percent_of_lexical_tokens",
    "ngsl_token_percent_of_response_slots",
    "ngsl_token_score",
    "ngsl_type_score",
    "nj8_band",
    "nj8_rank",
    "nj8_score_token",
    "nj8_score_type",
    "nj8_token_percent",
    "nj8_token_percent_of_lexical_tokens",
    "nj8_token_percent_of_response_slots",
    "nj8_token_score",
    "nj8_type_score",
    "no_audio_play_percent",
    "no_response_slots",
    "occurrences",
    "participants",
    "analysis_sessions",
    "all_token_bnc_coca_token_score",
    "all_token_bnc_coca_type_score",
    "all_token_lexical_tokens",
    "all_token_list_disagreement_tokens",
    "all_token_ngsl_token_score",
    "all_token_ngsl_type_score",
    "all_token_nj8_token_score",
    "all_token_nj8_type_score",
    "all_token_review_tokens",
    "paired_n",
    "pearson_r",
    "p10_score",
    "p90_score",
    "p10_percent_of_response_slots",
    "p90_percent_of_response_slots",
    "response_order",
    "response_slots",
    "review_priority_rank",
    "rows",
    "random_split_spearman_brown_ci95_high",
    "random_split_spearman_brown_ci95_low",
    "random_split_spearman_brown_mean",
    "sd_total_score",
    "sd_item_score",
    "sessions_total",
    "sd_percent_of_response_slots",
    "sd_score",
    "slot_token_count",
    "split_half_odd_even_r",
    "split_half_odd_even_spearman_brown",
    "item_rest_correlation",
    "item_rest_correlation_ci95_high",
    "item_rest_correlation_ci95_low",
    "item_score_zero_percent",
    "item_score_positive_percent",
    "item_score_positive_percent_ci95_high",
    "item_score_positive_percent_ci95_low",
    "item_total_correlation",
    "observed_sessions",
    "bootstrap_cronbach_alpha_ci95_high",
    "bootstrap_cronbach_alpha_ci95_low",
    "bootstrap_split_half_spearman_brown_ci95_high",
    "bootstrap_split_half_spearman_brown_ci95_low",
    "stimuli",
    "stimulus_order",
    "stimulus_repetitions",
    "token_index",
    "total_audio_play_count",
    "unique_stimuli",
    "valid_in_list_tokens",
    "zero_score_percent",
    "zero_score_sessions",
    "ceiling_band_percent",
    "ceiling_band_sessions",
    "ceiling_threshold_percent_of_response_slots",
    "collocation_applicable_items",
    "collocation_correct_items",
    "collocation_correct_percent",
    "category_applicable_items",
    "category_correct_items",
    "category_correct_percent",
    "synonym_applicable_items",
    "synonym_correct_items",
    "synonym_correct_percent",
    "antonym_applicable_items",
    "antonym_correct_items",
    "antonym_correct_percent",
    "low_filled_slot_percent",
    "low_filled_slot_sessions",
}
DATA_DICTIONARY_ROWS = [
    ["Sheet", "Field or Flag", "Meaning"],
    ["Decision_Summary", "Complete-case candidates", "Participant sessions with no workbook-level QC flag."],
    ["Summary / Scored_Tokens", "analysis_session_key", "Stable source/session/participant key used to keep retakes separate."],
    ["Summary", "multiword_response_slots", "Answer slots containing more than one lexical token."],
    ["Summary", "extra_tokens_in_response_slots", "Additional lexical tokens beyond the first token in multiword answer slots."],
    ["Summary", "*_percent_of_lexical_tokens", "Token-score percentage using produced lexical tokens as the denominator."],
    ["Summary", "*_percent_of_response_slots", "Token-score percentage using response slots as the denominator; can reveal sparse or multiword responses."],
    ["Participant_QC", "qc_status", "`ok` when no automatic QC flag is present; `review` otherwise."],
    ["Participant_QC", "analysis_set_hint", "Suggested inclusion-review starting point, not an automatic exclusion decision."],
    ["Participant_QC", "primary_complete_case_candidate", "`yes` when no automatic participant-level QC flag is present."],
    ["Participant_QC", "incomplete_30_items", "The session has fewer or more than the expected 30 unique stimuli."],
    ["Participant_QC", "duplicate_stimuli", "The same stimulus appears more than once in one participant/session export."],
    ["Participant_QC", "missing_audio_play_logs", "The CSV lacks current audio-play logging columns for at least one row."],
    ["Participant_QC", "no_audio_play_item", "At least one listening item has zero recorded audio plays."],
    ["Participant_QC", "high_auto_advance", "At least 25% of items advanced by timeout."],
    ["Participant_QC", "low_filled_slot_rate", "Fewer than 50% of answer slots were filled."],
    ["Participant_QC / Item_Summary", "followup_completion_percent", "Percent of rows with completed post-association follow-up data when follow-up is enabled."],
    ["Participant_QC / Item_Summary", "mean_*_confidence", "Mean 0-100 follow-up confidence slider value for heard/meaning/response checks."],
    ["Participant_QC / Item_Summary", "*_correct_percent", "Percent correct for receptive follow-up probes with an applicable answer key."],
    ["Participant_QC / Item_Summary", "japanese_meaning_items", "Rows with a non-empty Japanese meaning response in the follow-up section."],
    ["Score_Diagnostics", "floor_band_sessions", f"Complete sessions scoring <= {FLOOR_PERCENT_OF_RESPONSE_SLOTS}% of response slots for that score field."],
    ["Score_Diagnostics", "ceiling_band_sessions", f"Complete sessions scoring >= {CEILING_PERCENT_OF_RESPONSE_SLOTS}% of response slots for that score field."],
    ["Score_Diagnostics", "low_filled_slot_sessions", f"Complete sessions with fewer than {LOW_FILLED_SLOT_PERCENT}% of answer slots filled."],
    ["Score_Diagnostics", "diagnostic_flags", "Distribution and response-density flags for pilot interpretation review."],
    ["Sensitivity", "all_token_*", "Current all-token pilot scores copied from the participant summary for comparison."],
    ["Sensitivity", "first_token_*", "Scores after keeping only the first token in each answer slot."],
    ["Sensitivity", "first_token_score_delta_*", "First-token score minus the current all-token score; negative values suggest score inflation under all-token scoring."],
    ["External_Criteria", "link_status", "Whether a participant/session summary row matched an external criterion row."],
    ["External_Criteria", "criterion_*", "External criterion columns copied from the supplied external-criteria CSV."],
    ["Criterion_Correlations", "pearson_r", "Pearson correlation between a Lex30 score field and a numeric external criterion field."],
    ["Criterion_Correlations", "paired_n", "Rows with both Lex30 score and external criterion values available for that correlation."],
    ["Review_Items", "review_priority", "`high` for both-off-list review; `medium` for NJ8/BNC-COCA disagreement."],
    ["Review_Items", "manual_review_required", "Inspect before final scoring; the form is outside both primary lists."],
    ["Review_Items", "check_list_disagreement", "Inspect because NJ8 and BNC/COCA disagree on list membership."],
    ["Review_Items", "document_manual_override", "A manual override has already been applied; retain an audit note."],
    ["Item_Summary", "stimulus_qc_status", "`review` when item-level timing, response, or audio flags are present."],
    ["Item_Summary", "inspect_before_final_form", "Review the stimulus before treating it as final-form evidence."],
    ["Psychometrics", "split_half_odd_even_spearman_brown", "Odd/even split-half reliability adjusted with the Spearman-Brown formula."],
    ["Psychometrics", "*_ci95_low / *_ci95_high", "Bootstrap or random-split 95% interval; descriptive pilot diagnostic only."],
    ["Psychometrics", "lowest_item_rest_stimulus", "Cue with the lowest item-rest correlation for that score field."],
    ["Item_Diagnostics", "item_total_correlation", "Correlation between cue score and total score; includes the item in the total."],
    ["Item_Diagnostics", "item_rest_correlation", "Correlation between cue score and total score excluding that cue."],
    ["Item_Diagnostics", "item_score_positive_percent", "Percentage of complete sessions with a positive cue score."],
    ["Manual decision columns", "decision_by / decision_at", "Optional human-entered audit trail in the Excel workbook only."],
    ["Manual decision columns", "decision_note", "Optional rationale for inclusion, exclusion, correction, or item-retention decisions."],
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_file_or_none(path: Path) -> str | None:
    return sha256_file(path) if path.exists() else None


def package_version(name: str) -> str | None:
    try:
        return importlib_metadata.version(name)
    except importlib_metadata.PackageNotFoundError:
        return None


def relative_or_absolute(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def run_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def parse_float(value: str | None) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def parse_int(value: str | None) -> int | None:
    parsed = parse_float(value)
    return None if parsed is None else int(parsed)


def parse_bool(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def percent(numerator: float, denominator: float) -> float:
    return round(100 * numerator / denominator, 2) if denominator else 0.0


def mean(values: list[float]) -> float | None:
    return round(statistics.fmean(values), 2) if values else None


def median(values: list[float]) -> float | None:
    return round(statistics.median(values), 2) if values else None


def find_answer_columns(fieldnames: list[str]) -> list[str]:
    cols = [name for name in fieldnames if ANSWER_RE.match(name or "")]
    return sorted(cols, key=lambda name: int(ANSWER_RE.match(name).group(1))) if cols else list(score_lex30.ANSWER_COLUMNS)


def collect_raw_csvs(input_path: Path) -> list[Path]:
    return score_lex30.collect_input_csvs(input_path)


def expected_item_count(experiment_id: str) -> int:
    config_path = PROJECT_ROOT / "configs" / f"{experiment_id}.json"
    if not config_path.exists():
        return 30
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 30
    stimuli = config.get("stimuli")
    return len(stimuli) if isinstance(stimuli, list) and stimuli else 30


def load_experiment_config(experiment_id: str) -> dict[str, Any]:
    config_path = PROJECT_ROOT / "configs" / f"{experiment_id}.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Experiment config not found: {config_path}")
    return json.loads(config_path.read_text(encoding="utf-8"))


def validate_raw_rows_against_config(raw_rows: list[dict[str, str]], config: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def present_values(field: str) -> set[str]:
        return {
            str(row.get(field) or "").strip()
            for row in raw_rows
            if str(row.get(field) or "").strip()
        }

    checks = [
        ("ExperimentId", str(config.get("experimentId") or "").strip()),
        ("Mode", str(config.get("mode") or "").strip()),
        ("StimulusSetId", str(config.get("stimulusSetId") or "").strip()),
    ]
    if (config.get("stimulusPresentation") or "") == "audio":
        checks.append(("AudioVersion", str(config.get("audioVersion") or "").strip()))

    for field, expected in checks:
        values = present_values(field)
        if expected and values and values != {expected}:
            errors.append(f"{field} mismatch: expected {expected}, found {', '.join(sorted(values))}")

    expected_stimuli = {str(value).strip() for value in config.get("stimuli", []) if str(value).strip()}
    observed_stimuli = present_values("Stimulus")
    unexpected_stimuli = sorted(observed_stimuli.difference(expected_stimuli))
    if unexpected_stimuli:
        errors.append(f"Unexpected stimuli for selected experiment: {', '.join(unexpected_stimuli[:20])}")

    return errors


def read_raw_rows(paths: list[Path]) -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    answer_columns: set[str] = set()
    for path in paths:
        with path.open(encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            fieldnames = list(reader.fieldnames or [])
            answer_columns.update(find_answer_columns(fieldnames))
            for row in reader:
                row["_source_file"] = path.name
                rows.append(row)
    return rows, sorted(answer_columns, key=lambda name: int(ANSWER_RE.match(name).group(1)))


def row_session_key(row: dict[str, str]) -> tuple[str, str, str]:
    participant = (row.get("Participant") or "").strip()
    session = (row.get("ParticipantSessionId") or "").strip()
    source = (row.get("_source_file") or "").strip()
    return source, session, participant


def response_tokens(row: dict[str, str], answer_columns: list[str]) -> list[str]:
    tokens: list[str] = []
    for col in answer_columns:
        tokens.extend(WORD_RE.findall(row.get(col) or ""))
    return tokens


def answer_slot_token_counts(row: dict[str, str], answer_columns: list[str]) -> list[int]:
    return [len(WORD_RE.findall(row.get(col) or "")) for col in answer_columns]


def multiword_slot_count(rows: list[dict[str, str]], answer_columns: list[str]) -> int:
    return sum(1 for row in rows for count in answer_slot_token_counts(row, answer_columns) if count > 1)


def extra_tokens_in_slots(rows: list[dict[str, str]], answer_columns: list[str]) -> int:
    return sum(max(0, count - 1) for row in rows for count in answer_slot_token_counts(row, answer_columns))


def filled_slots(row: dict[str, str], answer_columns: list[str]) -> int:
    return sum(1 for col in answer_columns if (row.get(col) or "").strip())


def numeric_field_values(rows: list[dict[str, str]], field: str) -> list[float]:
    return [
        parsed
        for parsed in (parse_float(row.get(field)) for row in rows)
        if parsed is not None
    ]


def nonempty_field_count(rows: list[dict[str, str]], field: str) -> int:
    return sum(1 for row in rows if (row.get(field) or "").strip())


def followup_enabled(rows: list[dict[str, str]]) -> bool:
    return any(parse_bool(row.get("FollowUpEnabled")) for row in rows)


def followup_completed_count(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if parse_bool(row.get("FollowUpCompleted")))


def probe_summary(rows: list[dict[str, str]], prefix: str) -> dict[str, Any]:
    answer_field = f"{prefix}Answer"
    correct_field = f"{prefix}Correct"
    applicable = sum(1 for row in rows if (row.get(answer_field) or "").strip())
    correct = sum(1 for row in rows if parse_bool(row.get(correct_field)))
    key = prefix.lower()
    return {
        f"{key}_applicable_items": applicable,
        f"{key}_correct_items": correct,
        f"{key}_correct_percent": percent(correct, applicable) if applicable else "",
    }


def followup_metrics(rows: list[dict[str, str]]) -> dict[str, Any]:
    enabled = followup_enabled(rows)
    completed = followup_completed_count(rows)
    metrics: dict[str, Any] = {
        "followup_completed_items": completed,
        "followup_completion_percent": percent(completed, len(rows)) if enabled else "",
        "mean_heard_confidence": mean(numeric_field_values(rows, "HeardConfidence")),
        "mean_meaning_confidence": mean(numeric_field_values(rows, "MeaningConfidence")),
        "mean_response_confidence": mean(numeric_field_values(rows, "ResponseConfidence")),
        "japanese_meaning_items": nonempty_field_count(rows, "JapaneseMeaning"),
    }
    for prefix in ("Collocation", "Category", "Synonym", "Antonym"):
        metrics.update(probe_summary(rows, prefix))
    return metrics


def field_int(row: dict[str, Any], field: str) -> int:
    value = row.get(field)
    if value is None or str(value).strip() == "":
        return 0
    return int(float(str(value)))


def field_float(row: dict[str, Any], field: str) -> float:
    value = row.get(field)
    if value is None or str(value).strip() == "":
        return 0.0
    return float(str(value))


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def joined_flags(flags: dict[str, bool]) -> str:
    return ";".join(flag for flag, active in flags.items() if active)


def participant_analysis_hint(qc_flags: str) -> str:
    flags = set(qc_flags.split(";")) if qc_flags else set()
    if {"incomplete_30_items", "duplicate_stimuli"} & flags:
        return "review_before_complete_case_analysis"
    if flags:
        return "review_before_include"
    return "complete_case_candidate"


def stimulus_review_hint(qc_flags: str) -> str:
    return "inspect_before_final_form" if qc_flags else "retain_candidate"


def review_priority(row: dict[str, str]) -> tuple[int, str, str]:
    if parse_bool(row.get("manual_override_applied")):
        return 1, "applied_override", "document_manual_override"
    if (row.get("oov_status") or "") == "both_off_list_review":
        return 1, "high", "manual_review_required"
    if parse_bool(row.get("list_disagreement")):
        return 2, "medium", "check_list_disagreement"
    return 3, "low", "document_only"


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    if not rows:
        return ["None."]
    def cell(value: Any) -> str:
        if value is None or value == "":
            return "-"
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(value) for value in row) + " |")
    return lines


def write_dict_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns: list[str] = list(fieldnames or [])
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def excel_cell_value(value: str, header: str = "") -> str | int | float:
    if value == "":
        return ""
    text = str(value)
    if header in EXCEL_NUMERIC_FIELDS:
        try:
            if re.fullmatch(r"[+-]?\d+", text):
                return int(text)
            if re.fullmatch(r"[+-]?\d+\.\d+", text):
                return float(text)
        except ValueError:
            return text
    if text[:1] in {"=", "+", "-", "@"}:
        return f"'{text}"
    return text


def add_manual_decision_columns(sheet: Any, title: str) -> None:
    from openpyxl.styles import Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.utils import get_column_letter

    columns = MANUAL_DECISION_COLUMNS.get(title)
    if not columns:
        return

    start_col = sheet.max_column + 1
    decision_fill = PatternFill("solid", fgColor="CFE2F3")
    for offset, header in enumerate(columns):
        col_idx = start_col + offset
        cell = sheet.cell(row=1, column=col_idx, value=header)
        cell.font = Font(bold=True)
        cell.fill = decision_fill
        sheet.column_dimensions[get_column_letter(col_idx)].width = 24 if header != "decision_note" else 52

        options = MANUAL_DECISION_VALIDATIONS.get(header)
        if not options:
            continue
        validation = DataValidation(
            type="list",
            formula1=f'"{",".join(options)}"',
            allow_blank=True,
        )
        validation.error = "Choose a value from the list or leave the cell blank."
        validation.errorTitle = "Invalid decision value"
        validation.prompt = "Use this optional column to record researcher decisions in the workbook."
        validation.promptTitle = "Manual decision"
        sheet.add_data_validation(validation)
        last_row = max(sheet.max_row, 1000)
        validation.add(f"{get_column_letter(col_idx)}2:{get_column_letter(col_idx)}{last_row}")


def write_csv_sheet(workbook: Any, *, title: str, path: Path) -> None:
    from openpyxl.styles import Font, PatternFill
    from openpyxl.utils import get_column_letter

    sheet = workbook.create_sheet(title)
    if not path.exists():
        sheet.append(["Missing file", str(path)])
        return

    headers: list[str] = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not headers:
                headers = row
                sheet.append(row)
                continue
            sheet.append(
                [
                    excel_cell_value(value, headers[index] if index < len(headers) else "")
                    for index, value in enumerate(row)
                ]
            )

    if sheet.max_row == 1 and sheet.max_column == 1 and sheet["A1"].value is None:
        sheet["A1"] = "No rows."
        return

    add_manual_decision_columns(sheet, title)

    header_fill = PatternFill("solid", fgColor="D9EAD3")
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        if cell.value not in {
            column
            for columns in MANUAL_DECISION_COLUMNS.values()
            for column in columns
        }:
            cell.fill = header_fill
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions

    for column_cells in sheet.columns:
        letter = get_column_letter(column_cells[0].column)
        max_len = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells[:200])
        sheet.column_dimensions[letter].width = min(max(max_len + 2, 10), 48)

    status_fills = {
        "ok": PatternFill("solid", fgColor="D9EAD3"),
        "yes": PatternFill("solid", fgColor="D9EAD3"),
        "complete_case_candidate": PatternFill("solid", fgColor="D9EAD3"),
        "retain_candidate": PatternFill("solid", fgColor="D9EAD3"),
        "review": PatternFill("solid", fgColor="FCE5CD"),
        "medium": PatternFill("solid", fgColor="FFF2CC"),
        "low": PatternFill("solid", fgColor="EADCF8"),
        "high": PatternFill("solid", fgColor="F4CCCC"),
        "applied_override": PatternFill("solid", fgColor="D9EAD3"),
        "review_before_include": PatternFill("solid", fgColor="FCE5CD"),
        "review_before_complete_case_analysis": PatternFill("solid", fgColor="F4CCCC"),
        "inspect_before_final_form": PatternFill("solid", fgColor="FCE5CD"),
        "manual_review_required": PatternFill("solid", fgColor="F4CCCC"),
        "check_list_disagreement": PatternFill("solid", fgColor="FFF2CC"),
        "document_manual_override": PatternFill("solid", fgColor="D9EAD3"),
        "document_only": PatternFill("solid", fgColor="EADCF8"),
        "collect_complete_sessions": PatternFill("solid", fgColor="F4CCCC"),
        "inspect_distribution": PatternFill("solid", fgColor="FCE5CD"),
        "document_distribution": PatternFill("solid", fgColor="D9EAD3"),
        "matched": PatternFill("solid", fgColor="D9EAD3"),
        "missing_external": PatternFill("solid", fgColor="FCE5CD"),
        "unmatched_external": PatternFill("solid", fgColor="F4CCCC"),
        "inspect_multiword_effect": PatternFill("solid", fgColor="FCE5CD"),
        "document_no_difference": PatternFill("solid", fgColor="D9EAD3"),
    }
    status_headers = {
        "qc_status",
        "analysis_set_hint",
        "primary_complete_case_candidate",
        "diagnostic_status",
        "diagnostic_action_hint",
        "sensitivity_status",
        "sensitivity_action_hint",
        "link_status",
        "stimulus_qc_status",
        "stimulus_review_hint",
        "review_priority",
        "review_action_hint",
    }
    for header_cell in sheet[1]:
        if header_cell.value not in status_headers:
            continue
        for row in sheet.iter_rows(min_row=2, min_col=header_cell.column, max_col=header_cell.column):
            cell = row[0]
            fill = status_fills.get(str(cell.value or "").strip().lower())
            if fill:
                cell.fill = fill


def write_report_sheet(workbook: Any, *, path: Path) -> None:
    from openpyxl.styles import Font

    sheet = workbook.create_sheet("Report")
    sheet["A1"] = "pilot_report.md"
    sheet["A1"].font = Font(bold=True)
    if not path.exists():
        sheet["A2"] = f"Missing file: {path}"
        return
    for row_index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=2):
        sheet.cell(row=row_index, column=1, value=line)
    sheet.column_dimensions["A"].width = 120


def write_data_dictionary_sheet(workbook: Any) -> None:
    from openpyxl.styles import Font, PatternFill
    from openpyxl.utils import get_column_letter

    sheet = workbook.create_sheet("Data_Dictionary")
    for row in DATA_DICTIONARY_ROWS:
        sheet.append(row)

    header_fill = PatternFill("solid", fgColor="D9EAD3")
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.fill = header_fill
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    for column_cells in sheet.columns:
        letter = get_column_letter(column_cells[0].column)
        max_len = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
        sheet.column_dimensions[letter].width = min(max(max_len + 2, 10), 90)


def write_decision_summary_sheet(
    workbook: Any,
    *,
    summary_rows: list[dict[str, str]],
    review_rows: list[dict[str, str]],
    item_rows: list[dict[str, str]],
    qc_rows: list[dict[str, str]],
    score_diagnostic_rows: list[dict[str, str]],
    sensitivity_rows: list[dict[str, str]],
    external_correlation_rows: list[dict[str, str]],
    external_metadata: dict[str, Any],
    freeze_errors: list[str],
    with_gpt: bool,
) -> None:
    from openpyxl.styles import Font, PatternFill

    sheet = workbook.create_sheet("Decision_Summary")
    sheet["A1"] = "Lex30 Analysis Decision Summary"
    sheet["A1"].font = Font(bold=True, size=14)
    sheet.column_dimensions["A"].width = 34
    sheet.column_dimensions["B"].width = 30
    sheet.column_dimensions["C"].width = 80

    participant_review_count = sum(1 for row in qc_rows if (row.get("qc_status") or "") != "ok")
    complete_case_candidates = sum(1 for row in qc_rows if (row.get("primary_complete_case_candidate") or "") == "yes")
    stimulus_review_count = sum(1 for row in item_rows if (row.get("stimulus_qc_status") or "") != "ok")
    high_review_count = sum(1 for row in review_rows if (row.get("review_priority") or "") == "high")
    medium_review_count = sum(1 for row in review_rows if (row.get("review_priority") or "") == "medium")
    multiword_session_count = sum(1 for row in qc_rows if field_int(row, "multiword_response_slots") > 0)
    multiword_slot_total = sum(field_int(row, "multiword_response_slots") for row in qc_rows)
    extra_token_total = sum(field_int(row, "extra_tokens_in_response_slots") for row in qc_rows)
    both_off_list_total = sum(field_int(row, "both_off_list_review_tokens") for row in summary_rows)
    list_disagreement_total = sum(field_int(row, "list_disagreement_tokens") for row in summary_rows)
    score_diagnostic_review_count = sum(1 for row in score_diagnostic_rows if (row.get("diagnostic_status") or "") != "ok")
    floor_review_count = sum(1 for row in score_diagnostic_rows if "floor_concentration" in str(row.get("diagnostic_flags", "")))
    ceiling_review_count = sum(1 for row in score_diagnostic_rows if "ceiling_concentration" in str(row.get("diagnostic_flags", "")))
    sparse_review_count = sum(1 for row in score_diagnostic_rows if "sparse_response_concentration" in str(row.get("diagnostic_flags", "")))
    sensitivity_review_count = sum(1 for row in sensitivity_rows if (row.get("sensitivity_status") or "") != "ok")
    sensitivity_extra_tokens_excluded = sum(field_int(row, "first_token_extra_tokens_excluded") for row in sensitivity_rows)
    followup_participant_count = sum(1 for row in qc_rows if str(row.get("followup_completion_percent") or "").strip())
    low_followup_completion_count = sum(
        1 for row in qc_rows
        if str(row.get("followup_completion_percent") or "").strip()
        and field_float(row, "followup_completion_percent") < 90
    )
    external_enabled = bool(external_metadata.get("enabled"))
    external_numeric_fields = external_metadata.get("numericCriterionFields") or []

    first_actions: list[str] = []
    if freeze_errors:
        first_actions.append("Resolve freeze verification errors before treating this as the frozen v0.3 form.")
    if participant_review_count:
        first_actions.append("Open Participant_QC and resolve review-marked sessions before final complete-case analysis.")
    if score_diagnostic_review_count:
        first_actions.append("Open Score_Diagnostics and inspect floor/ceiling or sparse-response flags before interpreting score distributions.")
    if sensitivity_review_count:
        first_actions.append("Open Sensitivity and inspect how first-token scoring changes participant scores.")
    if low_followup_completion_count:
        first_actions.append("Inspect follow-up completion fields before modeling cue-recognition or semantic-depth predictors.")
    if external_enabled and not external_numeric_fields:
        first_actions.append("External criteria were linked, but no numeric criterion fields were available for correlations.")
    if high_review_count:
        first_actions.append("Open Review_Items and inspect high-priority off-list or spelling-review forms.")
    if multiword_slot_total:
        first_actions.append("Review multiword answer slots before interpreting token-based scores.")
    if stimulus_review_count:
        first_actions.append("Open Item_Summary and inspect stimuli marked for final-form review.")
    if not first_actions:
        first_actions.append("No blocking workbook-level issue is flagged; proceed to manual review before reporting scores.")

    sheet_guide = [
        ["Participant_QC", "Session-level inclusion review", "Start here for complete-case decisions."],
        ["Score_Diagnostics", "Floor/ceiling and sparse-response distribution checks", "Use before interpreting score distributions."],
        ["Sensitivity", "All-token vs first-token scoring comparison", "Use before finalizing the multiword-slot scoring policy."],
    ]
    if external_enabled:
        sheet_guide.extend(
            [
                ["External_Criteria", "Linked external criterion rows", "Use to audit participant/session linkage."],
                ["Criterion_Correlations", "Criterion/convergent diagnostics", "Descriptive only; inspect missing data and QC decisions first."],
            ]
        )
    sheet_guide.extend(
        [
            ["Review_Items", "Token-level manual review", "Check high-priority rows before final scoring."],
            ["Item_Summary", "Stimulus-level timing and response QC", "Use for pilot item-retention decisions."],
            ["Psychometrics", "Pilot reliability and distribution diagnostics", "Descriptive only; not validation evidence by itself."],
            ["Item_Diagnostics", "Cue-level item-total/item-rest diagnostics", "Use for pilot item-retention review."],
            ["Cue_Score_Matrix", "Session-by-cue token-score matrix", "Use as input for item and reliability analyses."],
            ["Data_Dictionary", "Flag and manual-decision field definitions", "Use when documenting analysis decisions."],
            ["Summary", "Participant-level score summary", "Use after QC decisions are finalized."],
            ["Scored_Tokens", "Full token-level scoring table", "Use for audits and secondary analyses."],
        ]
    )

    sections: list[tuple[str, list[list[Any]]]] = [
        (
            "Batch Snapshot",
            [
                ["Participant sessions", len(qc_rows), ""],
                ["Complete-case candidates", complete_case_candidates, ""],
                ["Participant sessions needing review", participant_review_count, ""],
                ["Stimuli needing review", stimulus_review_count, ""],
                ["Review item rows", len(review_rows), ""],
                ["High-priority review rows", high_review_count, ""],
                ["Medium-priority review rows", medium_review_count, ""],
                ["Sessions with multiword answer slots", multiword_session_count, ""],
                ["Multiword answer slots", multiword_slot_total, ""],
                ["Extra tokens in multiword slots", extra_token_total, ""],
                ["Score diagnostic rows needing review", score_diagnostic_review_count, ""],
                ["Floor-concentration score fields", floor_review_count, ""],
                ["Ceiling-concentration score fields", ceiling_review_count, ""],
                ["Sparse-response score fields", sparse_review_count, ""],
                ["Sensitivity rows needing review", sensitivity_review_count, ""],
                ["Extra tokens excluded by first-token policy", sensitivity_extra_tokens_excluded, ""],
                ["Participants with follow-up rows", followup_participant_count, ""],
                ["Participants with low follow-up completion", low_followup_completion_count, ""],
                ["External criteria linked", "yes" if external_enabled else "no", external_metadata.get("path", "") if external_enabled else ""],
                ["External matched summary rows", external_metadata.get("matchedSummaryRows", 0) if external_enabled else 0, ""],
                ["External numeric criterion fields", len(external_numeric_fields), ";".join(external_numeric_fields) if external_numeric_fields else ""],
                ["Criterion correlation rows", len(external_correlation_rows), ""],
                ["Both-off-list review tokens", both_off_list_total, ""],
                ["List-disagreement tokens", list_disagreement_total, ""],
                ["Freeze verification", "OK" if not freeze_errors else "FAILED", ""],
                ["GPT annotation", "enabled" if with_gpt else "disabled", "GPT output is optional review metadata only."],
            ],
        ),
        ("Recommended First Actions", [[f"{index}.", action, ""] for index, action in enumerate(first_actions, start=1)]),
        ("Sheet Guide", sheet_guide),
    ]

    row_index = 3
    title_fill = PatternFill("solid", fgColor="D9EAD3")
    for title, rows in sections:
        sheet.cell(row=row_index, column=1, value=title).font = Font(bold=True)
        sheet.cell(row=row_index, column=1).fill = title_fill
        row_index += 1
        for row in rows:
            for column_index, value in enumerate(row, start=1):
                sheet.cell(row=row_index, column=column_index, value=value)
            row_index += 1
        row_index += 1


def write_readme_sheet(
    workbook: Any,
    *,
    input_path: Path,
    raw_csvs: list[Path],
    outputs: dict[str, Path],
    freeze_errors: list[str],
    with_gpt: bool,
    external_metadata: dict[str, Any] | None = None,
) -> None:
    from openpyxl.styles import Font, PatternFill

    sheet = workbook.active
    sheet.title = "README"
    rows = [
        ["Lex30 pilot analysis workbook", ""],
        ["Generated at", datetime.now(timezone.utc).isoformat()],
        ["Input path", relative_or_absolute(input_path)],
        ["Raw CSV files", len(raw_csvs)],
        ["Freeze verification", "OK" if not freeze_errors else "FAILED"],
        ["GPT annotation", "enabled" if with_gpt else "disabled"],
        ["Primary scoring", "Deterministic rule scores; GPT is review metadata only."],
        ["Spelling policy", "Responses are scored as typed unless manual overrides are supplied."],
        ["Manual decision columns", "Blue Excel columns are optional researcher notes; CSV outputs remain machine-generated."],
        ["", ""],
        ["Sheet", "Contents"],
        ["Decision_Summary", "First-view batch QC snapshot and recommended review order."],
        ["Data_Dictionary", "Definitions for QC flags, review priorities, and manual-decision fields."],
        ["Report", "Markdown pilot report copied into Excel."],
        ["Participant_QC", "Participant/session completeness, timing, and audio QC."],
        ["Score_Diagnostics", "Floor/ceiling and sparse-response distribution diagnostics."],
        ["Sensitivity", "All-token vs first-token multiword-slot scoring sensitivity."],
        *(
            [["External_Criteria", "Linked participant/session summaries and supplied external criteria."]]
            if "external_criteria_linked_csv" in outputs
            else []
        ),
        *(
            [["Criterion_Correlations", "Descriptive Lex30 score correlations with numeric external criteria."]]
            if "external_criteria_correlations_csv" in outputs
            else []
        ),
        ["Item_Summary", "Stimulus-level response, timing, and audio-play QC."],
        ["Psychometrics", "Descriptive pilot reliability and score-distribution diagnostics."],
        ["Cue_Score_Matrix", "Cue-level token scores by analysis session."],
        ["Summary", "Participant-level NJ8/BNC-COCA/NGSL scores."],
        ["Review_Items", "Human-review items such as off-list and list-disagreement forms."],
        ["Scored_Tokens", "Detailed token-level scored responses."],
        ["Manifest", "Input/output paths and freeze-check metadata."],
        ["", ""],
        ["Output workbook", relative_or_absolute(outputs["workbook_xlsx"])],
    ]
    for row in rows:
        sheet.append(row)

    sheet["A1"].font = Font(bold=True, size=14)
    header_fill = PatternFill("solid", fgColor="D9EAD3")
    for row in sheet.iter_rows():
        if row[0].value == "Sheet":
            for cell in row:
                cell.font = Font(bold=True)
                cell.fill = header_fill
            break
    sheet.column_dimensions["A"].width = 26
    sheet.column_dimensions["B"].width = 96


def write_analysis_workbook(
    path: Path,
    *,
    input_path: Path,
    raw_csvs: list[Path],
    outputs: dict[str, Path],
    freeze_errors: list[str],
    with_gpt: bool,
    external_metadata: dict[str, Any] | None = None,
) -> None:
    from openpyxl import Workbook

    path.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    write_readme_sheet(
        workbook,
        input_path=input_path,
        raw_csvs=raw_csvs,
        outputs=outputs,
        freeze_errors=freeze_errors,
        with_gpt=with_gpt,
    )
    summary_rows = read_dict_csv(outputs["summary_csv"])
    review_rows = read_dict_csv(outputs["review_csv"])
    item_rows = read_dict_csv(outputs["item_summary_csv"])
    qc_rows = read_dict_csv(outputs["participant_qc_csv"])
    score_diagnostic_rows = read_dict_csv(outputs["score_diagnostics_csv"])
    sensitivity_rows = read_dict_csv(outputs["multiword_sensitivity_csv"])
    external_correlation_rows = (
        read_dict_csv(outputs["external_criteria_correlations_csv"])
        if "external_criteria_correlations_csv" in outputs
        else []
    )
    write_decision_summary_sheet(
        workbook,
        summary_rows=summary_rows,
        review_rows=review_rows,
        item_rows=item_rows,
        qc_rows=qc_rows,
        score_diagnostic_rows=score_diagnostic_rows,
        sensitivity_rows=sensitivity_rows,
        external_correlation_rows=external_correlation_rows,
        external_metadata=external_metadata or {"enabled": False},
        freeze_errors=freeze_errors,
        with_gpt=with_gpt,
    )
    write_data_dictionary_sheet(workbook)
    write_report_sheet(workbook, path=outputs["report_md"])
    write_csv_sheet(workbook, title="Participant_QC", path=outputs["participant_qc_csv"])
    write_csv_sheet(workbook, title="Score_Diagnostics", path=outputs["score_diagnostics_csv"])
    write_csv_sheet(workbook, title="Sensitivity", path=outputs["multiword_sensitivity_csv"])
    if "external_criteria_linked_csv" in outputs:
        write_csv_sheet(workbook, title="External_Criteria", path=outputs["external_criteria_linked_csv"])
    if "external_criteria_correlations_csv" in outputs:
        write_csv_sheet(workbook, title="Criterion_Correlations", path=outputs["external_criteria_correlations_csv"])
    write_csv_sheet(workbook, title="Review_Items", path=outputs["review_csv"])
    write_csv_sheet(workbook, title="Item_Summary", path=outputs["item_summary_csv"])
    write_csv_sheet(workbook, title="Psychometrics", path=outputs["psychometrics_summary_csv"])
    write_csv_sheet(workbook, title="Item_Diagnostics", path=outputs["item_diagnostics_csv"])
    write_csv_sheet(workbook, title="Cue_Score_Matrix", path=outputs["cue_score_matrix_csv"])
    write_csv_sheet(workbook, title="Summary", path=outputs["summary_csv"])
    write_csv_sheet(workbook, title="Scored_Tokens", path=outputs["scored_csv"])
    write_json_sheet(workbook, title="Manifest", path=outputs["analysis_manifest_json"])
    workbook.save(path)


def write_json_sheet(workbook: Any, *, title: str, path: Path) -> None:
    sheet = workbook.create_sheet(title)
    sheet["A1"] = path.name
    if not path.exists():
        sheet["A2"] = f"Missing file: {path}"
        return
    for row_index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=2):
        sheet.cell(row=row_index, column=1, value=line)
    sheet.column_dimensions["A"].width = 120


def item_summary(raw_rows: list[dict[str, str]], answer_columns: list[str]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in raw_rows:
        grouped[(row.get("Stimulus") or "").strip()].append(row)

    rows: list[dict[str, Any]] = []
    for stimulus, item_rows in sorted(grouped.items()):
        rt_values = [
            parsed
            for parsed in (parse_float(row.get("ReactionTime(ms)")) for row in item_rows)
            if parsed is not None
        ]
        play_values = [
            parsed
            for parsed in (parse_int(row.get("AudioPlayCount")) for row in item_rows)
            if parsed is not None
        ]
        lexical_counts = [len(response_tokens(row, answer_columns)) for row in item_rows]
        answer_slots = len(item_rows) * len(answer_columns)
        filled = sum(filled_slots(row, answer_columns) for row in item_rows)
        multiword_slots = multiword_slot_count(item_rows, answer_columns)
        extra_tokens = extra_tokens_in_slots(item_rows, answer_columns)
        no_audio_play = sum(1 for row in item_rows if parse_int(row.get("AudioPlayCount")) == 0)
        auto_advanced = sum(1 for row in item_rows if parse_bool(row.get("AutoAdvanced")))
        mean_tokens = mean([float(value) for value in lexical_counts])
        mean_rt = mean(rt_values)
        median_rt = median(rt_values)
        mean_play_count = mean([float(value) for value in play_values])
        missing_audio_logs = sum(1 for row in item_rows if "AudioPlayCount" not in row)
        filled_percent = percent(filled, answer_slots)
        auto_percent = percent(auto_advanced, len(item_rows))
        followup = followup_metrics(item_rows)
        low_followup_completion = bool(
            followup_enabled(item_rows)
            and field_float(followup, "followup_completion_percent") < 90
        )
        qc_flags = joined_flags(
            {
                "low_filled_slot_rate": filled_percent < 50,
                "multiword_response_slots": multiword_slots > 0,
                "missing_audio_play_logs": missing_audio_logs > 0,
                "no_audio_play_items": no_audio_play > 0,
                "high_auto_advance": auto_percent >= 25,
                "near_timeout_mean_rt": bool(mean_rt is not None and mean_rt >= 25000),
                "low_followup_completion": low_followup_completion,
            }
        )
        rows.append(
            {
                "stimulus_qc_status": "review" if qc_flags else "ok",
                "stimulus_review_hint": stimulus_review_hint(qc_flags),
                "stimulus_qc_flags": qc_flags,
                "stimulus": stimulus,
                "rows": len(item_rows),
                "participants": len({row_session_key(row) for row in item_rows}),
                "answer_slots": answer_slots,
                "filled_slots": filled,
                "filled_slot_percent": filled_percent,
                "multiword_response_slots": multiword_slots,
                "extra_tokens_in_response_slots": extra_tokens,
                "multiword_slot_percent": percent(multiword_slots, answer_slots),
                "lexical_tokens": sum(lexical_counts),
                "mean_lexical_tokens_per_item": mean_tokens,
                "mean_reaction_time_ms": mean_rt,
                "median_reaction_time_ms": median_rt,
                "mean_audio_play_count": mean_play_count,
                "items_missing_audio_play_log": missing_audio_logs,
                "items_with_no_audio_play": no_audio_play,
                "no_audio_play_percent": percent(no_audio_play, len(item_rows)),
                "auto_advanced_items": auto_advanced,
                "auto_advanced_percent": auto_percent,
                **followup,
            }
        )
    return rows


def participant_qc(raw_rows: list[dict[str, str]], answer_columns: list[str], *, expected_items: int) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in raw_rows:
        grouped[row_session_key(row)].append(row)

    rows: list[dict[str, Any]] = []
    for (source_file, session_id, participant), participant_rows in sorted(grouped.items()):
        rt_values = [
            parsed
            for parsed in (parse_float(row.get("ReactionTime(ms)")) for row in participant_rows)
            if parsed is not None
        ]
        stimuli = [(row.get("Stimulus") or "").strip() for row in participant_rows if (row.get("Stimulus") or "").strip()]
        experiment_ids = sorted({(row.get("ExperimentId") or "").strip() for row in participant_rows if (row.get("ExperimentId") or "").strip()})
        audio_versions = sorted({(row.get("AudioVersion") or "").strip() for row in participant_rows if (row.get("AudioVersion") or "").strip()})
        answer_slots = len(participant_rows) * len(answer_columns)
        filled = sum(filled_slots(row, answer_columns) for row in participant_rows)
        multiword_slots = multiword_slot_count(participant_rows, answer_columns)
        extra_tokens = extra_tokens_in_slots(participant_rows, answer_columns)
        auto_advanced = sum(1 for row in participant_rows if parse_bool(row.get("AutoAdvanced")))
        no_audio_play = sum(1 for row in participant_rows if parse_int(row.get("AudioPlayCount")) == 0)
        completion_percent = percent(len(set(stimuli)), expected_items)
        filled_percent = percent(filled, answer_slots)
        auto_percent = percent(auto_advanced, len(participant_rows))
        no_audio_percent = percent(no_audio_play, len(participant_rows))
        followup = followup_metrics(participant_rows)
        low_followup_completion = bool(
            followup_enabled(participant_rows)
            and field_float(followup, "followup_completion_percent") < 90
        )
        flags = joined_flags(
            {
                "incomplete_30_items": len(set(stimuli)) != expected_items,
                "duplicate_stimuli": len(stimuli) != len(set(stimuli)),
                "missing_audio_play_logs": any("AudioPlayCount" not in row for row in participant_rows),
                "no_audio_play_item": any(parse_int(row.get("AudioPlayCount")) == 0 for row in participant_rows),
                "high_auto_advance": auto_percent >= 25,
                "low_filled_slot_rate": filled_percent < 50,
                "multiword_response_slots": multiword_slots > 0,
                "low_followup_completion": low_followup_completion,
            }
        )
        rows.append(
            {
                "qc_status": "review" if flags else "ok",
                "analysis_set_hint": participant_analysis_hint(flags),
                "primary_complete_case_candidate": yes_no(not flags),
                "source_file": source_file,
                "participant_session_id": session_id,
                "analysis_session_key": score_lex30.analysis_session_key(source_file, session_id, participant),
                "participant_id": participant,
                "experiment_ids": ";".join(experiment_ids),
                "audio_versions": ";".join(audio_versions),
                "rows": len(participant_rows),
                "unique_stimuli": len(set(stimuli)),
                "completion_percent": completion_percent,
                "duplicate_stimulus_rows": len(stimuli) - len(set(stimuli)),
                "answer_slots": answer_slots,
                "filled_slots": filled,
                "filled_slot_percent": filled_percent,
                "multiword_response_slots": multiword_slots,
                "extra_tokens_in_response_slots": extra_tokens,
                "multiword_slot_percent": percent(multiword_slots, answer_slots),
                "lexical_tokens": sum(len(response_tokens(row, answer_columns)) for row in participant_rows),
                "mean_reaction_time_ms": mean(rt_values),
                "median_reaction_time_ms": median(rt_values),
                "auto_advanced_items": auto_advanced,
                "auto_advanced_percent": auto_percent,
                "items_with_no_audio_play": no_audio_play,
                "no_audio_play_percent": no_audio_percent,
                "total_audio_play_count": sum(parse_int(row.get("AudioPlayCount")) or 0 for row in participant_rows),
                "started_at_min": min((row.get("StartedAt") or "" for row in participant_rows), default=""),
                "completed_at_max": max((row.get("CompletedAt") or "" for row in participant_rows), default=""),
                "qc_flags": flags,
                **followup,
            }
        )
    return rows


def read_dict_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def sample_variance(values: list[float]) -> float:
    return statistics.variance(values) if len(values) >= 2 else 0.0


def optional_float(value: Any) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def finite_number(value: float | None) -> bool:
    return value is not None and math.isfinite(value)


def rounded_or_blank(value: float | None, digits: int = 3) -> float | str:
    return round(value, digits) if finite_number(value) else ""


def pearson_correlation(x_values: list[float], y_values: list[float]) -> float | None:
    pairs = [
        (float(x), float(y))
        for x, y in zip(x_values, y_values)
        if math.isfinite(float(x)) and math.isfinite(float(y))
    ]
    if len(pairs) < 2:
        return None
    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    mean_x = statistics.fmean(xs)
    mean_y = statistics.fmean(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    x_ss = sum((x - mean_x) ** 2 for x in xs)
    y_ss = sum((y - mean_y) ** 2 for y in ys)
    if x_ss <= 0 or y_ss <= 0:
        return None
    return numerator / math.sqrt(x_ss * y_ss)


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value or "").strip().lower())


def find_field_by_alias(fieldnames: list[str], aliases: list[str]) -> str | None:
    normalized = {normalize_header(field): field for field in fieldnames}
    for alias in aliases:
        match = normalized.get(normalize_header(alias))
        if match:
            return match
    return None


def canonical_external_key(requested_key: str | None, fieldnames: list[str]) -> tuple[str, str]:
    if requested_key and requested_key != "auto":
        for canonical, aliases in EXTERNAL_JOIN_KEY_ALIASES:
            if normalize_header(requested_key) in {normalize_header(alias) for alias in aliases + [canonical]}:
                field = find_field_by_alias(fieldnames, aliases + [canonical, requested_key])
                if not field:
                    raise ValueError(f"External criteria key not found in CSV: {requested_key}")
                return canonical, field
        field = find_field_by_alias(fieldnames, [requested_key])
        if not field:
            raise ValueError(f"External criteria key not found in CSV: {requested_key}")
        return requested_key, field

    for canonical, aliases in EXTERNAL_JOIN_KEY_ALIASES:
        field = find_field_by_alias(fieldnames, aliases + [canonical])
        if field:
            return canonical, field
    raise ValueError(
        "External criteria CSV needs one join key column: "
        "analysis_session_key, participant_session_id, or participant_id/Participant."
    )


def read_external_criteria(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(f"External criteria CSV not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if not fieldnames:
        raise ValueError(f"External criteria CSV has no header row: {path}")
    return fieldnames, rows


def looks_like_identifier_field(field: str) -> bool:
    normalized = normalize_header(field)
    return any(token in normalized for token in ("id", "session", "name", "note", "comment"))


def numeric_external_fields(fieldnames: list[str], rows: list[dict[str, str]], key_field: str) -> list[str]:
    fields: list[str] = []
    for field in fieldnames:
        if field == key_field or looks_like_identifier_field(field):
            continue
        values = [optional_float(row.get(field)) for row in rows]
        if any(value is not None for value in values):
            fields.append(field)
    return fields


def criterion_column_name(field: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_]+", "_", field.strip()).strip("_").lower()
    return f"criterion_{normalized or 'value'}"


def analyze_external_criteria(
    *,
    path: Path,
    summary_rows: list[dict[str, Any]],
    requested_key: str | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    fieldnames, criteria_rows = read_external_criteria(path)
    summary_fields = list(summary_rows[0].keys()) if summary_rows else []
    summary_key, criteria_key = canonical_external_key(requested_key, fieldnames)
    if summary_key not in summary_fields:
        raise ValueError(f"Summary output does not include external criteria join key: {summary_key}")

    criteria_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in criteria_rows:
        key = str(row.get(criteria_key) or "").strip()
        if key:
            criteria_by_key[key].append(row)

    external_numeric_fields = numeric_external_fields(fieldnames, criteria_rows, criteria_key)
    linked_rows: list[dict[str, Any]] = []
    matched_external_ids: set[int] = set()
    for summary_row in summary_rows:
        key_value = str(summary_row.get(summary_key) or "").strip()
        matches = criteria_by_key.get(key_value, [])
        if not matches:
            linked_rows.append(
                {
                    "link_status": "missing_external",
                    "join_key": summary_key,
                    "join_key_value": key_value,
                    **summary_row,
                }
            )
            continue
        for criteria_row in matches:
            matched_external_ids.add(id(criteria_row))
            criterion_values = {
                criterion_column_name(field): criteria_row.get(field, "")
                for field in fieldnames
            }
            linked_rows.append(
                {
                    "link_status": "matched",
                    "join_key": summary_key,
                    "join_key_value": key_value,
                    **summary_row,
                    **criterion_values,
                }
            )

    summary_keys = {
        str(row.get(summary_key) or "").strip()
        for row in summary_rows
        if str(row.get(summary_key) or "").strip()
    }
    for criteria_row in criteria_rows:
        key_value = str(criteria_row.get(criteria_key) or "").strip()
        if key_value in summary_keys or id(criteria_row) in matched_external_ids:
            continue
        criterion_values = {
            criterion_column_name(field): criteria_row.get(field, "")
            for field in fieldnames
        }
        linked_rows.append(
            {
                "link_status": "unmatched_external",
                "join_key": summary_key,
                "join_key_value": key_value,
                **criterion_values,
            }
        )

    matched_rows = [row for row in linked_rows if row.get("link_status") == "matched"]
    correlation_rows: list[dict[str, Any]] = []
    for criterion_field in external_numeric_fields:
        criterion_column = criterion_column_name(criterion_field)
        for score_field, score_label in EXTERNAL_SCORE_FIELDS:
            pairs: list[tuple[float, float]] = []
            for row in matched_rows:
                score_value = optional_float(row.get(score_field))
                criterion_value = optional_float(row.get(criterion_column))
                if score_value is not None and criterion_value is not None:
                    pairs.append((float(score_value), float(criterion_value)))
            r_value = pearson_correlation(
                [pair[0] for pair in pairs],
                [pair[1] for pair in pairs],
            ) if len(pairs) >= 2 else None
            correlation_rows.append(
                {
                    "criterion_field": criterion_field,
                    "score_field": score_field,
                    "score_label": score_label,
                    "paired_n": len(pairs),
                    "pearson_r": rounded_or_blank(r_value),
                    "lex30_mean": mean([pair[0] for pair in pairs]),
                    "criterion_mean": mean([pair[1] for pair in pairs]),
                    "correlation_note": (
                        "Descriptive criterion/convergent diagnostic only; inspect QC decisions, missing data, and sample size before interpretation."
                    ),
                }
            )

    metadata = {
        "enabled": True,
        "path": relative_or_absolute(path),
        "sha256": sha256_file_or_none(path),
        "summaryJoinKey": summary_key,
        "criteriaJoinKey": criteria_key,
        "criteriaRows": len(criteria_rows),
        "linkedExternalRows": sum(1 for row in linked_rows if row.get("link_status") == "matched"),
        "matchedSummaryRows": len({row.get("analysis_session_key") for row in matched_rows if row.get("analysis_session_key")}),
        "numericCriterionFields": external_numeric_fields,
    }
    return linked_rows, correlation_rows, metadata


def spearman_brown(r_value: float | None) -> float | None:
    if not finite_number(r_value) or r_value <= -1:
        return None
    return (2 * r_value) / (1 + r_value)


def cronbach_alpha(matrix: list[list[float]]) -> float | None:
    if len(matrix) < 2 or not matrix or len(matrix[0]) < 2:
        return None
    item_count = len(matrix[0])
    columns = [[row[index] for row in matrix] for index in range(item_count)]
    total_scores = [sum(row) for row in matrix]
    total_variance = sample_variance(total_scores)
    if total_variance <= 0:
        return None
    item_variance_sum = sum(sample_variance(column) for column in columns)
    return round((item_count / (item_count - 1)) * (1 - item_variance_sum / total_variance), 3)


def percentile(values: list[float], q: float) -> float | None:
    clean = sorted(value for value in values if math.isfinite(value))
    if not clean:
        return None
    if len(clean) == 1:
        return clean[0]
    position = (len(clean) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return clean[int(position)]
    weight = position - lower
    return clean[lower] * (1 - weight) + clean[upper] * weight


def ci_bounds(values: list[float], digits: int = 3) -> tuple[float | str, float | str]:
    return (
        rounded_or_blank(percentile(values, 0.025), digits),
        rounded_or_blank(percentile(values, 0.975), digits),
    )


def rounded_percentile(values: list[float], q: float, digits: int = 2) -> float | str:
    return rounded_or_blank(percentile(values, q), digits)


def score_percent_of_response_slots(row: dict[str, Any], score_field: str) -> float:
    if score_field.endswith("_token_score"):
        percent_field = score_field.replace("_token_score", "_token_percent_of_response_slots")
        parsed_percent = optional_float(row.get(percent_field))
        if parsed_percent is not None:
            return float(parsed_percent)

    score = optional_float(row.get(score_field)) or 0.0
    response_slots = optional_float(row.get("response_slots")) or 0.0
    return percent(score, response_slots)


def score_diagnostic_action_hint(flags: str) -> str:
    flag_set = set(flags.split(";")) if flags else set()
    if "no_complete_sessions" in flag_set or "small_complete_sample" in flag_set:
        return "collect_complete_sessions"
    if flag_set:
        return "inspect_distribution"
    return "document_distribution"


def write_score_diagnostics(
    *,
    path: Path,
    summary_rows: list[dict[str, Any]],
    qc_rows: list[dict[str, Any]],
    expected_items: int,
) -> list[dict[str, Any]]:
    qc_by_session_key = {
        str(row.get("analysis_session_key") or ""): row
        for row in qc_rows
    }
    complete_session_keys = {
        str(row.get("analysis_session_key") or "")
        for row in qc_rows
        if field_int(row, "unique_stimuli") == expected_items
    }
    complete_summary_rows = [
        row for row in summary_rows
        if str(row.get("analysis_session_key") or "") in complete_session_keys
    ]

    rows: list[dict[str, Any]] = []
    for score_field, score_label in SCORE_DIAGNOSTIC_FIELDS:
        values = [field_float(row, score_field) for row in complete_summary_rows]
        percents = [score_percent_of_response_slots(row, score_field) for row in complete_summary_rows]
        filled_percents = [
            field_float(
                qc_by_session_key.get(str(row.get("analysis_session_key") or ""), {}),
                "filled_slot_percent",
            )
            for row in complete_summary_rows
        ]
        multiword_sessions = sum(1 for row in complete_summary_rows if field_int(row, "multiword_response_slots") > 0)
        floor_sessions = sum(1 for value in percents if value <= FLOOR_PERCENT_OF_RESPONSE_SLOTS)
        ceiling_sessions = sum(1 for value in percents if value >= CEILING_PERCENT_OF_RESPONSE_SLOTS)
        zero_sessions = sum(1 for value in values if value == 0)
        low_filled_sessions = sum(1 for value in filled_percents if value < LOW_FILLED_SLOT_PERCENT)
        floor_percent = percent(floor_sessions, len(percents))
        ceiling_percent = percent(ceiling_sessions, len(percents))
        low_filled_percent = percent(low_filled_sessions, len(filled_percents))
        flags = joined_flags(
            {
                "no_complete_sessions": not complete_summary_rows,
                "small_complete_sample": 0 < len(complete_summary_rows) < MIN_SCORE_DISTRIBUTION_SESSIONS,
                "floor_concentration": bool(complete_summary_rows and floor_percent >= SCORE_CONCENTRATION_REVIEW_PERCENT),
                "ceiling_concentration": bool(complete_summary_rows and ceiling_percent >= SCORE_CONCENTRATION_REVIEW_PERCENT),
                "sparse_response_concentration": bool(complete_summary_rows and low_filled_percent >= LOW_FILLED_SLOT_REVIEW_PERCENT),
                "multiword_response_slots": multiword_sessions > 0,
            }
        )
        rows.append(
            {
                "diagnostic_status": "review" if flags else "ok",
                "diagnostic_action_hint": score_diagnostic_action_hint(flags),
                "diagnostic_flags": flags,
                "score_field": score_field,
                "score_label": score_label,
                "analysis_scope": f"complete_{expected_items}_item_sessions",
                "sessions_total": len(summary_rows),
                "complete_sessions_used": len(complete_summary_rows),
                "floor_threshold_percent_of_response_slots": FLOOR_PERCENT_OF_RESPONSE_SLOTS,
                "ceiling_threshold_percent_of_response_slots": CEILING_PERCENT_OF_RESPONSE_SLOTS,
                "mean_score": mean(values),
                "sd_score": round(statistics.stdev(values), 2) if len(values) >= 2 else "",
                "min_score": min(values) if values else "",
                "p10_score": rounded_percentile(values, 0.10),
                "median_score": rounded_percentile(values, 0.50),
                "p90_score": rounded_percentile(values, 0.90),
                "max_score": max(values) if values else "",
                "mean_percent_of_response_slots": mean(percents),
                "sd_percent_of_response_slots": round(statistics.stdev(percents), 2) if len(percents) >= 2 else "",
                "min_percent_of_response_slots": min(percents) if percents else "",
                "p10_percent_of_response_slots": rounded_percentile(percents, 0.10),
                "median_percent_of_response_slots": rounded_percentile(percents, 0.50),
                "p90_percent_of_response_slots": rounded_percentile(percents, 0.90),
                "max_percent_of_response_slots": max(percents) if percents else "",
                "zero_score_sessions": zero_sessions,
                "zero_score_percent": percent(zero_sessions, len(values)),
                "floor_band_sessions": floor_sessions,
                "floor_band_percent": floor_percent,
                "ceiling_band_sessions": ceiling_sessions,
                "ceiling_band_percent": ceiling_percent,
                "mean_filled_slot_percent": mean(filled_percents),
                "low_filled_slot_sessions": low_filled_sessions,
                "low_filled_slot_percent": low_filled_percent,
                "multiword_sessions": multiword_sessions,
                "multiword_session_percent": percent(multiword_sessions, len(complete_summary_rows)),
                "mean_multiword_response_slots": mean([field_float(row, "multiword_response_slots") for row in complete_summary_rows]),
                "mean_extra_tokens_in_response_slots": mean([field_float(row, "extra_tokens_in_response_slots") for row in complete_summary_rows]),
                "mean_lexical_tokens": mean([field_float(row, "lexical_tokens") for row in complete_summary_rows]),
                "mean_no_response_slots": mean([field_float(row, "no_response_slots") for row in complete_summary_rows]),
                "diagnostic_note": "Descriptive pilot distribution diagnostic only; flags are prompts for review, not automatic exclusion decisions.",
            }
        )
    write_dict_csv(path, rows)
    return rows


def first_token_type_score(rows: list[dict[str, Any]], token_score_field: str) -> int:
    seen: set[str] = set()
    total = 0
    for row in rows:
        if not parse_bool(row.get("is_lexical_token")):
            continue
        normalized_head = str(row.get("normalized_head") or row.get("lookup_token") or row.get("normalized_token") or "").strip()
        if not normalized_head or normalized_head in seen:
            continue
        seen.add(normalized_head)
        total += field_int(row, token_score_field)
    return total


def sensitivity_action_hint(has_delta: bool) -> str:
    return "inspect_multiword_effect" if has_delta else "document_no_difference"


def write_multiword_sensitivity(
    *,
    path: Path,
    scored_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    scored_by_session: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored_rows:
        scored_by_session[str(row.get("analysis_session_key") or "")].append(row)

    rows: list[dict[str, Any]] = []
    for summary in summary_rows:
        session_key = str(summary.get("analysis_session_key") or "")
        token_rows = scored_by_session.get(session_key, [])
        first_token_rows = [
            row for row in token_rows
            if field_int(row, "token_index") <= 1
        ]
        first_lexical_rows = [
            row for row in first_token_rows
            if parse_bool(row.get("is_lexical_token"))
            and not parse_bool(row.get("is_stimulus_repetition"))
        ]
        first_scores = {
            "nj8_token": sum(field_int(row, "nj8_score_token") for row in first_token_rows),
            "bnc_coca_token": sum(field_int(row, "bnc_coca_score_token") for row in first_token_rows),
            "ngsl_token": sum(field_int(row, "ngsl_score_token") for row in first_token_rows),
            "nj8_type": first_token_type_score(first_token_rows, "nj8_score_token"),
            "bnc_coca_type": first_token_type_score(first_token_rows, "bnc_coca_score_token"),
            "ngsl_type": first_token_type_score(first_token_rows, "ngsl_score_token"),
        }
        all_scores = {
            "nj8_token": field_int(summary, "nj8_token_score"),
            "bnc_coca_token": field_int(summary, "bnc_coca_token_score"),
            "ngsl_token": field_int(summary, "ngsl_token_score"),
            "nj8_type": field_int(summary, "nj8_type_score"),
            "bnc_coca_type": field_int(summary, "bnc_coca_type_score"),
            "ngsl_type": field_int(summary, "ngsl_type_score"),
        }
        deltas = {
            key: first_scores[key] - all_scores[key]
            for key in first_scores
        }
        has_delta = any(value != 0 for value in deltas.values())
        rows.append(
            {
                "sensitivity_status": "review" if has_delta else "ok",
                "sensitivity_action_hint": sensitivity_action_hint(has_delta),
                "analysis_session_key": session_key,
                "source_file": summary.get("source_file", ""),
                "participant_session_id": summary.get("participant_session_id", ""),
                "participant_id": summary.get("participant_id", ""),
                "response_slots": summary.get("response_slots", ""),
                "multiword_response_slots": summary.get("multiword_response_slots", ""),
                "extra_tokens_in_response_slots": summary.get("extra_tokens_in_response_slots", ""),
                "first_token_extra_tokens_excluded": summary.get("extra_tokens_in_response_slots", ""),
                "all_token_lexical_tokens": summary.get("lexical_tokens", ""),
                "first_token_lexical_tokens": len(first_lexical_rows),
                "all_token_review_tokens": summary.get("both_off_list_review_tokens", ""),
                "first_token_review_tokens": sum(1 for row in first_token_rows if (row.get("oov_status") or "") == "both_off_list_review"),
                "all_token_list_disagreement_tokens": summary.get("list_disagreement_tokens", ""),
                "first_token_list_disagreement_tokens": sum(1 for row in first_token_rows if parse_bool(row.get("list_disagreement"))),
                "all_token_nj8_token_score": all_scores["nj8_token"],
                "first_token_nj8_token_score": first_scores["nj8_token"],
                "first_token_score_delta_nj8_token": deltas["nj8_token"],
                "all_token_nj8_type_score": all_scores["nj8_type"],
                "first_token_nj8_type_score": first_scores["nj8_type"],
                "first_token_score_delta_nj8_type": deltas["nj8_type"],
                "all_token_bnc_coca_token_score": all_scores["bnc_coca_token"],
                "first_token_bnc_coca_token_score": first_scores["bnc_coca_token"],
                "first_token_score_delta_bnc_coca_token": deltas["bnc_coca_token"],
                "all_token_bnc_coca_type_score": all_scores["bnc_coca_type"],
                "first_token_bnc_coca_type_score": first_scores["bnc_coca_type"],
                "first_token_score_delta_bnc_coca_type": deltas["bnc_coca_type"],
                "all_token_ngsl_token_score": all_scores["ngsl_token"],
                "first_token_ngsl_token_score": first_scores["ngsl_token"],
                "first_token_score_delta_ngsl_token": deltas["ngsl_token"],
                "all_token_ngsl_type_score": all_scores["ngsl_type"],
                "first_token_ngsl_type_score": first_scores["ngsl_type"],
                "first_token_score_delta_ngsl_type": deltas["ngsl_type"],
                "sensitivity_note": (
                    "Descriptive sensitivity diagnostic only. Primary v0.3 scoring remains all-token unless a human-reviewed final policy changes it."
                ),
            }
        )
    write_dict_csv(path, rows)
    return rows


def bootstrap_statistic(
    values: list[Any],
    statistic_fn: Any,
    *,
    rng: random.Random,
    iterations: int = BOOTSTRAP_ITERATIONS,
) -> list[float]:
    if len(values) < 2:
        return []
    estimates: list[float] = []
    for _ in range(iterations):
        sample = [values[rng.randrange(len(values))] for _ in values]
        estimate = statistic_fn(sample)
        if finite_number(estimate):
            estimates.append(float(estimate))
    return estimates


def random_split_indexes(item_count: int, rng: random.Random) -> tuple[list[int], list[int]]:
    indexes = list(range(item_count))
    rng.shuffle(indexes)
    midpoint = item_count // 2
    return sorted(indexes[:midpoint]), sorted(indexes[midpoint:])


def split_half_reliability(
    matrix: list[list[float]],
    left_indexes: list[int],
    right_indexes: list[int],
) -> tuple[float | None, float | None]:
    if len(matrix) < 2 or not left_indexes or not right_indexes:
        return None, None
    left_scores = [sum(row[index] for index in left_indexes) for row in matrix]
    right_scores = [sum(row[index] for index in right_indexes) for row in matrix]
    r_value = pearson_correlation(left_scores, right_scores)
    return r_value, spearman_brown(r_value)


def random_split_spearman_brown_values(
    matrix: list[list[float]],
    *,
    rng: random.Random,
    iterations: int = RANDOM_SPLIT_ITERATIONS,
) -> list[float]:
    if len(matrix) < 2 or not matrix or len(matrix[0]) < 2:
        return []
    values: list[float] = []
    for _ in range(iterations):
        left, right = random_split_indexes(len(matrix[0]), rng)
        _r_value, sb_value = split_half_reliability(matrix, left, right)
        if finite_number(sb_value):
            values.append(float(sb_value))
    return values


def bootstrap_random_split_spearman_brown_values(
    matrix: list[list[float]],
    *,
    rng: random.Random,
    iterations: int = BOOTSTRAP_ITERATIONS,
) -> list[float]:
    if len(matrix) < 2 or not matrix or len(matrix[0]) < 2:
        return []
    values: list[float] = []
    for _ in range(iterations):
        sample = [matrix[rng.randrange(len(matrix))] for _ in matrix]
        left, right = random_split_indexes(len(matrix[0]), rng)
        _r_value, sb_value = split_half_reliability(sample, left, right)
        if finite_number(sb_value):
            values.append(float(sb_value))
    return values


def psychometric_session_maps(
    cue_rows: list[dict[str, Any]],
    stimuli: list[str],
) -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, dict[str, dict[str, Any]]]]:
    stimulus_set = set(stimuli)
    by_session: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in cue_rows:
        session_key = str(row.get("analysis_session_key") or "")
        stimulus = str(row.get("stimulus") or "")
        if session_key and stimulus:
            by_session[session_key][stimulus] = row
    complete_sessions = {
        session: item_rows
        for session, item_rows in by_session.items()
        if stimulus_set.issubset(item_rows.keys())
    }
    return by_session, complete_sessions


def score_matrix(
    complete_sessions: dict[str, dict[str, dict[str, Any]]],
    stimuli: list[str],
    score_field: str,
) -> list[list[float]]:
    return [
        [float(complete_sessions[session][stimulus].get(score_field) or 0) for stimulus in stimuli]
        for session in sorted(complete_sessions)
    ]


def lowest_item_correlation(
    item_diagnostic_rows: list[dict[str, Any]],
    *,
    score_field: str,
    field: str,
) -> tuple[float | None, str]:
    candidates = []
    for row in item_diagnostic_rows:
        if row.get("score_field") != score_field:
            continue
        value = optional_float(row.get(field))
        if finite_number(value):
            candidates.append((float(value), str(row.get("stimulus") or "")))
    if not candidates:
        return None, ""
    return min(candidates, key=lambda item: item[0])


def write_cue_score_matrix(
    *,
    path: Path,
    scored_rows: list[dict[str, str]],
    stimuli: list[str],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in scored_rows:
        grouped[(row.get("analysis_session_key") or "", row.get("stimulus") or "")].append(row)

    stimulus_order = {stimulus: index + 1 for index, stimulus in enumerate(stimuli)}
    matrix_rows: list[dict[str, Any]] = []
    for (session_key, stimulus), rows in sorted(grouped.items(), key=lambda item: (item[0][0], stimulus_order.get(item[0][1], 999), item[0][1])):
        first = rows[0]
        lexical_rows = [row for row in rows if parse_bool(row.get("is_lexical_token")) and not parse_bool(row.get("is_stimulus_repetition"))]
        matrix_rows.append(
            {
                "analysis_session_key": session_key,
                "source_file": first.get("source_file") or "",
                "participant_session_id": first.get("participant_session_id") or "",
                "participant_id": first.get("participant_id") or "",
                "stimulus_order": stimulus_order.get(stimulus, ""),
                "stimulus": stimulus,
                "response_slots": len({row.get("answer_column") or "" for row in rows}),
                "lexical_tokens": len(lexical_rows),
                "multiword_response_slots": len({row.get("answer_column") or "" for row in rows if field_int(row, "extra_tokens_in_slot") > 0}),
                "extra_tokens_in_response_slots": sum(1 for row in rows if parse_bool(row.get("is_extra_token_in_slot"))),
                "nj8_token_score": sum(field_int(row, "nj8_score_token") for row in rows),
                "bnc_coca_token_score": sum(field_int(row, "bnc_coca_score_token") for row in rows),
                "ngsl_token_score": sum(field_int(row, "ngsl_score_token") for row in rows),
                "both_off_list_review_tokens": sum(1 for row in rows if (row.get("oov_status") or "") == "both_off_list_review"),
                "list_disagreement_tokens": sum(1 for row in rows if parse_bool(row.get("list_disagreement"))),
            }
        )
    write_dict_csv(path, matrix_rows)
    return matrix_rows


def write_psychometrics_summary(
    *,
    path: Path,
    cue_rows: list[dict[str, Any]],
    stimuli: list[str],
    item_diagnostic_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_session, complete_sessions = psychometric_session_maps(cue_rows, stimuli)

    summary_rows: list[dict[str, Any]] = []
    for field_index, score_field in enumerate(SCORE_FIELDS):
        matrix = score_matrix(complete_sessions, stimuli, score_field)
        totals = [sum(row) for row in matrix]
        odd_indexes = list(range(0, len(stimuli), 2))
        even_indexes = list(range(1, len(stimuli), 2))
        split_r, split_sb = split_half_reliability(matrix, odd_indexes, even_indexes)
        rng = random.Random(BOOTSTRAP_SEED + field_index)
        mean_total_estimates = bootstrap_statistic(
            matrix,
            lambda sample: statistics.fmean(sum(row) for row in sample),
            rng=rng,
        )
        alpha_estimates = bootstrap_statistic(matrix, cronbach_alpha, rng=rng)
        random_split_values = random_split_spearman_brown_values(matrix, rng=rng)
        bootstrap_split_values = bootstrap_random_split_spearman_brown_values(matrix, rng=rng)
        mean_total_ci_low, mean_total_ci_high = ci_bounds(mean_total_estimates, digits=2)
        alpha_ci_low, alpha_ci_high = ci_bounds(alpha_estimates)
        random_split_ci_low, random_split_ci_high = ci_bounds(random_split_values)
        bootstrap_split_ci_low, bootstrap_split_ci_high = ci_bounds(bootstrap_split_values)
        min_item_total, lowest_item_total_stimulus = lowest_item_correlation(
            item_diagnostic_rows,
            score_field=score_field,
            field="item_total_correlation",
        )
        min_item_rest, lowest_item_rest_stimulus = lowest_item_correlation(
            item_diagnostic_rows,
            score_field=score_field,
            field="item_rest_correlation",
        )
        negative_item_rest_count = sum(
            1
            for row in item_diagnostic_rows
            if row.get("score_field") == score_field
            and (optional_float(row.get("item_rest_correlation")) is not None)
            and float(optional_float(row.get("item_rest_correlation"))) < 0
        )
        summary_rows.append(
            {
                "score_field": score_field,
                "sessions_total": len(by_session),
                "complete_sessions_used": len(matrix),
                "stimuli": len(stimuli),
                "mean_total_score": mean(totals),
                "mean_total_score_ci95_low": mean_total_ci_low,
                "mean_total_score_ci95_high": mean_total_ci_high,
                "sd_total_score": round(statistics.stdev(totals), 2) if len(totals) >= 2 else "",
                "min_total_score": min(totals) if totals else "",
                "max_total_score": max(totals) if totals else "",
                "cronbach_alpha_complete_sessions": cronbach_alpha(matrix),
                "bootstrap_cronbach_alpha_ci95_low": alpha_ci_low,
                "bootstrap_cronbach_alpha_ci95_high": alpha_ci_high,
                "split_half_odd_even_r": rounded_or_blank(split_r),
                "split_half_odd_even_spearman_brown": rounded_or_blank(split_sb),
                "random_split_spearman_brown_mean": rounded_or_blank(statistics.fmean(random_split_values) if random_split_values else None),
                "random_split_spearman_brown_ci95_low": random_split_ci_low,
                "random_split_spearman_brown_ci95_high": random_split_ci_high,
                "bootstrap_split_half_spearman_brown_ci95_low": bootstrap_split_ci_low,
                "bootstrap_split_half_spearman_brown_ci95_high": bootstrap_split_ci_high,
                "min_item_total_correlation": rounded_or_blank(min_item_total),
                "lowest_item_total_stimulus": lowest_item_total_stimulus,
                "min_item_rest_correlation": rounded_or_blank(min_item_rest),
                "lowest_item_rest_stimulus": lowest_item_rest_stimulus,
                "negative_item_rest_correlation_count": negative_item_rest_count,
                "bootstrap_iterations": BOOTSTRAP_ITERATIONS,
                "random_split_iterations": RANDOM_SPLIT_ITERATIONS,
                "psychometric_note": "Descriptive pilot diagnostic only; not validation evidence by itself.",
            }
        )
    write_dict_csv(path, summary_rows)
    return summary_rows


def build_item_diagnostics(
    *,
    cue_rows: list[dict[str, Any]],
    stimuli: list[str],
    by_session: dict[str, dict[str, dict[str, Any]]],
    complete_sessions: dict[str, dict[str, dict[str, Any]]],
    score_field: str,
    rng: random.Random,
) -> list[dict[str, Any]]:
    matrix = score_matrix(complete_sessions, stimuli, score_field)
    totals = [sum(row) for row in matrix]
    observed_by_stimulus: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in cue_rows:
        observed_by_stimulus[str(row.get("stimulus") or "")].append(row)

    rows: list[dict[str, Any]] = []
    for column_index, stimulus in enumerate(stimuli):
        item_scores = [row[column_index] for row in matrix]
        rest_scores = [totals[index] - item_scores[index] for index in range(len(item_scores))]
        observed_rows = observed_by_stimulus.get(stimulus, [])
        item_total = pearson_correlation(item_scores, totals)
        item_rest = pearson_correlation(item_scores, rest_scores)
        mean_item_estimates = bootstrap_statistic(
            item_scores,
            lambda sample: statistics.fmean(sample),
            rng=rng,
        )
        positive_percent_estimates = bootstrap_statistic(
            item_scores,
            lambda sample: percent(sum(1 for value in sample if value > 0), len(sample)),
            rng=rng,
        )
        paired_scores = list(zip(item_scores, rest_scores))
        item_rest_estimates = bootstrap_statistic(
            paired_scores,
            lambda sample: pearson_correlation(
                [pair[0] for pair in sample],
                [pair[1] for pair in sample],
            ),
            rng=rng,
        )
        mean_item_ci_low, mean_item_ci_high = ci_bounds(mean_item_estimates, digits=2)
        positive_ci_low, positive_ci_high = ci_bounds(positive_percent_estimates, digits=2)
        item_rest_ci_low, item_rest_ci_high = ci_bounds(item_rest_estimates)
        rows.append(
            {
                "score_field": score_field,
                "stimulus_order": column_index + 1,
                "stimulus": stimulus,
                "sessions_total": len(by_session),
                "complete_sessions_used": len(matrix),
                "observed_sessions": len(observed_rows),
                "mean_item_score": mean(item_scores),
                "mean_item_score_ci95_low": mean_item_ci_low,
                "mean_item_score_ci95_high": mean_item_ci_high,
                "sd_item_score": round(statistics.stdev(item_scores), 2) if len(item_scores) >= 2 else "",
                "min_item_score": min(item_scores) if item_scores else "",
                "max_item_score": max(item_scores) if item_scores else "",
                "item_score_zero_percent": percent(sum(1 for value in item_scores if value == 0), len(item_scores)),
                "item_score_positive_percent": percent(sum(1 for value in item_scores if value > 0), len(item_scores)),
                "item_score_positive_percent_ci95_low": positive_ci_low,
                "item_score_positive_percent_ci95_high": positive_ci_high,
                "item_total_correlation": rounded_or_blank(item_total),
                "item_rest_correlation": rounded_or_blank(item_rest),
                "item_rest_correlation_ci95_low": item_rest_ci_low,
                "item_rest_correlation_ci95_high": item_rest_ci_high,
                "mean_lexical_tokens_observed": mean([field_float(row, "lexical_tokens") for row in observed_rows]),
                "mean_multiword_response_slots_observed": mean([field_float(row, "multiword_response_slots") for row in observed_rows]),
                "mean_both_off_list_review_tokens_observed": mean([field_float(row, "both_off_list_review_tokens") for row in observed_rows]),
                "item_diagnostic_note": "Descriptive pilot item diagnostic only; inspect sparse or unstable estimates before item decisions.",
            }
        )
    return rows


def write_item_diagnostics(
    *,
    path: Path,
    cue_rows: list[dict[str, Any]],
    stimuli: list[str],
) -> list[dict[str, Any]]:
    by_session, complete_sessions = psychometric_session_maps(cue_rows, stimuli)
    rows: list[dict[str, Any]] = []
    for field_index, score_field in enumerate(SCORE_FIELDS):
        rows.extend(
            build_item_diagnostics(
                cue_rows=cue_rows,
                stimuli=stimuli,
                by_session=by_session,
                complete_sessions=complete_sessions,
                score_field=score_field,
                rng=random.Random(BOOTSTRAP_SEED + 100 + field_index),
            )
        )
    write_dict_csv(path, rows)
    return rows


def enrich_review_rows(review_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for row in review_rows:
        priority_rank, priority, action_hint = review_priority(row)
        enriched.append(
            {
                "review_priority_rank": priority_rank,
                "review_priority": priority,
                "review_action_hint": action_hint,
                **row,
            }
        )
    return sorted(
        enriched,
        key=lambda row: (
            int(row.get("review_priority_rank") or 99),
            -field_int(row, "occurrences"),
            str(row.get("stimulus") or ""),
            str(row.get("response_token") or ""),
        ),
    )


def top_counter(rows: list[dict[str, str]], field: str) -> Counter[str]:
    return Counter((row.get(field) or "").strip() or "(missing)" for row in rows)


def make_report(
    *,
    path: Path,
    input_path: Path,
    raw_csvs: list[Path],
    raw_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    review_rows: list[dict[str, str]],
    item_rows: list[dict[str, Any]],
    item_diagnostic_rows: list[dict[str, Any]],
    score_diagnostic_rows: list[dict[str, Any]],
    sensitivity_rows: list[dict[str, Any]],
    external_correlation_rows: list[dict[str, Any]],
    external_metadata: dict[str, Any],
    qc_rows: list[dict[str, Any]],
    output_dir: Path,
    freeze_errors: list[str],
    expected_items: int,
) -> None:
    experiment_counts = top_counter(raw_rows, "ExperimentId")
    audio_counts = top_counter(raw_rows, "AudioVersion")
    participant_count = len({row_session_key(row) for row in raw_rows})
    complete_count = sum(1 for row in qc_rows if field_int(row, "unique_stimuli") == expected_items)
    complete_case_candidate_count = sum(1 for row in qc_rows if str(row.get("primary_complete_case_candidate") or "") == "yes")
    incomplete_count = sum(1 for row in qc_rows if "incomplete_30_items" in str(row.get("qc_flags", "")))
    duplicate_count = sum(1 for row in qc_rows if "duplicate_stimuli" in str(row.get("qc_flags", "")))
    missing_audio_log_count = sum(1 for row in qc_rows if "missing_audio_play_logs" in str(row.get("qc_flags", "")))
    no_audio_play_count = sum(1 for row in qc_rows if "no_audio_play_item" in str(row.get("qc_flags", "")))
    high_auto_count = sum(1 for row in qc_rows if "high_auto_advance" in str(row.get("qc_flags", "")))
    low_fill_count = sum(1 for row in qc_rows if "low_filled_slot_rate" in str(row.get("qc_flags", "")))
    multiword_session_count = sum(1 for row in qc_rows if "multiword_response_slots" in str(row.get("qc_flags", "")))
    multiword_slot_total = sum(field_int(row, "multiword_response_slots") for row in qc_rows)
    extra_token_total = sum(field_int(row, "extra_tokens_in_response_slots") for row in qc_rows)
    both_off_list_total = sum(int(row.get("both_off_list_review_tokens") or 0) for row in summary_rows)
    list_disagreement_total = sum(int(row.get("list_disagreement_tokens") or 0) for row in summary_rows)
    lexical_tokens = sum(int(row.get("lexical_tokens") or 0) for row in summary_rows)
    valid_tokens = sum(int(row.get("valid_in_list_tokens") or 0) for row in summary_rows)
    no_response_slots = sum(int(row.get("no_response_slots") or 0) for row in summary_rows)
    stimulus_repetitions = sum(int(row.get("stimulus_repetitions") or 0) for row in summary_rows)
    followup_enabled_row_count = sum(1 for row in raw_rows if parse_bool(row.get("FollowUpEnabled")))
    followup_completed_row_count = sum(1 for row in raw_rows if parse_bool(row.get("FollowUpCompleted")))
    followup_completion_percent = percent(followup_completed_row_count, followup_enabled_row_count)
    mean_heard_confidence = mean(numeric_field_values(raw_rows, "HeardConfidence"))
    mean_meaning_confidence = mean(numeric_field_values(raw_rows, "MeaningConfidence"))
    mean_response_confidence = mean(numeric_field_values(raw_rows, "ResponseConfidence"))
    mean_nj8_type = mean([field_float(row, "nj8_type_score") for row in summary_rows])
    mean_bnc_type = mean([field_float(row, "bnc_coca_type_score") for row in summary_rows])
    mean_ngsl_type = mean([field_float(row, "ngsl_type_score") for row in summary_rows])
    score_diagnostic_review_count = sum(1 for row in score_diagnostic_rows if (row.get("diagnostic_status") or "") != "ok")
    floor_review_count = sum(1 for row in score_diagnostic_rows if "floor_concentration" in str(row.get("diagnostic_flags", "")))
    ceiling_review_count = sum(1 for row in score_diagnostic_rows if "ceiling_concentration" in str(row.get("diagnostic_flags", "")))
    sparse_review_count = sum(1 for row in score_diagnostic_rows if "sparse_response_concentration" in str(row.get("diagnostic_flags", "")))
    sensitivity_review_count = sum(1 for row in sensitivity_rows if (row.get("sensitivity_status") or "") != "ok")
    sensitivity_extra_tokens_excluded = sum(field_int(row, "first_token_extra_tokens_excluded") for row in sensitivity_rows)
    external_enabled = bool(external_metadata.get("enabled"))
    external_numeric_fields = external_metadata.get("numericCriterionFields") or []

    review_status_counts: Counter[str] = Counter()
    review_ngsl_counts: Counter[str] = Counter()
    for row in review_rows:
        occurrences = int(row.get("occurrences") or 0)
        review_status_counts[row.get("oov_status") or "(missing)"] += occurrences
        review_ngsl_counts[row.get("ngsl_status") or "(missing)"] += occurrences

    participant_candidates = [
        row for row in qc_rows
        if row.get("qc_flags")
    ]
    participant_candidates = sorted(
        participant_candidates,
        key=lambda row: (
            field_float(row, "completion_percent"),
            field_float(row, "filled_slot_percent"),
            -field_float(row, "auto_advanced_percent"),
        ),
    )[:12]

    low_response_items = sorted(
        item_rows,
        key=lambda row: (
            field_float(row, "filled_slot_percent"),
            field_float(row, "mean_lexical_tokens_per_item"),
            -field_float(row, "mean_reaction_time_ms"),
        ),
    )[:10]
    slow_items = sorted(
        [row for row in item_rows if field_float(row, "mean_reaction_time_ms") > 0],
        key=lambda row: field_float(row, "mean_reaction_time_ms"),
        reverse=True,
    )[:10]
    audio_issue_items = [
        row for row in item_rows
        if field_int(row, "items_missing_audio_play_log") or field_int(row, "items_with_no_audio_play")
    ][:10]
    low_item_rest_rows = sorted(
        [
            row for row in item_diagnostic_rows
            if row.get("score_field") == "nj8_token_score"
            and optional_float(row.get("item_rest_correlation")) is not None
        ],
        key=lambda row: float(optional_float(row.get("item_rest_correlation"))),
    )[:10]

    recommendations: list[str] = []
    if freeze_errors:
        recommendations.append("Do not administer or analyze as frozen v0.3 until freeze verification errors are resolved.")
    if missing_audio_log_count:
        recommendations.append("Some files lack browser audio-play logs; confirm that the data came from the current browser export schema.")
    if incomplete_count:
        recommendations.append("Review incomplete participant sessions before inferential analysis; keep them out of primary complete-case summaries unless intentionally modeling partial sessions.")
    if duplicate_count:
        recommendations.append("Inspect duplicate stimulus rows; these can indicate repeated export or browser/session handling problems.")
    if no_audio_play_count:
        recommendations.append("Inspect sessions with no-audio-play items before treating listening-version responses as valid.")
    if high_auto_count:
        recommendations.append("Inspect high auto-advance sessions for low engagement or audio playback problems.")
    if score_diagnostic_review_count:
        recommendations.append("Inspect `score_diagnostics.csv` for floor/ceiling concentration, sparse-response patterns, or insufficient complete-session counts before interpreting score distributions.")
    if sensitivity_review_count:
        recommendations.append("Inspect `multiword_sensitivity.csv` before finalizing the multiword-slot scoring policy; deltas show how first-token scoring would change participant scores.")
    if followup_enabled_row_count and followup_completion_percent < 90:
        recommendations.append("Inspect follow-up completion fields in `participant_qc.csv` and `item_summary.csv` before modeling cue-knowledge predictors.")
    if external_enabled and not external_numeric_fields:
        recommendations.append("External criteria were supplied, but no numeric criterion fields were available for correlation diagnostics.")
    if external_enabled and external_correlation_rows:
        recommendations.append("Treat `external_criteria_correlations.csv` as descriptive criterion/convergent evidence only after QC and missing-data review.")
    if both_off_list_total or list_disagreement_total:
        recommendations.append("Review `pilot_review.csv` before reporting final scores; spelling is preserved as typed unless a manual override is justified.")
    if any(float(optional_float(row.get("item_rest_correlation"))) < 0 for row in low_item_rest_rows if optional_float(row.get("item_rest_correlation")) is not None):
        recommendations.append("Inspect cues with negative NJ8 item-rest correlations before making retention decisions.")
    if not recommendations:
        recommendations.append("No blocking QC issue is visible in this batch. Proceed to manual review of off-list items before reporting final scores.")

    lines = [
        "# Lex30 Pilot Analysis Report",
        "",
        f"- Generated at: {datetime.now(timezone.utc).isoformat()}",
        f"- Input path: `{relative_or_absolute(input_path)}`",
        f"- Output path: `{relative_or_absolute(output_dir)}`",
        f"- Raw CSV files: {len(raw_csvs)}",
        f"- Raw stimulus rows: {len(raw_rows)}",
        f"- Participant sessions: {participant_count}",
        f"- Item summary rows: {len(item_rows)}",
        f"- Review rows: {len(review_rows)}",
        f"- Freeze verification: {'OK' if not freeze_errors else 'FAILED'}",
        "",
        "## Data Quality Summary",
        "",
    ]
    lines.extend(
        markdown_table(
            ["Metric", "Value"],
            [
                ["Participant sessions", participant_count],
                ["Complete 30-item sessions", f"{complete_count} ({percent(complete_count, participant_count)}%)"],
                ["Primary complete-case candidates", complete_case_candidate_count],
                ["Incomplete sessions", incomplete_count],
                ["Duplicate-stimulus sessions", duplicate_count],
                ["Sessions missing audio-play logs", missing_audio_log_count],
                ["Sessions with no-audio-play item", no_audio_play_count],
                ["High auto-advance sessions", high_auto_count],
                ["Low filled-slot-rate sessions", low_fill_count],
                ["Sessions with multiword answer slots", multiword_session_count],
                ["Multiword answer slots", multiword_slot_total],
                ["Extra tokens in multiword slots", extra_token_total],
                ["Score diagnostic rows needing review", score_diagnostic_review_count],
                ["Floor-concentration score fields", floor_review_count],
                ["Ceiling-concentration score fields", ceiling_review_count],
                ["Sparse-response score fields", sparse_review_count],
                ["Sensitivity rows needing review", sensitivity_review_count],
                ["Extra tokens excluded by first-token policy", sensitivity_extra_tokens_excluded],
                ["Follow-up rows enabled", followup_enabled_row_count],
                ["Follow-up rows completed", f"{followup_completed_row_count} ({followup_completion_percent}%)"],
                ["Mean heard-confidence slider", mean_heard_confidence if mean_heard_confidence is not None else "-"],
                ["Mean meaning-confidence slider", mean_meaning_confidence if mean_meaning_confidence is not None else "-"],
                ["Mean response-confidence slider", mean_response_confidence if mean_response_confidence is not None else "-"],
                ["External criteria linked", "yes" if external_enabled else "no"],
                ["External matched summary rows", external_metadata.get("matchedSummaryRows", 0) if external_enabled else 0],
                ["External numeric criterion fields", len(external_numeric_fields)],
                ["Criterion correlation rows", len(external_correlation_rows)],
                ["Raw item rows", len(raw_rows)],
                ["No-response slots", no_response_slots],
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Scoring Summary",
            "",
        ]
    )
    lines.extend(
        markdown_table(
            ["Metric", "Value"],
            [
                ["Lexical tokens", lexical_tokens],
                ["Valid in-list tokens", valid_tokens],
                ["Stimulus repetitions", stimulus_repetitions],
                ["Both-off-list review tokens", both_off_list_total],
                ["List-disagreement tokens", list_disagreement_total],
                ["Mean NJ8 type score", mean_nj8_type if mean_nj8_type is not None else "-"],
                ["Mean BNC/COCA type score", mean_bnc_type if mean_bnc_type is not None else "-"],
                ["Mean NGSL type score", mean_ngsl_type if mean_ngsl_type is not None else "-"],
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Review Status Counts",
            "",
        ]
    )
    lines.extend(markdown_table(["Status", "Occurrences"], [[key, count] for key, count in review_status_counts.most_common()]))
    lines.extend(["", "## NGSL Review Counts", ""])
    lines.extend(markdown_table(["NGSL Status", "Occurrences"], [[key, count] for key, count in review_ngsl_counts.most_common()]))
    lines.extend(["", "## Score Distribution Diagnostics", ""])
    lines.extend(
        markdown_table(
            [
                "Score Field",
                "Status",
                "Complete Sessions",
                "Mean",
                "Median",
                "Floor %",
                "Ceiling %",
                "Mean Filled %",
                "Flags",
            ],
            [
                [
                    row.get("score_field"),
                    row.get("diagnostic_status"),
                    row.get("complete_sessions_used"),
                    row.get("mean_score"),
                    row.get("median_score"),
                    row.get("floor_band_percent"),
                    row.get("ceiling_band_percent"),
                    row.get("mean_filled_slot_percent"),
                    row.get("diagnostic_flags"),
                ]
                for row in score_diagnostic_rows
            ],
        )
    )
    sensitivity_candidates = sorted(
        [
            row for row in sensitivity_rows
            if (row.get("sensitivity_status") or "") != "ok"
        ],
        key=lambda row: (
            field_int(row, "first_token_score_delta_nj8_token"),
            field_int(row, "first_token_score_delta_bnc_coca_token"),
            field_int(row, "first_token_score_delta_ngsl_token"),
            -field_int(row, "first_token_extra_tokens_excluded"),
        ),
    )[:12]
    lines.extend(["", "## Multiword Scoring Sensitivity", ""])
    lines.extend(
        markdown_table(
            [
                "Participant",
                "Multiword Slots",
                "Extra Tokens",
                "NJ8 Token Delta",
                "BNC/COCA Token Delta",
                "NGSL Token Delta",
                "Status",
                "Action",
            ],
            [
                [
                    row.get("participant_id") or "(missing)",
                    row.get("multiword_response_slots"),
                    row.get("first_token_extra_tokens_excluded"),
                    row.get("first_token_score_delta_nj8_token"),
                    row.get("first_token_score_delta_bnc_coca_token"),
                    row.get("first_token_score_delta_ngsl_token"),
                    row.get("sensitivity_status"),
                    row.get("sensitivity_action_hint"),
                ]
                for row in sensitivity_candidates
            ],
        )
    )
    if external_enabled:
        lines.extend(["", "## External Criterion Diagnostics", ""])
        lines.extend(
            markdown_table(
                ["Metric", "Value"],
                [
                    ["External criteria path", external_metadata.get("path", "")],
                    ["Summary join key", external_metadata.get("summaryJoinKey", "")],
                    ["Criteria join key", external_metadata.get("criteriaJoinKey", "")],
                    ["Criteria rows", external_metadata.get("criteriaRows", 0)],
                    ["Matched summary rows", external_metadata.get("matchedSummaryRows", 0)],
                    ["Numeric criterion fields", "; ".join(external_numeric_fields) if external_numeric_fields else "-"],
                ],
            )
        )
        lines.extend(["", "### Criterion Correlations", ""])
        lines.extend(
            markdown_table(
                ["Criterion", "Score Field", "N", "Pearson r", "Lex30 Mean", "Criterion Mean"],
                [
                    [
                        row.get("criterion_field"),
                        row.get("score_field"),
                        row.get("paired_n"),
                        row.get("pearson_r"),
                        row.get("lex30_mean"),
                        row.get("criterion_mean"),
                    ]
                    for row in external_correlation_rows
                ],
            )
        )
    lines.extend(["", "## Participant QC Candidates", ""])
    lines.extend(
        markdown_table(
            ["Participant", "Rows", "Unique Items", "Completion %", "Filled %", "Multiword Slots", "Auto %", "No-Audio Items", "Analysis Hint", "Flags"],
            [
                [
                    row.get("participant_id") or "(missing)",
                    row.get("rows"),
                    row.get("unique_stimuli"),
                    row.get("completion_percent"),
                    row.get("filled_slot_percent"),
                    row.get("multiword_response_slots"),
                    row.get("auto_advanced_percent"),
                    row.get("items_with_no_audio_play"),
                    row.get("analysis_set_hint"),
                    row.get("qc_flags"),
                ]
                for row in participant_candidates
            ],
        )
    )
    lines.extend(["", "## Stimulus QC Candidates", "", "### Lowest Response Completion", ""])
    lines.extend(
        markdown_table(
            ["Stimulus", "Rows", "Filled %", "Mean Tokens", "Mean RT ms", "Auto %"],
            [
                [
                    row.get("stimulus"),
                    row.get("rows"),
                    row.get("filled_slot_percent"),
                    row.get("mean_lexical_tokens_per_item"),
                    row.get("mean_reaction_time_ms"),
                    row.get("auto_advanced_percent"),
                ]
                for row in low_response_items
            ],
        )
    )
    lines.extend(["", "### Slowest Mean Response Times", ""])
    lines.extend(
        markdown_table(
            ["Stimulus", "Rows", "Mean RT ms", "Median RT ms", "Filled %", "Mean Tokens"],
            [
                [
                    row.get("stimulus"),
                    row.get("rows"),
                    row.get("mean_reaction_time_ms"),
                    row.get("median_reaction_time_ms"),
                    row.get("filled_slot_percent"),
                    row.get("mean_lexical_tokens_per_item"),
                ]
                for row in slow_items
            ],
        )
    )
    lines.extend(["", "### Audio Log Issues", ""])
    lines.extend(
        markdown_table(
            ["Stimulus", "Rows", "Missing Logs", "No-Audio Items", "No-Audio %", "Mean Play Count"],
            [
                [
                    row.get("stimulus"),
                    row.get("rows"),
                    row.get("items_missing_audio_play_log"),
                    row.get("items_with_no_audio_play"),
                    row.get("no_audio_play_percent"),
                    row.get("mean_audio_play_count"),
                ]
                for row in audio_issue_items
            ],
        )
    )
    lines.extend(["", "## Item-Rest Diagnostics", ""])
    lines.extend(
        markdown_table(
            ["Stimulus", "Mean NJ8 Item Score", "Item-Total r", "Item-Rest r", "Positive %", "Complete Sessions"],
            [
                [
                    row.get("stimulus"),
                    row.get("mean_item_score"),
                    row.get("item_total_correlation"),
                    row.get("item_rest_correlation"),
                    row.get("item_score_positive_percent"),
                    row.get("complete_sessions_used"),
                ]
                for row in low_item_rest_rows
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Experiment IDs",
            "",
        ]
    )
    lines.extend(f"- `{key}`: {count}" for key, count in experiment_counts.most_common())
    lines.extend(["", "## Audio Versions", ""])
    lines.extend(f"- `{key}`: {count}" for key, count in audio_counts.most_common())
    lines.extend(
        [
            "",
            "## Scoring Policy",
            "",
            "- Primary rule scoring remains deterministic: NJ8/BNC-COCA K1 = 0, K2+ = 1, off-list = review.",
            "- Spelling is preserved as typed unless a manual override CSV is supplied.",
            "- GPT annotation is optional review metadata only and is not part of the primary score.",
        ]
    )
    if review_rows:
        lines.extend(["", "## Top Review Items", ""])
        sorted_review = sorted(review_rows, key=lambda row: int(row.get("occurrences") or 0), reverse=True)[:15]
        lines.extend(
            markdown_table(
                ["Stimulus", "Token", "Lookup", "Status", "Occurrences", "Participants", "Example"],
                [
                    [
                        row.get("stimulus", ""),
                        row.get("response_token", ""),
                        row.get("lookup_token", ""),
                        row.get("oov_status", ""),
                        row.get("occurrences", "0"),
                        row.get("participants", "0"),
                        row.get("example_raw_response", ""),
                    ]
                    for row in sorted_review
                ],
            )
        )
    lines.extend(["", "## Recommended Decisions", ""])
    lines.extend(f"- {item}" for item in recommendations)
    if freeze_errors:
        lines.extend(["", "## Freeze Verification Errors", ""])
        lines.extend(f"- {error}" for error in freeze_errors)

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def make_manifest(
    *,
    path: Path,
    input_path: Path,
    raw_csvs: list[Path],
    output_dir: Path,
    outputs: dict[str, Path],
    freeze_errors: list[str],
    with_gpt: bool,
    external_metadata: dict[str, Any] | None = None,
) -> None:
    script_paths = [
        TOOLS_ROOT / "run_pilot_analysis.py",
        TOOLS_ROOT / "score_lex30.py",
        TOOLS_ROOT / "freeze_experiment.py",
    ]
    data_paths = [
        score_lex30.DEFAULT_NJ8_PATH,
        score_lex30.DEFAULT_BNC_COCA_XLSX,
        score_lex30.DEFAULT_ANTBNC_PATH,
        score_lex30.DEFAULT_NGSL_STATS_PATH,
        score_lex30.DEFAULT_NGSL_LEMMAS_PATH,
    ]
    payload = {
        "schemaVersion": "lex30-pilot-analysis-v1",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "inputPath": relative_or_absolute(input_path),
        "rawCsvs": [
            {
                "path": relative_or_absolute(csv_path),
                "bytes": csv_path.stat().st_size,
                "sha256": sha256_file(csv_path),
            }
            for csv_path in raw_csvs
        ],
        "outputDir": relative_or_absolute(output_dir),
        "outputs": {key: relative_or_absolute(value) for key, value in outputs.items()},
        "freezeVerification": {
            "ok": not freeze_errors,
            "errors": freeze_errors,
        },
        "gptEnabled": with_gpt,
        "externalCriteria": external_metadata or {"enabled": False},
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "packages": {
                "openpyxl": package_version("openpyxl"),
                "openai": package_version("openai"),
                "python-dotenv": package_version("python-dotenv"),
                "wordfreq": package_version("wordfreq"),
                "nltk": package_version("nltk"),
            },
        },
        "scriptHashes": {
            relative_or_absolute(path): sha256_file_or_none(path)
            for path in script_paths
        },
        "dataHashes": {
            relative_or_absolute(path): sha256_file_or_none(path)
            for path in data_paths
        },
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", nargs="?", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--manual-overrides", type=Path)
    parser.add_argument("--external-criteria", type=Path, help="Optional CSV with participant/session-linked external criterion fields.")
    parser.add_argument(
        "--external-criteria-key",
        default="auto",
        help="Join key in the external criteria CSV. Defaults to auto-detecting analysis_session_key, participant_session_id, or participant_id/Participant.",
    )
    parser.add_argument("--with-gpt", action="store_true", help="Pass through optional GPT annotation. Costs API credits.")
    parser.add_argument("--gpt-model", default="gpt-5.5")
    parser.add_argument("--experiment-id", default=DEFAULT_EXPERIMENT_ID)
    parser.add_argument("--skip-freeze-verify", action="store_true")
    parser.add_argument("--allow-mixed-experiments", action="store_true", help="Do not stop when raw CSV metadata/stimuli do not match --experiment-id.")
    parser.add_argument("--force", action="store_true", help="Allow writing into a non-empty explicit --output-dir.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    input_path = args.input_path
    if not input_path.exists():
        raise FileNotFoundError(f"Raw CSV input path does not exist: {input_path}")

    try:
        raw_csvs = collect_raw_csvs(input_path)
        raw_rows, answer_columns = read_raw_rows(raw_csvs)
    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(str(exc))
    if not raw_rows:
        raise SystemExit(f"No rows found in raw CSV exports under {input_path}")

    try:
        experiment_config = load_experiment_config(args.experiment_id)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc))
    batch_errors = validate_raw_rows_against_config(raw_rows, experiment_config)
    if batch_errors and not args.allow_mixed_experiments:
        raise SystemExit(
            "Raw CSV exports do not match the selected experiment. "
            "Use --allow-mixed-experiments only for deliberate diagnostic runs.\n"
            + "\n".join(f"- {error}" for error in batch_errors)
        )

    output_dir = args.output_dir or DEFAULT_ANALYSIS_ROOT / run_id()
    if args.output_dir and output_dir.exists() and any(output_dir.iterdir()) and not args.force:
        raise SystemExit(
            f"Output directory is not empty: {output_dir}. "
            "Choose a new --output-dir or pass --force after preserving any workbook decisions."
        )
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "scored_csv": output_dir / "pilot_scored.csv",
        "summary_csv": output_dir / "pilot_summary.csv",
        "review_csv": output_dir / "pilot_review.csv",
        "scored_json": output_dir / "pilot_scored.json",
        "item_summary_csv": output_dir / "item_summary.csv",
        "participant_qc_csv": output_dir / "participant_qc.csv",
        "score_diagnostics_csv": output_dir / "score_diagnostics.csv",
        "multiword_sensitivity_csv": output_dir / "multiword_sensitivity.csv",
        "report_md": output_dir / "pilot_report.md",
        "workbook_xlsx": output_dir / "pilot_workbook.xlsx",
        "cue_score_matrix_csv": output_dir / "cue_score_matrix.csv",
        "psychometrics_summary_csv": output_dir / "psychometrics_summary.csv",
        "item_diagnostics_csv": output_dir / "item_diagnostics.csv",
        "analysis_manifest_json": output_dir / "analysis_manifest.json",
    }
    if args.external_criteria:
        outputs["external_criteria_linked_csv"] = output_dir / "external_criteria_linked.csv"
        outputs["external_criteria_correlations_csv"] = output_dir / "external_criteria_correlations.csv"

    scorer_args = [
        str(input_path),
        "--output-csv",
        str(outputs["scored_csv"]),
        "--output-summary-csv",
        str(outputs["summary_csv"]),
        "--output-review-csv",
        str(outputs["review_csv"]),
        "--output-json",
        str(outputs["scored_json"]),
    ]
    if args.manual_overrides:
        scorer_args.extend(["--manual-overrides", str(args.manual_overrides)])
    if args.with_gpt:
        scorer_args.extend(["--with-gpt", "--gpt-model", args.gpt_model])
    score_lex30.main(scorer_args)

    expected_items = len(experiment_config.get("stimuli") or []) or expected_item_count(args.experiment_id)
    item_rows = item_summary(raw_rows, answer_columns)
    qc_rows = participant_qc(raw_rows, answer_columns, expected_items=expected_items)
    write_dict_csv(outputs["item_summary_csv"], item_rows)
    write_dict_csv(outputs["participant_qc_csv"], qc_rows)

    freeze_errors: list[str] = []
    if not args.skip_freeze_verify:
        freeze_path = PROJECT_ROOT / "configs" / f"{args.experiment_id}.freeze.json"
        freeze_errors = freeze_experiment.verify_freeze(freeze_path)

    summary_rows = read_dict_csv(outputs["summary_csv"])
    score_diagnostic_rows = write_score_diagnostics(
        path=outputs["score_diagnostics_csv"],
        summary_rows=summary_rows,
        qc_rows=qc_rows,
        expected_items=expected_items,
    )
    external_correlation_rows: list[dict[str, Any]] = []
    external_metadata: dict[str, Any] = {"enabled": False}
    if args.external_criteria:
        try:
            external_linked_rows, external_correlation_rows, external_metadata = analyze_external_criteria(
                path=args.external_criteria,
                summary_rows=summary_rows,
                requested_key=args.external_criteria_key,
            )
        except (FileNotFoundError, ValueError) as exc:
            raise SystemExit(str(exc))
        write_dict_csv(outputs["external_criteria_linked_csv"], external_linked_rows)
        write_dict_csv(outputs["external_criteria_correlations_csv"], external_correlation_rows)
    review_rows = enrich_review_rows(read_dict_csv(outputs["review_csv"]))
    write_dict_csv(outputs["review_csv"], review_rows, REVIEW_EXTRA_FIELDS + list(score_lex30.REVIEW_FIELDS))
    scored_rows = read_dict_csv(outputs["scored_csv"])
    sensitivity_rows = write_multiword_sensitivity(
        path=outputs["multiword_sensitivity_csv"],
        scored_rows=scored_rows,
        summary_rows=summary_rows,
    )
    cue_rows = write_cue_score_matrix(
        path=outputs["cue_score_matrix_csv"],
        scored_rows=scored_rows,
        stimuli=[str(stimulus) for stimulus in experiment_config.get("stimuli", [])],
    )
    item_diagnostic_rows = write_item_diagnostics(
        path=outputs["item_diagnostics_csv"],
        cue_rows=cue_rows,
        stimuli=[str(stimulus) for stimulus in experiment_config.get("stimuli", [])],
    )
    write_psychometrics_summary(
        path=outputs["psychometrics_summary_csv"],
        cue_rows=cue_rows,
        stimuli=[str(stimulus) for stimulus in experiment_config.get("stimuli", [])],
        item_diagnostic_rows=item_diagnostic_rows,
    )
    make_report(
        path=outputs["report_md"],
        input_path=input_path,
        raw_csvs=raw_csvs,
        raw_rows=raw_rows,
        summary_rows=summary_rows,
        review_rows=review_rows,
        item_rows=item_rows,
        item_diagnostic_rows=item_diagnostic_rows,
        score_diagnostic_rows=score_diagnostic_rows,
        sensitivity_rows=sensitivity_rows,
        external_correlation_rows=external_correlation_rows,
        external_metadata=external_metadata,
        qc_rows=qc_rows,
        output_dir=output_dir,
        freeze_errors=freeze_errors,
        expected_items=expected_items,
    )
    make_manifest(
        path=outputs["analysis_manifest_json"],
        input_path=input_path,
        raw_csvs=raw_csvs,
        output_dir=output_dir,
        outputs=outputs,
        freeze_errors=freeze_errors,
        with_gpt=args.with_gpt,
        external_metadata=external_metadata,
    )
    write_analysis_workbook(
        outputs["workbook_xlsx"],
        input_path=input_path,
        raw_csvs=raw_csvs,
        outputs=outputs,
        freeze_errors=freeze_errors,
        with_gpt=args.with_gpt,
        external_metadata=external_metadata,
    )

    for name, output_path in outputs.items():
        print(f"{name}: {output_path}")
    return 1 if freeze_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
