#!/usr/bin/env python3
import argparse
import json
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

ELEVENLABS_SFX_API = "https://api.elevenlabs.io/v1/sound-generation"

EFEITOS_PRESETS = {
    "whoosh": "cinematic whoosh transition sound",
    "impact": "deep bass impact hit",
    "rise": "tension building riser",
    "pop": "short pop notification",
    "ding": "bright bell ding",
    "click": "short mouse click",
    "swoosh": "fast air swoosh",
    "drop": "heavy bass drop",
    "glitch": "digital glitch sound",
    "reveal": "dramatic reveal sting",
    "success": "positive success chime",
    "error": "error buzzer sound",
    "transition": "smooth transition sweep",
    "heartbeat": "low heartbeat pulse",
    "thunder": "distant thunder rumble",
    "cash": "cash register cha-ching",
    "snap": "finger snap",
    "alarm": "subtle alert alarm",
}


def load_env(cliente: str) -> dict:
    base = os.path.expanduser(f"~/conteudo/campanhas/{cliente}")
    env_file = os.path.join(base, ".env.cliente")
    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
    creds = {
        "api_key": os.getenv("ELEVENLABS_API_KEY", ""),
    }
    return creds


def list_effects():
    print("Efeitos disponiveis (preset):")
    print("=" * 50)
    for nome, desc in sorted(EFEITOS_PRESETS.items()):
        print(f"  {nome:15s} - {desc}")
    print()
    print("Total: {} efeitos".format(len(EFEITOS_PRESETS)))
    print()
    print("Tambem pode usar qualquer descricao textual em ingles.")
    print("Exemplo: --efeitos 'sword clash, explosion, glass breaking'")


def generate_effect(api_key: str, descricao: str, duracao: float = 2.0) -> bytes:
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": descricao,
        "duration_seconds": duracao,
    }
    resp = requests.post(ELEVENLABS_SFX_API, json=payload, headers=headers, timeout=60)
    if resp.status_code != 200:
        erro_msg = resp.text[:500]
        raise Exception(f"Erro API ElevenLabs ({resp.status_code}): {erro_msg}")
    return resp.content


def main():
    parser = argparse.ArgumentParser(
        description="Gerador de efeitos sonoros via ElevenLabs Sound Effects API"
    )
    parser.add_argument(
        "--cliente", help="Nome do cliente (busca ELEVENLABS_API_KEY no .env.cliente)"
    )
    parser.add_argument(
        "--api-key", help="ElevenLabs API Key (alternativa ao --cliente)"
    )
    parser.add_argument(
        "--efeitos", help="Lista de efeitos separados por virgula (preset ou descricao)"
    )
    parser.add_argument(
        "--duracao",
        type=float,
        default=2.0,
        help="Duracao de cada efeito em segundos (padrao: 2.0)",
    )
    parser.add_argument(
        "--saida",
        default="brutos/efeitos/",
        help="Pasta de saida (padrao: brutos/efeitos/)",
    )
    parser.add_argument(
        "--listar", action="store_true", help="Listar efeitos preset disponiveis"
    )
    args = parser.parse_args()

    if args.listar:
        list_effects()
        return

    if not args.efeitos:
        parser.error("Use --efeitos ou --listar")
        return

    api_key = args.api_key
    if not api_key and args.cliente:
        creds = load_env(args.cliente)
        api_key = creds["api_key"]

    if not api_key:
        print("ERRO: Forneça --api-key ou --cliente com ELEVENLABS_API_KEY configurado")
        sys.exit(1)

    efeitos = [e.strip() for e in args.efeitos.split(",")]
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)

    print(f"Gerando {len(efeitos)} efeito(s)...")
    print()

    for i, efeito in enumerate(efeitos):
        descricao = EFEITOS_PRESETS.get(efeito, efeito)
        nome_arquivo = efeito.replace(" ", "_")

        print(f"  [{i + 1}/{len(efeitos)}] {efeito}...")
        try:
            audio_data = generate_effect(api_key, descricao, args.duracao)
            output_file = saida / f"{nome_arquivo}.mp3"
            output_file.write_bytes(audio_data)
            size_kb = len(audio_data) / 1024
            print(f"          OK -> {output_file} ({size_kb:.1f} KB)")
        except Exception as e:
            print(f"          ERRO: {e}")

    print()
    print("Concluido!")


if __name__ == "__main__":
    main()
