"""WordNet-based part-of-speech review helpers for stimulus selection.

These fields describe which content-word POS categories a stimulus can take in
WordNet. They are review controls, not scoring rules and not context-sensitive
POS tags.
"""
from __future__ import annotations

from typing import Any


POS_FIELDS = [
    "wordnet_primary_pos",
    "wordnet_possible_pos",
    "wordnet_pos_counts",
    "pos_review_flags",
]

POS_ORDER = ("noun", "verb", "adjective", "adverb")


def _empty_metrics(flag: str) -> dict[str, Any]:
    return {
        "wordnet_primary_pos": "unknown",
        "wordnet_possible_pos": "",
        "wordnet_pos_counts": "",
        "pos_review_flags": flag,
    }


def _wordnet_counts(word: str) -> dict[str, int] | None:
    try:
        from nltk.corpus import wordnet as wn
    except ImportError:
        return None

    try:
        return {
            "noun": len(wn.synsets(word, pos=wn.NOUN)),
            "verb": len(wn.synsets(word, pos=wn.VERB)),
            "adjective": len(wn.synsets(word, pos=wn.ADJ)) + len(wn.synsets(word, pos=wn.ADJ_SAT)),
            "adverb": len(wn.synsets(word, pos=wn.ADV)),
        }
    except LookupError:
        return None


def pos_metrics_for_word(word: str) -> dict[str, Any]:
    normalized = word.strip().lower()
    if not normalized:
        return _empty_metrics("missing_wordnet_pos")

    counts = _wordnet_counts(normalized)
    if counts is None:
        return _empty_metrics("wordnet_unavailable")

    possible = [pos for pos in POS_ORDER if counts[pos] > 0]
    if not possible:
        return _empty_metrics("missing_wordnet_pos")

    max_count = max(counts.values())
    primary_candidates = [pos for pos in POS_ORDER if counts[pos] == max_count and max_count > 0]
    primary = primary_candidates[0] if len(primary_candidates) == 1 else "ambiguous"

    flags: list[str] = []
    if len(possible) > 1:
        flags.append("multi_pos_review")
    if primary == "ambiguous":
        flags.append("ambiguous_primary_review")
    if primary == "adverb" or ("adverb" in possible and len(possible) == 1):
        flags.append("adverb_review")

    return {
        "wordnet_primary_pos": primary,
        "wordnet_possible_pos": ";".join(possible),
        "wordnet_pos_counts": ";".join(f"{pos}={counts[pos]}" for pos in POS_ORDER),
        "pos_review_flags": ";".join(flags),
    }
