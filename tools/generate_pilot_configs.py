#!/usr/bin/env python3
"""Generate draft Updated Lex30 pilot configs from the candidate pool."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from score_lex30 import PROJECT_ROOT


DEFAULT_CANDIDATES = PROJECT_ROOT / "tools" / "generated" / "stimulus_candidates.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "configs"
DEFAULT_SELECTION_CSV = PROJECT_ROOT / "tools" / "generated" / "updated_pilot_stimuli_v0.1.csv"
DEFAULT_EASYCUE_SELECTION_CSV = PROJECT_ROOT / "tools" / "generated" / "updated_easycue_pilot_stimuli_v0.2.csv"
DEFAULT_POSBALANCED_EASYCUE_SELECTION_CSV = (
    PROJECT_ROOT / "tools" / "generated" / "updated_easycue_posbalanced_pilot_stimuli_v0.3.csv"
)
DEFAULT_ORIGINAL_PROFILE = PROJECT_ROOT / "configs" / "lex30-original-written-v1_profile.json"
DEFAULT_SEED = "updated-lex30-pilot-v0.1"
DEFAULT_EASYCUE_SEED = "updated-lex30-easycue-pilot-v0.2"
DEFAULT_POSBALANCED_EASYCUE_SEED = "updated-lex30-easycue-posbalanced-pilot-v0.3"
DEFAULT_POS_TARGETS = {"noun": 18, "verb": 8, "adjective": 4}

ABSTRACT_SUFFIXES = (
    "tion",
    "sion",
    "ment",
    "ness",
    "ity",
    "ance",
    "ence",
    "ism",
    "ship",
)

SELECTION_FIELDS = [
    "stimulus_order",
    "candidate",
    "letters",
    "initial",
    "nj8_rank",
    "nj8_band",
    "bnc_coca_rank",
    "bnc_coca_band",
    "ngsl_rank",
    "ngsl_band",
    "concreteness_mean",
    "concreteness_percent_known",
    "wordfreq_zipf",
    "subtlex_lg10wf",
    "subtlex_lg10cd",
    "familiarity_proxy",
    "psycholinguistic_flags",
    "wordnet_primary_pos",
    "wordnet_possible_pos",
    "wordnet_pos_counts",
    "pos_review_flags",
    "selection_score",
    "selection_notes",
]


def load_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def as_int(value: Any) -> int | None:
    text = str(value or "").strip()
    return int(text) if text.isdigit() else None


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def stable_hash(seed: str, word: str) -> int:
    digest = hashlib.sha256(f"{seed}:{word}".encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


def target_nj8_counts(path: Path) -> dict[int, int]:
    if not path.exists():
        return {1: 16, 2: 8, 3: 4, 4: 2}
    profile = json.loads(path.read_text(encoding="utf-8"))
    counts = profile.get("nj8_band_counts", {})
    targets = {int(band): int(count) for band, count in counts.items() if str(band).isdigit() and int(band) <= 4}
    return targets or {1: 16, 2: 8, 3: 4, 4: 2}


def target_pos_counts(path: Path) -> dict[str, int]:
    if not path.exists():
        return dict(DEFAULT_POS_TARGETS)
    profile = json.loads(path.read_text(encoding="utf-8"))
    counts = profile.get("wordnet_primary_pos_counts", {})
    targets = {
        pos: int(counts.get(pos, 0))
        for pos in ("noun", "verb", "adjective")
        if int(counts.get(pos, 0)) > 0
    }
    return targets if sum(targets.values()) == 30 else dict(DEFAULT_POS_TARGETS)


def candidate_score(row: dict[str, Any], seed: str) -> tuple[int, int, int, int, int]:
    word = str(row["candidate"]).strip().lower()
    letters = as_int(row.get("letters")) or len(word)
    nj8_band = as_int(row.get("nj8_band")) or 99
    bnc_band = as_int(row.get("bnc_coca_band")) or 99
    ngsl_band = as_int(row.get("ngsl_band")) or 99
    suffix_penalty = 3 if word.endswith(ABSTRACT_SUFFIXES) else 0
    psych_flags = set(str(row.get("psycholinguistic_flags") or "").split(";"))
    psych_penalty = 0
    if "low_familiarity_proxy" in psych_flags:
        psych_penalty += 5
    if "low_percent_known" in psych_flags:
        psych_penalty += 3
    if "missing_concreteness" in psych_flags:
        psych_penalty += 2
    if "very_abstract_review" in psych_flags:
        psych_penalty += 1
    length_penalty = abs(6 - letters)
    cross_list_penalty = abs(bnc_band - nj8_band) + abs(ngsl_band - nj8_band)
    return (
        suffix_penalty + cross_list_penalty + psych_penalty,
        length_penalty,
        as_int(row.get("nj8_rank")) or 999999,
        stable_hash(seed, word),
        letters,
    )


def selection_notes(row: dict[str, Any]) -> str:
    word = str(row["candidate"]).strip().lower()
    notes: list[str] = []
    if word.endswith(ABSTRACT_SUFFIXES):
        notes.append("abstract_suffix_review")
    if len(word) > 9:
        notes.append("long_audio_review")
    psych_flags = str(row.get("psycholinguistic_flags") or "")
    if psych_flags:
        notes.append(psych_flags)
    pos_flags = str(row.get("pos_review_flags") or "")
    if pos_flags:
        notes.append(pos_flags)
    return ";".join(notes)


def select_stimuli(
    rows: list[dict[str, Any]],
    *,
    targets: dict[int, int],
    seed: str,
    max_initial: int,
    max_nj8_rank: int | None,
) -> list[dict[str, Any]]:
    pool = [
        row
        for row in rows
        if as_bool(row.get("recommended_for_audio_pilot"))
        and not as_bool(row.get("in_original_lex30"))
        and as_int(row.get("nj8_band")) in targets
        and (max_nj8_rank is None or (as_int(row.get("nj8_rank")) or 999999) <= max_nj8_rank)
    ]
    pool.sort(key=lambda row: candidate_score(row, seed))

    selected: list[dict[str, Any]] = []
    selected_words: set[str] = set()
    initial_counts: Counter[str] = Counter()

    for band, target_count in sorted(targets.items()):
        band_rows = [row for row in pool if as_int(row.get("nj8_band")) == band]
        picked_for_band = 0

        for row in band_rows:
            word = str(row["candidate"]).strip().lower()
            initial = word[0]
            if word in selected_words:
                continue
            if initial_counts[initial] >= max_initial:
                continue
            selected.append(row)
            selected_words.add(word)
            initial_counts[initial] += 1
            picked_for_band += 1
            if picked_for_band == target_count:
                break

        if picked_for_band < target_count:
            for row in band_rows:
                word = str(row["candidate"]).strip().lower()
                if word in selected_words:
                    continue
                selected.append(row)
                selected_words.add(word)
                picked_for_band += 1
                if picked_for_band == target_count:
                    break

        if picked_for_band < target_count:
            raise RuntimeError(f"Not enough candidates for NJ8 band {band}: needed {target_count}, got {picked_for_band}")

    selected.sort(key=lambda row: stable_hash(seed, str(row["candidate"]).strip().lower()))
    return selected


def select_stimuli_by_pos(
    rows: list[dict[str, Any]],
    *,
    pos_targets: dict[str, int],
    seed: str,
    max_initial: int,
    max_nj8_rank: int,
) -> list[dict[str, Any]]:
    pool = [
        row
        for row in rows
        if as_bool(row.get("recommended_for_audio_pilot"))
        and not as_bool(row.get("in_original_lex30"))
        and as_int(row.get("nj8_band")) == 1
        and (as_int(row.get("nj8_rank")) or 999999) <= max_nj8_rank
        and str(row.get("wordnet_primary_pos") or "") in pos_targets
    ]
    pool.sort(key=lambda row: candidate_score(row, seed))

    selected: list[dict[str, Any]] = []
    selected_words: set[str] = set()
    initial_counts: Counter[str] = Counter()

    for pos, target_count in pos_targets.items():
        pos_rows = [row for row in pool if str(row.get("wordnet_primary_pos") or "") == pos]
        picked_for_pos = 0

        for row in pos_rows:
            word = str(row["candidate"]).strip().lower()
            initial = word[0]
            if word in selected_words:
                continue
            if initial_counts[initial] >= max_initial:
                continue
            selected.append(row)
            selected_words.add(word)
            initial_counts[initial] += 1
            picked_for_pos += 1
            if picked_for_pos == target_count:
                break

        if picked_for_pos < target_count:
            for row in pos_rows:
                word = str(row["candidate"]).strip().lower()
                if word in selected_words:
                    continue
                selected.append(row)
                selected_words.add(word)
                picked_for_pos += 1
                if picked_for_pos == target_count:
                    break

        if picked_for_pos < target_count:
            raise RuntimeError(f"Not enough candidates for WordNet primary POS {pos}: needed {target_count}, got {picked_for_pos}")

    selected.sort(key=lambda row: stable_hash(seed, str(row["candidate"]).strip().lower()))
    return selected


def config_payload(
    *,
    experiment_id: str,
    experiment_version: str,
    label: str,
    mode: str,
    stimulus_presentation: str,
    stimulus_set_id: str,
    audio_base_path: str,
    stimuli: list[str],
    selection_metadata: dict[str, Any],
) -> dict[str, Any]:
    instructions = (
        "You will see 30 English words. For each word, type up to 4 words that come to your mind. "
        "Press SPACE to go to the next word at any time, or wait 30 seconds and it will move on automatically."
    )
    if stimulus_presentation == "audio":
        instructions = (
            "You will hear 30 English words. For each word, type up to 4 words that come to your mind. "
            "Press SPACE to go to the next word at any time, or wait 30 seconds and it will move on automatically."
        )

    payload = {
        "experimentId": experiment_id,
        "experimentVersion": experiment_version,
        "label": label,
        "mode": mode,
        "stimulusPresentation": stimulus_presentation,
        "stimulusSetId": stimulus_set_id,
        "responseCount": 4,
        "answerMaxLength": 30,
        "timerSeconds": 30,
        "advanceKey": "Space",
        "randomizeStimuli": False,
        "downloadPrefix": "lex30_results",
        "instructions": instructions,
        "selectionMetadata": selection_metadata,
        "stimuli": stimuli,
    }
    if stimulus_presentation == "audio":
        payload.update(
            {
                "audioBasePath": audio_base_path,
                "audioExtension": "mp3",
                "audioVersion": f"{experiment_version}-{stimulus_set_id}",
                "audioAutoplay": True,
            }
        )
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_selection_csv(path: Path, rows: list[dict[str, Any]], seed: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=SELECTION_FIELDS)
        writer.writeheader()
        for order, row in enumerate(rows, start=1):
            word = str(row["candidate"]).strip().lower()
            writer.writerow(
                {
                    "stimulus_order": order,
                    "candidate": word,
                    "letters": row.get("letters", ""),
                    "initial": word[0],
                    "nj8_rank": row.get("nj8_rank", ""),
                    "nj8_band": row.get("nj8_band", ""),
                    "bnc_coca_rank": row.get("bnc_coca_rank", ""),
                    "bnc_coca_band": row.get("bnc_coca_band", ""),
                    "ngsl_rank": row.get("ngsl_rank", ""),
                    "ngsl_band": row.get("ngsl_band", ""),
                    "concreteness_mean": row.get("concreteness_mean", ""),
                    "concreteness_percent_known": row.get("concreteness_percent_known", ""),
                    "wordfreq_zipf": row.get("wordfreq_zipf", ""),
                    "subtlex_lg10wf": row.get("subtlex_lg10wf", ""),
                    "subtlex_lg10cd": row.get("subtlex_lg10cd", ""),
                    "familiarity_proxy": row.get("familiarity_proxy", ""),
                    "psycholinguistic_flags": row.get("psycholinguistic_flags", ""),
                    "wordnet_primary_pos": row.get("wordnet_primary_pos", ""),
                    "wordnet_possible_pos": row.get("wordnet_possible_pos", ""),
                    "wordnet_pos_counts": row.get("wordnet_pos_counts", ""),
                    "pos_review_flags": row.get("pos_review_flags", ""),
                    "selection_score": "|".join(str(item) for item in candidate_score(row, seed)),
                    "selection_notes": selection_notes(row),
                }
            )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--original-profile", type=Path, default=DEFAULT_ORIGINAL_PROFILE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--selection-csv", type=Path)
    parser.add_argument("--seed")
    parser.add_argument("--max-initial", type=int, default=2)
    parser.add_argument(
        "--easy-cue",
        action="store_true",
        help="Generate v0.2 configs using only NJ8 K1 cues with rank <= --max-nj8-rank.",
    )
    parser.add_argument(
        "--pos-balanced-easy-cue",
        action="store_true",
        help="Generate v0.3 configs using easy NJ8 K1 cues while matching the original WordNet primary-POS profile.",
    )
    parser.add_argument("--max-nj8-rank", type=int, help="Maximum allowed NJ8 rank for stimulus cues.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if not args.candidates.exists():
        raise FileNotFoundError(f"{args.candidates} does not exist. Run tools/build_stimulus_candidates.py first.")

    pos_targets: dict[str, int] | None = None
    if args.pos_balanced_easy_cue:
        seed = args.seed or DEFAULT_POSBALANCED_EASYCUE_SEED
        selection_csv = args.selection_csv or DEFAULT_POSBALANCED_EASYCUE_SELECTION_CSV
        targets = {1: 30}
        pos_targets = target_pos_counts(args.original_profile)
        max_nj8_rank = args.max_nj8_rank or 1000
        experiment_version = "0.3.0"
        stimulus_set_id = "updated-easycue-posbalanced-pilot-30-v0.3"
        written_id = "updated-written-easycue-posbalanced-pilot-v0.3"
        listening_id = "updated-listening-easycue-posbalanced-pilot-v0.3"
        written_label = "Updated Lex30 - written easy-cue POS-balanced pilot v0.3"
        listening_label = "Updated Lex30 - listening easy-cue POS-balanced pilot v0.3"
        written_path = args.output_dir / f"{written_id}.json"
        listening_path = args.output_dir / f"{listening_id}.json"
        audio_base_path = f"audio/{listening_id}"
        cue_policy = (
            "All stimulus cues must be NJ8 K1 with rank <= 1000, and WordNet primary-POS counts "
            "must match the original Lex30 baseline."
        )
    elif args.easy_cue:
        seed = args.seed or DEFAULT_EASYCUE_SEED
        selection_csv = args.selection_csv or DEFAULT_EASYCUE_SELECTION_CSV
        targets = {1: 30}
        max_nj8_rank = args.max_nj8_rank or 1000
        experiment_version = "0.2.0"
        stimulus_set_id = "updated-easycue-pilot-30-v0.2"
        written_id = "updated-written-easycue-pilot-v0.2"
        listening_id = "updated-listening-easycue-pilot-v0.2"
        written_label = "Updated Lex30 - written easy-cue pilot v0.2"
        listening_label = "Updated Lex30 - listening easy-cue pilot v0.2"
        written_path = args.output_dir / f"{written_id}.json"
        listening_path = args.output_dir / f"{listening_id}.json"
        audio_base_path = f"audio/{listening_id}"
        cue_policy = "All stimulus cues must be NJ8 K1 with rank <= 1000."
    else:
        seed = args.seed or DEFAULT_SEED
        selection_csv = args.selection_csv or DEFAULT_SELECTION_CSV
        targets = target_nj8_counts(args.original_profile)
        max_nj8_rank = args.max_nj8_rank
        experiment_version = "0.1.0"
        stimulus_set_id = "updated-pilot-30-v0.1"
        written_id = "updated-written-pilot-v0.1"
        listening_id = "updated-listening-pilot-v0.1"
        written_label = "Updated Lex30 - written pilot v0.1"
        listening_label = "Updated Lex30 - listening pilot v0.1"
        written_path = args.output_dir / f"{written_id}.json"
        listening_path = args.output_dir / f"{listening_id}.json"
        audio_base_path = f"audio/{listening_id}"
        cue_policy = "NJ8 band counts are matched to the original Lex30 baseline."

    rows = load_rows(args.candidates)
    if pos_targets is None:
        selected = select_stimuli(
            rows,
            targets=targets,
            seed=seed,
            max_initial=args.max_initial,
            max_nj8_rank=max_nj8_rank,
        )
    else:
        selected = select_stimuli_by_pos(
            rows,
            pos_targets=pos_targets,
            seed=seed,
            max_initial=args.max_initial,
            max_nj8_rank=max_nj8_rank or 1000,
        )
    stimuli = [str(row["candidate"]).strip().lower() for row in selected]
    selection_metadata = {
        "status": "draft_for_researcher_review",
        "sourceCandidateFile": str(args.candidates.relative_to(PROJECT_ROOT) if args.candidates.is_relative_to(PROJECT_ROOT) else args.candidates),
        "seed": seed,
        "targetNj8BandCounts": {str(key): value for key, value in sorted(targets.items())},
        "targetWordNetPrimaryPosCounts": pos_targets or {},
        "maxNj8Rank": max_nj8_rank,
        "cueDifficultyPolicy": cue_policy,
        "selectionRule": (
            "Recommended audio candidates only; original Lex30 cues excluded; "
            "cross-list band mismatch, psycholinguistic review flags, abstract suffixes, word length, NJ8 rank, "
            "WordNet primary POS targets when requested, and stable hash used for deterministic ordering."
        ),
        "reviewWarning": "This is a draft candidate set, not a validated final Updated Lex30 stimulus set.",
    }

    write_selection_csv(selection_csv, selected, seed)
    write_json(
        written_path,
        config_payload(
            experiment_id=written_id,
            experiment_version=experiment_version,
            label=written_label,
            mode="written",
            stimulus_presentation="text",
            stimulus_set_id=stimulus_set_id,
            audio_base_path=audio_base_path,
            stimuli=stimuli,
            selection_metadata=selection_metadata,
        ),
    )
    write_json(
        listening_path,
        config_payload(
            experiment_id=listening_id,
            experiment_version=experiment_version,
            label=listening_label,
            mode="listening",
            stimulus_presentation="audio",
            stimulus_set_id=stimulus_set_id,
            audio_base_path=audio_base_path,
            stimuli=stimuli,
            selection_metadata=selection_metadata,
        ),
    )

    print(f"Wrote {selection_csv}")
    print(f"Wrote {written_path}")
    print(f"Wrote {listening_path}")
    print("Stimuli: " + ", ".join(stimuli))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
