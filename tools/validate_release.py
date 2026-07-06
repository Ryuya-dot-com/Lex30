#!/usr/bin/env python3
"""Validate the current Lex30 pilot release wiring before administration."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from freeze_experiment import audio_file_for, verify_freeze


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPERIMENT_ID = "updated-listening-easycue-posbalanced-followup-pilot-v0.4"


class IdCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name == "id" and value:
                self.ids.add(value)


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def collect_html_ids(path: Path) -> set[str]:
    parser = IdCollector()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.ids


def find_experiment(manifest: dict[str, Any], experiment_id: str) -> dict[str, Any] | None:
    for experiment in manifest.get("experiments", []):
        if experiment.get("id") == experiment_id:
            return experiment
    return None


def check_json_files(errors: list[str]) -> None:
    for path in sorted(PROJECT_ROOT.rglob("*.json")):
        if ".git" in path.parts:
            continue
        try:
            load_json(path)
        except Exception as exc:  # noqa: BLE001 - report every parse failure with path context.
            errors.append(f"JSON parse failed: {path.relative_to(PROJECT_ROOT)} ({exc})")


def check_config_and_manifest(experiment_id: str, errors: list[str], warnings: list[str]) -> dict[str, Any] | None:
    manifest_path = PROJECT_ROOT / "experiments.json"
    manifest = load_json(manifest_path)
    experiment = find_experiment(manifest, experiment_id)
    if not experiment:
        errors.append(f"Experiment is missing from experiments.json: {experiment_id}")
        return None

    default_id = manifest.get("defaultExperimentId")
    if default_id != experiment_id:
        warnings.append(f"defaultExperimentId is {default_id!r}, not {experiment_id!r}")

    config_path = PROJECT_ROOT / str(experiment.get("config", ""))
    if not config_path.exists():
        errors.append(f"Config path is missing: {config_path.relative_to(PROJECT_ROOT)}")
        return None

    config = load_json(config_path)
    expected_values = {
        "experimentId": experiment_id,
        "mode": "listening",
        "stimulusPresentation": "audio",
        "responseCount": 4,
        "timerSeconds": 30,
        "randomizeStimuli": False,
        "singleWordPerResponse": True,
        "dataExportSchemaVersion": "lex30-browser-results-v3",
        "pilotStatus": "frozen_followup_pilot",
    }
    for key, expected in expected_values.items():
        if config.get(key) != expected:
            errors.append(f"Config {key} is {config.get(key)!r}, expected {expected!r}")

    stimuli = config.get("stimuli") or []
    if len(stimuli) != 30:
        errors.append(f"Config has {len(stimuli)} stimuli, expected 30")
    if len(stimuli) != len(set(stimuli)):
        errors.append("Config stimuli are not unique")

    breaks = config.get("breaks") or {}
    if breaks.get("enabled") is not True:
        errors.append("v0.4 break setting is not enabled")
    if breaks.get("associationAfterStimulusOrders") != [15]:
        errors.append(f"Break order is {breaks.get('associationAfterStimulusOrders')!r}, expected [15]")

    follow_up = config.get("followUp") or {}
    if follow_up.get("enabled") is not True:
        errors.append("Follow-up section is not enabled")

    instructions = str(config.get("instructions") or "")
    for required_text in ("one word at a time", "Write only English words"):
        if required_text not in instructions:
            errors.append(f"Config instructions are missing {required_text!r}")

    freeze_path = PROJECT_ROOT / str(config.get("freezeManifest") or "")
    if not freeze_path.exists():
        errors.append(f"Freeze manifest is missing: {config.get('freezeManifest')!r}")
    else:
        freeze_errors = verify_freeze(freeze_path)
        errors.extend(f"Freeze verify failed: {error}" for error in freeze_errors)

    return config


def check_audio(config: dict[str, Any], errors: list[str]) -> None:
    for order, stimulus in enumerate(config.get("stimuli") or [], start=1):
        audio_path = audio_file_for(config, str(stimulus), order)
        if not audio_path.exists():
            errors.append(f"Audio file is missing: {audio_path.relative_to(PROJECT_ROOT)}")
        elif audio_path.stat().st_size <= 0:
            errors.append(f"Audio file is empty: {audio_path.relative_to(PROJECT_ROOT)}")


def check_followup_probes(config: dict[str, Any], errors: list[str]) -> None:
    follow_up = config.get("followUp") or {}
    probes = follow_up.get("probes") or {}
    required_probe_types = ("collocation", "category", "synonym")
    optional_probe_types = ("antonym",)

    for stimulus in config.get("stimuli") or []:
        cue_probes = probes.get(stimulus)
        if not isinstance(cue_probes, dict):
            errors.append(f"Follow-up probes missing for cue: {stimulus}")
            continue
        for probe_type in required_probe_types:
            validate_probe(stimulus, probe_type, cue_probes.get(probe_type), errors)
        for probe_type in optional_probe_types:
            if probe_type in cue_probes:
                validate_probe(stimulus, probe_type, cue_probes.get(probe_type), errors)


def validate_probe(stimulus: str, probe_type: str, probe: Any, errors: list[str]) -> None:
    if not isinstance(probe, dict):
        errors.append(f"{stimulus}: {probe_type} probe is missing")
        return
    options = probe.get("options") or []
    option_ids = {option.get("id") for option in options if isinstance(option, dict)}
    correct_option_id = probe.get("correctOptionId")
    if not probe.get("prompt"):
        errors.append(f"{stimulus}: {probe_type} probe is missing prompt")
    if correct_option_id not in option_ids:
        errors.append(f"{stimulus}: {probe_type} correctOptionId is not in options")
    if "dont_know" not in option_ids:
        errors.append(f"{stimulus}: {probe_type} probe is missing dont_know option")
    if len(options) < 4:
        errors.append(f"{stimulus}: {probe_type} probe has fewer than 4 options")


def check_html_and_js(errors: list[str]) -> None:
    index_ids = collect_html_ids(PROJECT_ROOT / "index.html")
    required_index_ids = {
        "lang-en",
        "lang-ja",
        "participant-id",
        "save-participant-id",
        "instructions",
        "instructions-text",
        "start-btn",
        "test-area",
        "stimulus",
        "timer-instruction",
        "answers-area",
        "association-answer-input",
        "add-answer-btn",
        "answer-count",
        "association-answer-list",
        "association-answer-slots",
        "download-backup-btn",
        "next-btn",
        "break-area",
        "continue-break-btn",
        "phase-break-area",
        "start-followup-btn",
        "followup-area",
        "followup-form",
        "followup-next-btn",
        "download-followup-backup-btn",
        "result-area",
        "download-btn",
        "download-json-btn",
        "clear-saved-backup-result",
    }
    for element_id in sorted(required_index_ids - index_ids):
        errors.append(f"index.html is missing required id: {element_id}")

    researcher_ids = collect_html_ids(PROJECT_ROOT / "researcher.html")
    required_researcher_ids = {
        "experiment-select",
        "participant-link",
        "copy-link",
        "open-link",
        "run-preflight",
        "preflight-summary",
        "preflight-counts",
        "preflight-results",
        "analysis-command",
        "copy-analysis-command",
    }
    for element_id in sorted(required_researcher_ids - researcher_ids):
        errors.append(f"researcher.html is missing required id: {element_id}")

    script = (PROJECT_ROOT / "script.js").read_text(encoding="utf-8")
    required_snippets = {
        'next: "Next"': "English Next label",
        'next: "次へ"': "Japanese Next label",
        "association-answer-input": "one-at-a-time association input",
        "addAssociationAnswerFromInput": "single answer add handler",
        "scheduleAutomaticDownloads": "automatic download handler",
        "InterfaceLanguage": "language export column",
        "CompletedAssociationBreakOrders": "break export column",
        "singleWordPerResponse": "single-word response setting",
        "Write only English words": "English-only instruction in English UI",
        "回答は必ず英語": "English-only instruction in Japanese UI",
    }
    for snippet, label in required_snippets.items():
        if snippet not in script:
            errors.append(f"script.js is missing {label}: {snippet!r}")


def run_node_check(errors: list[str], warnings: list[str]) -> None:
    node = shutil.which("node")
    if not node:
        warnings.append("node is not available; skipped script.js syntax check")
        return
    result = subprocess.run(
        [node, "--check", str(PROJECT_ROOT / "script.js")],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        errors.append(f"node --check script.js failed: {detail}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment_id", nargs="?", default=DEFAULT_EXPERIMENT_ID)
    parser.add_argument("--skip-node-check", action="store_true")
    args = parser.parse_args(argv)

    errors: list[str] = []
    warnings: list[str] = []

    check_json_files(errors)
    config = check_config_and_manifest(args.experiment_id, errors, warnings)
    if config:
        check_audio(config, errors)
        check_followup_probes(config, errors)
    check_html_and_js(errors)
    if not args.skip_node_check:
        run_node_check(errors, warnings)

    if errors:
        print("Release check failed:")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"- {warning}")
        return 1

    if warnings:
        print("Release check warnings:")
        for warning in warnings:
            print(f"- {warning}")

    stimulus_count = len(config.get("stimuli") or []) if config else 0
    print(f"Release check OK: {args.experiment_id}")
    print(f"- stimuli/audio: {stimulus_count}")
    print("- freeze manifest: OK")
    print("- one-at-a-time UI wiring: OK")
    print("- follow-up probes: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
