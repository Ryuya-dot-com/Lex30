#!/usr/bin/env python3
"""Automated regression and verification tests for v0.5 spoken modes and 6-dimension multifaceted scoring."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import wave
import zipfile
from pathlib import Path

TOOLS_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_ROOT.parent
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

import openpyxl  # noqa: E402
import recover_browser_backup  # noqa: E402
import run_pilot_analysis  # noqa: E402
import score_lex30  # noqa: E402
import transcribe_spoken_lex30  # noqa: E402


def _make_synthetic_wav_16k(
    duration_ms: int,
    segments: list[tuple[int, int, float, float]],
    *,
    noise_amp: float = 0.002,
) -> bytes:
    """Create a 16 kHz mono 16-bit PCM WAV with (start_ms, end_ms, amp, freq_hz) segments."""
    sample_rate = 16000
    n_samples = int(round((duration_ms / 1000.0) * sample_rate))
    rng = random.Random(42)
    pcm = bytearray(n_samples * 2)

    for idx in range(n_samples):
        t_ms = (idx * 1000.0) / sample_rate
        val = rng.uniform(-noise_amp, noise_amp)
        for start_ms, end_ms, amp, freq_hz in segments:
            if start_ms <= t_ms <= end_ms:
                val += amp * math.sin(2.0 * math.pi * freq_hz * (idx / sample_rate))
        clamped = max(-1.0, min(1.0, val))
        int_s = int(round(clamped * 32767.0))
        struct.pack_into("<h", pcm, idx * 2, int_s)

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(bytes(pcm))
    return buf.getvalue()


class SpokenAndMultifacetedTests(unittest.TestCase):
    def test_browser_js_wav_sha256_zip_roundtrip(self) -> None:
        node = shutil.which("node")
        if not node:
            self.skipTest("node binary not available")

        with tempfile.TemporaryDirectory() as tmp:
            zip_out = Path(tmp) / "browser_bundle.zip"
            meta_out = Path(tmp) / "meta.json"
            js_driver = f"""
const fs = require("fs");
const vm = require("vm");
const code = fs.readFileSync({json.dumps(str(PROJECT_ROOT / "script.js"))}, "utf8");
const sandbox = {{
  console,
  Math,
  Number,
  String,
  Array,
  Object,
  Map,
  Set,
  Date,
  Promise,
  Uint8Array,
  Uint32Array,
  Float32Array,
  DataView,
  TextEncoder,
  URLSearchParams,
  window: {{ location: {{ search: "" }} }},
  document: {{ addEventListener() {{}}, getElementById() {{ return null; }}, documentElement: {{ lang: "en" }} }},
  localStorage: {{ getItem() {{ return null; }}, setItem() {{}} }},
  performance: {{ now: () => 0 }}
}};
vm.createContext(sandbox);
vm.runInContext(code, sandbox);

const srcRate = 48000;
const samples = new Float32Array(24000); // 500 ms
for (let i = 0; i < samples.length; i++) {{
  samples[i] = 0.5 * Math.sin(2 * Math.PI * 440 * (i / srcRate));
}}
const encoded = sandbox.encodeWav16kMono([samples.subarray(0, 12000), samples.subarray(12000)], srcRate);
const sha = sandbox.sha256HexSync(encoded.wavBytes);
const csvBytes = new TextEncoder().encode("Participant,Stimulus\\nP1,center\\n");
const zipBytes = sandbox.buildZipBytes([
  {{ name: "results.csv", bytes: csvBytes }},
  {{ name: "audio/01-center.wav", bytes: encoded.wavBytes }}
]);
fs.writeFileSync({json.dumps(str(zip_out))}, Buffer.from(zipBytes));
fs.writeFileSync({json.dumps(str(meta_out))}, JSON.stringify({{ sha256: sha, durationMs: encoded.durationMs, clipped: encoded.clippedSamples }}));
"""
            proc = subprocess.run([node, "-e", js_driver], capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)

            meta = json.loads(meta_out.read_text(encoding="utf-8"))
            self.assertEqual(meta["durationMs"], 500)
            self.assertEqual(meta["clipped"], 0)

            with zipfile.ZipFile(zip_out, "r") as zf:
                self.assertIsNone(zf.testzip())
                self.assertEqual(sorted(zf.namelist()), ["audio/01-center.wav", "results.csv"])
                wav_bytes = zf.read("audio/01-center.wav")

            self.assertEqual(hashlib.sha256(wav_bytes).hexdigest(), meta["sha256"])
            with wave.open(io.BytesIO(wav_bytes), "rb") as wf:
                self.assertEqual(wf.getnchannels(), 1)
                self.assertEqual(wf.getsampwidth(), 2)
                self.assertEqual(wf.getframerate(), 16000)
                self.assertEqual(wf.getnframes(), 8000)

    def test_transcribe_spoken_acoustics_bleed_homophone_and_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            # Cue bleed 0-400 ms, silence, burst 1 at 1250-1600 ms, burst 2 (high-ZCR fricative/tone) at 2350-2700 ms.
            wav_bytes = _make_synthetic_wav_16k(
                3400,
                [
                    (20, 400, 0.35, 320.0),
                    (1250, 1600, 0.32, 240.0),
                    (2350, 2700, 0.22, 2600.0),
                ],
            )
            wav_sha = hashlib.sha256(wav_bytes).hexdigest()
            csv_buf = io.StringIO()
            writer = csv.DictWriter(
                csv_buf,
                fieldnames=[
                    "ExperimentId",
                    "Mode",
                    "StimulusPresentation",
                    "ResponseModality",
                    "SpokenTaskStyle",
                    "ParticipantSessionId",
                    "Participant",
                    "StimulusOrder",
                    "Stimulus",
                    "Answer1",
                    "Answer2",
                    "Answer3",
                    "Answer4",
                    "ReactionTime(ms)",
                    "AudioFirstPlayAt(ms)",
                    "AudioLastEndedAt(ms)",
                    "Slot1Onset(ms)",
                    "Slot2Onset(ms)",
                    "Slot3Onset(ms)",
                    "Slot4Onset(ms)",
                    "SpokenAudioFile",
                    "SpokenAudioSha256",
                ],
            )
            writer.writeheader()
            writer.writerow(
                {
                    "ExperimentId": "updated-listening-spoken-discrete-pilot-v0.5",
                    "Mode": "listening_spoken",
                    "StimulusPresentation": "audio",
                    "ResponseModality": "spoken",
                    "SpokenTaskStyle": "discrete_naming",
                    "ParticipantSessionId": "sess-spoken-1",
                    "Participant": "SP01",
                    "StimulusOrder": "1",
                    "Stimulus": "center",
                    "Answer1": "",
                    "Answer2": "",
                    "Answer3": "",
                    "Answer4": "",
                    "ReactionTime(ms)": "3400",
                    "AudioFirstPlayAt(ms)": "0",
                    "AudioLastEndedAt(ms)": "340",
                    "Slot1Onset(ms)": "",
                    "Slot2Onset(ms)": "",
                    "Slot3Onset(ms)": "",
                    "Slot4Onset(ms)": "",
                    "SpokenAudioFile": "audio/01-center.wav",
                    "SpokenAudioSha256": wav_sha,
                }
            )

            zip_path = tmp_dir / "SP01_bundle.zip"
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("lex30_results_SP01.csv", csv_buf.getvalue())
                zf.writestr("audio/01-center.wav", wav_bytes)

            out_dir = tmp_dir / "transcribed"
            rc = transcribe_spoken_lex30.main([str(zip_path), "--output-dir", str(out_dir), "--acoustic-only"])
            self.assertEqual(rc, 0)

            out_csv = out_dir / "lex30_results_SP01.csv"
            with out_csv.open(encoding="utf-8", newline="") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(len(rows), 1)
            rt1 = int(rows[0]["AcousticRT1(ms)"])
            self.assertTrue(1238 <= rt1 <= 1264, f"Expected AcousticRT1 near 1250ms (ignoring 0-460ms bleed), got {rt1}ms")
            self.assertTrue(2338 <= int(rows[0]["Slot2Onset(ms)"]) <= 2364)

            # Verify filler stripping + homophone detection.
            cleaned = transcribe_spoken_lex30.clean_asr_tokens(
                {
                    "raw_text": "uh knight um write hospital clinic extra",
                    "words": [
                        {"word": "uh", "start_ms": 900, "end_ms": 980, "prob": 0.9},
                        {"word": "knight", "start_ms": 1250, "end_ms": 1580, "prob": 0.92},
                        {"word": "um", "start_ms": 1800, "end_ms": 1900, "prob": 0.85},
                        {"word": "write", "start_ms": 2350, "end_ms": 2680, "prob": 0.88},
                        {"word": "hospital", "start_ms": 2800, "end_ms": 3100, "prob": 0.95},
                        {"word": "clinic", "start_ms": 3150, "end_ms": 3380, "prob": 0.91},
                        {"word": "extra", "start_ms": 3400, "end_ms": 3600, "prob": 0.90},
                    ],
                }
            )
            self.assertEqual([w["word"] for w in cleaned["selected"]], ["knight", "write", "hospital", "clinic"])
            self.assertEqual(cleaned["fillers"], ["uh", "um"])
            self.assertEqual(cleaned["extra_word_count"], 1)
            self.assertIn("knight:night", cleaned["homophone_alternatives"])
            self.assertIn("write:right/rite", cleaned["homophone_alternatives"])

            # Verify --apply-review-csv overrides Answer1..Answer4 deterministically.
            review_csv = out_dir / "spoken_transcription_review.csv"
            with review_csv.open(encoding="utf-8", newline="") as fh:
                rev_rows = list(csv.DictReader(fh))
                rev_fields = list(rev_rows[0].keys())
            rev_rows[0]["reviewer_answer1"] = "middle"
            rev_rows[0]["reviewer_answer2"] = "core"
            with review_csv.open("w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=rev_fields)
                w.writeheader()
                w.writerows(rev_rows)

            out_dir_reviewed = tmp_dir / "transcribed_reviewed"
            rc2 = transcribe_spoken_lex30.main(
                [
                    str(zip_path),
                    "--output-dir",
                    str(out_dir_reviewed),
                    "--acoustic-only",
                    "--apply-review-csv",
                    str(review_csv),
                ]
            )
            self.assertEqual(rc2, 0)
            with (out_dir_reviewed / "lex30_results_SP01.csv").open(encoding="utf-8", newline="") as fh:
                reviewed_rows = list(csv.DictReader(fh))
            self.assertEqual(reviewed_rows[0]["Answer1"], "middle")
            self.assertEqual(reviewed_rows[0]["Answer2"], "core")
            self.assertEqual(reviewed_rows[0]["AsrBackend"], "human_review_override")

    def test_recover_browser_backup_v4_written_cue_spoken(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            backup_path = tmp_dir / "backup_v4.json"
            out_csv = tmp_dir / "recovered.csv"
            payload = {
                "schemaVersion": "lex30-browser-results-v4",
                "exportedAt": "2026-11-08T00:00:00Z",
                "experiment": {
                    "experimentId": "updated-written-spoken-discrete-pilot-v0.5",
                    "experimentVersion": "0.5.0",
                    "mode": "written_cue_spoken",
                    "stimulusPresentation": "text",
                    "responseModality": "spoken",
                    "spokenTaskStyle": "discrete_naming",
                    "discreteAdvanceMode": "vad_and_key",
                    "associationInstructionStyle": "star_no_chaining",
                    "stimulusSetId": "updated-easycue-posbalanced-pilot-30-v0.3",
                    "responseCount": 4,
                },
                "participant": {
                    "participantId": "P_REC_01",
                    "participantSessionId": "sess-rec-01",
                    "interfaceLanguage": "ja",
                },
                "timing": {
                    "startedAt": "2026-11-08T00:00:00Z",
                    "completedAt": "2026-11-08T00:10:00Z",
                },
                "state": {
                    "isComplete": False,
                    "completedResponseCount": 1,
                    "totalStimuli": 30,
                    "completedAssociationBreakOrders": [],
                },
                "responses": [
                    {
                        "stimulusOrder": 1,
                        "stimulus": "center",
                        "answers": ["", "", "", ""],
                        "stimulusStartedAt": "2026-11-08T00:00:01Z",
                        "stimulusEndedAt": "2026-11-08T00:00:08Z",
                        "reactionTime": 7000,
                        "elapsedSinceTestStartMs": 7000,
                        "advanceTrigger": "vad_all_slots",
                        "autoAdvanced": True,
                        "audio": {"audioPlayCount": 0, "audioEndedCount": 0},
                        "slotOnsetMs": [910, 2300, "", ""],
                        "slotCompletedMs": [1450, 2900, "", ""],
                        "spoken": {
                            "audioFile": "audio/01-center.wav",
                            "sha256": "deadbeef",
                            "durationMs": 7000,
                        },
                    }
                ],
            }
            backup_path.write_text(json.dumps(payload), encoding="utf-8")
            rc = recover_browser_backup.main(
                [str(backup_path), "--output-dir", str(tmp_dir / "rec_out"), "--output-csv", str(out_csv)]
            )
            self.assertEqual(rc, 0)
            with out_csv.open(encoding="utf-8", newline="") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(len(rows), 1)
            self.assertNotIn("completed_item_with_no_audio_play", rows[0]["RecoveryFlags"])
            self.assertEqual(rows[0]["ResponseModality"], "spoken")
            self.assertEqual(rows[0]["AssociationInstructionStyle"], "star_no_chaining")
            self.assertEqual(rows[0]["Slot1Onset(ms)"], "910")
            self.assertEqual(rows[0]["SpokenAudioFile"], "audio/01-center.wav")

    def test_six_dimension_pipeline_and_backward_compatibility(self) -> None:
        v05_cfg = json.loads((PROJECT_ROOT / "configs" / "updated-written-spoken-discrete-pilot-v0.5.json").read_text(encoding="utf-8"))
        v04_cfg = json.loads((PROJECT_ROOT / "configs" / "updated-listening-easycue-posbalanced-followup-pilot-v0.4.json").read_text(encoding="utf-8"))
        stimuli = v05_cfg["stimuli"]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)

            # Association norms fixture.
            norms_csv = tmp_dir / "assoc_norms.csv"
            norms_csv.write_text("cue,response,strength\ncenter,core,0.42\ngarden,botanical,0.18\n", encoding="utf-8")

            # 1) Full 30-item v0.5 written-cue spoken discrete session.
            v05_raw_dir = tmp_dir / "raw_v05"
            v05_raw_dir.mkdir()
            v05_csv = v05_raw_dir / "lex30_results_SPK05.csv"
            v05_fields = [
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
                "Answer1",
                "Answer2",
                "Answer3",
                "Answer4",
                "ReactionTime(ms)",
                "AudioPlayCount",
                "AudioEndedCount",
                "ResponseModality",
                "SpokenTaskStyle",
                "DiscreteAdvanceMode",
                "AssociationInstructionStyle",
                "Slot1Onset(ms)",
                "Slot2Onset(ms)",
                "Slot3Onset(ms)",
                "Slot4Onset(ms)",
            ]
            custom_responses = {
                "center": ("core", "organization", "information", "axis"),
                "garden": ("botanical", "fertilizer", "greenhouse", "blossom"),
                "white": ("write", "ivory", "porcelain", "chalk"),     # clang: white -> write (also homophone)
                "letter": ("litter", "envelope", "postage", "stamp"),   # clang: letter -> litter
                "family": ("knight", "ancestor", "sibling", "kinship"), # homophone: knight/night
            }
            with v05_csv.open("w", encoding="utf-8", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=v05_fields)
                writer.writeheader()
                for idx, cue in enumerate(stimuli, start=1):
                    ans = custom_responses.get(cue, ("hospital", "clinic", "surgeon", "therapy"))
                    writer.writerow(
                        {
                            "ExperimentId": "updated-written-spoken-discrete-pilot-v0.5",
                            "ExperimentVersion": "0.5.0",
                            "Mode": "written_cue_spoken",
                            "InterfaceLanguage": "ja",
                            "StimulusPresentation": "text",
                            "StimulusSetId": v05_cfg["stimulusSetId"],
                            "AudioVersion": "",
                            "StimulusOrder": str(idx),
                            "StartedAt": "2026-11-08T01:00:00Z",
                            "CompletedAt": "2026-11-08T01:12:00Z",
                            "ParticipantSessionId": "sess-v05-1",
                            "Participant": "SPK05",
                            "Stimulus": cue,
                            "Answer1": ans[0],
                            "Answer2": ans[1],
                            "Answer3": ans[2],
                            "Answer4": ans[3],
                            "ReactionTime(ms)": "14000",
                            "AudioPlayCount": "0",
                            "AudioEndedCount": "0",
                            "ResponseModality": "spoken",
                            "SpokenTaskStyle": "discrete_naming",
                            "DiscreteAdvanceMode": "vad_and_key",
                            "AssociationInstructionStyle": "free",
                            "Slot1Onset(ms)": "950",
                            "Slot2Onset(ms)": "4100",
                            "Slot3Onset(ms)": "8200",
                            "Slot4Onset(ms)": "12400",
                        }
                    )

            v05_out = tmp_dir / "analysis_v05"
            rc_v05 = run_pilot_analysis.main(
                [
                    str(v05_raw_dir),
                    "--experiment-id",
                    "updated-written-spoken-discrete-pilot-v0.5",
                    "--association-norms",
                    str(norms_csv),
                    "--output-dir",
                    str(v05_out),
                ]
            )
            self.assertEqual(rc_v05, 0)

            with (v05_out / "participant_qc.csv").open(encoding="utf-8", newline="") as fh:
                qc_rows = list(csv.DictReader(fh))
            self.assertEqual(qc_rows[0]["qc_status"], "ok", msg=f"Unexpected QC flags: {qc_rows[0]['qc_flags']}")
            self.assertEqual(qc_rows[0]["items_with_no_audio_play"], "0")

            with (v05_out / "pilot_scored.csv").open(encoding="utf-8", newline="") as fh:
                scored_tokens = list(csv.DictReader(fh))
            with (v05_out / "multifaceted_summary.csv").open(encoding="utf-8", newline="") as fh:
                mf_rows = list(csv.DictReader(fh))
            self.assertEqual(len(mf_rows), 1)
            mf = mf_rows[0]

            # Primary deterministic binary score check (K1=0, K2+=1 untouched; nj8_band is integer 1, 2, ...).
            expected_binary = sum(
                1
                for r in scored_tokens
                if r["is_stimulus_repetition"] == "False" and r["nj8_band"] not in ("", "1")
            )
            self.assertEqual(int(mf["nj8_token_score"]), expected_binary)
            self.assertGreater(int(mf["nj8_polytomous_token_score"]), int(mf["nj8_token_score"]))
            self.assertGreater(int(mf["nj8_polytomous_type_score"]), 0)
            self.assertGreaterEqual(
                int(mf["nj8_polytomous_type_score"]),
                int(mf["nj8_polytomous_type_no_clang_score"]),
            )
            self.assertGreaterEqual(
                int(mf["nj8_polytomous_type_no_clang_score"]),
                int(mf["nj8_unique_cue_polytomous_no_clang_score"]),
            )
            self.assertIn("cross_cue_repeated_tokens", mf)
            self.assertIn("cross_cue_recycling_percent", mf)
            self.assertIn("max_cues_per_lemma", mf)
            self.assertGreater(float(mf["nj8_eb_type_sophistication"]), 0.0)
            self.assertIn("bnc_coca_polytomous_type_score", mf)

            # Dimension 2: fluency & time-cutoff monotonic order (5s <= 10s <= 30s total).
            k2_5s = int(mf["nj8_k2plus_within_5s"])
            k2_10s = int(mf["nj8_k2plus_within_10s"])
            self.assertTrue(0 < k2_5s <= k2_10s <= expected_binary)
            self.assertAlmostEqual(float(mf["mean_rt1_onset_ms"]), 950.0, places=1)

            # Dimension 3: clang + homophone bounds.
            self.assertGreaterEqual(int(mf["clang_candidate_tokens"]), 2)
            self.assertGreaterEqual(int(mf["homophone_ambiguous_tokens"]), 2)
            self.assertGreaterEqual(
                int(mf["homophone_lenient_nj8_score"]),
                int(mf["homophone_conservative_nj8_score"]),
            )

            # Dimension 4 & 5: association strength, chaining, concreteness, derivational suffixes.
            self.assertGreater(float(mf["mean_association_norm_strength"]), 0.0)
            self.assertNotEqual(mf["mean_chaining_index"], "")
            self.assertGreater(float(mf["mean_response_concreteness"]), 1.0)
            self.assertGreater(float(mf["derivational_suffix_ratio"]), 0.0)

            # 2) Full 30-item v0.4 follow-up session for Dimension 6 receptive-productive bottleneck.
            v04_raw_dir = tmp_dir / "raw_v04"
            v04_raw_dir.mkdir()
            v04_csv = v04_raw_dir / "lex30_results_LIS04.csv"
            v04_fields = v05_fields + [
                "AudioFile",
                "FollowUpEnabled",
                "FollowUpCompleted",
                "HeardWord",
                "JapaneseMeaning",
                "CollocationCorrect",
                "CategoryCorrect",
                "SynonymCorrect",
            ]
            with v04_csv.open("w", encoding="utf-8", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=v04_fields)
                writer.writeheader()
                for idx, cue in enumerate(v04_cfg["stimuli"], start=1):
                    # Cue 1 ("center"): exact heard + matched Japanese meaning "中心" + K2+ answers -> productive hit
                    # Cue 2 ("garden"): exact heard + negated Japanese meaning "わからない" + 0 probes -> not receptively known
                    # Cue 3 ("health"): exact heard + matched Japanese meaning "健康" + only K1 answers ("good", "bad") -> receptive-productive gap!
                    # Cue 30 ("return"): misheard ("turnip")
                    if cue == "center":
                        ans = ("core", "axis", "middle", "focus")
                        heard = "center"
                        ja = "中心"
                        p_ok = "True"
                    elif cue == "garden":
                        ans = ("flower", "tree", "green", "grass")
                        heard = "garden"
                        ja = "わからない"
                        p_ok = "False"
                    elif cue == "health":
                        ans = ("good", "bad", "body", "life")  # K1 words -> 0 K2+ points despite knowing cue!
                        heard = "health"
                        ja = "健康"
                        p_ok = "True"
                    elif cue == "return":
                        ans = ("back", "home", "go", "again")
                        heard = "turnip"
                        ja = ""
                        p_ok = "False"
                    else:
                        ans = ("clinic", "surgeon", "therapy", "ward")
                        heard = cue
                        ja = ""
                        p_ok = "True"

                    writer.writerow(
                        {
                            "ExperimentId": "updated-listening-easycue-posbalanced-followup-pilot-v0.4",
                            "ExperimentVersion": "0.4.0",
                            "Mode": "listening",
                            "InterfaceLanguage": "ja",
                            "StimulusPresentation": "audio",
                            "StimulusSetId": v04_cfg["stimulusSetId"],
                            "AudioVersion": v04_cfg["audioVersion"],
                            "StimulusOrder": str(idx),
                            "StartedAt": "2026-11-08T02:00:00Z",
                            "CompletedAt": "2026-11-08T02:20:00Z",
                            "ParticipantSessionId": "sess-v04-1",
                            "Participant": "LIS04",
                            "Stimulus": cue,
                            "Answer1": ans[0],
                            "Answer2": ans[1],
                            "Answer3": ans[2],
                            "Answer4": ans[3],
                            "ReactionTime(ms)": "9000",
                            "AudioPlayCount": "1",
                            "AudioEndedCount": "1",
                            "ResponseModality": "written",
                            "SpokenTaskStyle": "",
                            "DiscreteAdvanceMode": "",
                            "AssociationInstructionStyle": "free",
                            "Slot1Onset(ms)": "1200",
                            "Slot2Onset(ms)": "3100",
                            "Slot3Onset(ms)": "5200",
                            "Slot4Onset(ms)": "7100",
                            "AudioFile": f"audio/updated-listening-easycue-posbalanced-pilot-v0.3/{idx:02d}-{cue}.mp3",
                            "FollowUpEnabled": "True",
                            "FollowUpCompleted": "True",
                            "HeardWord": heard,
                            "JapaneseMeaning": ja,
                            "CollocationCorrect": p_ok,
                            "CategoryCorrect": p_ok,
                            "SynonymCorrect": p_ok,
                        }
                    )

            v04_out = tmp_dir / "analysis_v04"
            rc_v04 = run_pilot_analysis.main(
                [
                    str(v04_raw_dir),
                    "--experiment-id",
                    "updated-listening-easycue-posbalanced-followup-pilot-v0.4",
                    "--output-dir",
                    str(v04_out),
                ]
            )
            self.assertEqual(rc_v04, 0)
            with (v04_out / "multifaceted_summary.csv").open(encoding="utf-8", newline="") as fh:
                mf_v04 = list(csv.DictReader(fh))[0]
            self.assertEqual(mf_v04["heard_exact_items"], "29")
            self.assertEqual(mf_v04["japanese_meaning_matched_items"], "2")  # "中心" and "健康", NOT "わからない"
            self.assertEqual(mf_v04["receptive_known_items"], "28")
            self.assertGreater(float(mf_v04["productive_retrieval_gap_percent"]), 0.0)

            wb = openpyxl.load_workbook(v04_out / "pilot_workbook.xlsx", read_only=True)
            self.assertIn("Multifaceted", wb.sheetnames)
            wb.close()

            # 3) Legacy examples/sample_results.csv backward compatibility check.
            sample_csv = PROJECT_ROOT / "examples" / "sample_results.csv"
            if sample_csv.exists():
                legacy_out = tmp_dir / "legacy_out"
                legacy_out.mkdir()
                rc_legacy = score_lex30.main(
                    [
                        str(sample_csv),
                        "--output-csv",
                        str(legacy_out / "scored.csv"),
                        "--output-summary-csv",
                        str(legacy_out / "summary.csv"),
                        "--output-review-csv",
                        str(legacy_out / "review.csv"),
                        "--output-json",
                        str(legacy_out / "scored.json"),
                    ]
                )
                self.assertEqual(rc_legacy, 0)
                with (legacy_out / "summary.csv").open(encoding="utf-8", newline="") as fh:
                    legacy_summary = list(csv.DictReader(fh))
                self.assertGreaterEqual(len(legacy_summary), 1)
                self.assertIn("nj8_polytomous_token_score", legacy_summary[0])
                self.assertIn("nj8_token_score", legacy_summary[0])

    def test_wave2_practice_parallel_forms_and_review_ui(self) -> None:
        node = shutil.which("node")
        if not node:
            self.skipTest("node binary not available")

        # 0) Verify practice audio files and matched parallel halves metadata.
        for fname in ("01-book.mp3", "02-water.mp3", "manifest.json"):
            p = PROJECT_ROOT / "audio" / "practice" / fname
            self.assertTrue(p.exists() and p.stat().st_size > 100, f"Missing or empty practice asset: {p}")

        halves_data = json.loads((PROJECT_ROOT / "tools" / "data" / "parallel_split_halves.json").read_text(encoding="utf-8"))
        halves = halves_data["sets"]["updated-easycue-posbalanced-pilot-30-v0.3"]
        self.assertEqual(len(halves["form_a"]), 15)
        self.assertEqual(len(halves["form_b"]), 15)
        self.assertEqual(len(set(halves["form_a"]) | set(halves["form_b"])), 30)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)

            # 1) Verify script.js Form B subset, canonical audio path, practice count, and counterbalanced_ba order.
            v05_listen_path = PROJECT_ROOT / "configs" / "updated-listening-spoken-continuous-pilot-v0.5.json"
            js_out_path = tmp_dir / "wave2_js_check.json"
            wav_bytes = _make_synthetic_wav_16k(
                3000,
                [
                    (20, 380, 0.35, 320.0),
                    (1250, 1620, 0.32, 250.0),
                ],
            )
            wav_in_path = tmp_dir / "synth.wav"
            wav_in_path.write_bytes(wav_bytes)
            review_csv_out = tmp_dir / "ui_exported_review.csv"
            bundle_zip_path = tmp_dir / "ui_bundle.zip"

            review_html = (PROJECT_ROOT / "review_spoken.html").read_text(encoding="utf-8")
            script_start = review_html.index("<script>") + len("<script>")
            script_end = review_html.rindex("</script>")
            review_js_path = tmp_dir / "review_inline.js"
            review_js_path.write_text(review_html[script_start:script_end], encoding="utf-8")

            js_driver = f"""
const fs = require("fs");
const vm = require("vm");
const rawCfg = JSON.parse(fs.readFileSync({json.dumps(str(v05_listen_path))}, "utf8"));
const scriptCode = fs.readFileSync({json.dumps(str(PROJECT_ROOT / "script.js"))}, "utf8");

function makeSandbox(search) {{
  const sb = {{
    console, Math, Number, String, Array, Object, Map, Set, Date, Promise, RegExp,
    Uint8Array, Uint32Array, Float32Array, DataView, TextEncoder, TextDecoder, URLSearchParams,
    window: {{ location: {{ search }} }},
    document: {{ addEventListener() {{}}, getElementById() {{ return null; }}, documentElement: {{ lang: "en" }} }},
    localStorage: {{ getItem() {{ return null; }}, setItem() {{}} }},
    performance: {{ now: () => 0 }}
  }};
  vm.createContext(sb);
  vm.runInContext(scriptCode, sb);
  return sb;
}}

const sbFormB = makeSandbox("?subset=form_b&practice=2");
const resFormB = vm.runInContext(`
  experimentConfig = normalizeConfig(${{JSON.stringify(rawCfg)}});
  interfaceLanguage = "en";
  const enInstr = localizedInstructions();
  interfaceLanguage = "ja";
  const jaInstr = localizedInstructions();
  ({{
    stimuli: experimentConfig.stimuli,
    practiceCount: experimentConfig.practiceCount,
    healthAudio: audioPathForStimulus("health", 0),
    practiceBookAudio: audioPathForPracticeStimulus("book", 0),
    enInstr,
    jaInstr
  }})
`, sbFormB);

const sbCb = makeSandbox("?order=counterbalanced_ba");
const cbOrder = vm.runInContext(`
  experimentConfig = normalizeConfig(${{JSON.stringify(rawCfg)}});
  buildStimulusOrder(experimentConfig)
`, sbCb);

// Build a spoken ZIP archive with script.js buildZipBytes and test review_spoken.html inline JS on it.
const wavBuf = new Uint8Array(fs.readFileSync({json.dumps(str(wav_in_path))}));
const csvStr = [
  "ExperimentId,StimulusPresentation,ResponseModality,ParticipantSessionId,Participant,StimulusOrder,Stimulus,Answer1,Answer2,Answer3,Answer4,ReactionTime(ms),AudioFirstPlayAt(ms),AudioLastEndedAt(ms),SpokenAudioFile",
  "updated-listening-spoken-continuous-pilot-v0.5,audio,spoken,sess-ui-1,P_UI,1,health,,,,,3000,0,340,audio/01-health.wav"
].join("\\n") + "\\n";
const zipBytes = sbFormB.buildZipBytes([
  {{ name: "results.csv", bytes: new TextEncoder().encode(csvStr) }},
  {{ name: "audio/01-health.wav", bytes: wavBuf }}
]);
fs.writeFileSync({json.dumps(str(bundle_zip_path))}, Buffer.from(zipBytes));

const reviewCode = fs.readFileSync({json.dumps(str(review_js_path))}, "utf8");
const dummyEl = () => ({{
  addEventListener() {{}},
  appendChild() {{}},
  append() {{}},
  innerHTML: "",
  textContent: "",
  value: "",
  disabled: false,
  checked: false,
  classList: {{ add() {{}}, remove() {{}}, toggle() {{}} }},
  getContext: () => ({{ fillRect() {{}}, clearRect() {{}}, fillText() {{}}, beginPath() {{}}, moveTo() {{}}, lineTo() {{}}, stroke() {{}} }})
}});
const revSb = {{
  console, Math, Number, String, Array, Object, Map, Set, Date, Promise, RegExp,
  Uint8Array, Uint32Array, Float32Array, DataView, TextEncoder, TextDecoder,
  window: {{ addEventListener() {{}} }},
  document: {{ addEventListener() {{}}, getElementById: () => dummyEl(), createElement: () => dummyEl() }},
  URL: {{ createObjectURL: () => "blob:mock", revokeObjectURL() {{}} }}
}};
vm.createContext(revSb);
vm.runInContext(reviewCode, revSb);

(async () => {{
  const entries = await revSb.parseZipEntries(zipBytes);
  const parsedWav = entries.get("audio/01-health.wav");
  const decoded = revSb.decodePcmWav16(parsedWav);
  const ac = revSb.computeBrowserAcoustics(decoded.samples, decoded.sampleRate, 460);
  const csvOut = revSb.serializeReviewCsv([{{
    source_archive: "ui_bundle.zip",
    participant_id: "P_UI",
    participant_session_id: "sess-ui-1",
    stimulus_order: "1",
    stimulus: "health",
    audio_wav_path: "audio/01-health.wav",
    sha256_verified: "yes",
    bleed_mask_ms: "460",
    acoustic_rt1_ms: String(ac.rt1Ms),
    acoustic_burst_count: String(ac.burstCount),
    snr_db: String(ac.snrDb),
    asr_backend: "browser_acoustic_preview",
    asr_raw_transcript: "",
    fillers_removed: "",
    answer1: "knight",
    answer2: "",
    answer3: "",
    answer4: "",
    homophone_alternatives: "knight:night",
    needs_human_listen: "yes",
    reviewer_answer1: "night",
    reviewer_answer2: "clinic",
    reviewer_answer3: "",
    reviewer_answer4: "",
    reviewer_note: "disambiguated in review_spoken.html"
  }}]);
  fs.writeFileSync({json.dumps(str(review_csv_out))}, csvOut);

  // Verify acceptCurrentAndAdvance does NOT write verified_blank when ASR slots are present,
  // and DOES write verified_blank when all slots are genuinely empty.
  const domMap = new Map();
  revSb.document.getElementById = id => {{
    if (!domMap.has(id)) domMap.set(id, {{ ...dummyEl(), style: {{}}, removeAttribute() {{}}, play: () => Promise.resolve() }});
    return domMap.get(id);
  }};
  vm.runInContext(`
    reviewRows = [
      {{ participant_id: "P1", participant_session_id: "s1", stimulus_order: "1", stimulus: "center", answer1: "core", answer2: "", answer3: "", answer4: "", reviewer_answer1: "", reviewer_answer2: "", reviewer_answer3: "", reviewer_answer4: "", reviewer_note: "" }},
      {{ participant_id: "P1", participant_session_id: "s1", stimulus_order: "2", stimulus: "garden", answer1: "", answer2: "", answer3: "", answer4: "", reviewer_answer1: "", reviewer_answer2: "", reviewer_answer3: "", reviewer_answer4: "", reviewer_note: "" }}
    ];
    filteredIndices = [0, 1];
    selectRow(0, false);
    acceptCurrentAndAdvance(); // copies "core" into slot 1, advances to row 1 without verified_blank
    acceptCurrentAndAdvance(); // row 1 is empty -> sets verified_blank
  `, revSb);
  const acceptCheck = vm.runInContext(`reviewRows.map(r => ({{ r1: r.reviewer_answer1, note: r.reviewer_note }}))`, revSb);

  // Verify multiword draft rejection in script.js keeps autoNextTimer alive instead of cancelling it!
  const sbTimer = makeSandbox("");
  const timerStayedAlive = vm.runInContext(`
    const els = new Map();
    document.getElementById = id => {{
      if (!els.has(id)) els.set(id, {{ value: "", textContent: "", focus() {{}}, classList: {{ add() {{}}, remove() {{}}, toggle() {{}} }}, style: {{}} }});
      return els.get(id);
    }};
    document.querySelectorAll = () => [];
    setTimeout = () => 999;
    clearTimeout = () => {{}};
    experimentConfig = normalizeConfig({{ ...${{JSON.stringify(rawCfg)}}, responseModality: "written", stimulusPresentation: "text" }});
    testInProgress = true;
    activePhase = "association";
    currentResponseTimerStarted = true;
    startTime = 100;
    autoNextTimer = 777;
    document.getElementById("association-answer-input").value = "two words";
    nextStimulus("button");
    ({{ autoNextTimer, notice: document.getElementById("task-inline-notice").textContent }})
  `, sbTimer);

  fs.writeFileSync({json.dumps(str(js_out_path))}, JSON.stringify({{ resFormB, cbOrder, ac, acceptCheck, timerStayedAlive }}));
}})().catch(err => {{ console.error(err); process.exit(1); }});
"""
            proc = subprocess.run([node, "-e", js_driver], capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)

            js_res = json.loads(js_out_path.read_text(encoding="utf-8"))
            res_b = js_res["resFormB"]
            self.assertEqual(res_b["stimuli"], halves["form_b"])
            self.assertEqual(res_b["practiceCount"], 2)
            # "health" is index 0 in Form B, but canonical index 2 (03-health.mp3) in the frozen 30-cue set!
            self.assertIn("/03-health.mp3", res_b["healthAudio"])
            self.assertEqual(res_b["practiceBookAudio"], "audio/practice/01-book.mp3")
            # Instructions must update cue count to 15 while keeping timer at 30 seconds / 30秒.
            self.assertIn("15 English words", res_b["enInstr"])
            self.assertIn("30 seconds", res_b["enInstr"])
            self.assertIn("15個", res_b["jaInstr"])
            self.assertIn("30秒", res_b["jaInstr"])

            # Counterbalanced BA puts the 15 Form B items first, then the 15 Form A items.
            self.assertEqual(js_res["cbOrder"], halves["form_b"] + halves["form_a"])

            # Verify browser acoustic RT1 matches Python CLI (~1250 ms, ignoring 0-460 ms cue bleed).
            self.assertTrue(1238 <= int(js_res["ac"]["rt1Ms"]) <= 1264, f"Unexpected browser RT1: {js_res['ac']}")
            self.assertEqual(js_res["acceptCheck"][0], {"r1": "core", "note": ""})
            self.assertEqual(js_res["acceptCheck"][1], {"r1": "", "note": "verified_blank"})
            self.assertEqual(js_res["timerStayedAlive"]["autoNextTimer"], 777)
            self.assertIn("one English word", js_res["timerStayedAlive"]["notice"])

            index_html = (PROJECT_ROOT / "index.html").read_text(encoding="utf-8")
            researcher_html = (PROJECT_ROOT / "researcher.html").read_text(encoding="utf-8")
            for ui_id in ("item-timer-bar", "timer-pill", "task-inline-notice", "saved-backup-card"):
                self.assertIn(f'id="{ui_id}"', index_html)
            self.assertIn('id="session-preview-bar"', researcher_html)
            self.assertIn('id="playback-rate-select"', review_html)

            # Verify review_spoken.html exported CSV feeds cleanly into transcribe_spoken_lex30.py --apply-review-csv!
            applied_dir = tmp_dir / "applied_from_ui"
            rc_apply = transcribe_spoken_lex30.main(
                [
                    str(bundle_zip_path),
                    "--output-dir",
                    str(applied_dir),
                    "--acoustic-only",
                    "--apply-review-csv",
                    str(review_csv_out),
                ]
            )
            self.assertEqual(rc_apply, 0)
            with (applied_dir / "results.csv").open(encoding="utf-8", newline="") as fh:
                applied_rows = list(csv.DictReader(fh))
            self.assertEqual(applied_rows[0]["Answer1"], "night")
            self.assertEqual(applied_rows[0]["Answer2"], "clinic")
            self.assertEqual(applied_rows[0]["AsrBackend"], "human_review_override")

            # 2) Verify 15-item parallel split-half Form A session auto-detection & QC in run_pilot_analysis.py.
            form_a_dir = tmp_dir / "raw_form_a"
            form_a_dir.mkdir()
            form_a_csv = form_a_dir / "lex30_results_FA01.csv"
            fields = [
                "ExperimentId",
                "ExperimentVersion",
                "Mode",
                "InterfaceLanguage",
                "StimulusPresentation",
                "StimulusSetId",
                "StimulusSubset",
                "StimulusOrderPolicy",
                "AudioVersion",
                "StimulusOrder",
                "StartedAt",
                "CompletedAt",
                "ParticipantSessionId",
                "Participant",
                "Stimulus",
                "Answer1",
                "Answer2",
                "Answer3",
                "Answer4",
                "ReactionTime(ms)",
                "AudioPlayCount",
                "AudioEndedCount",
                "ResponseModality",
                "SpokenTaskStyle",
            ]
            with form_a_csv.open("w", encoding="utf-8", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=fields)
                writer.writeheader()
                for idx, cue in enumerate(halves["form_a"], start=1):
                    writer.writerow(
                        {
                            "ExperimentId": "updated-written-spoken-continuous-pilot-v0.5",
                            "ExperimentVersion": "0.5.0",
                            "Mode": "written_cue_spoken",
                            "InterfaceLanguage": "ja",
                            "StimulusPresentation": "text",
                            "StimulusSetId": "updated-easycue-posbalanced-pilot-30-v0.3",
                            "StimulusSubset": "form_a",
                            "StimulusOrderPolicy": "fixed",
                            "AudioVersion": "",
                            "StimulusOrder": str(idx),
                            "StartedAt": "2026-11-08T03:00:00Z",
                            "CompletedAt": "2026-11-08T03:06:00Z",
                            "ParticipantSessionId": "sess-fa-01",
                            "Participant": "FA01",
                            "Stimulus": cue,
                            "Answer1": "clinic",
                            "Answer2": "surgeon",
                            "Answer3": "therapy",
                            "Answer4": "hospital",
                            "ReactionTime(ms)": "9500",
                            "AudioPlayCount": "0",
                            "AudioEndedCount": "0",
                            "ResponseModality": "spoken",
                            "SpokenTaskStyle": "continuous_4",
                        }
                    )

            form_a_out = tmp_dir / "analysis_form_a"
            rc_fa = run_pilot_analysis.main(
                [
                    str(form_a_dir),
                    "--experiment-id",
                    "updated-written-spoken-continuous-pilot-v0.5",
                    "--output-dir",
                    str(form_a_out),
                ]
            )
            self.assertEqual(rc_fa, 0)
            with (form_a_out / "participant_qc.csv").open(encoding="utf-8", newline="") as fh:
                fa_qc = list(csv.DictReader(fh))[0]
            self.assertEqual(fa_qc["qc_status"], "ok", msg=f"Unexpected Form A QC flags: {fa_qc['qc_flags']}")
            self.assertEqual(fa_qc["completion_percent"], "100.0")
            with (form_a_out / "cue_score_matrix.csv").open(encoding="utf-8", newline="") as fh:
                matrix_cues = [r["stimulus"] for r in csv.DictReader(fh)]
            self.assertEqual(matrix_cues, halves["form_a"])
            with (form_a_out / "item_diagnostics.csv").open(encoding="utf-8", newline="") as fh:
                diag_cues = [r["stimulus"] for r in csv.DictReader(fh)]
            self.assertEqual(diag_cues, halves["form_a"] * 3)

    def test_bilingual_switching_across_all_views(self) -> None:
        node = shutil.which("node")
        if not node:
            self.skipTest("node not installed")

        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "i18n_check.json"
            driver = f"""
const fs = require("fs");
const vm = require("vm");

// 1) Participant script.js: ?lang=ja&langLock=1 + all 99 v0.4 probe prompts + unchanged CSV option labels
const scriptCode = fs.readFileSync("script.js", "utf8");
const v04 = JSON.parse(fs.readFileSync("configs/updated-listening-easycue-posbalanced-followup-pilot-v0.4.json", "utf8"));
const sbScript = {{
  URL,
  URLSearchParams,
  console,
  Math,
  Date,
  Set,
  Map,
  Array,
  Object,
  Number,
  String,
  Boolean,
  RegExp,
  JSON,
  Promise,
  performance: {{ now: () => 0 }},
  navigator: {{ language: "en-US" }},
  localStorage: {{ getItem: () => null, setItem: () => {{}}, removeItem: () => {{}} }},
  window: {{ location: {{ search: "?experiment=updated-listening-easycue-posbalanced-followup-pilot-v0.4&lang=ja&langLock=1" }}, addEventListener() {{}}, scrollTo() {{}} }},
  document: {{
    documentElement: {{ lang: "en" }},
    title: "",
    addEventListener() {{}},
    getElementById: () => null,
    querySelector: () => null,
    querySelectorAll: () => []
  }}
}};
vm.createContext(sbScript);
vm.runInContext(scriptCode, sbScript);

const initLang = vm.runInContext("initialInterfaceLanguage()", sbScript);
vm.runInContext('interfaceLanguage = "ja";', sbScript);
let totalPrompts = 0;
let translatedPrompts = 0;
let sampleJaPrompt = "";
let dontKnowExportLabel = "";
for (const [cue, probes] of Object.entries(v04.followUp.probes || {{}})) {{
  for (const [ptype, p] of Object.entries(probes)) {{
    totalPrompts += 1;
    const jaText = vm.runInContext(`localizedProbePrompt(${{JSON.stringify(p.prompt)}}, ${{JSON.stringify(ptype)}})`, sbScript);
    if (jaText !== p.prompt && /[ぁ-んァ-ヶ一-龠]/.test(jaText)) {{
      translatedPrompts += 1;
      if (!sampleJaPrompt) sampleJaPrompt = jaText;
    }}
    if (!dontKnowExportLabel) {{
      dontKnowExportLabel = vm.runInContext(`probeOptionLabel(${{JSON.stringify(p)}}, "dont_know")`, sbScript);
    }}
  }}
}}
const jaDontKnowUi = vm.runInContext('t("dontKnowOption")', sbScript);
const jaFollowupProg = vm.runInContext('t("followupProgressPrefix", {{ current: 3, total: 30, stage: t("followupMeaningLabel") }})', sbScript);

// 2) researcher.html: setResearcherLanguage("ja") + buildParticipantUrl with ja_locked
const resHtml = fs.readFileSync("researcher.html", "utf8");
const resMatch = resHtml.match(/<script>([\\s\\S]*?)<\\/script>/);
const resEls = new Map();
function getResEl(id) {{
  if (!resEls.has(id)) {{
    resEls.set(id, {{
      value: id === "participant-lang-select" ? "ja_locked"
        : id === "instruction-style-select" ? "free"
        : id === "practice-count-select" ? "auto"
        : id === "stimulus-subset-select" ? "all"
        : id === "stimulus-order-select" ? "fixed"
        : "",
      textContent: "",
      innerHTML: "",
      disabled: false,
      hidden: false,
      style: {{}},
      classList: {{ toggle() {{}}, add() {{}}, remove() {{}} }},
      setAttribute() {{}},
      addEventListener() {{}},
      appendChild() {{}}
    }});
  }}
  return resEls.get(id);
}}
const sbRes = {{
  URL,
  URLSearchParams,
  Map,
  Set,
  Math,
  Number,
  String,
  Boolean,
  Array,
  Object,
  JSON,
  console,
  navigator: {{ language: "ja-JP" }},
  localStorage: {{ store: {{}}, getItem(k) {{ return this.store[k] || null; }}, setItem(k, v) {{ this.store[k] = v; }} }},
  window: {{ location: {{ href: "http://127.0.0.1:8000/researcher.html", search: "", protocol: "http:" }} }},
  document: {{
    documentElement: {{ lang: "en" }},
    title: "",
    addEventListener() {{}},
    getElementById: getResEl,
    querySelectorAll: () => [],
    createElement: () => ({{ className: "", textContent: "", value: "" }})
  }}
}};
vm.createContext(sbRes);
vm.runInContext(resMatch[1], sbRes);
const resDetected = vm.runInContext("detectInitialLanguage()", sbRes);
vm.runInContext('setResearcherLanguage("ja")', sbRes);
const resHeadingJa = vm.runInContext('rt("pageHeading")', sbRes);
const builtLockedUrl = vm.runInContext(`buildParticipantUrl("updated-listening-easycue-posbalanced-followup-pilot-v0.4", ${{JSON.stringify(v04)}})`, sbRes);

// 3) review_spoken.html: setReviewLanguage("ja") + CSV serialization invariant
const revHtml = fs.readFileSync("review_spoken.html", "utf8");
const revMatch = revHtml.match(/<script>([\\s\\S]*?)<\\/script>/);
const revEls = new Map();
function getRevEl(id) {{
  if (!revEls.has(id)) {{
    revEls.set(id, {{
      value: "",
      textContent: "",
      innerHTML: "",
      title: "",
      placeholder: "",
      disabled: false,
      checked: false,
      clientWidth: 720,
      clientHeight: 96,
      width: 720,
      height: 96,
      style: {{}},
      classList: {{ toggle() {{}}, add() {{}}, remove() {{}} }},
      setAttribute() {{}},
      removeAttribute() {{}},
      appendChild() {{}},
      append() {{}},
      getContext: () => ({{ fillStyle: "", strokeStyle: "", font: "", lineWidth: 1, fillRect() {{}}, fillText() {{}}, beginPath() {{}}, moveTo() {{}}, lineTo() {{}}, stroke() {{}} }})
    }});
  }}
  return revEls.get(id);
}}
const sbRev = {{
  URL,
  URLSearchParams,
  Map,
  Set,
  Math,
  Number,
  String,
  Boolean,
  Array,
  Object,
  Float32Array,
  Uint8Array,
  DataView,
  JSON,
  console,
  navigator: {{ language: "ja" }},
  localStorage: {{ store: {{}}, getItem(k) {{ return this.store[k] || null; }}, setItem(k, v) {{ this.store[k] = v; }}, removeItem(k) {{ delete this.store[k]; }} }},
  window: {{ location: {{ search: "" }}, devicePixelRatio: 1, addEventListener() {{}} }},
  document: {{
    documentElement: {{ lang: "en" }},
    title: "",
    addEventListener() {{}},
    getElementById: getRevEl,
    querySelectorAll: () => [],
    createElement: () => ({{ className: "", textContent: "", innerHTML: "", value: "", append() {{}}, appendChild() {{}} }})
  }}
}};
vm.createContext(sbRev);
vm.runInContext(revMatch[1], sbRev);
vm.runInContext('setReviewLanguage("ja")', sbRev);
const revBadgeJa = vm.runInContext('rvt("badgeReviewed")', sbRev);
const revProgJa = vm.runInContext('rvt("progressSummary", {{ done: 2, total: 5 }})', sbRev);
const csvHeaderLine = vm.runInContext('serializeReviewCsv([])', sbRev).trim();

fs.writeFileSync({json.dumps(str(out_path))}, JSON.stringify({{
  initLang,
  totalPrompts,
  translatedPrompts,
  sampleJaPrompt,
  dontKnowExportLabel,
  jaDontKnowUi,
  jaFollowupProg,
  resDetected,
  resHeadingJa,
  builtLockedUrl,
  revBadgeJa,
  revProgJa,
  csvHeaderLine
}}));
"""
            proc = subprocess.run([node, "-e", driver], cwd=PROJECT_ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)
            res = json.loads(out_path.read_text(encoding="utf-8"))

            self.assertEqual(res["initLang"], "ja")
            self.assertEqual(res["totalPrompts"], 99)
            self.assertEqual(res["translatedPrompts"], 99)
            self.assertEqual(res["dontKnowExportLabel"], "I don't know")
            self.assertEqual(res["jaDontKnowUi"], "わからない")
            self.assertEqual(res["jaFollowupProg"], "確認問題 3 / 30 - 意味確認")
            self.assertEqual(res["resDetected"], "ja")
            self.assertEqual(res["resHeadingJa"], "Lex30 研究者設定")
            self.assertIn("lang=ja", res["builtLockedUrl"])
            self.assertIn("langLock=1", res["builtLockedUrl"])
            self.assertEqual(res["revBadgeJa"], "確認済")
            self.assertEqual(res["revProgJa"], "2 / 5 確認済")
            self.assertTrue(res["csvHeaderLine"].startswith("source_archive,participant_id,participant_session_id,"))

    def test_simulate_lex30_scoring_cli(self) -> None:
        import simulate_lex30_scoring

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "sim_out"
            rc = simulate_lex30_scoring.main(["--n-learners", "60", "--output-dir", str(out_dir)])
            self.assertEqual(rc, 0)
            summary_csv = out_dir / "scoring_simulation_summary.csv"
            summary_json = out_dir / "scoring_simulation_summary.json"
            self.assertTrue(summary_csv.exists())
            self.assertTrue(summary_json.exists())
            with summary_csv.open(encoding="utf-8", newline="") as fh:
                rows = list(csv.DictReader(fh))
            # 4 scenarios x 10 indices = 40 rows
            self.assertEqual(len(rows), 40)
            jp_rows = {r["scoring_method"]: r for r in rows if r["scenario"] == "jp_efl_mixed_univ"}
            self.assertGreater(
                float(jp_rows["nj8_polytomous_type_no_clang_score"]["r_true_theta"]),
                float(jp_rows["nj8_token_score"]["r_true_theta"]),
            )
            self.assertLess(
                float(jp_rows["nj8_unique_cue_polytomous_no_clang_score"]["partial_r_recycling_gaming"]),
                float(jp_rows["nj8_polytomous_type_no_clang_score"]["partial_r_recycling_gaming"]),
            )


if __name__ == "__main__":
    unittest.main()
