#!/usr/bin/env python3
"""Score Lex30 CSV exports for research use.

This script keeps deterministic list-based scoring separate from optional GPT
annotation. The rule scores are the columns to use for primary Lex30 scoring;
GPT output is written as review metadata only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - requirements guard
    load_dotenv = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "tools" / "data"
DEFAULT_NJ8_PATH = DATA_ROOT / "NJ8" / "NJ8.csv"
DEFAULT_BNC_COCA_XLSX = DATA_ROOT / "bnc_coca" / "BNC_COCA_lists.xlsx"
DEFAULT_ANTBNC_PATH = DATA_ROOT / "antbnc" / "antbnc_lemmas_ver_004.txt"
DEFAULT_NGSL_STATS_PATH = DATA_ROOT / "ngsl" / "NGSL_1.2_stats.csv"
DEFAULT_NGSL_LEMMAS_PATH = DATA_ROOT / "ngsl" / "NGSL_1.2_lemmatized_for_research.csv"
DEFAULT_ENV_PATH = Path("/Users/tohokusla/Desktop/.env")

ANSWER_COLUMNS = ("Answer1", "Answer2", "Answer3", "Answer4")
WORD_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*")
BNC_COCA_LEVEL_RE = re.compile(r"^\s*(\d+)\s*k\s*$", re.IGNORECASE)
BNC_COCA_RELATED_FORM_RE = re.compile(r"([^,()]+?)\s*\((\d+)\)")

RELATION_CATEGORIES = (
    "lexical_set",
    "other_conceptual",
    "collocation",
    "free_combination",
    "form_based",
    "form_and_meaning",
    "position_and_meaning",
    "erratic",
    "no_response",
    "invalid_or_non_english",
    "proper_noun",
    "uncertain",
)

SUMMARY_FIELDS = [
    "source_file",
    "participant_session_id",
    "analysis_session_key",
    "participant_id",
    "response_slots",
    "multiword_response_slots",
    "extra_tokens_in_response_slots",
    "multiword_slot_percent",
    "lexical_tokens",
    "valid_in_list_tokens",
    "no_response_slots",
    "both_off_list_review_tokens",
    "list_disagreement_tokens",
    "stimulus_repetitions",
    "nj8_token_score",
    "nj8_type_score",
    "nj8_token_percent",
    "nj8_token_percent_of_lexical_tokens",
    "nj8_token_percent_of_response_slots",
    "bnc_coca_token_score",
    "bnc_coca_type_score",
    "bnc_coca_token_percent",
    "bnc_coca_token_percent_of_lexical_tokens",
    "bnc_coca_token_percent_of_response_slots",
    "ngsl_token_score",
    "ngsl_type_score",
    "ngsl_token_percent",
    "ngsl_token_percent_of_lexical_tokens",
    "ngsl_token_percent_of_response_slots",
    "ngsl_off_list_tokens",
]

REVIEW_FIELDS = [
    "source_files",
    "stimulus",
    "response_token",
    "lookup_token",
    "normalized_head",
    "oov_status",
    "nj8_status",
    "bnc_coca_status",
    "ngsl_status",
    "list_disagreement",
    "manual_override_applied",
    "occurrences",
    "participants",
    "analysis_sessions",
    "participant_ids",
    "analysis_session_keys",
    "example_raw_response",
    "suggested_corrected_form",
    "review_note",
]


@dataclass
class RankHit:
    head: str | None
    rank: int | None
    band: int | None
    source: str


@dataclass
class ScoredToken:
    source_file: str
    participant_session_id: str
    analysis_session_key: str
    participant_id: str
    stimulus: str
    answer_column: str
    response_order: int
    token_index: int
    raw_response: str
    slot_token_count: int
    extra_tokens_in_slot: int
    is_extra_token_in_slot: bool
    response_token: str
    normalized_token: str
    lookup_token: str
    normalized_head: str
    manual_override_applied: bool
    manual_corrected_form: str | None
    manual_override_note: str | None
    is_empty_response: bool
    is_lexical_token: bool
    is_stimulus_repetition: bool
    duplicate_token_count_so_far: int
    nj8_head: str | None
    nj8_rank: int | None
    nj8_band: int | None
    nj8_source: str
    nj8_score_token: int
    nj8_score_type: int
    bnc_coca_head: str | None
    bnc_coca_rank: int | None
    bnc_coca_band: int | None
    bnc_coca_source: str
    bnc_coca_score_token: int
    bnc_coca_score_type: int
    ngsl_head: str | None
    ngsl_rank: int | None
    ngsl_band: int | None
    ngsl_source: str
    ngsl_score_token: int
    ngsl_score_type: int
    nj8_status: str
    bnc_coca_status: str
    ngsl_status: str
    list_disagreement: bool
    oov_status: str
    needs_human_review: bool
    gpt_validity: str | None = None
    gpt_relation_category: str | None = None
    gpt_corrected_form: str | None = None
    gpt_confidence: float | None = None
    gpt_needs_human_review: bool | None = None
    gpt_note: str | None = None


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def level_of(rank: int | None) -> int | None:
    return None if rank is None else (rank - 1) // 1000 + 1


def score_from_band(band: int | None) -> int:
    return 1 if band is not None and band > 1 else 0


def split_response(text: str) -> list[str]:
    return WORD_RE.findall(text or "")


def analysis_session_key(source_file: str, participant_session_id: str, participant_id: str) -> str:
    parts = [source_file or "unknown_source", participant_session_id or "no_session", participant_id or "anonymous"]
    return "::".join(parts)


def load_nj8(path: Path) -> dict[str, int]:
    rank: dict[str, int] = {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.reader(fh):
            if not row or len(row) < 2 or not row[0].strip().isdigit():
                continue
            r = int(row[0])
            raw = row[1].strip()
            head = re.sub(r"\s*\([^)]*\)\s*$", "", raw).lower()
            if head:
                rank.setdefault(head, r)
            match = re.search(r"\(([^)]*)\)", raw)
            if match:
                for variant in re.split(r"[,\s]+", match.group(1)):
                    variant = variant.strip().lower()
                    if variant:
                        rank.setdefault(variant, r)
    return rank


def load_antbnc(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    mapping: dict[str, str] = {}
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if "->" in line:
                head, rest = line.split("->", 1)
                forms = re.split(r"[,\s]+", rest.strip())
            else:
                parts = re.split(r"\t+", line)
                head, forms = parts[0], parts[1:]
            head = head.strip().lower()
            if not head:
                continue
            mapping.setdefault(head, head)
            for form in forms:
                form = form.strip().lower()
                if form:
                    mapping.setdefault(form, head)
    return mapping


def load_bnc_coca_families(path: Path) -> dict[str, dict[str, int | str]]:
    from openpyxl import load_workbook

    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    header = ["" if value is None else str(value).strip().lower() for value in next(rows, ())]
    try:
        list_idx = next(i for i, value in enumerate(header) if value.startswith("list"))
        head_idx = next(i for i, value in enumerate(header) if value.startswith("headword"))
        related_idx = next(i for i, value in enumerate(header) if value.startswith("related"))
    except StopIteration as exc:
        raise ValueError(f"Unexpected BNC/COCA family list header in {path}") from exc

    rank: dict[str, dict[str, int | str]] = {}
    per_level_seen: Counter[int] = Counter()
    for row in rows:
        label = "" if row[list_idx] is None else str(row[list_idx]).strip()
        match = BNC_COCA_LEVEL_RE.match(label)
        if not match:
            continue
        level = int(match.group(1))
        per_level_seen[level] += 1
        ordinal = min(per_level_seen[level], 1000)
        family_rank = (level - 1) * 1000 + ordinal
        family_head = "" if row[head_idx] is None else str(row[head_idx]).strip().lower()
        if not family_head:
            continue
        related_text = "" if row[related_idx] is None else str(row[related_idx])
        forms = {
            form.strip().lower()
            for form, _freq in BNC_COCA_RELATED_FORM_RE.findall(related_text)
            if form.strip()
        }
        forms.add(family_head)
        entry = {"head": family_head, "rank": family_rank, "level": level}
        for form in forms:
            rank.setdefault(form, entry)
    return rank


def load_ngsl(stats_path: Path, lemmas_path: Path) -> dict[str, dict[str, int | str]]:
    ranks_by_head: dict[str, int] = {}
    with stats_path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"Lemma", "SFI Rank"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required NGSL stats columns in {stats_path}: {', '.join(sorted(missing))}")
        for row in reader:
            head = (row.get("Lemma") or "").strip().lower()
            rank_text = (row.get("SFI Rank") or "").strip()
            if not head or not rank_text.isdigit():
                continue
            ranks_by_head[head] = int(rank_text)

    mapping: dict[str, dict[str, int | str]] = {}

    def add_form(form: str, head: str, rank: int) -> None:
        form = form.strip().lower()
        if not form:
            return
        existing = mapping.get(form)
        if existing is None or int(existing["rank"]) > rank:
            mapping[form] = {"head": head, "rank": rank, "level": level_of(rank) or 0}

    with lemmas_path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.reader(line for line in fh if not line.startswith("#")):
            if not row:
                continue
            head = row[0].strip().lower()
            rank = ranks_by_head.get(head)
            if not head or rank is None:
                continue
            add_form(head, head, rank)
            for form in row[1:]:
                add_form(form, head, rank)

    for head, rank in ranks_by_head.items():
        add_form(head, head, rank)
    return mapping


def antbnc_normalize(token: str, antbnc: dict[str, str]) -> str:
    token = token.lower()
    return antbnc.get(token, token)


def lookup_nj8(token: str, nj8: dict[str, int], antbnc: dict[str, str]) -> RankHit:
    if token in nj8:
        rank = nj8[token]
        return RankHit(token, rank, level_of(rank), "surface")
    head = antbnc_normalize(token, antbnc)
    if head in nj8:
        rank = nj8[head]
        return RankHit(head, rank, level_of(rank), "antbnc")
    return RankHit(head or token, None, None, "off_list")


def lookup_bnc_coca(
    token: str,
    bnc_coca: dict[str, dict[str, int | str]],
    antbnc: dict[str, str],
) -> RankHit:
    if token in bnc_coca:
        entry = bnc_coca[token]
        rank = int(entry["rank"])
        return RankHit(str(entry["head"]), rank, level_of(rank), "surface_family")
    head = antbnc_normalize(token, antbnc)
    if head in bnc_coca:
        entry = bnc_coca[head]
        rank = int(entry["rank"])
        return RankHit(str(entry["head"]), rank, level_of(rank), "antbnc_family")
    return RankHit(head or token, None, None, "off_list")


def lookup_ngsl(
    token: str,
    ngsl: dict[str, dict[str, int | str]],
    antbnc: dict[str, str],
) -> RankHit:
    if token in ngsl:
        entry = ngsl[token]
        rank = int(entry["rank"])
        return RankHit(str(entry["head"]), rank, level_of(rank), "surface_ngsl")
    head = antbnc_normalize(token, antbnc)
    if head in ngsl:
        entry = ngsl[head]
        rank = int(entry["rank"])
        return RankHit(str(entry["head"]), rank, level_of(rank), "antbnc_ngsl")
    return RankHit(head or token, None, None, "off_list")


def list_status(
    *,
    is_empty: bool,
    is_lexical: bool,
    is_repetition: bool,
    hit: RankHit,
) -> str:
    if is_empty:
        return "no_response"
    if not is_lexical:
        return "invalid_or_non_lexical"
    if is_repetition:
        return "stimulus_repetition"
    return "in_list" if hit.rank is not None else "off_list"


def derive_oov_status(
    *,
    is_empty: bool,
    is_lexical: bool,
    is_repetition: bool,
    nj8_hit: RankHit,
    bnc_hit: RankHit,
) -> tuple[str, bool, str, str, bool]:
    nj8_status = list_status(
        is_empty=is_empty,
        is_lexical=is_lexical,
        is_repetition=is_repetition,
        hit=nj8_hit,
    )
    bnc_status = list_status(
        is_empty=is_empty,
        is_lexical=is_lexical,
        is_repetition=is_repetition,
        hit=bnc_hit,
    )
    list_disagreement = nj8_status != bnc_status
    if is_empty:
        return "no_response", False, nj8_status, bnc_status, list_disagreement
    if not is_lexical:
        return "invalid_or_non_lexical", True, nj8_status, bnc_status, list_disagreement
    if is_repetition:
        return "stimulus_repetition", False, nj8_status, bnc_status, list_disagreement
    if nj8_hit.rank is not None and bnc_hit.rank is not None:
        return "both_in_list", False, nj8_status, bnc_status, list_disagreement
    if nj8_hit.rank is not None:
        return "nj8_only", False, nj8_status, bnc_status, list_disagreement
    if bnc_hit.rank is not None:
        return "bnc_coca_only", False, nj8_status, bnc_status, list_disagreement
    return "both_off_list_review", True, nj8_status, bnc_status, list_disagreement


def read_lex30_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    required = {"Participant", "Stimulus", *ANSWER_COLUMNS}
    missing = required.difference(reader.fieldnames or [])
    if missing:
        raise ValueError(f"Missing required columns in {path}: {', '.join(sorted(missing))}")
    for row in rows:
        row["_source_file"] = path.name
    return rows


def collect_input_csvs(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    if not input_path.is_dir():
        raise FileNotFoundError(input_path)

    excluded_stems = ("_scored", "_summary", "_review")
    paths = [
        path
        for path in sorted(input_path.glob("*.csv"))
        if not path.name.startswith(".")
        and path.name != "manual_overrides.csv"
        and not path.stem.endswith(excluded_stems)
    ]
    if not paths:
        raise ValueError(f"No raw Lex30 CSV files found in {input_path}")
    return paths


def read_lex30_csvs(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        rows.extend(read_lex30_csv(path))
    return rows


def load_manual_overrides(path: Path | None) -> dict[tuple[str, str], dict[str, str]]:
    """Load optional no-API spelling overrides.

    Expected columns:
      token, corrected_form, note

    Optional stimulus column can scope an override to one cue word:
      stimulus, token, corrected_form, note
    """
    if not path:
        return {}
    overrides: dict[tuple[str, str], dict[str, str]] = {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"token", "corrected_form"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required override columns in {path}: {', '.join(sorted(missing))}")
        for row in reader:
            token = (row.get("token") or "").strip().lower()
            corrected = (row.get("corrected_form") or "").strip().lower()
            stimulus = (row.get("stimulus") or "").strip().lower()
            if not token or not corrected:
                continue
            overrides[(stimulus, token)] = {
                "corrected_form": corrected,
                "note": (row.get("note") or "").strip(),
            }
    return overrides


def manual_override_for(
    overrides: dict[tuple[str, str], dict[str, str]],
    *,
    stimulus: str,
    token: str,
) -> dict[str, str] | None:
    normalized_stimulus = stimulus.strip().lower()
    normalized_token = token.strip().lower()
    return overrides.get((normalized_stimulus, normalized_token)) or overrides.get(("", normalized_token))


def score_rows(
    raw_rows: list[dict[str, str]],
    *,
    nj8: dict[str, int],
    bnc_coca: dict[str, dict[str, int | str]],
    ngsl: dict[str, dict[str, int | str]],
    antbnc: dict[str, str],
    manual_overrides: dict[tuple[str, str], dict[str, str]] | None = None,
) -> list[ScoredToken]:
    scored: list[ScoredToken] = []
    seen_by_participant: defaultdict[str, Counter[str]] = defaultdict(Counter)
    manual_overrides = manual_overrides or {}

    for raw_row in raw_rows:
        source_file = (raw_row.get("_source_file") or "").strip()
        participant_session_id = (raw_row.get("ParticipantSessionId") or "").strip()
        participant = (raw_row.get("Participant") or "").strip()
        session_key = analysis_session_key(source_file, participant_session_id, participant)
        participant_scope = session_key
        stimulus = (raw_row.get("Stimulus") or "").strip()
        stimulus_norm = antbnc_normalize(stimulus.lower(), antbnc)

        for order, col in enumerate(ANSWER_COLUMNS, start=1):
            response = (raw_row.get(col) or "").strip()
            tokens = split_response(response)
            if not tokens:
                empty_hit = RankHit(None, None, None, "no_response")
                scored.append(
                    ScoredToken(
                        source_file=source_file,
                        participant_session_id=participant_session_id,
                        analysis_session_key=session_key,
                        participant_id=participant,
                        stimulus=stimulus,
                        answer_column=col,
                        response_order=order,
                        token_index=0,
                        raw_response=response,
                        slot_token_count=0,
                        extra_tokens_in_slot=0,
                        is_extra_token_in_slot=False,
                        response_token="",
                        normalized_token="",
                        lookup_token="",
                        normalized_head="",
                        manual_override_applied=False,
                        manual_corrected_form=None,
                        manual_override_note=None,
                        is_empty_response=True,
                        is_lexical_token=False,
                        is_stimulus_repetition=False,
                        duplicate_token_count_so_far=0,
                        nj8_head=None,
                        nj8_rank=None,
                        nj8_band=None,
                        nj8_source="no_response",
                        nj8_score_token=0,
                        nj8_score_type=0,
                        bnc_coca_head=None,
                        bnc_coca_rank=None,
                        bnc_coca_band=None,
                        bnc_coca_source="no_response",
                        bnc_coca_score_token=0,
                        bnc_coca_score_type=0,
                        ngsl_head=None,
                        ngsl_rank=None,
                        ngsl_band=None,
                        ngsl_source="no_response",
                        ngsl_score_token=0,
                        ngsl_score_type=0,
                        nj8_status="no_response",
                        bnc_coca_status="no_response",
                        ngsl_status="no_response",
                        list_disagreement=False,
                        oov_status="no_response",
                        needs_human_review=False,
                    )
                )
                continue

            for token_index, token in enumerate(tokens, start=1):
                normalized = token.lower()
                override = manual_override_for(manual_overrides, stimulus=stimulus, token=normalized)
                lookup_token = override["corrected_form"] if override else normalized
                is_lexical = bool(WORD_RE.fullmatch(token))
                normalized_head = antbnc_normalize(lookup_token, antbnc)
                is_repetition = normalized_head == stimulus_norm
                duplicate_count = seen_by_participant[participant_scope][normalized_head]
                seen_by_participant[participant_scope][normalized_head] += 1

                nj8_hit = lookup_nj8(lookup_token, nj8, antbnc)
                bnc_hit = lookup_bnc_coca(lookup_token, bnc_coca, antbnc)
                ngsl_hit = lookup_ngsl(lookup_token, ngsl, antbnc)
                oov_status, needs_review, nj8_status, bnc_status, list_disagreement = derive_oov_status(
                    is_empty=False,
                    is_lexical=is_lexical,
                    is_repetition=is_repetition,
                    nj8_hit=nj8_hit,
                    bnc_hit=bnc_hit,
                )
                ngsl_status = list_status(
                    is_empty=False,
                    is_lexical=is_lexical,
                    is_repetition=is_repetition,
                    hit=ngsl_hit,
                )

                nj8_token_score = 0 if is_repetition else score_from_band(nj8_hit.band)
                bnc_token_score = 0 if is_repetition else score_from_band(bnc_hit.band)
                ngsl_token_score = 0 if is_repetition else score_from_band(ngsl_hit.band)
                is_first_type = duplicate_count == 0
                scored.append(
                    ScoredToken(
                        source_file=source_file,
                        participant_session_id=participant_session_id,
                        analysis_session_key=session_key,
                        participant_id=participant,
                        stimulus=stimulus,
                        answer_column=col,
                        response_order=order,
                        token_index=token_index,
                        raw_response=response,
                        slot_token_count=len(tokens),
                        extra_tokens_in_slot=max(0, len(tokens) - 1),
                        is_extra_token_in_slot=token_index > 1,
                        response_token=token,
                        normalized_token=normalized,
                        lookup_token=lookup_token,
                        normalized_head=normalized_head,
                        manual_override_applied=bool(override),
                        manual_corrected_form=override["corrected_form"] if override else None,
                        manual_override_note=override["note"] if override else None,
                        is_empty_response=False,
                        is_lexical_token=is_lexical,
                        is_stimulus_repetition=is_repetition,
                        duplicate_token_count_so_far=duplicate_count,
                        nj8_head=nj8_hit.head,
                        nj8_rank=nj8_hit.rank,
                        nj8_band=nj8_hit.band,
                        nj8_source=nj8_hit.source,
                        nj8_score_token=nj8_token_score,
                        nj8_score_type=nj8_token_score if is_first_type else 0,
                        bnc_coca_head=bnc_hit.head,
                        bnc_coca_rank=bnc_hit.rank,
                        bnc_coca_band=bnc_hit.band,
                        bnc_coca_source=bnc_hit.source,
                        bnc_coca_score_token=bnc_token_score,
                        bnc_coca_score_type=bnc_token_score if is_first_type else 0,
                        ngsl_head=ngsl_hit.head,
                        ngsl_rank=ngsl_hit.rank,
                        ngsl_band=ngsl_hit.band,
                        ngsl_source=ngsl_hit.source,
                        ngsl_score_token=ngsl_token_score,
                        ngsl_score_type=ngsl_token_score if is_first_type else 0,
                        nj8_status=nj8_status,
                        bnc_coca_status=bnc_status,
                        ngsl_status=ngsl_status,
                        list_disagreement=list_disagreement,
                        oov_status=oov_status,
                        needs_human_review=needs_review,
                    )
                )
    return scored


def aggregate(scored: list[ScoredToken]) -> list[dict[str, Any]]:
    by_participant: dict[tuple[str, str, str], list[ScoredToken]] = defaultdict(list)
    for row in scored:
        by_participant[(row.source_file, row.participant_session_id, row.participant_id)].append(row)

    summary: list[dict[str, Any]] = []
    for (source_file, participant_session_id, participant), rows in sorted(by_participant.items()):
        lexical_rows = [r for r in rows if r.is_lexical_token and not r.is_stimulus_repetition]
        valid_rows = [r for r in lexical_rows if r.oov_status in {"both_in_list", "nj8_only", "bnc_coca_only"}]
        response_slots = {
            (r.stimulus, r.answer_column)
            for r in rows
        }
        response_slot_count = len(response_slots)
        multiword_slots = {
            (r.stimulus, r.answer_column)
            for r in rows
            if r.extra_tokens_in_slot > 0
        }
        nj8_token_score = sum(r.nj8_score_token for r in rows)
        bnc_token_score = sum(r.bnc_coca_score_token for r in rows)
        ngsl_token_score = sum(r.ngsl_score_token for r in rows)
        nj8_lexical_percent = round(100 * nj8_token_score / len(lexical_rows), 2) if lexical_rows else 0.0
        bnc_lexical_percent = round(100 * bnc_token_score / len(lexical_rows), 2) if lexical_rows else 0.0
        ngsl_lexical_percent = round(100 * ngsl_token_score / len(lexical_rows), 2) if lexical_rows else 0.0
        summary.append(
            {
                "source_file": source_file,
                "participant_session_id": participant_session_id,
                "analysis_session_key": analysis_session_key(source_file, participant_session_id, participant),
                "participant_id": participant,
                "response_slots": response_slot_count,
                "multiword_response_slots": len(multiword_slots),
                "extra_tokens_in_response_slots": sum(1 for r in rows if r.is_extra_token_in_slot),
                "multiword_slot_percent": round(100 * len(multiword_slots) / response_slot_count, 2) if response_slot_count else 0.0,
                "lexical_tokens": len(lexical_rows),
                "valid_in_list_tokens": len(valid_rows),
                "no_response_slots": sum(1 for r in rows if r.is_empty_response),
                "both_off_list_review_tokens": sum(1 for r in rows if r.oov_status == "both_off_list_review"),
                "list_disagreement_tokens": sum(1 for r in rows if r.list_disagreement),
                "stimulus_repetitions": sum(1 for r in rows if r.is_stimulus_repetition),
                "nj8_token_score": nj8_token_score,
                "nj8_type_score": sum(r.nj8_score_type for r in rows),
                "nj8_token_percent": nj8_lexical_percent,
                "nj8_token_percent_of_lexical_tokens": nj8_lexical_percent,
                "nj8_token_percent_of_response_slots": round(100 * nj8_token_score / response_slot_count, 2) if response_slot_count else 0.0,
                "bnc_coca_token_score": bnc_token_score,
                "bnc_coca_type_score": sum(r.bnc_coca_score_type for r in rows),
                "bnc_coca_token_percent": bnc_lexical_percent,
                "bnc_coca_token_percent_of_lexical_tokens": bnc_lexical_percent,
                "bnc_coca_token_percent_of_response_slots": round(100 * bnc_token_score / response_slot_count, 2) if response_slot_count else 0.0,
                "ngsl_token_score": ngsl_token_score,
                "ngsl_type_score": sum(r.ngsl_score_type for r in rows),
                "ngsl_token_percent": ngsl_lexical_percent,
                "ngsl_token_percent_of_lexical_tokens": ngsl_lexical_percent,
                "ngsl_token_percent_of_response_slots": round(100 * ngsl_token_score / response_slot_count, 2) if response_slot_count else 0.0,
                "ngsl_off_list_tokens": sum(1 for r in lexical_rows if r.ngsl_status == "off_list"),
            }
        )
    return summary


def review_items(scored: list[ScoredToken]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str, str, str, str, str], list[ScoredToken]] = defaultdict(list)
    for row in scored:
        if row.is_empty_response or row.is_stimulus_repetition:
            continue
        if not (row.needs_human_review or row.list_disagreement or row.manual_override_applied):
            continue
        key = (
            row.stimulus,
            row.response_token.lower(),
            row.lookup_token,
            row.normalized_head,
            row.oov_status,
            row.nj8_status,
            row.bnc_coca_status,
            row.ngsl_status,
        )
        grouped[key].append(row)

    review_rows: list[dict[str, Any]] = []
    for key, rows in sorted(grouped.items()):
        stimulus, response_token, lookup_token, normalized_head, oov_status, nj8_status, bnc_status, ngsl_status = key
        source_files = sorted({row.source_file for row in rows if row.source_file})
        participants = sorted({row.participant_id for row in rows if row.participant_id})
        session_keys = sorted({row.analysis_session_key for row in rows if row.analysis_session_key})
        first = rows[0]
        review_rows.append(
            {
                "source_files": ";".join(source_files),
                "stimulus": stimulus,
                "response_token": response_token,
                "lookup_token": lookup_token,
                "normalized_head": normalized_head,
                "oov_status": oov_status,
                "nj8_status": nj8_status,
                "bnc_coca_status": bnc_status,
                "ngsl_status": ngsl_status,
                "list_disagreement": any(row.list_disagreement for row in rows),
                "manual_override_applied": any(row.manual_override_applied for row in rows),
                "occurrences": len(rows),
                "participants": len(participants),
                "analysis_sessions": len(session_keys),
                "participant_ids": ";".join(participants),
                "analysis_session_keys": ";".join(session_keys),
                "example_raw_response": first.raw_response,
                "suggested_corrected_form": first.manual_corrected_form or "",
                "review_note": first.manual_override_note or "",
            }
        )
    return review_rows


def gpt_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "annotations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "string"},
                        "validity": {
                            "type": "string",
                            "enum": [
                                "valid_english_word",
                                "misspelling_or_typo",
                                "proper_noun",
                                "non_english",
                                "not_a_word",
                                "uncertain",
                            ],
                        },
                        "relation_category": {"type": "string", "enum": list(RELATION_CATEGORIES)},
                        "corrected_form": {"type": ["string", "null"]},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "needs_human_review": {"type": "boolean"},
                        "note": {"type": "string"},
                    },
                    "required": [
                        "id",
                        "validity",
                        "relation_category",
                        "corrected_form",
                        "confidence",
                        "needs_human_review",
                        "note",
                    ],
                },
            }
        },
        "required": ["annotations"],
    }


def annotate_with_gpt(
    scored: list[ScoredToken],
    *,
    model: str,
    env_path: Path | None,
    batch_size: int = 40,
) -> None:
    if load_dotenv and env_path and env_path.exists():
        load_dotenv(env_path)
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set. Provide --env or export it before --with-gpt.")

    from openai import OpenAI

    client = OpenAI()
    targets = [
        row
        for row in scored
        if row.is_lexical_token and not row.is_stimulus_repetition
    ]
    for start in range(0, len(targets), batch_size):
        batch = targets[start : start + batch_size]
        payload = [
            {
                "id": f"{start + i}",
                "stimulus": row.stimulus,
                "response": row.response_token,
                "raw_response": row.raw_response,
                "nj8_band": row.nj8_band,
                "bnc_coca_band": row.bnc_coca_band,
                "oov_status": row.oov_status,
            }
            for i, row in enumerate(batch)
        ]
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You annotate second-language word association responses. "
                        "Do not decide the Lex30 score. Classify validity and the cue-response "
                        "relationship for research review. Be conservative: mark uncertain "
                        "or needs_human_review when the relation is ambiguous."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(payload, ensure_ascii=False),
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "lex30_gpt_annotations",
                    "schema": gpt_schema(),
                    "strict": True,
                }
            },
        )
        parsed = json.loads(response.output_text)
        by_id = {item["id"]: item for item in parsed["annotations"]}
        for i, row in enumerate(batch):
            annotation = by_id.get(f"{start + i}")
            if not annotation:
                row.gpt_validity = "uncertain"
                row.gpt_relation_category = "uncertain"
                row.gpt_needs_human_review = True
                row.gpt_note = "Missing GPT annotation for this row."
                continue
            row.gpt_validity = annotation["validity"]
            row.gpt_relation_category = annotation["relation_category"]
            row.gpt_corrected_form = annotation["corrected_form"]
            row.gpt_confidence = annotation["confidence"]
            row.gpt_needs_human_review = annotation["needs_human_review"]
            row.gpt_note = annotation["note"]


def write_csv(path: Path, scored: list[ScoredToken]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [asdict(row) for row in scored]
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_dict_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(
    path: Path,
    scored: list[ScoredToken],
    summary: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
    metadata: dict[str, Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": metadata,
        "summary": summary,
        "review_items": review_rows,
        "responses": [asdict(row) for row in scored],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path, help="Raw Lex30 CSV file, or a directory of raw CSV files.")
    parser.add_argument("--output-csv", type=Path, help="Detailed scored response CSV.")
    parser.add_argument("--output-json", type=Path, help="Detailed JSON with metadata and summary.")
    parser.add_argument("--output-summary-csv", type=Path, help="Participant-level summary CSV.")
    parser.add_argument("--output-review-csv", type=Path, help="Aggregated human-review item CSV.")
    parser.add_argument("--nj8", type=Path, default=DEFAULT_NJ8_PATH, help="Path to NJ8.csv.")
    parser.add_argument(
        "--bnc-coca-xlsx",
        type=Path,
        default=DEFAULT_BNC_COCA_XLSX,
        help="Path to Nation BNC/COCA word-family spreadsheet.",
    )
    parser.add_argument(
        "--antbnc",
        type=Path,
        default=DEFAULT_ANTBNC_PATH,
        help="Path to AntBNC lemma list for fallback normalization.",
    )
    parser.add_argument(
        "--ngsl-stats",
        type=Path,
        default=DEFAULT_NGSL_STATS_PATH,
        help="Path to NGSL stats CSV.",
    )
    parser.add_argument(
        "--ngsl-lemmas",
        type=Path,
        default=DEFAULT_NGSL_LEMMAS_PATH,
        help="Path to NGSL lemmatized-for-research CSV.",
    )
    parser.add_argument(
        "--manual-overrides",
        type=Path,
        help=(
            "Optional CSV for no-API spelling corrections. Columns: token, corrected_form, note. "
            "Optional stimulus column scopes a correction to one cue."
        ),
    )
    parser.add_argument("--with-gpt", action="store_true", help="Add GPT annotations. Not used for rule score.")
    parser.add_argument("--gpt-model", default=os.environ.get("LEX30_GPT_MODEL", "gpt-5.5"))
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV_PATH, help="Optional .env file for OPENAI_API_KEY.")
    return parser.parse_args(argv)


def default_output_paths(input_path: Path, args: argparse.Namespace) -> tuple[Path, Path, Path, Path]:
    if input_path.is_dir():
        base_dir = input_path
        stem = input_path.name
    else:
        base_dir = input_path.parent
        stem = input_path.stem
    return (
        args.output_csv or base_dir / f"{stem}_scored.csv",
        args.output_json or base_dir / f"{stem}_scored.json",
        args.output_summary_csv or base_dir / f"{stem}_summary.csv",
        args.output_review_csv or base_dir / f"{stem}_review.csv",
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    input_path = args.input_path
    if not input_path.exists():
        raise FileNotFoundError(input_path)
    input_csvs = collect_input_csvs(input_path)
    output_csv, output_json, output_summary_csv, output_review_csv = default_output_paths(input_path, args)

    nj8 = load_nj8(args.nj8)
    bnc_coca = load_bnc_coca_families(args.bnc_coca_xlsx)
    ngsl = load_ngsl(args.ngsl_stats, args.ngsl_lemmas)
    antbnc = load_antbnc(args.antbnc)
    manual_overrides = load_manual_overrides(args.manual_overrides)
    raw_rows = read_lex30_csvs(input_csvs)
    scored = score_rows(
        raw_rows,
        nj8=nj8,
        bnc_coca=bnc_coca,
        ngsl=ngsl,
        antbnc=antbnc,
        manual_overrides=manual_overrides,
    )

    if args.with_gpt:
        annotate_with_gpt(scored, model=args.gpt_model, env_path=args.env)

    summary = aggregate(scored)
    review_rows = review_items(scored)
    metadata = {
        "input_path": str(input_path),
        "input_csvs": [str(path) for path in input_csvs],
        "nj8_path": str(args.nj8),
        "nj8_sha256": sha256_file(args.nj8),
        "bnc_coca_xlsx": str(args.bnc_coca_xlsx),
        "bnc_coca_sha256": sha256_file(args.bnc_coca_xlsx),
        "ngsl_stats_path": str(args.ngsl_stats),
        "ngsl_stats_sha256": sha256_file(args.ngsl_stats),
        "ngsl_lemmas_path": str(args.ngsl_lemmas),
        "ngsl_lemmas_sha256": sha256_file(args.ngsl_lemmas),
        "antbnc_path": str(args.antbnc),
        "antbnc_sha256": sha256_file(args.antbnc),
        "manual_overrides_path": str(args.manual_overrides) if args.manual_overrides else None,
        "manual_overrides_sha256": sha256_file(args.manual_overrides) if args.manual_overrides else None,
        "manual_overrides_count": len(manual_overrides),
        "scoring_policy": {
            "primary_rule": "K1=0, K2+=1, off-list=review; stimulus repetitions score 0.",
            "nj8_unit": "POS-less flemma/head lookup with AntBNC fallback.",
            "bnc_coca_unit": "Nation BNC/COCA word-family lookup with related forms.",
            "ngsl_unit": "NGSL headword/rank lookup with lemmatized-for-research forms.",
            "oov_status": "both_in_list / nj8_only / bnc_coca_only / both_off_list_review are reported separately.",
            "spelling_policy": (
                "No automatic spelling correction is applied. Misspellings are scored as typed; "
                "unmatched forms remain review items unless --manual-overrides is supplied."
            ),
            "multiword_slot_policy": (
                "All lexical tokens in an answer slot are currently tokenized and scored. "
                "multiword_response_slots and extra_tokens_in_response_slots flag potential score inflation for review."
            ),
            "gpt_role": "annotation only; not included in rule scores.",
        },
        "gpt_enabled": bool(args.with_gpt),
        "gpt_model": args.gpt_model if args.with_gpt else None,
    }

    write_csv(output_csv, scored)
    write_dict_csv(output_summary_csv, summary, SUMMARY_FIELDS)
    write_dict_csv(output_review_csv, review_rows, REVIEW_FIELDS)
    write_json(output_json, scored, summary, review_rows, metadata)

    print(f"Wrote {output_csv}")
    print(f"Wrote {output_summary_csv}")
    print(f"Wrote {output_review_csv}")
    print(f"Wrote {output_json}")
    for row in summary:
        label = row.get("analysis_session_key") or (
            f"{row['source_file']}:{row['participant_id']}" if row["source_file"] else row["participant_id"]
        )
        print(
            "{label}: NJ8 type={nj8_type_score}, BNC/COCA type={bnc_coca_type_score}, NGSL type={ngsl_type_score}, "
            "both-off-list review={both_off_list_review_tokens}, list disagreements={list_disagreement_tokens}".format(
                label=label,
                **row,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
