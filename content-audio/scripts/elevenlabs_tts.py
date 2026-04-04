#!/usr/bin/env python3
"""TTS com ElevenLabs - gera voz AI a partir de texto ou arquivo."""

import argparse
import json
import os
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

API_BASE = "https://api.elevenlabs.io/v1"


def load_env(cliente: str) -> dict:
    base = Path.home() / "conteudo" / "campanhas" / cliente
    env_path = base / ".env.cliente"
    if not env_path.exists():
        print(f"ERRO: .env.cliente nao encontrado: {env_path}")
        sys.exit(1)
    load_dotenv(env_path)
    key = os.getenv("ELEVENLABS_API_KEY", "")
    if not key:
        print("ERRO: ELEVENLABS_API_KEY nao configurada no .env.cliente")
        sys.exit(1)
    return {
        "api_key": key,
        "voice_id": os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"),
        "model_id": os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
        "output_format": os.getenv("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128"),
    }


def list_voices(env: dict, language: str = None) -> list:
    print("Buscando vozes disponiveis...")
    resp = requests.get(
        f"{API_BASE}/voices",
        headers={"xi-api-key": env["api_key"]},
        timeout=30,
    )
    resp.raise_for_status()
    voices = resp.json().get("voices", [])

    if language:
        voices = [
            v for v in voices if language.lower() in str(v.get("labels", [])).lower()
        ]

    print(f"\n{len(voices)} vozes encontradas:\n")
    print(f"{'Nome':<25} {'ID':<30} {'Estilo'}")
    print("-" * 80)
    for v in voices[:30]:
        name = v.get("name", "")
        vid = v.get("voice_id", "")
        labels = v.get("labels", [])
        style = ", ".join(labels[:3])
        print(f"{name:<25} {vid:<30} {style}")

    return voices


def generate_tts(
    text: str, env: dict, stability: float = 0.5, similarity_boost: float = 0.75
) -> bytes:
    if len(text) > 5000:
        print("Texto muito longo (>5000 chars). Usando streaming...")

    url = f"{API_BASE}/text-to-speech/{env['voice_id']}"
    headers = {
        "xi-api-key": env["api_key"],
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    body = {
        "text": text,
        "model_id": env["model_id"],
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }

    resp = requests.post(url, json=body, headers=headers, timeout=120)
    if resp.status_code != 200:
        print(f"ERRO API ({resp.status_code}): {resp.text[:300]}")
        sys.exit(1)

    return resp.content


def generate_tts_stream(text: str, env: dict, output_path: str):
    url = f"{API_BASE}/text-to-speech/{env['voice_id']}/stream"
    headers = {
        "xi-api-key": env["api_key"],
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    chunks = []
    chunk_size = 4000
    offset = 0

    while offset < len(text):
        chunk_text = text[offset : offset + chunk_size]
        if not chunk_text.strip():
            break

        body = {
            "text": chunk_text,
            "model_id": env["model_id"],
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True,
            },
        }

        print(f"  Gerando chunk {offset // chunk_size + 1}...")
        resp = requests.post(url, json=body, headers=headers, timeout=120)
        if resp.status_code != 200:
            print(f"ERRO no chunk: {resp.status_code}")
            break

        chunks.append(resp.content)
        offset += chunk_size

    if chunks:
        with open(output_path, "wb") as f:
            for chunk in chunks:
                f.write(chunk)
        print(
            f"Audio salvo: {output_path} ({os.path.getsize(output_path) / 1024:.0f}KB)"
        )
    else:
        print("ERRO: Nenhum audio gerado")


def main():
    parser = argparse.ArgumentParser(description="TTS com ElevenLabs")
    parser.add_argument("--texto", default=None, help="Texto para converter em fala")
    parser.add_argument("--arquivo", default=None, help="Arquivo de texto")
    parser.add_argument("--cliente", default=None, help="Nome do cliente")
    parser.add_argument(
        "--voz", default=None, help="Voice ID (sobrescreve .env.cliente)"
    )
    parser.add_argument("--modelo", default=None, help="Model ID")
    parser.add_argument("--saida", default=None, help="Caminho de saida")
    parser.add_argument(
        "--listar-vozes", action="store_true", help="Listar vozes disponiveis"
    )
    parser.add_argument("--idioma", default=None, help="Filtrar vozes por idioma")
    parser.add_argument("--estabilidade", type=float, default=0.5)
    parser.add_argument("--similaridade", type=float, default=0.75)
    args = parser.parse_args()

    if args.listar_vozes:
        env = (
            load_env(args.cliente)
            if args.cliente
            else {"api_key": os.getenv("ELEVENLABS_API_KEY", "")}
        )
        if not env["api_key"]:
            print("ERRO: Forneça --cliente ou ELEVENLABS_API_KEY")
            sys.exit(1)
        list_voices(env, args.idioma)
        return

    if not args.cliente:
        print("ERRO: --cliente e obrigatorio (para credenciais)")
        sys.exit(1)

    env = load_env(args.cliente)

    if args.voz:
        env["voice_id"] = args.voz
    if args.modelo:
        env["model_id"] = args.modelo

    text = ""
    if args.texto:
        text = args.texto
    elif args.arquivo:
        if not os.path.exists(args.arquivo):
            print(f"ERRO: Arquivo nao encontrado: {args.arquivo}")
            sys.exit(1)
        with open(args.arquivo, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        print("ERRO: Forneça --texto ou --arquivo")
        sys.exit(1)

    print(f"Gerando voz com ElevenLabs...")
    print(f"  Voz: {env['voice_id']}")
    print(f"  Modelo: {env['model_id']}")
    print(f"  Texto: {len(text)} caracteres")

    if args.saida:
        output_path = args.saida
        out_dir = Path(output_path).parent
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_path = "voz_gerada.mp3"

    if len(text) > 4000:
        generate_tts_stream(text, env, output_path)
    else:
        audio_data = generate_tts(text, env, args.estabilidade, args.similaridade)
        with open(output_path, "wb") as f:
            f.write(audio_data)
        size_kb = len(audio_data) / 1024
        print(f"Audio salvo: {output_path} ({size_kb:.0f}KB)")


if __name__ == "__main__":
    main()
