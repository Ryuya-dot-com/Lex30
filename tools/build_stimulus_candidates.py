#!/usr/bin/env python3
"""Build a stimulus-candidate pool from bundled vocabulary lists."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

from score_lex30 import (
    DEFAULT_ANTBNC_PATH,
    DEFAULT_BNC_COCA_XLSX,
    DEFAULT_NGSL_LEMMAS_PATH,
    DEFAULT_NGSL_STATS_PATH,
    DEFAULT_NJ8_PATH,
    PROJECT_ROOT,
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
from pos_profile import POS_FIELDS, pos_metrics_for_word


CANDIDATE_FIELDS = [
    "candidate",
    "letters",
    "nj8_head",
    "nj8_rank",
    "nj8_band",
    "bnc_coca_head",
    "bnc_coca_rank",
    "bnc_coca_band",
    "ngsl_head",
    "ngsl_rank",
    "ngsl_band",
    "pronunciation_risk",
    *PSYCHOLINGUISTIC_FIELDS,
    *POS_FIELDS,
    "in_original_lex30",
    "recommended_for_written_pilot",
    "recommended_for_audio_pilot",
    "exclusion_reason",
]

ALPHA_RE = re.compile(r"^[a-z]+$")
FUNCTION_LIKE = {
    "a", "an", "the", "and", "or", "but", "if", "of", "to", "in", "on", "at", "by", "for",
    "from", "with", "as", "than", "that", "this", "these", "those", "is", "are", "was",
    "were", "be", "been", "being", "do", "does", "did", "have", "has", "had", "will",
    "would", "can", "could", "may", "might", "must", "shall", "should", "not", "no", "yes",
    "i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves", "you",
    "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "itself", "its", "they", "them", "their", "theirs",
    "themselves", "who", "whom", "whose",
    "about", "above", "across", "after", "against", "ago", "ahead", "all", "almost",
    "already", "also", "although", "always", "among", "another", "any", "anyone",
    "anything", "around", "before", "behind", "below", "beneath", "beside", "between",
    "both", "during", "each", "either", "else", "enough", "even", "ever", "every",
    "everyone", "everything", "few", "here", "however", "just", "least", "less", "little",
    "many", "more", "most", "much", "near", "never", "now", "once", "only", "other",
    "often", "perhaps", "quite", "rather", "really", "same", "several", "since", "so", "some",
    "someone", "something", "still", "such", "then", "there", "therefore", "though",
    "through", "thus", "too", "toward", "under", "until", "upon", "usually", "very", "when",
    "where", "whether", "while", "why", "inside", "outside", "within", "without", "yet",
}

PRONUNCIATION_RISK = {
    "close",
    "conduct",
    "content",
    "contract",
    "contrast",
    "convert",
    "convict",
    "digest",
    "does",
    "entrance",
    "export",
    "import",
    "increase",
    "insult",
    "invalid",
    "lead",
    "live",
    "minute",
    "moderate",
    "object",
    "perfect",
    "permit",
    "present",
    "produce",
    "progress",
    "project",
    "protest",
    "rebel",
    "record",
    "refuse",
    "reject",
    "separate",
    "subject",
    "suspect",
    "tear",
    "use",
    "wind",
    "wound",
}


def load_original_stimuli(path: Path) -> set[str]:
    if not path.exists():
        return set()
    config = json.loads(path.read_text(encoding="utf-8"))
    return {str(item).strip().lower() for item in config.get("stimuli", []) if str(item).strip()}


def exclusion_reason(
    word: str,
    *,
    nj8_band: int | None,
    bnc_band: int | None,
    ngsl_band: int | None,
    in_original: bool,
    min_letters: int,
    max_letters: int,
) -> str:
    reasons: list[str] = []
    if not ALPHA_RE.fullmatch(word):
        reasons.append("non_alpha")
    if not (min_letters <= len(word) <= max_letters):
        reasons.append("length")
    if word in FUNCTION_LIKE:
        reasons.append("function_like")
    if in_original:
        reasons.append("original_lex30")
    if word in PRONUNCIATION_RISK:
        reasons.append("pronunciation_risk")
    if nj8_band is None:
        reasons.append("nj8_off_list")
    if bnc_band is None:
        reasons.append("bnc_coca_off_list")
    if ngsl_band is None:
        reasons.append("ngsl_off_list")
    return ";".join(reasons)


def build_candidates(
    *,
    nj8: dict[str, int],
    bnc_coca: dict[str, dict[str, int | str]],
    ngsl: dict[str, dict[str, int | str]],
    antbnc: dict[str, str],
    concreteness: dict[str, dict[str, float | int]],
    subtlex_us: dict[str, dict[str, float | int]],
    original_stimuli: set[str],
    min_letters: int,
    max_letters: int,
    include_wordfreq: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for word in sorted(nj8):
        if not word:
            continue
        nj8_hit = lookup_nj8(word, nj8, antbnc)
        bnc_hit = lookup_bnc_coca(word, bnc_coca, antbnc)
        ngsl_hit = lookup_ngsl(word, ngsl, antbnc)
        psych_metrics = metrics_for_word(
            word,
            concreteness=concreteness,
            subtlex_us=subtlex_us,
            include_wordfreq=include_wordfreq,
        )
        in_original = word in original_stimuli
        reason = exclusion_reason(
            word,
            nj8_band=nj8_hit.band,
            bnc_band=bnc_hit.band,
            ngsl_band=ngsl_hit.band,
            in_original=in_original,
            min_letters=min_letters,
            max_letters=max_letters,
        )
        recommended_written = not reason
        recommended_audio = recommended_written and 3 <= len(word) <= 12
        rows.append(
            {
                "candidate": word,
                "letters": len(word),
                "nj8_head": nj8_hit.head,
                "nj8_rank": nj8_hit.rank,
                "nj8_band": nj8_hit.band,
                "bnc_coca_head": bnc_hit.head,
                "bnc_coca_rank": bnc_hit.rank,
                "bnc_coca_band": bnc_hit.band,
                "ngsl_head": ngsl_hit.head,
                "ngsl_rank": ngsl_hit.rank,
                "ngsl_band": ngsl_hit.band,
                "pronunciation_risk": word in PRONUNCIATION_RISK,
                **psych_metrics,
                **pos_metrics_for_word(word),
                "in_original_lex30": in_original,
                "recommended_for_written_pilot": recommended_written,
                "recommended_for_audio_pilot": recommended_audio,
                "exclusion_reason": reason,
            }
        )
    return rows


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=PROJECT_ROOT / "tools" / "generated" / "stimulus_candidates.csv",
    )
    parser.add_argument(
        "--original-config",
        type=Path,
        default=PROJECT_ROOT / "configs" / "lex30-original-written-v1.json",
    )
    parser.add_argument("--min-letters", type=int, default=3)
    parser.add_argument("--max-letters", type=int, default=12)
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
    antbnc = load_antbnc(args.antbnc)
    rows = build_candidates(
        nj8=load_nj8(args.nj8),
        bnc_coca=load_bnc_coca_families(args.bnc_coca_xlsx),
        ngsl=load_ngsl(args.ngsl_stats, args.ngsl_lemmas),
        antbnc=antbnc,
        concreteness=load_concreteness(args.concreteness_xlsx),
        subtlex_us=load_subtlex_us(args.subtlex_us),
        original_stimuli=load_original_stimuli(args.original_config),
        min_letters=args.min_letters,
        max_letters=args.max_letters,
        include_wordfreq=not args.no_wordfreq,
    )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CANDIDATE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    written = sum(1 for row in rows if row["recommended_for_written_pilot"])
    audio = sum(1 for row in rows if row["recommended_for_audio_pilot"])
    print(f"Wrote {args.output_csv}")
    print(f"Candidates={len(rows)}, written-pilot={written}, audio-pilot={audio}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
