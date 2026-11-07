#!/usr/bin/env python3
"""Extract acoustic voice-onset latencies (Naming RT) and optional ASR transcripts from spoken Lex30 exports."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import struct
import tempfile
import wave
import zipfile
from pathlib import Path
from typing import Any


WORD_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*")
FILLER_WORDS = {"uh", "um", "umm", "uhh", "er", "erm", "ah", "ahh", "hmm", "hm", "mm", "eh"}

# Common English homophone sets where frequency-band membership (K1 vs K2+) can diverge.
# shortcut: static high-impact homophone table (~48 groups); upgrade to CMUdict pronunciation-key grouping if exhaustive rare homophones are needed.
HOMOPHONE_GROUPS: tuple[tuple[str, ...], ...] = (
    ("night", "knight"),
    ("sun", "son"),
    ("sea", "see"),
    ("write", "right", "rite"),
    ("flower", "flour"),
    ("peace", "piece"),
    ("bare", "bear"),
    ("wait", "weight"),
    ("weak", "week"),
    ("mail", "male"),
    ("plain", "plane"),
    ("sail", "sale"),
    ("steal", "steel"),
    ("tail", "tale"),
    ("waist", "waste"),
    ("stair", "stare"),
    ("brake", "break"),
    ("cell", "sell"),
    ("cent", "scent"),
    ("die", "dye"),
    ("fair", "fare"),
    ("heal", "heel"),
    ("hear", "here"),
    ("hole", "whole"),
    ("hour", "our"),
    ("knot", "not"),
    ("meat", "meet"),
    ("pair", "pear"),
    ("pray", "prey"),
    ("principal", "principle"),
    ("rain", "reign", "rein"),
    ("road", "rode"),
    ("role", "roll"),
    ("root", "route"),
    ("scene", "seen"),
    ("seam", "seem"),
    ("sole", "soul"),
    ("some", "sum"),
    ("stationary", "stationery"),
    ("suite", "sweet"),
    ("weather", "whether"),
    ("witch", "which"),
    ("wood", "would"),
    ("board", "bored"),
    ("aloud", "allowed"),
    ("altar", "alter"),
    ("cereal", "serial"),
    ("coarse", "course"),
    ("morning", "mourning"),
    ("profit", "prophet"),
)

HOMOPHONE_LOOKUP: dict[str, tuple[str, ...]] = {
    word: group
    for group in HOMOPHONE_GROUPS
    for word in group
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def read_wav_mono_float(wav_bytes: bytes) -> tuple[list[float], int]:
    """Decode 16-bit (or 8/32-bit) PCM WAV bytes into mono [-1.0, 1.0] floats and sample_rate."""
    with wave.open(io.BytesIO(wav_bytes), "rb") as wf:
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        sample_rate = wf.getframerate()
        nframes = wf.getnframes()
        raw = wf.readframes(nframes)

    if nframes == 0 or channels <= 0 or sample_rate <= 0:
        return [], sample_rate or 16000

    total_samples = nframes * channels
    if sampwidth == 2:
        ints = struct.unpack(f"<{total_samples}h", raw)
        scale = 32768.0
        floats = [val / scale for val in ints]
    elif sampwidth == 1:
        uints = struct.unpack(f"<{total_samples}B", raw)
        floats = [(val - 128) / 128.0 for val in uints]
    elif sampwidth == 4:
        ints = struct.unpack(f"<{total_samples}i", raw)
        floats = [val / 2147483648.0 for val in ints]
    else:
        raise ValueError(f"Unsupported WAV sample width: {sampwidth} bytes")

    if channels == 1:
        return floats, sample_rate

    mono: list[float] = []
    for idx in range(0, total_samples, channels):
        mono.append(sum(floats[idx : idx + channels]) / channels)
    return mono, sample_rate


def analyze_acoustics(
    samples: list[float],
    sample_rate: int,
    *,
    bleed_mask_ms: float = 0.0,
    min_speech_ms: float = 55.0,
    min_silence_gap_ms: float = 210.0,
) -> dict[str, Any]:
    """Detect millisecond-accurate voice onset time (RT1), speech bursts, and SNR."""
    if not samples or sample_rate <= 0:
        return {
            "duration_ms": 0,
            "noise_floor_rms": 0.0,
            "peak_rms": 0.0,
            "snr_db": 0.0,
            "rt1_onset_ms": None,
            "bursts": [],
        }

    duration_ms = round(len(samples) * 1000.0 / sample_rate)
    win_samples = max(16, int(round(sample_rate * 0.010)))   # 10 ms analysis window
    hop_samples = max(8, int(round(sample_rate * 0.002)))    # 2 ms hop for ms resolution
    mask_sample = max(0, int(round((bleed_mask_ms / 1000.0) * sample_rate)))

    frame_rms: list[float] = []
    frame_zcr: list[float] = []
    frame_starts: list[int] = []

    limit = len(samples) - win_samples
    if limit < 0:
        rms_val = math.sqrt(sum(x * x for x in samples) / len(samples))
        return {
            "duration_ms": duration_ms,
            "noise_floor_rms": round(rms_val, 5),
            "peak_rms": round(rms_val, 5),
            "snr_db": 0.0,
            "rt1_onset_ms": None,
            "bursts": [],
        }

    for start in range(0, limit + 1, hop_samples):
        window = samples[start : start + win_samples]
        sum_sq = 0.0
        zc = 0
        prev = window[0]
        for s in window:
            sum_sq += s * s
            if (s >= 0.0 > prev) or (s < 0.0 <= prev):
                zc += 1
            prev = s
        frame_starts.append(start)
        frame_rms.append(math.sqrt(sum_sq / win_samples))
        frame_zcr.append(zc / win_samples)

    post_mask_rms = [
        r for s, r in zip(frame_starts, frame_rms) if s >= mask_sample
    ] or frame_rms
    sorted_rms = sorted(post_mask_rms)
    q15_idx = min(len(sorted_rms) - 1, max(0, int(len(sorted_rms) * 0.15)))
    noise_floor = min(max(sorted_rms[q15_idx], 0.002), 0.045)
    peak_rms = max(post_mask_rms) if post_mask_rms else 0.0
    snr_db = round(20.0 * math.log10(peak_rms / noise_floor), 2) if peak_rms > noise_floor > 0 else 0.0

    voiced_thresh = max(noise_floor * 3.5, 0.015)
    fricative_thresh = max(noise_floor * 2.4, 0.010)
    release_thresh = max(noise_floor * 1.8, 0.008)

    min_speech_frames = max(1, int(round(min_speech_ms / 2.0)))
    min_gap_frames = max(1, int(round(min_silence_gap_ms / 2.0)))

    raw_bursts: list[tuple[int, int]] = []
    in_burst = False
    burst_start_idx = 0
    silence_run = 0

    for idx, (s_pos, rms, zcr) in enumerate(zip(frame_starts, frame_rms, frame_zcr)):
        if s_pos < mask_sample:
            continue
        is_active = rms >= voiced_thresh or (rms >= fricative_thresh and zcr >= 0.18)
        if not in_burst:
            if is_active:
                in_burst = True
                burst_start_idx = idx
                silence_run = 0
        else:
            if rms >= release_thresh or is_active:
                silence_run = 0
            else:
                silence_run += 1
                if silence_run >= min_gap_frames:
                    end_idx = max(burst_start_idx, idx - silence_run)
                    if end_idx - burst_start_idx + 1 >= min_speech_frames:
                        raw_bursts.append((burst_start_idx, end_idx))
                    in_burst = False
                    silence_run = 0

    if in_burst:
        end_idx = len(frame_starts) - 1 - silence_run
        if end_idx - burst_start_idx + 1 >= min_speech_frames:
            raw_bursts.append((burst_start_idx, end_idx))

    bursts: list[dict[str, int]] = []
    for b_start_idx, b_end_idx in raw_bursts:
        # Backtrack up to 16 ms to catch weak consonant release right above release_thresh.
        refined_idx = b_start_idx
        while refined_idx > 0 and frame_starts[refined_idx - 1] >= mask_sample and frame_rms[refined_idx - 1] >= release_thresh:
            if b_start_idx - refined_idx >= 8:
                break
            refined_idx -= 1
        onset_ms = round(frame_starts[refined_idx] * 1000.0 / sample_rate)
        offset_ms = round((frame_starts[b_end_idx] + win_samples) * 1000.0 / sample_rate)
        bursts.append({"onset_ms": onset_ms, "offset_ms": offset_ms})

    return {
        "duration_ms": duration_ms,
        "noise_floor_rms": round(noise_floor, 5),
        "peak_rms": round(peak_rms, 5),
        "snr_db": snr_db,
        "rt1_onset_ms": bursts[0]["onset_ms"] if bursts else None,
        "bursts": bursts,
    }


def cue_bleed_mask_ms(row: dict[str, str]) -> float:
    """Compute stimulus audio bleed window at the start of the item WAV."""
    if (row.get("StimulusPresentation") or "").strip().lower() != "audio":
        return 0.0
    first_play = parse_float(row.get("AudioFirstPlayAt(ms)"))
    last_ended = parse_float(row.get("AudioLastEndedAt(ms)"))
    if first_play is not None and last_ended is not None and last_ended >= first_play:
        return round((last_ended - first_play) + 120.0, 1)
    return 0.0


def load_asr_runner(backend: str, model_name: str):
    """Return (resolved_backend_name, transcribe_callable(wav_bytes, bleed_mask_ms))."""
    if backend == "none":
        return "none", None

    if backend in ("auto", "faster-whisper"):
        try:
            from faster_whisper import WhisperModel  # type: ignore

            model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=2)

            def _run_faster(wav_bytes: bytes, mask_ms: float) -> dict[str, Any]:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
                    tmp.write(_zero_prefix_wav(wav_bytes, mask_ms))
                    tmp.flush()
                    segments, _info = model.transcribe(
                        tmp.name,
                        language="en",
                        word_timestamps=True,
                        vad_filter=True,
                    )
                    words: list[dict[str, Any]] = []
                    raw_parts: list[str] = []
                    for seg in segments:
                        raw_parts.append(seg.text.strip())
                        for w in seg.words or []:
                            words.append(
                                {
                                    "word": w.word.strip(),
                                    "start_ms": round(float(w.start) * 1000.0),
                                    "end_ms": round(float(w.end) * 1000.0),
                                    "prob": round(float(getattr(w, "probability", 1.0)), 3),
                                }
                            )
                    return {"raw_text": " ".join(p for p in raw_parts if p), "words": words}

            return "faster-whisper", _run_faster
        except ImportError:
            if backend == "faster-whisper":
                raise SystemExit("faster-whisper is not installed. Install it or pass --asr none.")

    if backend in ("auto", "openai-whisper"):
        try:
            import whisper  # type: ignore

            model = whisper.load_model(model_name, device="cpu")

            def _run_openai(wav_bytes: bytes, mask_ms: float) -> dict[str, Any]:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
                    tmp.write(_zero_prefix_wav(wav_bytes, mask_ms))
                    tmp.flush()
                    result = model.transcribe(tmp.name, language="en", fp16=False, word_timestamps=True)
                    words: list[dict[str, Any]] = []
                    for seg in result.get("segments") or []:
                        for w in seg.get("words") or []:
                            words.append(
                                {
                                    "word": str(w.get("word") or "").strip(),
                                    "start_ms": round(float(w.get("start") or 0.0) * 1000.0),
                                    "end_ms": round(float(w.get("end") or 0.0) * 1000.0),
                                    "prob": round(float(w.get("probability") or 1.0), 3),
                                }
                            )
                    return {"raw_text": str(result.get("text") or "").strip(), "words": words}

            return "openai-whisper", _run_openai
        except ImportError:
            if backend == "openai-whisper":
                raise SystemExit("openai-whisper is not installed. Install it or pass --asr none.")

    return "none", None


def _zero_prefix_wav(wav_bytes: bytes, mask_ms: float) -> bytes:
    """Zero out the cue playback bleed window in 16-bit PCM WAV before ASR."""
    if mask_ms <= 0:
        return wav_bytes
    with wave.open(io.BytesIO(wav_bytes), "rb") as wf:
        params = wf.getparams()
        raw = bytearray(wf.readframes(params.nframes))
    if params.sampwidth == 2 and params.framerate > 0:
        mask_frames = min(params.nframes, max(0, int(round((mask_ms / 1000.0) * params.framerate))))
        zero_bytes = mask_frames * params.nchannels * 2
        raw[:zero_bytes] = b"\x00" * zero_bytes
    out = io.BytesIO()
    with wave.open(out, "wb") as wf_out:
        wf_out.setparams(params)
        wf_out.writeframes(bytes(raw))
    return out.getvalue()


def clean_asr_tokens(asr_result: dict[str, Any], max_slots: int = 4) -> dict[str, Any]:
    """Filter fillers/disfluencies and extract up to max_slots English lexical words + homophone flags."""
    lexical_words: list[dict[str, Any]] = []
    fillers: list[str] = []

    word_entries = asr_result.get("words") or []
    if not word_entries and asr_result.get("raw_text"):
        word_entries = [{"word": tok, "start_ms": None, "end_ms": None, "prob": None} for tok in WORD_RE.findall(asr_result["raw_text"])]

    for item in word_entries:
        tokens = WORD_RE.findall(str(item.get("word") or ""))
        for tok in tokens:
            low = tok.lower()
            if low in FILLER_WORDS:
                fillers.append(low)
                continue
            lexical_words.append(
                {
                    "word": low,
                    "start_ms": item.get("start_ms"),
                    "end_ms": item.get("end_ms"),
                    "prob": item.get("prob"),
                }
            )

    selected = lexical_words[:max_slots]
    homophones: list[str] = []
    low_conf = False
    for entry in selected:
        w = entry["word"]
        if w in HOMOPHONE_LOOKUP:
            alts = [alt for alt in HOMOPHONE_LOOKUP[w] if alt != w]
            homophones.append(f"{w}:{'/'.join(alts)}")
        if entry.get("prob") is not None and float(entry["prob"]) < 0.65:
            low_conf = True

    return {
        "selected": selected,
        "extra_word_count": max(0, len(lexical_words) - max_slots),
        "fillers": fillers,
        "homophone_alternatives": ";".join(homophones),
        "low_confidence": low_conf,
    }


def homophone_flags_for_existing_answers(answers: list[str]) -> str:
    flags: list[str] = []
    for ans in answers:
        for tok in WORD_RE.findall(ans or ""):
            low = tok.lower()
            if low in HOMOPHONE_LOOKUP:
                alts = [alt for alt in HOMOPHONE_LOOKUP[low] if alt != low]
                flags.append(f"{low}:{'/'.join(alts)}")
    return ";".join(flags)


def load_archive_bundle(source_path: Path) -> tuple[str, str, list[dict[str, str]], list[str], dict[str, bytes]]:
    """Return (archive_label, csv_stem, csv_rows, fieldnames, wav_bytes_by_relpath)."""
    wav_map: dict[str, bytes] = {}
    csv_text = ""
    csv_stem = source_path.stem

    if source_path.is_file() and source_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(source_path, "r") as zf:
            csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv") and not Path(n).name.startswith(".")]
            if not csv_names:
                raise ValueError(f"No CSV file found inside {source_path}")
            csv_name = sorted(csv_names)[0]
            csv_stem = Path(csv_name).stem
            csv_text = zf.read(csv_name).decode("utf-8-sig")
            for name in zf.namelist():
                if name.lower().endswith(".wav"):
                    data = zf.read(name)
                    wav_map[name] = data
                    wav_map[f"audio/{Path(name).name}"] = data
                    wav_map[Path(name).name] = data
    elif source_path.is_dir():
        csv_files = [
            p for p in sorted(source_path.glob("*.csv"))
            if not p.name.startswith(".") and p.name != "spoken_transcription_review.csv"
        ]
        if not csv_files:
            raise ValueError(f"No session CSV found in directory {source_path}")
        csv_file = csv_files[0]
        csv_stem = csv_file.stem
        csv_text = csv_file.read_text(encoding="utf-8-sig")
        for wav_path in source_path.rglob("*.wav"):
            rel = wav_path.relative_to(source_path).as_posix()
            data = wav_path.read_bytes()
            wav_map[rel] = data
            wav_map[wav_path.name] = data
    else:
        raise ValueError(f"Unsupported spoken input: {source_path}")

    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    return source_path.name, csv_stem, rows, list(reader.fieldnames or []), wav_map


def collect_spoken_inputs(input_path: Path) -> list[Path]:
    if input_path.is_file() and input_path.suffix.lower() == ".zip":
        return [input_path]
    if input_path.is_dir():
        zips = sorted(p for p in input_path.glob("*.zip") if not p.name.startswith("."))
        if zips:
            return zips
        return [input_path]
    raise FileNotFoundError(input_path)


def load_review_overrides(path: Path | None) -> dict[tuple[str, str], list[str]]:
    if not path or not path.exists():
        return {}
    overrides: dict[tuple[str, str], list[str]] = {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            session_id = (row.get("participant_session_id") or row.get("participant_id") or "").strip()
            stimulus = (row.get("stimulus") or "").strip().lower()
            rev_answers = [(row.get(f"reviewer_answer{i}") or "").strip() for i in range(1, 5)]
            if session_id and stimulus and any(rev_answers):
                overrides[(session_id, stimulus)] = rev_answers
    return overrides


def process_spoken_inputs(
    input_path: Path,
    *,
    output_dir: Path,
    asr_backend: str = "auto",
    whisper_model: str = "small.en",
    apply_review_csv: Path | None = None,
) -> dict[str, Any]:
    sources = collect_spoken_inputs(input_path)
    resolved_asr, transcribe_fn = load_asr_runner(asr_backend, whisper_model)
    review_overrides = load_review_overrides(apply_review_csv)

    output_dir.mkdir(parents=True, exist_ok=True)
    wav_export_root = output_dir / "spoken_audio"
    review_rows: list[dict[str, Any]] = []
    written_csvs: list[Path] = []

    extra_cols = [
        "AcousticRT1(ms)",
        "AcousticBurstCount",
        "AcousticSnrDb",
        "CueBleedMask(ms)",
        "SpokenRawTranscript",
        "SpokenFillers",
        "HomophoneAlternatives",
        "AsrBackend",
    ]

    for src in sources:
        archive_label, csv_stem, rows, fieldnames, wav_map = load_archive_bundle(src)
        out_fields = list(fieldnames)
        for col in [
            "Slot1Onset(ms)",
            "Slot2Onset(ms)",
            "Slot3Onset(ms)",
            "Slot4Onset(ms)",
            *extra_cols,
        ]:
            if col not in out_fields:
                out_fields.append(col)

        for row in rows:
            session_id = (row.get("ParticipantSessionId") or row.get("Participant") or "session").strip()
            participant_id = (row.get("Participant") or "anonymous").strip()
            stimulus = (row.get("Stimulus") or "").strip()
            order = (row.get("StimulusOrder") or "").strip()
            audio_ref = (row.get("SpokenAudioFile") or "").strip()
            expected_sha = (row.get("SpokenAudioSha256") or "").strip().lower()

            wav_bytes = wav_map.get(audio_ref) or wav_map.get(Path(audio_ref).name if audio_ref else "")
            bleed_ms = cue_bleed_mask_ms(row)
            sha_ok = False
            exported_wav_rel = ""

            acoustics = {
                "rt1_onset_ms": None,
                "bursts": [],
                "snr_db": 0.0,
            }
            asr_cleaned = {
                "selected": [],
                "extra_word_count": 0,
                "fillers": [],
                "homophone_alternatives": "",
                "low_confidence": False,
            }
            raw_transcript = ""

            if wav_bytes:
                actual_sha = sha256_bytes(wav_bytes)
                sha_ok = (not expected_sha) or (actual_sha == expected_sha)
                safe_sess = re.sub(r"[^A-Za-z0-9_-]+", "_", session_id)[:60]
                wav_name = Path(audio_ref).name if audio_ref else f"{int(order or 0):02d}-{stimulus}.wav"
                wav_dest = wav_export_root / safe_sess / wav_name
                wav_dest.parent.mkdir(parents=True, exist_ok=True)
                wav_dest.write_bytes(wav_bytes)
                exported_wav_rel = wav_dest.relative_to(output_dir).as_posix()

                samples, sr = read_wav_mono_float(wav_bytes)
                acoustics = analyze_acoustics(samples, sr, bleed_mask_ms=bleed_ms)

                if transcribe_fn is not None:
                    asr_raw = transcribe_fn(wav_bytes, bleed_ms)
                    raw_transcript = asr_raw.get("raw_text") or ""
                    asr_cleaned = clean_asr_tokens(asr_raw, max_slots=4)

            override_key = (session_id, stimulus.lower())
            alt_override_key = (participant_id, stimulus.lower())
            rev_override = review_overrides.get(override_key) or review_overrides.get(alt_override_key)

            if rev_override:
                for i in range(4):
                    row[f"Answer{i + 1}"] = rev_override[i]
            elif asr_cleaned["selected"] and not any((row.get(f"Answer{i}") or "").strip() for i in range(1, 5)):
                for i, entry in enumerate(asr_cleaned["selected"][:4], start=1):
                    row[f"Answer{i}"] = entry["word"]
                    if entry.get("start_ms") is not None and not str(row.get(f"Slot{i}Onset(ms)") or "").strip():
                        row[f"Slot{i}Onset(ms)"] = str(entry["start_ms"])

            # Populate Slot1..4Onset(ms) from acoustic bursts when browser slot onsets were empty.
            for idx, burst in enumerate(acoustics["bursts"][:4], start=1):
                col = f"Slot{idx}Onset(ms)"
                if not str(row.get(col) or "").strip():
                    row[col] = str(burst["onset_ms"])

            current_answers = [(row.get(f"Answer{i}") or "").strip() for i in range(1, 5)]
            homophones = asr_cleaned["homophone_alternatives"] or homophone_flags_for_existing_answers(current_answers)

            row["AcousticRT1(ms)"] = "" if acoustics["rt1_onset_ms"] is None else str(acoustics["rt1_onset_ms"])
            row["AcousticBurstCount"] = str(len(acoustics["bursts"]))
            row["AcousticSnrDb"] = str(acoustics["snr_db"])
            row["CueBleedMask(ms)"] = str(bleed_ms)
            row["SpokenRawTranscript"] = raw_transcript
            row["SpokenFillers"] = ";".join(asr_cleaned["fillers"])
            row["HomophoneAlternatives"] = homophones
            row["AsrBackend"] = "human_review_override" if rev_override else resolved_asr

            needs_listen = bool(
                not rev_override
                and (
                    resolved_asr == "none"
                    or asr_cleaned["low_confidence"]
                    or bool(homophones)
                    or asr_cleaned["extra_word_count"] > 0
                    or (len(acoustics["bursts"]) > 0 and not any(current_answers))
                )
            )
            review_rows.append(
                {
                    "source_archive": archive_label,
                    "participant_id": participant_id,
                    "participant_session_id": session_id,
                    "stimulus_order": order,
                    "stimulus": stimulus,
                    "audio_wav_path": exported_wav_rel,
                    "sha256_verified": "yes" if sha_ok else "no",
                    "bleed_mask_ms": bleed_ms,
                    "acoustic_rt1_ms": "" if acoustics["rt1_onset_ms"] is None else acoustics["rt1_onset_ms"],
                    "acoustic_burst_count": len(acoustics["bursts"]),
                    "snr_db": acoustics["snr_db"],
                    "asr_backend": row["AsrBackend"],
                    "asr_raw_transcript": raw_transcript,
                    "fillers_removed": ";".join(asr_cleaned["fillers"]),
                    "answer1": current_answers[0],
                    "answer2": current_answers[1],
                    "answer3": current_answers[2],
                    "answer4": current_answers[3],
                    "homophone_alternatives": homophones,
                    "needs_human_listen": "yes" if needs_listen else "no",
                    "reviewer_answer1": rev_override[0] if rev_override else "",
                    "reviewer_answer2": rev_override[1] if rev_override else "",
                    "reviewer_answer3": rev_override[2] if rev_override else "",
                    "reviewer_answer4": rev_override[3] if rev_override else "",
                    "reviewer_note": "",
                }
            )

        out_csv = output_dir / f"{csv_stem}.csv"
        with out_csv.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=out_fields)
            writer.writeheader()
            writer.writerows(rows)
        written_csvs.append(out_csv)

    review_csv_path = output_dir / "spoken_transcription_review.csv"
    review_fields = [
        "source_archive",
        "participant_id",
        "participant_session_id",
        "stimulus_order",
        "stimulus",
        "audio_wav_path",
        "sha256_verified",
        "bleed_mask_ms",
        "acoustic_rt1_ms",
        "acoustic_burst_count",
        "snr_db",
        "asr_backend",
        "asr_raw_transcript",
        "fillers_removed",
        "answer1",
        "answer2",
        "answer3",
        "answer4",
        "homophone_alternatives",
        "needs_human_listen",
        "reviewer_answer1",
        "reviewer_answer2",
        "reviewer_answer3",
        "reviewer_answer4",
        "reviewer_note",
    ]
    with review_csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=review_fields)
        writer.writeheader()
        writer.writerows(review_rows)

    manifest_path = output_dir / "spoken_transcription_manifest.json"
    manifest_payload = {
        "schemaVersion": "lex30-spoken-transcription-v1",
        "asrBackend": resolved_asr,
        "whisperModel": whisper_model if resolved_asr != "none" else None,
        "writtenCsvs": [p.name for p in written_csvs],
        "reviewCsv": review_csv_path.name,
        "itemRowsProcessed": len(review_rows),
    }
    manifest_path.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "asr_backend": resolved_asr,
        "written_csvs": written_csvs,
        "review_csv": review_csv_path,
        "manifest_json": manifest_path,
        "rows_processed": len(review_rows),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path, help="Spoken Lex30 .zip file, directory of .zip files, or unpacked session folder.")
    parser.add_argument("--output-dir", type=Path, default=Path("results/raw_exports"), help="Output directory for scoring-ready CSVs and spoken_transcription_review.csv.")
    parser.add_argument("--asr", choices=("auto", "none", "faster-whisper", "openai-whisper"), default="auto", help="ASR backend (defaults to auto-detecting faster-whisper/openai-whisper, or acoustic-only if neither is installed).")
    parser.add_argument("--acoustic-only", action="store_true", help="Alias for --asr none (compute deterministic acoustic voice-onset RT without ASR).")
    parser.add_argument("--whisper-model", default="small.en", help="Whisper model size when ASR is enabled.")
    parser.add_argument("--apply-review-csv", type=Path, help="Optional human-edited spoken_transcription_review.csv to apply reviewer_answer1..4 overrides.")
    args = parser.parse_args(argv)
    if args.acoustic_only:
        args.asr = "none"
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = process_spoken_inputs(
        args.input_path,
        output_dir=args.output_dir,
        asr_backend=args.asr,
        whisper_model=args.whisper_model,
        apply_review_csv=args.apply_review_csv,
    )
    print(f"ASR backend: {result['asr_backend']}")
    for path in result["written_csvs"]:
        print(f"Scoring CSV: {path}")
    print(f"Review CSV:  {result['review_csv']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
