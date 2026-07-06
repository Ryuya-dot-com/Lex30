#!/usr/bin/env python3
"""Generate audio stimulus files for Lex30 listening configs.

The script is dry-run by default. Add --execute to call the ElevenLabs API.
"""
from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from score_lex30 import DEFAULT_ENV_PATH, PROJECT_ROOT

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - requirements guard
    load_dotenv = None

try:
    import certifi
except ImportError:  # pragma: no cover - requirements guard
    certifi = None


DEFAULT_CONFIG = PROJECT_ROOT / "configs" / "updated-listening-easycue-posbalanced-pilot-v0.3.json"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"
DEFAULT_STABILITY = 0.85
DEFAULT_SIMILARITY_BOOST = 0.9
DEFAULT_STYLE = 0.0


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sanitize_file_part(value: str) -> str:
    keep = []
    for char in value.lower():
        keep.append(char if char.isalnum() or char in {"-", "_"} else "_")
    return "".join(keep).strip("_")[:80] or "stimulus"


def audio_path(config: dict[str, Any], stimulus: str, index: int, output_dir: Path | None) -> Path:
    extension = str(config.get("audioExtension") or "mp3").lstrip(".")
    filename = f"{index + 1:02d}-{sanitize_file_part(stimulus)}.{extension}"
    if output_dir:
        return output_dir / filename
    base = str(config.get("audioBasePath") or f"audio/{config.get('experimentId', 'lex30-audio')}")
    return PROJECT_ROOT / base / filename


def elevenlabs_tts(
    *,
    api_key: str,
    voice_id: str,
    text: str,
    model_id: str,
    output_format: str,
    language_code: str,
    stability: float,
    similarity_boost: float,
    style: float,
    use_speaker_boost: bool,
    timeout: int,
) -> bytes:
    query = urllib.parse.urlencode({"output_format": output_format})
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{urllib.parse.quote(voice_id)}?{query}"
    payload = json.dumps(
        {
            "text": text,
            "model_id": model_id,
            **({"language_code": language_code} if language_code else {}),
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style,
                "use_speaker_boost": use_speaker_boost,
            },
        }
    ).encode("utf-8")
    context = ssl.create_default_context(cafile=certifi.where() if certifi else None)
    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ElevenLabs API error {exc.code}: {detail}") from exc


def write_manifest(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, nargs="?", default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, help="Override the config audioBasePath.")
    parser.add_argument("--manifest", type=Path, help="Audio generation manifest JSON.")
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV_PATH)
    parser.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID"))
    parser.add_argument("--model-id", default=os.environ.get("ELEVENLABS_MODEL_ID", DEFAULT_MODEL_ID))
    parser.add_argument("--output-format", default=os.environ.get("ELEVENLABS_OUTPUT_FORMAT", DEFAULT_OUTPUT_FORMAT))
    parser.add_argument("--language-code", default=os.environ.get("ELEVENLABS_LANGUAGE_CODE", "en"))
    parser.add_argument("--stability", type=float, default=float(os.environ.get("ELEVENLABS_STABILITY", DEFAULT_STABILITY)))
    parser.add_argument(
        "--similarity-boost",
        type=float,
        default=float(os.environ.get("ELEVENLABS_SIMILARITY_BOOST", DEFAULT_SIMILARITY_BOOST)),
    )
    parser.add_argument("--style", type=float, default=float(os.environ.get("ELEVENLABS_STYLE", DEFAULT_STYLE)))
    parser.add_argument(
        "--no-speaker-boost",
        action="store_true",
        help="Disable ElevenLabs speaker boost. Speaker boost is enabled by default for stimulus consistency.",
    )
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--pause-seconds", type=float, default=0.2)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--execute", action="store_true", help="Actually call ElevenLabs and write audio files.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if load_dotenv and args.env and args.env.exists():
        load_dotenv(args.env)

    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    voice_id = args.voice_id or os.environ.get("ELEVENLABS_FEMALE_VOICE_ID") or os.environ.get("ELEVENLABS_MALE_VOICE_ID")
    config = load_config(args.config)
    stimuli = [str(item).strip() for item in config.get("stimuli", []) if str(item).strip()]
    output_paths = [audio_path(config, stimulus, index, args.output_dir) for index, stimulus in enumerate(stimuli)]
    manifest_path = args.manifest or (output_paths[0].parent / "manifest.json" if output_paths else PROJECT_ROOT / "audio" / "manifest.json")

    if args.execute and not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is not set. Use --env or export it before --execute.")
    if args.execute and not voice_id:
        raise RuntimeError("No voice ID set. Provide --voice-id or ELEVENLABS_VOICE_ID/FEMALE/MALE in .env.")

    files: list[dict[str, Any]] = []
    for index, (stimulus, path) in enumerate(zip(stimuli, output_paths), start=1):
        status = "dry_run"
        if path.exists() and not args.overwrite:
            status = "exists"
        elif args.execute:
            path.parent.mkdir(parents=True, exist_ok=True)
            audio = elevenlabs_tts(
                api_key=api_key,
                voice_id=voice_id,
                text=stimulus,
                model_id=args.model_id,
                output_format=args.output_format,
                language_code=args.language_code,
                stability=args.stability,
                similarity_boost=args.similarity_boost,
                style=args.style,
                use_speaker_boost=not args.no_speaker_boost,
                timeout=args.timeout,
            )
            path.write_bytes(audio)
            status = "written"
            time.sleep(args.pause_seconds)
        files.append(
            {
                "order": index,
                "stimulus": stimulus,
                "path": str(path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path),
                "status": status,
            }
        )

    write_manifest(
        manifest_path,
        {
            "config": str(args.config.relative_to(PROJECT_ROOT) if args.config.is_relative_to(PROJECT_ROOT) else args.config),
            "experimentId": config.get("experimentId"),
            "modelId": args.model_id,
            "outputFormat": args.output_format,
            "languageCode": args.language_code,
            "voiceId": voice_id,
            "voiceSettings": {
                "stability": args.stability,
                "similarityBoost": args.similarity_boost,
                "style": args.style,
                "useSpeakerBoost": not args.no_speaker_boost,
            },
            "execute": bool(args.execute),
            "files": files,
        },
    )

    print(f"Wrote {manifest_path}")
    print(f"Mode: {'execute' if args.execute else 'dry-run'}")
    print(f"Stimuli: {len(stimuli)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
