#!/usr/bin/env python3
"""Recover raw Lex30 CSV rows from browser JSON backup exports."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "results" / "recovered"
EXPECTED_SCHEMAS = {"lex30-browser-results-v2", "lex30-browser-results-v3", "lex30-browser-results-v4"}
BASE_COLUMNS = [
    "ExperimentId",
    "ExperimentVersion",
    "Mode",
    "InterfaceLanguage",
    "StimulusPresentation",
    "StimulusSetId",
    "AudioVersion",
    "StimulusOrder",
    "StartedAt",
    "CompletedAt",
    "ParticipantSessionId",
    "Participant",
    "Stimulus",
    "StimulusStartedAt",
    "StimulusEndedAt",
]
TAIL_COLUMNS = [
    "ReactionTime(ms)",
    "ElapsedSinceTestStart(ms)",
    "AdvanceTrigger",
    "AutoAdvanced",
    "AudioFile",
    "AudioPlayCount",
    "AudioEndedCount",
    "AudioFirstPlayAt(ms)",
    "AudioLastPlayAt(ms)",
    "AudioLastEndedAt(ms)",
    "AudioLoadedMetadataAt(ms)",
    "AudioCanPlayAt(ms)",
    "AudioPlayFailureAt(ms)",
    "AudioAutoplayBlockedAt(ms)",
    "AudioErrorAt(ms)",
    "AudioTimerStartedAt(ms)",
    "AudioTimerStartReason",
    "CompletedAssociationBreakOrders",
    "FollowUpEnabled",
    "FollowUpCompleted",
    "FollowUpRecognitionStartedAt",
    "FollowUpRecognitionEndedAt",
    "FollowUpRecognitionRT(ms)",
    "HeardWord",
    "HeardConfidence",
    "FollowUpSemanticStartedAt",
    "FollowUpSemanticEndedAt",
    "FollowUpSemanticRT(ms)",
    "MeaningConfidence",
    "ResponseConfidence",
    "JapaneseMeaning",
    "CollocationChoice",
    "CollocationCorrect",
    "CollocationAnswer",
    "CategoryChoice",
    "CategoryCorrect",
    "CategoryAnswer",
    "SynonymChoice",
    "SynonymCorrect",
    "SynonymAnswer",
    "AntonymChoice",
    "AntonymCorrect",
    "AntonymAnswer",
    "ResponseModality",
    "SpokenTaskStyle",
    "DiscreteAdvanceMode",
    "AssociationInstructionStyle",
    "Slot1Onset(ms)",
    "Slot2Onset(ms)",
    "Slot3Onset(ms)",
    "Slot4Onset(ms)",
    "Slot1Completed(ms)",
    "Slot2Completed(ms)",
    "Slot3Completed(ms)",
    "Slot4Completed(ms)",
    "SpokenAudioFile",
    "SpokenAudioSha256",
    "SpokenDuration(ms)",
    "StimulusSubset",
    "StimulusOrderPolicy",
    "RecoverySourceFile",
    "RecoveryRowType",
    "RecoveryIsComplete",
    "RecoveryCompletedResponseCount",
    "RecoveryTotalStimuli",
    "RecoveryExportedAt",
    "RecoveryAutosavedAt",
    "RecoveryFlags",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def relative_or_absolute(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def sanitize_file_part(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in value)
    return (cleaned or "backup")[:80]


def collect_json_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    if not input_path.is_dir():
        raise FileNotFoundError(input_path)
    paths = sorted(path for path in input_path.glob("*.json") if not path.name.startswith("."))
    if not paths:
        raise ValueError(f"No browser backup JSON files found in {input_path}")
    return paths


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return payload


def answer_columns(response_count: int) -> list[str]:
    return [f"Answer{index}" for index in range(1, max(4, response_count) + 1)]


def max_response_count(payloads: list[dict[str, Any]]) -> int:
    count = 4
    for payload in payloads:
        experiment = payload.get("experiment") or {}
        count = max(count, int(experiment.get("responseCount") or 4))
        for response in payload.get("responses") or []:
            count = max(count, len(response.get("answers") or []))
        draft = payload.get("currentDraft") or {}
        count = max(count, len(draft.get("answers") or []))
    return count


def audio_value(response: dict[str, Any], key: str) -> Any:
    audio = response.get("audio") or {}
    return audio.get(key, "")


def followup_by_order(payload: dict[str, Any]) -> dict[int, dict[str, Any]]:
    records: dict[int, dict[str, Any]] = {}
    for record in payload.get("followUpResponses") or []:
        try:
            order = int(record.get("stimulusOrder") or 0)
        except (TypeError, ValueError):
            continue
        if order:
            records[order] = record
    return records


def probe_value(probes: dict[str, Any], probe_type: str, key: str) -> Any:
    probe = probes.get(probe_type) or {}
    return probe.get(key, "")


def followup_values(payload: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    try:
        order = int(response.get("stimulusOrder") or 0)
    except (TypeError, ValueError):
        order = 0
    record = followup_by_order(payload).get(order, {})
    recognition = record.get("recognition") or {}
    semantic = record.get("semantic") or {}
    probes = semantic.get("probes") or {}
    return {
        "FollowUpEnabled": bool((payload.get("experiment") or {}).get("followUpEnabled")),
        "FollowUpCompleted": bool(recognition.get("endedAt") or semantic.get("endedAt")),
        "FollowUpRecognitionStartedAt": recognition.get("startedAt", ""),
        "FollowUpRecognitionEndedAt": recognition.get("endedAt", ""),
        "FollowUpRecognitionRT(ms)": recognition.get("reactionTimeMs", ""),
        "HeardWord": recognition.get("heardWord", ""),
        "HeardConfidence": recognition.get("heardConfidence", ""),
        "FollowUpSemanticStartedAt": semantic.get("startedAt", ""),
        "FollowUpSemanticEndedAt": semantic.get("endedAt", ""),
        "FollowUpSemanticRT(ms)": semantic.get("reactionTimeMs", ""),
        "MeaningConfidence": semantic.get("meaningConfidence", ""),
        "ResponseConfidence": semantic.get("responseConfidence", ""),
        "JapaneseMeaning": semantic.get("japaneseMeaning", ""),
        "CollocationChoice": probe_value(probes, "collocation", "choiceLabel"),
        "CollocationCorrect": probe_value(probes, "collocation", "correct"),
        "CollocationAnswer": probe_value(probes, "collocation", "correctLabel"),
        "CategoryChoice": probe_value(probes, "category", "choiceLabel"),
        "CategoryCorrect": probe_value(probes, "category", "correct"),
        "CategoryAnswer": probe_value(probes, "category", "correctLabel"),
        "SynonymChoice": probe_value(probes, "synonym", "choiceLabel"),
        "SynonymCorrect": probe_value(probes, "synonym", "correct"),
        "SynonymAnswer": probe_value(probes, "synonym", "correctLabel"),
        "AntonymChoice": probe_value(probes, "antonym", "choiceLabel"),
        "AntonymCorrect": probe_value(probes, "antonym", "correct"),
        "AntonymAnswer": probe_value(probes, "antonym", "correctLabel"),
    }


def payload_flags(payload: dict[str, Any], *, include_draft: bool) -> list[str]:
    state = payload.get("state") or {}
    responses = payload.get("responses") or []
    total = int(state.get("totalStimuli") or 0)
    completed = int(state.get("completedResponseCount") or len(responses))
    flags: list[str] = []
    if payload.get("schemaVersion") not in EXPECTED_SCHEMAS:
        flags.append("unexpected_schema")
    if not payload.get("participant", {}).get("participantId"):
        flags.append("missing_participant_id")
    if not payload.get("participant", {}).get("participantSessionId"):
        flags.append("missing_participant_session_id")
    if not state.get("isComplete"):
        flags.append("incomplete_session")
    if total and len(responses) < total:
        flags.append("fewer_than_total_stimuli")
    if completed != len(responses):
        flags.append("completed_count_mismatch")
    if not responses:
        flags.append("no_completed_rows")
    if payload.get("currentDraft") and include_draft:
        flags.append("current_draft_recovered_separately")
    is_audio_cue = ((payload.get("experiment") or {}).get("stimulusPresentation") or "") == "audio"
    if any("audio" not in response for response in responses):
        flags.append("missing_audio_log")
    if is_audio_cue and any((response.get("audio") or {}).get("audioPlayCount") == 0 for response in responses):
        flags.append("completed_item_with_no_audio_play")
    return flags


def base_row(
    payload: dict[str, Any],
    *,
    response: dict[str, Any],
    source_file: str,
    row_type: str,
    answer_cols: list[str],
    flags: list[str],
) -> dict[str, Any]:
    experiment = payload.get("experiment") or {}
    participant = payload.get("participant") or {}
    timing = payload.get("timing") or {}
    state = payload.get("state") or {}
    answers = list(response.get("answers") or [])
    completed_break_orders = state.get("completedAssociationBreakOrders") or []

    row: dict[str, Any] = {
        "ExperimentId": experiment.get("experimentId", ""),
        "ExperimentVersion": experiment.get("experimentVersion", ""),
        "Mode": experiment.get("mode", ""),
        "InterfaceLanguage": participant.get("interfaceLanguage", ""),
        "StimulusPresentation": experiment.get("stimulusPresentation", ""),
        "StimulusSetId": experiment.get("stimulusSetId", ""),
        "AudioVersion": experiment.get("audioVersion", ""),
        "StimulusOrder": response.get("stimulusOrder", ""),
        "StartedAt": timing.get("startedAt", ""),
        "CompletedAt": timing.get("completedAt", ""),
        "ParticipantSessionId": participant.get("participantSessionId", ""),
        "Participant": participant.get("participantId", ""),
        "Stimulus": response.get("stimulus", ""),
        "StimulusStartedAt": response.get("stimulusStartedAt", ""),
        "StimulusEndedAt": response.get("stimulusEndedAt", ""),
        "ReactionTime(ms)": round(response["reactionTime"]) if isinstance(response.get("reactionTime"), (int, float)) else "",
        "ElapsedSinceTestStart(ms)": response.get("elapsedSinceTestStartMs", ""),
        "AdvanceTrigger": response.get("advanceTrigger", ""),
        "AutoAdvanced": response.get("autoAdvanced", ""),
        "AudioFile": audio_value(response, "audioFile"),
        "AudioPlayCount": audio_value(response, "audioPlayCount"),
        "AudioEndedCount": audio_value(response, "audioEndedCount"),
        "AudioFirstPlayAt(ms)": audio_value(response, "audioFirstPlayAtMs"),
        "AudioLastPlayAt(ms)": audio_value(response, "audioLastPlayAtMs"),
        "AudioLastEndedAt(ms)": audio_value(response, "audioLastEndedAtMs"),
        "AudioLoadedMetadataAt(ms)": audio_value(response, "audioLoadedMetadataAtMs"),
        "AudioCanPlayAt(ms)": audio_value(response, "audioCanPlayAtMs"),
        "AudioPlayFailureAt(ms)": audio_value(response, "audioPlayFailureAtMs"),
        "AudioAutoplayBlockedAt(ms)": audio_value(response, "audioAutoplayBlockedAtMs"),
        "AudioErrorAt(ms)": audio_value(response, "audioErrorAtMs"),
        "AudioTimerStartedAt(ms)": audio_value(response, "audioTimerStartedAtMs"),
        "AudioTimerStartReason": audio_value(response, "audioTimerStartReason"),
        "CompletedAssociationBreakOrders": "|".join(str(order) for order in completed_break_orders),
        **followup_values(payload, response),
        "ResponseModality": experiment.get("responseModality", "written"),
        "SpokenTaskStyle": experiment.get("spokenTaskStyle", ""),
        "DiscreteAdvanceMode": experiment.get("discreteAdvanceMode", ""),
        "AssociationInstructionStyle": experiment.get("associationInstructionStyle", "free"),
        "Slot1Onset(ms)": (response.get("slotOnsetMs") or ["", "", "", ""])[0] if len(response.get("slotOnsetMs") or []) > 0 else "",
        "Slot2Onset(ms)": (response.get("slotOnsetMs") or ["", "", "", ""])[1] if len(response.get("slotOnsetMs") or []) > 1 else "",
        "Slot3Onset(ms)": (response.get("slotOnsetMs") or ["", "", "", ""])[2] if len(response.get("slotOnsetMs") or []) > 2 else "",
        "Slot4Onset(ms)": (response.get("slotOnsetMs") or ["", "", "", ""])[3] if len(response.get("slotOnsetMs") or []) > 3 else "",
        "Slot1Completed(ms)": (response.get("slotCompletedMs") or ["", "", "", ""])[0] if len(response.get("slotCompletedMs") or []) > 0 else "",
        "Slot2Completed(ms)": (response.get("slotCompletedMs") or ["", "", "", ""])[1] if len(response.get("slotCompletedMs") or []) > 1 else "",
        "Slot3Completed(ms)": (response.get("slotCompletedMs") or ["", "", "", ""])[2] if len(response.get("slotCompletedMs") or []) > 2 else "",
        "Slot4Completed(ms)": (response.get("slotCompletedMs") or ["", "", "", ""])[3] if len(response.get("slotCompletedMs") or []) > 3 else "",
        "SpokenAudioFile": (response.get("spoken") or {}).get("audioFile", ""),
        "SpokenAudioSha256": (response.get("spoken") or {}).get("sha256", ""),
        "SpokenDuration(ms)": (response.get("spoken") or {}).get("durationMs", ""),
        "StimulusSubset": experiment.get("stimulusSubset", "all"),
        "StimulusOrderPolicy": experiment.get("stimulusOrderPolicy", "fixed"),
        "RecoverySourceFile": source_file,
        "RecoveryRowType": row_type,
        "RecoveryIsComplete": bool(state.get("isComplete")),
        "RecoveryCompletedResponseCount": state.get("completedResponseCount", ""),
        "RecoveryTotalStimuli": state.get("totalStimuli", ""),
        "RecoveryExportedAt": payload.get("exportedAt", ""),
        "RecoveryAutosavedAt": (payload.get("autosave") or {}).get("savedAt", ""),
        "RecoveryFlags": ";".join(flags),
    }
    for index, col in enumerate(answer_cols):
        row[col] = answers[index] if index < len(answers) else ""
    return row


def draft_row(
    payload: dict[str, Any],
    *,
    source_file: str,
    answer_cols: list[str],
    flags: list[str],
) -> dict[str, Any] | None:
    draft = payload.get("currentDraft")
    if not draft:
        return None
    response = {
        "stimulusOrder": draft.get("stimulusOrder", ""),
        "stimulus": draft.get("stimulus", ""),
        "answers": draft.get("answers") or [],
        "stimulusStartedAt": draft.get("stimulusStartedAt", ""),
        "stimulusEndedAt": "",
        "reactionTime": draft.get("elapsedOnItemMs", ""),
        "elapsedSinceTestStartMs": "",
        "advanceTrigger": "current_draft",
        "autoAdvanced": False,
        "audio": draft.get("audio") or {},
    }
    row = base_row(
        payload,
        response=response,
        source_file=source_file,
        row_type="current_draft_review",
        answer_cols=answer_cols,
        flags=flags,
    )
    row["CompletedAt"] = ""
    row["StimulusEndedAt"] = ""
    row["ReactionTime(ms)"] = draft.get("elapsedOnItemMs", "")
    return row


def ordered_columns(answer_cols: list[str]) -> list[str]:
    return BASE_COLUMNS + answer_cols + TAIL_COLUMNS


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    *,
    input_path: Path,
    json_files: list[Path],
    completed_rows: list[dict[str, Any]],
    draft_rows: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
    outputs: dict[str, Path],
) -> None:
    payload = {
        "schemaVersion": "lex30-browser-backup-recovery-v1",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "inputPath": relative_or_absolute(input_path),
        "inputs": [
            {
                "path": relative_or_absolute(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in json_files
        ],
        "outputs": {key: relative_or_absolute(value) for key, value in outputs.items()},
        "completedRows": len(completed_rows),
        "draftReviewRows": len(draft_rows),
        "recoveryReviewRows": len(review_rows),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def default_output_dir(input_path: Path) -> Path:
    label = sanitize_file_part(input_path.stem if input_path.is_file() else input_path.name)
    return DEFAULT_OUTPUT_ROOT / f"{run_id()}_{label}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path, help="Browser backup JSON file, or a directory of backup JSON files.")
    parser.add_argument("--output-dir", type=Path, help="Directory for recovered CSV and recovery logs.")
    parser.add_argument("--output-csv", type=Path, help="Completed-response CSV path. Useful for writing directly into results/raw_exports/.")
    parser.add_argument("--draft-csv", type=Path, help="Draft-review CSV path.")
    parser.add_argument("--review-csv", type=Path, help="Recovery-review CSV path.")
    parser.add_argument("--manifest-json", type=Path, help="Recovery manifest JSON path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_path = args.input_path
    json_files = collect_json_files(input_path)
    payloads: list[tuple[Path, dict[str, Any]]] = [(path, load_json(path)) for path in json_files]
    valid_payloads = [payload for _path, payload in payloads if payload.get("schemaVersion") in EXPECTED_SCHEMAS]
    if not valid_payloads:
        raise SystemExit(f"No supported Lex30 browser backup payloads found in {input_path}")

    answer_cols = answer_columns(max_response_count(valid_payloads))
    completed_rows: list[dict[str, Any]] = []
    draft_rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []

    for path, payload in payloads:
        flags = payload_flags(payload, include_draft=True)
        source_file = path.name
        if payload.get("schemaVersion") not in EXPECTED_SCHEMAS:
            review_rows.append(
                {
                    "source_file": source_file,
                    "schema_version": payload.get("schemaVersion", ""),
                    "participant_id": "",
                    "participant_session_id": "",
                    "experiment_id": "",
                    "completed_rows": 0,
                    "draft_rows": 0,
                    "flags": "unexpected_schema",
                }
            )
            continue

        for response in payload.get("responses") or []:
            completed_rows.append(
                base_row(
                    payload,
                    response=response,
                    source_file=source_file,
                    row_type="completed_response",
                    answer_cols=answer_cols,
                    flags=flags,
                )
            )

        draft = draft_row(payload, source_file=source_file, answer_cols=answer_cols, flags=flags)
        if draft:
            draft_rows.append(draft)

        participant = payload.get("participant") or {}
        experiment = payload.get("experiment") or {}
        review_rows.append(
            {
                "source_file": source_file,
                "schema_version": payload.get("schemaVersion", ""),
                "participant_id": participant.get("participantId", ""),
                "participant_session_id": participant.get("participantSessionId", ""),
                "experiment_id": experiment.get("experimentId", ""),
                "completed_rows": len(payload.get("responses") or []),
                "draft_rows": 1 if payload.get("currentDraft") else 0,
                "flags": ";".join(flags),
            }
        )

    output_dir = args.output_dir or default_output_dir(input_path)
    output_csv = args.output_csv or output_dir / "recovered.csv"
    draft_csv = args.draft_csv or output_dir / "recovered_draft_review.csv"
    review_csv = args.review_csv or output_dir / "recovery_review.csv"
    manifest_json = args.manifest_json or output_dir / "recovery_manifest.json"

    columns = ordered_columns(answer_cols)
    write_csv(output_csv, completed_rows, columns)
    write_csv(draft_csv, draft_rows, columns)
    write_csv(
        review_csv,
        review_rows,
        [
            "source_file",
            "schema_version",
            "participant_id",
            "participant_session_id",
            "experiment_id",
            "completed_rows",
            "draft_rows",
            "flags",
        ],
    )
    outputs = {
        "completed_csv": output_csv,
        "draft_review_csv": draft_csv,
        "recovery_review_csv": review_csv,
        "recovery_manifest_json": manifest_json,
    }
    write_manifest(
        manifest_json,
        input_path=input_path,
        json_files=json_files,
        completed_rows=completed_rows,
        draft_rows=draft_rows,
        review_rows=review_rows,
        outputs=outputs,
    )

    for name, path in outputs.items():
        print(f"{name}: {path}")
    print(f"completed_rows={len(completed_rows)} draft_review_rows={len(draft_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
