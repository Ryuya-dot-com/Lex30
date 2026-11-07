#!/usr/bin/env python3
"""Write a reproducibility lock file for a Lex30 experiment config."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPERIMENT_ID = "updated-listening-easycue-posbalanced-followup-pilot-v0.4"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def find_experiment(manifest: dict[str, Any], experiment_id: str) -> dict[str, Any]:
    for experiment in manifest.get("experiments", []):
        if experiment.get("id") == experiment_id:
            return experiment
    raise ValueError(f"Unknown experiment id: {experiment_id}")


def audio_file_for(config: dict[str, Any], stimulus: str, order: int) -> Path:
    explicit = config.get("audioFiles") or {}
    if stimulus in explicit:
        return PROJECT_ROOT / explicit[stimulus]
    base_path = str(config.get("audioBasePath") or "")
    extension = str(config.get("audioExtension") or "mp3").lstrip(".")
    file_part = "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in stimulus).lower()
    return PROJECT_ROOT / base_path / f"{order:02d}-{file_part}.{extension}"


def relative(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def build_freeze(experiment_id: str) -> dict[str, Any]:
    manifest_path = PROJECT_ROOT / "experiments.json"
    manifest = load_json(manifest_path)
    experiment = find_experiment(manifest, experiment_id)
    config_path = PROJECT_ROOT / experiment["config"]
    config = load_json(config_path)

    files: list[dict[str, Any]] = [
        {
            "role": "experiment_config",
            "path": relative(config_path),
            "bytes": config_path.stat().st_size,
            "sha256": sha256_file(config_path),
        },
    ]

    for suffix in ("_profile.json", "_profile.csv"):
        profile_path = config_path.with_name(f"{config_path.stem}{suffix}")
        if profile_path.exists():
            files.append(
                {
                    "role": "stimulus_profile",
                    "path": relative(profile_path),
                    "bytes": profile_path.stat().st_size,
                    "sha256": sha256_file(profile_path),
                }
            )

    audio_files: list[dict[str, Any]] = []
    if config.get("stimulusPresentation") == "audio":
        for order, stimulus in enumerate(config.get("stimuli", []), start=1):
            audio_path = audio_file_for(config, stimulus, order)
            if not audio_path.exists():
                raise FileNotFoundError(audio_path)
            audio_files.append(
                {
                    "order": order,
                    "stimulus": stimulus,
                    "path": relative(audio_path),
                    "bytes": audio_path.stat().st_size,
                    "sha256": sha256_file(audio_path),
                }
            )

    return {
        "schemaVersion": "lex30-freeze-v1",
        "frozenAt": datetime.now(timezone.utc).isoformat(),
        "experimentId": config.get("experimentId"),
        "experimentVersion": config.get("experimentVersion"),
        "label": config.get("label"),
        "registryEntry": {
            "id": experiment.get("id"),
            "label": experiment.get("label"),
            "config": experiment.get("config"),
            "mode": experiment.get("mode"),
            "status": experiment.get("status"),
        },
        "mode": config.get("mode"),
        "stimulusPresentation": config.get("stimulusPresentation"),
        "stimulusSetId": config.get("stimulusSetId"),
        "stimulusCount": len(config.get("stimuli", [])),
        "responseCount": config.get("responseCount"),
        "timerSeconds": config.get("timerSeconds"),
        "randomizeStimuli": config.get("randomizeStimuli"),
        "audioBasePath": config.get("audioBasePath"),
        "audioExtension": config.get("audioExtension"),
        "audioVersion": config.get("audioVersion"),
        "audioAutoplay": config.get("audioAutoplay"),
        "stimuli": config.get("stimuli", []),
        "files": files,
        "audioFiles": audio_files,
        "notes": [
            "This lock file records the exact config and audio file checksums for pilot administration.",
            "Rule-based scoring remains primary; optional GPT annotations are review metadata only.",
            "Spelling is preserved as typed unless a researcher supplies a manual override file during scoring.",
        ],
    }


def verify_freeze(path: Path) -> list[str]:
    freeze = load_json(path)
    errors: list[str] = []
    entries = list(freeze.get("files", [])) + list(freeze.get("audioFiles", []))
    for entry in entries:
        relative_path = entry.get("path")
        if not relative_path:
            errors.append("Entry is missing path")
            continue
        file_path = PROJECT_ROOT / relative_path
        if not file_path.exists():
            errors.append(f"Missing file: {relative_path}")
            continue
        actual_size = file_path.stat().st_size
        if actual_size != entry.get("bytes"):
            errors.append(f"Size mismatch for {relative_path}: {actual_size} != {entry.get('bytes')}")
        actual_hash = sha256_file(file_path)
        if actual_hash != entry.get("sha256"):
            errors.append(f"SHA-256 mismatch for {relative_path}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_id", nargs="?", default=DEFAULT_EXPERIMENT_ID)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    output = args.output or PROJECT_ROOT / "configs" / f"{args.experiment_id}.freeze.json"
    if args.verify:
        errors = verify_freeze(output)
        if errors:
            for error in errors:
                print(error)
            raise SystemExit(1)
        print(f"Freeze OK: {output.relative_to(PROJECT_ROOT)}")
        return

    freeze = build_freeze(args.experiment_id)
    output.write_text(json.dumps(freeze, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output.relative_to(PROJECT_ROOT))


if __name__ == "__main__":
    main()
