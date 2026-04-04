#!/usr/bin/env python3
"""Gera musica de fundo baseada no objetivo do video."""

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

try:
    from dotenv import load_dotenv
except ImportError:
    print("Instale python-dotenv: pip3 install python-dotenv")
    sys.exit(1)


MOOD_PROMPTS = {
    "motivacional": {
        "description": "Energetico e inspirador, com build-up gradual",
        "prompt": "upbeat motivational corporate background music with piano and electronic beats, energetic build up, positive and inspiring",
        "bpm_range": [120, 140],
        "instruments": "piano, electronic drums, synth pads",
        "volume_db": -18,
    },
    "educacional": {
        "description": "Calmo e focado, nao distrai do conteudo",
        "prompt": "calm lo-fi study background music with soft piano and gentle acoustic guitar, minimal and clean, no distracting elements",
        "bpm_range": [80, 100],
        "instruments": "piano, acoustic guitar, soft percussion",
        "volume_db": -22,
    },
    "humor": {
        "description": "Divertido e leve, bom para transicoes",
        "prompt": "fun and quirky background music with bouncy bass and playful synth, lighthearted and comedic",
        "bpm_range": [110, 130],
        "instruments": "bass, synth, claps, quirky percussion",
        "volume_db": -20,
    },
    "dramatico": {
        "description": "Intenso com build-up emocional",
        "prompt": "cinematic dramatic background music with strings and deep piano, slow build up to emotional climax, epic and powerful",
        "bpm_range": [90, 120],
        "instruments": "strings, piano, timpani, brass",
        "volume_db": -18,
    },
    "relaxante": {
        "description": "Suave e espacoso, bom para lifestyle",
        "prompt": "relaxing ambient background music with soft nature sounds and gentle piano, peaceful and dreamy",
        "bpm_range": [60, 80],
        "instruments": "piano, nature sounds, ambient pads",
        "volume_db": -24,
    },
    "tecnologia": {
        "description": "Moderno e clean, bom para reviews tech",
        "prompt": "modern tech background music with clean synths and subtle electronic beats, futuristic and professional",
        "bpm_range": [100, 120],
        "instruments": "synths, electronic beats, subtle bass",
        "volume_db": -20,
    },
    "negocios": {
        "description": "Profissional e confiante",
        "prompt": "corporate business background music with warm piano and gentle strings, professional and trustworthy",
        "bpm_range": [90, 110],
        "instruments": "piano, strings, light percussion",
        "volume_db": -20,
    },
    "fitness": {
        "description": "Energetico com ritmo marcante",
        "prompt": "high energy workout background music with powerful bass drops and driving beats, intense and motivating",
        "bpm_range": [128, 150],
        "instruments": "bass, electronic drums, synth leads",
        "volume_db": -16,
    },
}


def generate_silence(duration: float, output_path: str) -> bool:
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"anullsrc=r={44100}:cl=stereo",
        "-t",
        str(duration),
        "-acodec",
        "aac",
        "-b:a",
        "128k",
        output_path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def generate_tone_music(duration: float, mood: dict, output_path: str) -> bool:
    bpm = sum(mood["bpm_range"]) // 2
    freq = 440

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency={freq}:duration={duration}",
        "-af",
        (
            f"lowpass=f=2000,"
            f"volume={mood['volume_db']}dB,"
            f"afade=t=in:st=0:d=2,afade=t=out:st={max(0, duration - 2)}:d=2"
        ),
        "-acodec",
        "aac",
        "-b:a",
        "128k",
        output_path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def generate_with_suno_api(
    mood: dict, duration: float, output_path: str, api_key: str = None
) -> bool:
    if not api_key:
        return False

    prompt = mood["prompt"]
    print(f"[Suno] Gerando musica com prompt: {prompt[:80]}...")

    try:
        resp = requests.post(
            "https://api.suno.ai/v1/generate",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "prompt": prompt,
                "duration": int(duration),
                "instrumental": True,
            },
            timeout=120,
        )
        if resp.status_code == 200:
            audio_url = resp.json().get("audio_url")
            if audio_url:
                audio_resp = requests.get(audio_url, timeout=60)
                if audio_resp.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(audio_resp.content)
                    return True
    except Exception:
        pass

    return False


def generate_background_music(args):
    mood_name = args.objetivo.lower()
    if mood_name not in MOOD_PROMPTS:
        print(f"Objetivos disponiveis: {', '.join(MOOD_PROMPTS.keys())}")
        print(f"Aliases: {' '.join(MOOD_PROMPTS.keys())}")
        sys.exit(1)

    mood = MOOD_PROMPTS[mood_name]

    if args.saida:
        out_dir = Path(args.saida)
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(out_dir / f"musica_{mood_name}.mp3")
    else:
        output_path = f"musica_{mood_name}.mp3"

    print(f"Gerando musica de fundo...")
    print(f"  Objetivo: {mood_name}")
    print(f"  Descricao: {mood['description']}")
    print(f"  BPM: {mood['bpm_range'][0]}-{mood['bpm_range'][1]}")
    print(f"  Volume: {mood['volume_db']} dB")
    print(f"  Duracao: {args.duracao}s")

    suno_key = os.getenv("SUNO_API_KEY", "")

    if suno_key and args.metodo == "auto":
        print("\n  Tentando Suno API...")
        if generate_with_suno_api(mood, args.duracao, output_path, suno_key):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"  Musica gerada (Suno): {output_path} ({size_kb:.0f}KB)")
            return output_path
        print("  Suno nao disponivel, usando gerador local...")

    if args.metodo == "suno":
        print("ERRO: SUNO_API_KEY nao configurada")
        print("  Configure no .env.cliente ou use --metodo local")
        sys.exit(1)

    print("  Gerando audio de referencia (silencio com fade)...")
    success = generate_silence(args.duracao, output_path)

    if not success:
        print("  FFmpeg nao encontrado. Criando placeholder...")
        with open(output_path, "wb") as f:
            f.write(b"")
        print(f"  Placeholder criado: {output_path}")
        print(f"\n  NOTA: Para musica real, configure:")
        print(f"  1. SUNO_API_KEY no .env.cliente (musica gerada por IA)")
        print(f"  2. Ou forneça seu proprio arquivo de musica")
        return output_path

    print(f"  Audio de referencia salvo: {output_path}")
    print(f"\n  Para melhor resultado, substitua por:")
    print(f"  1. Musica de biblioteca (Epidemic Sound, Artlist)")
    print(f"  2. Musica gerada por IA (Suno, Udio)")
    print(f"  3. Musica royalty-free (Pixabay, Freesound)")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Gera musica de fundo por objetivo")
    parser.add_argument("--cliente", default=None, help="Nome do cliente")
    parser.add_argument("--objetivo", required=True, choices=list(MOOD_PROMPTS.keys()))
    parser.add_argument(
        "--duracao", type=float, default=60.0, help="Duracao em segundos (default: 60)"
    )
    parser.add_argument("--saida", default=None, help="Diretorio de saida")
    parser.add_argument("--metodo", default="auto", choices=["auto", "suno", "local"])
    args = parser.parse_args()

    if args.cliente:
        base = Path.home() / "conteudo" / "campanhas" / args.cliente / ".env.cliente"
        if base.exists():
            load_dotenv(base)

    generate_background_music(args)


if __name__ == "__main__":
    main()
