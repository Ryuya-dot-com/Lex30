#!/usr/bin/env python3
"""Profile Lex30 stimulus sets against bundled vocabulary lists."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from score_lex30 import (
    DEFAULT_ANTBNC_PATH,
    DEFAULT_BNC_COCA_XLSX,
    DEFAULT_NGSL_LEMMAS_PATH,
    DEFAULT_NGSL_STATS_PATH,
    DEFAULT_NJ8_PATH,
    PROJECT_ROOT,
    antbnc_normalize,
    load_antbnc,
    load_bnc_coca_families,
    load_ngsl,
    load_nj8,
    lookup_bnc_coca,
    lookup_ngsl,
    lookup_nj8,
)
from psycholinguistic import (
    DEFAULT_CONCRETENESS_XLSX,
    DEFAULT_SUBTLEX_US_TSV,
    PSYCHOLINGUISTIC_FIELDS,
    load_concreteness,
    load_subtlex_us,
    metrics_for_word,
)
from pos_profile import POS_FIELDS, POS_ORDER, pos_metrics_for_word


PROFILE_FIELDS = [
    "experiment_id",
    "experiment_version",
    "stimulus_set_id",
    "mode",
    "stimulus_order",
    "stimulus",
    "normalized_stimulus",
    "antbnc_head",
    "letters",
    "is_single_alpha_token",
    "audio_surface_ok",
    "nj8_head",
    "nj8_rank",
    "nj8_band",
    "nj8_source",
    "bnc_coca_head",
    "bnc_coca_rank",
    "bnc_coca_band",
    "bnc_coca_source",
    "ngsl_head",
    "ngsl_rank",
    "ngsl_band",
    "ngsl_source",
    *PSYCHOLINGUISTIC_FIELDS,
    *POS_FIELDS,
    "in_all_lists",
    "off_list_any",
    "band_profile",
]

SINGLE_ALPHA_RE = re.compile(r"^[A-Za-z]+$")


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def profile_config(
    config: dict[str, Any],
    *,
    nj8: dict[str, int],
    bnc_coca: dict[str, dict[str, int | str]],
    ngsl: dict[str, dict[str, int | str]],
    antbnc: dict[str, str],
    concreteness: dict[str, dict[str, float | int]],
    subtlex_us: dict[str, dict[str, float | int]],
    include_wordfreq: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    stimuli = [str(item).strip() for item in config.get("stimuli", []) if str(item).strip()]

    for index, stimulus in enumerate(stimuli, start=1):
        normalized = stimulus.lower()
        antbnc_head = antbnc_normalize(normalized, antbnc)
        nj8_hit = lookup_nj8(normalized, nj8, antbnc)
        bnc_hit = lookup_bnc_coca(normalized, bnc_coca, antbnc)
        ngsl_hit = lookup_ngsl(normalized, ngsl, antbnc)
        psych_metrics = metrics_for_word(
            normalized,
            concreteness=concreteness,
            subtlex_us=subtlex_us,
            include_wordfreq=include_wordfreq,
        )
        is_single_alpha = bool(SINGLE_ALPHA_RE.fullmatch(stimulus))
        audio_surface_ok = is_single_alpha and 3 <= len(stimulus) <= 14
        in_all_lists = all(hit.rank is not None for hit in (nj8_hit, bnc_hit, ngsl_hit))
        off_list_any = any(hit.rank is None for hit in (nj8_hit, bnc_hit, ngsl_hit))

        rows.append(
            {
                "experiment_id": config.get("experimentId", ""),
                "experiment_version": config.get("experimentVersion", ""),
                "stimulus_set_id": config.get("stimulusSetId", ""),
                "mode": config.get("mode", ""),
                "stimulus_order": index,
                "stimulus": stimulus,
                "normalized_stimulus": normalized,
                "antbnc_head": antbnc_head,
                "letters": len(stimulus),
                "is_single_alpha_token": is_single_alpha,
                "audio_surface_ok": audio_surface_ok,
                "nj8_head": nj8_hit.head,
                "nj8_rank": nj8_hit.rank,
                "nj8_band": nj8_hit.band,
                "nj8_source": nj8_hit.source,
                "bnc_coca_head": bnc_hit.head,
                "bnc_coca_rank": bnc_hit.rank,
                "bnc_coca_band": bnc_hit.band,
                "bnc_coca_source": bnc_hit.source,
                "ngsl_head": ngsl_hit.head,
                "ngsl_rank": ngsl_hit.rank,
                "ngsl_band": ngsl_hit.band,
                "ngsl_source": ngsl_hit.source,
                **psych_metrics,
                **pos_metrics_for_word(normalized),
                "in_all_lists": in_all_lists,
                "off_list_any": off_list_any,
                "band_profile": f"NJ8:{nj8_hit.band or 'off'}|BNC:{bnc_hit.band or 'off'}|NGSL:{ngsl_hit.band or 'off'}",
            }
        )

    summary = summarize(rows)
    summary.update(
        {
            "experiment_id": config.get("experimentId", ""),
            "experiment_version": config.get("experimentVersion", ""),
            "stimulus_set_id": config.get("stimulusSetId", ""),
            "mode": config.get("mode", ""),
        }
    )
    return rows, summary


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    def band_counts(prefix: str) -> dict[str, int]:
        counts = Counter(str(row.get(f"{prefix}_band") or "off") for row in rows)
        return dict(sorted(counts.items(), key=lambda item: (item[0] == "off", item[0])))

    def mean_of(field: str) -> float | None:
        values = [
            float(row[field])
            for row in rows
            if row.get(field) not in (None, "")
        ]
        return round(sum(values) / len(values), 3) if values else None

    return {
        "stimulus_count": len(rows),
        "single_alpha_tokens": sum(1 for row in rows if row["is_single_alpha_token"]),
        "audio_surface_ok": sum(1 for row in rows if row["audio_surface_ok"]),
        "in_all_lists": sum(1 for row in rows if row["in_all_lists"]),
        "off_list_any": sum(1 for row in rows if row["off_list_any"]),
        "nj8_band_counts": band_counts("nj8"),
        "bnc_coca_band_counts": band_counts("bnc_coca"),
        "ngsl_band_counts": band_counts("ngsl"),
        "concreteness_available": sum(1 for row in rows if row.get("concreteness_mean") not in (None, "")),
        "concreteness_mean": mean_of("concreteness_mean"),
        "wordfreq_zipf_mean": mean_of("wordfreq_zipf"),
        "subtlex_lg10cd_mean": mean_of("subtlex_lg10cd"),
        "familiarity_proxy_counts": dict(Counter(str(row.get("familiarity_proxy") or "unknown") for row in rows)),
        "psycholinguistic_flag_counts": dict(
            Counter(
                flag
                for row in rows
                for flag in str(row.get("psycholinguistic_flags") or "").split(";")
                if flag
            )
        ),
        "wordnet_primary_pos_counts": dict(
            Counter(str(row.get("wordnet_primary_pos") or "unknown") for row in rows)
        ),
        "wordnet_possible_pos_counts": {
            pos: sum(
                1
                for row in rows
                if pos in str(row.get("wordnet_possible_pos") or "").split(";")
            )
            for pos in POS_ORDER
        },
        "wordnet_multi_pos_count": sum(
            1
            for row in rows
            if len([pos for pos in str(row.get("wordnet_possible_pos") or "").split(";") if pos]) > 1
        ),
        "pos_review_flag_counts": dict(
            Counter(
                flag
                for row in rows
                for flag in str(row.get("pos_review_flags") or "").split(";")
                if flag
            )
        ),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=PROFILE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "config",
        type=Path,
        nargs="?",
        default=PROJECT_ROOT / "configs" / "lex30-original-written-v1.json",
        help="Experiment config JSON containing a stimuli array.",
    )
    parser.add_argument("--output-csv", type=Path, help="Stimulus-level profile CSV.")
    parser.add_argument("--output-json", type=Path, help="Profile summary JSON.")
    parser.add_argument("--nj8", type=Path, default=DEFAULT_NJ8_PATH)
    parser.add_argument("--bnc-coca-xlsx", type=Path, default=DEFAULT_BNC_COCA_XLSX)
    parser.add_argument("--antbnc", type=Path, default=DEFAULT_ANTBNC_PATH)
    parser.add_argument("--ngsl-stats", type=Path, default=DEFAULT_NGSL_STATS_PATH)
    parser.add_argument("--ngsl-lemmas", type=Path, default=DEFAULT_NGSL_LEMMAS_PATH)
    parser.add_argument("--concreteness-xlsx", type=Path, default=DEFAULT_CONCRETENESS_XLSX)
    parser.add_argument("--subtlex-us", type=Path, default=DEFAULT_SUBTLEX_US_TSV)
    parser.add_argument("--no-wordfreq", action="store_true", help="Do not call the wordfreq Python package.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    config = load_config(args.config)
    output_csv = args.output_csv or args.config.with_name(f"{args.config.stem}_profile.csv")
    output_json = args.output_json or args.config.with_name(f"{args.config.stem}_profile.json")

    antbnc = load_antbnc(args.antbnc)
    rows, summary = profile_config(
        config,
        nj8=load_nj8(args.nj8),
        bnc_coca=load_bnc_coca_families(args.bnc_coca_xlsx),
        ngsl=load_ngsl(args.ngsl_stats, args.ngsl_lemmas),
        antbnc=antbnc,
        concreteness=load_concreteness(args.concreteness_xlsx),
        subtlex_us=load_subtlex_us(args.subtlex_us),
        include_wordfreq=not args.no_wordfreq,
    )

    write_csv(output_csv, rows)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote {output_csv}")
    print(f"Wrote {output_json}")
    print(
        "Stimuli={stimulus_count}, in all lists={in_all_lists}, off-list-any={off_list_any}, "
        "audio-surface-ok={audio_surface_ok}".format(**summary)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
