#!/usr/bin/env python3
"""Mixa trilhas de audio (voz + musica + efeitos) com video."""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def mix_audio(
    video_path: str,
    voice_path: str = None,
    music_path: str = None,
    effects_path: str = None,
    output_path: str = None,
    voice_volume: float = 0.0,
    music_volume: float = -14.0,
    effects_volume: float = -6.0,
    video_duration: float = None,
) -> str:
    if not check_ffmpeg():
        print("ERRO: FFmpeg nao encontrado. Instale: brew install ffmpeg")
        sys.exit(1)

    if not os.path.exists(video_path):
        print(f"ERRO: Video nao encontrado: {video_path}")
        sys.exit(1)

    if output_path is None:
        base = os.path.splitext(video_path)[0]
        output_path = f"{base}_mixado.mp4"

    inputs = ["-i", video_path]
    filter_parts = []
    audio_labels = []

    has_video_audio = True
    cmd_probe = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_streams",
        video_path,
    ]
    try:
        result = subprocess.run(cmd_probe, capture_output=True, text=True, timeout=10)
        data = {}
        if result.returncode == 0:
            import json

            data = json.loads(result.stdout)
            streams = data.get("streams", [])
            has_video_audio = any(s.get("codec_type") == "audio" for s in streams)
    except Exception:
        pass

    if has_video_audio:
        filter_parts.append("[0:a]anull[original_audio]")

    input_idx = 1

    if voice_path and os.path.exists(voice_path):
        inputs.extend(["-i", voice_path])
        label = f"[{input_idx}:a]"
        voice_vol = voice_volume
        filter_parts.append(
            f"{label}volume={voice_vol}dB,loudnorm=I=-14:TP=-1:LRA=11[voice]"
        )
        audio_labels.append("voice")
        input_idx += 1

    if music_path and os.path.exists(music_path):
        inputs.extend(["-i", music_path])
        label = f"[{input_idx}:a]"
        filter_parts.append(f"{label}volume={music_volume}dB[musica]")
        if video_duration:
            filter_parts.append(
                f"[musica]afade=t=out:st={max(0, video_duration - 2)}:d=2[musica_f]"
            )
        else:
            filter_parts.append("[musica]afade=t=out:st=58:d=2[musica_f]")
        audio_labels.append("musica_f")
        input_idx += 1

    if effects_path and os.path.exists(effects_path):
        effects_dir = Path(effects_path)
        if effects_dir.is_dir():
            effect_files = sorted(effects_dir.glob("*.mp3")) + sorted(
                effects_dir.glob("*.wav")
            )
            for ef in effect_files[:5]:
                inputs.extend(["-i", str(ef)])
                label = f"[{input_idx}:a]"
                filter_parts.append(f"{label}volume={effects_volume}dB[fx_{input_idx}]")
                audio_labels.append(f"fx_{input_idx}")
                input_idx += 1
        elif os.path.exists(effects_path):
            inputs.extend(["-i", effects_path])
            label = f"[{input_idx}:a]"
            filter_parts.append(f"{label}volume={effects_volume}dB[fx]")
            audio_labels.append("fx")
            input_idx += 1

    if not audio_labels:
        print("Nenhuma trilha de audio fornecida. Copiando video original.")
        cmd = ["ffmpeg", "-y", "-i", video_path, "-c", "copy", output_path]
        subprocess.run(cmd, capture_output=True, timeout=120)
        print(f"Video copiado: {output_path}")
        return output_path

    amix_inputs = "+".join(audio_labels)
    filter_str = ";".join(filter_parts)
    filter_str += f";{amix_inputs}[aout]"
    filter_str += ";[aout]loudnorm=I=-14:TP=-1:LRA=11[final]"

    cmd = (
        ["ffmpeg", "-y"]
        + inputs
        + [
            "-filter_complex",
            filter_str,
            "-map",
            "0:v",
            "-map",
            "[final]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            output_path,
        ]
    )

    print(f"Mixando audio...")
    print(f"  Video: {video_path}")
    if voice_path:
        print(f"  Voz: {voice_path} ({voice_volume} dB)")
    if music_path:
        print(f"  Musica: {music_path} ({music_volume} dB)")
    if effects_path:
        print(f"  Efeitos: {effects_path} ({effects_volume} dB)")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"ERRO FFmpeg: {result.stderr[-500:]}")
            return None
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\nVideo mixado: {output_path} ({size_mb:.1f}MB)")
        return output_path
    except subprocess.TimeoutExpired:
        print("ERRO: Timeout na mixagem")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Mixa audio com video (voz + musica + efeitos)"
    )
    parser.add_argument("--video", required=True, help="Video base")
    parser.add_argument("--voz", default=None, help="Arquivo de voz/narracao")
    parser.add_argument("--musica", default=None, help="Arquivo de musica de fundo")
    parser.add_argument(
        "--efeitos", default=None, help="Arquivo ou diretorio de efeitos"
    )
    parser.add_argument("--saida", default=None, help="Caminho de saida")
    parser.add_argument(
        "--voz-volume", type=float, default=0.0, help="Volume da voz em dB (default: 0)"
    )
    parser.add_argument(
        "--musica-volume",
        type=float,
        default=-14.0,
        help="Volume da musica em dB (default: -14)",
    )
    parser.add_argument(
        "--efeitos-volume",
        type=float,
        default=-6.0,
        help="Volume dos efeitos em dB (default: -6)",
    )
    parser.add_argument(
        "--duracao", type=float, default=None, help="Duracao do video (para fade)"
    )
    args = parser.parse_args()

    result = mix_audio(
        video_path=args.video,
        voice_path=args.voz,
        music_path=args.musica,
        effects_path=args.efeitos,
        output_path=args.saida,
        voice_volume=args.voz_volume,
        music_volume=args.musica_volume,
        effects_volume=args.efeitos_volume,
        video_duration=args.duracao,
    )

    if result:
        print(f"\nProximo passo: publicar com content-publishing /publicar")


if __name__ == "__main__":
    main()
