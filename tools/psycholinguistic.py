"""Psycholinguistic norm loaders used for stimulus review.

These variables are used as stimulus-selection controls, not as Lex30 scoring
rules.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from score_lex30 import DATA_ROOT


DEFAULT_CONCRETENESS_XLSX = DATA_ROOT / "Brysbaert et al. (2014)" / "13428_2013_403_MOESM1_ESM.xlsx"
DEFAULT_SUBTLEX_US_TSV = DATA_ROOT / "SUBTLEXus" / "SUBTLEXus74286wordstextversion.txt"

PSYCHOLINGUISTIC_FIELDS = [
    "concreteness_mean",
    "concreteness_sd",
    "concreteness_percent_known",
    "subtlex_freq_count",
    "subtlex_cd_count",
    "subtlex_subtlwf",
    "subtlex_lg10wf",
    "subtlex_subtlcd",
    "subtlex_lg10cd",
    "wordfreq_zipf",
    "familiarity_proxy",
    "psycholinguistic_flags",
]


def to_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def to_int(value: Any) -> int | None:
    number = to_float(value)
    return None if number is None else int(number)


def rounded(value: float | None, digits: int = 3) -> float | None:
    return None if value is None else round(value, digits)


def load_concreteness(path: Path = DEFAULT_CONCRETENESS_XLSX) -> dict[str, dict[str, float | int]]:
    if not path.exists():
        return {}

    from openpyxl import load_workbook

    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    header = ["" if item is None else str(item).strip() for item in next(rows, ())]
    index = {name: i for i, name in enumerate(header)}
    required = {"Word", "Conc.M", "Conc.SD", "Percent_known"}
    missing = required.difference(index)
    if missing:
        raise ValueError(f"Missing concreteness columns in {path}: {', '.join(sorted(missing))}")

    mapping: dict[str, dict[str, float | int]] = {}
    for row in rows:
        word = "" if row[index["Word"]] is None else str(row[index["Word"]]).strip().lower()
        if not word:
            continue
        mapping[word] = {
            "concreteness_mean": to_float(row[index["Conc.M"]]),
            "concreteness_sd": to_float(row[index["Conc.SD"]]),
            "concreteness_percent_known": to_float(row[index["Percent_known"]]),
        }
    return mapping


def load_subtlex_us(path: Path = DEFAULT_SUBTLEX_US_TSV) -> dict[str, dict[str, float | int]]:
    if not path.exists():
        return {}

    mapping: dict[str, dict[str, float | int]] = {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        required = {"Word", "FREQcount", "CDcount", "SUBTLWF", "Lg10WF", "SUBTLCD", "Lg10CD"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing SUBTLEX-US columns in {path}: {', '.join(sorted(missing))}")
        for row in reader:
            word = (row.get("Word") or "").strip().lower()
            if not word:
                continue
            mapping[word] = {
                "subtlex_freq_count": to_int(row.get("FREQcount")),
                "subtlex_cd_count": to_int(row.get("CDcount")),
                "subtlex_subtlwf": to_float(row.get("SUBTLWF")),
                "subtlex_lg10wf": to_float(row.get("Lg10WF")),
                "subtlex_subtlcd": to_float(row.get("SUBTLCD")),
                "subtlex_lg10cd": to_float(row.get("Lg10CD")),
            }
    return mapping


def wordfreq_zipf(word: str, enabled: bool = True) -> float | None:
    if not enabled:
        return None
    try:
        from wordfreq import zipf_frequency
    except ImportError:
        return None
    return float(zipf_frequency(word, "en"))


def familiarity_proxy(zipf: float | None, subtlex_cd: float | None) -> str:
    if zipf is None and subtlex_cd is None:
        return "unknown"
    if (zipf is not None and zipf >= 4.5) or (subtlex_cd is not None and subtlex_cd >= 2.0):
        return "high"
    if (zipf is not None and zipf >= 3.5) or (subtlex_cd is not None and subtlex_cd >= 1.0):
        return "medium"
    return "low"


def flags_for_metrics(metrics: dict[str, Any]) -> str:
    flags: list[str] = []
    concreteness = metrics.get("concreteness_mean")
    percent_known = metrics.get("concreteness_percent_known")
    zipf = metrics.get("wordfreq_zipf")
    subtlex_cd = metrics.get("subtlex_lg10cd")

    if concreteness is None:
        flags.append("missing_concreteness")
    elif concreteness < 2.0:
        flags.append("very_abstract_review")
    elif concreteness > 4.5:
        flags.append("very_concrete_review")

    if percent_known is not None and percent_known < 0.85:
        flags.append("low_percent_known")

    if zipf is None and subtlex_cd is None:
        flags.append("missing_familiarity_proxy")
    elif familiarity_proxy(zipf, subtlex_cd) == "low":
        flags.append("low_familiarity_proxy")

    return ";".join(flags)


def metrics_for_word(
    word: str,
    *,
    concreteness: dict[str, dict[str, float | int]],
    subtlex_us: dict[str, dict[str, float | int]],
    include_wordfreq: bool = True,
) -> dict[str, Any]:
    normalized = word.strip().lower()
    metrics: dict[str, Any] = {
        "concreteness_mean": None,
        "concreteness_sd": None,
        "concreteness_percent_known": None,
        "subtlex_freq_count": None,
        "subtlex_cd_count": None,
        "subtlex_subtlwf": None,
        "subtlex_lg10wf": None,
        "subtlex_subtlcd": None,
        "subtlex_lg10cd": None,
        "wordfreq_zipf": None,
        "familiarity_proxy": "unknown",
        "psycholinguistic_flags": "",
    }

    conc_row = concreteness.get(normalized)
    if conc_row:
        metrics.update({key: rounded(value) for key, value in conc_row.items()})

    subtlex_row = subtlex_us.get(normalized)
    if subtlex_row:
        metrics.update(
            {
                key: rounded(value) if isinstance(value, float) else value
                for key, value in subtlex_row.items()
            }
        )

    metrics["wordfreq_zipf"] = rounded(wordfreq_zipf(normalized, include_wordfreq), 3)
    metrics["familiarity_proxy"] = familiarity_proxy(
        metrics["wordfreq_zipf"],
        metrics["subtlex_lg10cd"],
    )
    metrics["psycholinguistic_flags"] = flags_for_metrics(metrics)
    return metrics
