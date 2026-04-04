#!/usr/bin/env python3
"""Gera legendas automaticas para videos usando Whisper (OpenAI)."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Instale requests: pip3 install requests")
    sys.exit(1)


def check_whisper():
    try:
        subprocess.run(
            ["whisper", "--help"],
            capture_output=True,
            timeout=5,
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def generate_with_local_whisper(video_path: str, language: str = "pt") -> dict:
    print(f"Gerando legendas com Whisper local para: {video_path}")
    cmd = [
        "whisper",
        video_path,
        "--model",
        "base",
        "--language",
        language,
        "--output_format",
        "json",
        "--output_dir",
        os.path.dirname(video_path) or ".",
        "--word_timestamps",
        "True",
    ]
    subprocess.run(cmd, check=True)
    base = os.path.splitext(video_path)[0]
    json_path = f"{base}.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return _parse_whisper_segments(data)
    return {}


def generate_with_openai_api(
    video_path: str, api_key: str, language: str = "pt"
) -> dict:
    print(f"Gerando legendas com OpenAI Whisper API para: {video_path}")

    audio_path = video_path
    if not video_path.endswith((".mp3", ".wav", ".m4a", ".flac")):
        audio_path = _extract_audio(video_path)
        if not audio_path:
            print("ERRO: Nao foi possivel extrair audio do video")
            return {}

    with open(audio_path, "rb") as f:
        resp = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (os.path.basename(audio_path), f)},
            data={
                "model": "whisper-1",
                "language": language,
                "response_format": "verbose_json",
                "timestamp_granularities[]": "word",
            },
            timeout=300,
        )

    if resp.status_code != 200:
        print(f"ERRO: OpenAI API retornou {resp.status_code}: {resp.text}")
        return {}

    data = resp.json()
    return _parse_openai_segments(data)


def _extract_audio(video_path: str):
    output = os.path.splitext(video_path)[0] + ".mp3"
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-vn",
                "-acodec",
                "libmp3lame",
                "-q:a",
                "2",
                output,
                "-y",
            ],
            capture_output=True,
            timeout=120,
        )
        if os.path.exists(output):
            return output
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def _parse_whisper_segments(data: dict) -> dict:
    segments = data.get("segments", [])
    words = []
    for seg in segments:
        for w in seg.get("words", []):
            words.append(
                {
                    "word": w.get("word", "").strip(),
                    "start": w.get("start", 0),
                    "end": w.get("end", 0),
                }
            )
    text = " ".join(w["word"] for w in words)
    return {"text": text, "words": words, "language": data.get("language", "unknown")}


def _parse_openai_segments(data: dict) -> dict:
    text = data.get("text", "")
    words = []
    for seg in data.get("segments", []):
        for w in seg.get("words", []):
            words.append(
                {
                    "word": w.get("word", "").strip(),
                    "start": w.get("start", 0),
                    "end": w.get("end", 0),
                }
            )
    return {"text": text, "words": words, "language": data.get("language", "unknown")}


def generate_srt(subtitle_data: dict) -> str:
    words = subtitle_data.get("words", [])
    if not words:
        return ""

    lines = []
    current_start = words[0]["start"]
    current_end = words[0]["end"]
    current_words = [words[0]["word"]]

    for w in words[1:]:
        if w["start"] - current_end > 1.5:
            lines.append((current_start, current_end, " ".join(current_words)))
            current_start = w["start"]
            current_words = [w["word"]]
        else:
            current_words.append(w["word"])
        current_end = w["end"]

    if current_words:
        lines.append((current_start, current_end, " ".join(current_words)))

    srt = ""
    for i, (start, end, text) in enumerate(lines, 1):
        srt += f"{i}\n"
        srt += f"{_fmt_time(start)} --> {_fmt_time(end)}\n"
        srt += f"{text}\n\n"

    return srt


def generate_remotion_json(subtitle_data: dict) -> str:
    words = subtitle_data.get("words", [])
    if not words:
        return "[]"

    subtitles = []
    for w in words:
        subtitles.append(
            {
                "text": w["word"],
                "startFrame": int(w["start"] * 30),
                "endFrame": int(w["end"] * 30),
            }
        )

    return json.dumps(subtitles, ensure_ascii=False, indent=2)


def _fmt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    parser = argparse.ArgumentParser(
        description="Gera legendas automaticas para videos"
    )
    parser.add_argument("--video", required=True, help="Caminho do video")
    parser.add_argument(
        "--cliente",
        default=None,
        help="Nome do cliente (busca OPENAI_API_KEY no .env.cliente)",
    )
    parser.add_argument("--api-key", default=None, help="OpenAI API key (override)")
    parser.add_argument("--idioma", default="pt", help="Idioma do audio (default: pt)")
    parser.add_argument(
        "--formato", default="srt", choices=["srt", "json", "remotion", "todos"]
    )
    parser.add_argument("--metodo", default="auto", choices=["local", "api", "auto"])
    args = parser.parse_args()

    api_key = args.api_key
    if not api_key and args.cliente:
        env_path = (
            Path.home() / "conteudo" / "campanhas" / args.cliente / ".env.cliente"
        )
        if env_path.exists():
            for line in env_path.read_text().strip().splitlines():
                if line.startswith("OPENAI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()

    if args.metodo == "auto":
        if api_key:
            args.metodo = "api"
            print("Usando OpenAI Whisper API")
        elif check_whisper():
            args.metodo = "local"
            print("Usando Whisper local")
        else:
            print("ERRO: Nenhum metodo disponivel.")
            print("  Instale Whisper local: pip3 install openai-whisper")
            print("  Ou forneca --api-key ou configure OPENAI_API_KEY no .env.cliente")
            sys.exit(1)

    if args.metodo == "local":
        subtitle_data = generate_with_local_whisper(args.video, args.idioma)
    else:
        if not api_key:
            print("ERRO: API key necessaria para metodo 'api'")
            sys.exit(1)
        subtitle_data = generate_with_openai_api(args.video, api_key, args.idioma)

    if not subtitle_data:
        print("ERRO: Nenhuma legenda gerada")
        sys.exit(1)

    print(f"Texto detectado ({len(subtitle_data.get('words', []))} palavras):")
    print(f"  {subtitle_data['text'][:200]}...")

    base = os.path.splitext(args.video)[0]
    if args.formato in ("srt", "todos"):
        srt = generate_srt(subtitle_data)
        srt_path = f"{base}.srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt)
        print(f"SRT salvo: {srt_path}")

    if args.formato in ("json", "todos"):
        json_path = f"{base}_legendas.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(subtitle_data, f, ensure_ascii=False, indent=2)
        print(f"JSON salvo: {json_path}")

    if args.formato in ("remotion", "todos"):
        remotion = generate_remotion_json(subtitle_data)
        rem_path = f"{base}_remotion_subtitles.json"
        with open(rem_path, "w", encoding="utf-8") as f:
            f.write(remotion)
        print(f"Remotion JSON salvo: {rem_path}")


if __name__ == "__main__":
    main()
