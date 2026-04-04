#!/usr/bin/env python3
"""Analisa video para identificar pontos de corte, silencios e mudancas de cena."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run_ffprobe(video_path: str, args: list) -> dict:
    cmd = ["ffprobe", "-v", "quiet"] + args + [video_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"ERRO ffprobe: {e}")
        return {}


def get_metadata(video_path: str) -> dict:
    data = run_ffprobe(
        video_path,
        [
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
        ],
    )

    metadata = {
        "duracao": 0.0,
        "resolucao": "desconhecida",
        "fps": 0,
        "bitrate": 0,
        "codec_video": "",
        "codec_audio": "",
        "canais_audio": 0,
        "tem_audio": False,
    }

    fmt = data.get("format", {})
    metadata["duracao"] = float(fmt.get("duration", 0))
    metadata["bitrate"] = int(fmt.get("bit_rate", 0))

    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            w = stream.get("width", 0)
            h = stream.get("height", 0)
            metadata["resolucao"] = f"{w}x{h}"
            r_frame_rate = stream.get("r_frame_rate", "0/1")
            try:
                num, den = r_frame_rate.split("/")
                metadata["fps"] = round(float(num) / float(den))
            except (ValueError, ZeroDivisionError):
                metadata["fps"] = 30
            metadata["codec_video"] = stream.get("codec_name", "")
        elif stream.get("codec_type") == "audio":
            metadata["tem_audio"] = True
            metadata["codec_audio"] = stream.get("codec_name", "")
            metadata["canais_audio"] = int(stream.get("channels", 0))

    return metadata


def detect_silences(
    video_path: str, noise_db: float = -35, min_duration: float = 0.5
) -> list:
    cmd = [
        "ffmpeg",
        "-i",
        video_path,
        "-af",
        f"silencedetect=noise={noise_db}dB:d={min_duration}",
        "-f",
        "null",
        "-",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    silences = []
    for line in result.stderr.splitlines():
        line = line.strip()
        if line.startswith("silence_start"):
            start = float(line.split("=")[1])
        elif line.startswith("silence_end"):
            end = float(line.split("=")[1].split(" ")[0])
            silences.append(
                {
                    "start": round(start, 2),
                    "end": round(end, 2),
                    "duracao": round(end - start, 2),
                }
            )

    return silences


def detect_scenes(video_path: str, threshold: float = 0.3) -> list:
    try:
        from scenedetect import SceneManager, open_video
        from scenedetect.detectors import ContentDetector
    except ImportError:
        print("[INFO] scenedetect nao instalado, usando deteccao basica com ffmpeg")
        return _detect_scenes_ffmpeg(video_path, threshold)

    try:
        video = open_video(video_path)
        sm = SceneManager()
        sm.add_detector(ContentDetector(threshold=threshold))
        sm.detect_scenes(video, show_progress=False)
        scenes = sm.get_scene_list()
        return [
            {
                "timestamp": round(scene[0].get_seconds(), 2),
                "tipo": "hard_cut",
            }
            for scene in scenes
            if scene[0].get_seconds() > 1.0
        ]
    except Exception as e:
        print(f"[scenedetect] Erro: {e}")
        return []


def _detect_scenes_ffmpeg(video_path: str, threshold: float) -> list:
    data = run_ffprobe(
        video_path,
        [
            "-select_streams",
            "v:0",
            "-show_entries",
            "frame=pts_time",
            "-print_format",
            "json",
            "-skip_frame",
            "nokey",
        ],
    )
    if not data:
        return []

    frames = data.get("frames", [])
    if len(frames) < 10:
        return []

    cmd = [
        "ffmpeg",
        "-i",
        video_path,
        "-vf",
        f"select='gt(scene,{threshold})',showinfo",
        "-f",
        "null",
        "-",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    scenes = []
    for line in result.stderr.splitlines():
        if "pts_time:" in line:
            parts = line.split("pts_time:")
            if len(parts) > 1:
                try:
                    ts = float(parts[1].split(")")[0].strip())
                    if ts > 1.0:
                        scenes.append(
                            {
                                "timestamp": round(ts, 2),
                                "tipo": "hard_cut",
                            }
                        )
                except (ValueError, IndexError):
                    continue

    return scenes


def get_audio_loudness(video_path: str) -> dict:
    data = run_ffprobe(
        video_path,
        [
            "-f",
            "lavfi",
            "-i",
            f"amovie={video_path},astats=metadata=1:reset=0,ametadata=print:key=lavfi.astats.Overall.RMS_level:key=lavfi.astats.Overall.Peak_level:key=lavfi.astats.Overall.Flat_factor",
            "-show_frames",
            "-print_format",
            "json",
        ],
    )

    cmd = [
        "ffmpeg",
        "-i",
        video_path,
        "-af",
        "loudnorm=print_format=json",
        "-f",
        "null",
        "-",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {}

    loudness = {}
    for line in result.stderr.splitlines():
        line = line.strip().strip("{}").strip(",")
        if not line:
            continue
        try:
            key, val = line.split(":", 1)
            key = key.strip().strip('"')
            val = val.strip().strip('"')
            loudness[key] = (
                float(val) if val.lstrip("-").replace(".", "", 1).isdigit() else val
            )
        except (ValueError, AttributeError):
            continue

    return loudness


def find_interesting_segments(
    silences: list,
    scenes: list,
    duration: float,
    min_segment: float = 15.0,
    max_segment: float = 90.0,
) -> list:
    cut_points = set()
    for s in silences:
        if s["duracao"] >= 0.5:
            mid = (s["start"] + s["end"]) / 2
            cut_points.add(mid)
    for s in scenes:
        cut_points.add(s["timestamp"])

    sorted_cuts = sorted(cut_points)
    if not sorted_cuts:
        segments = [
            {"start": 0, "end": min(duration, max_segment), "motivo": "video_completo"}
        ]
        return segments

    boundaries = [0.0] + sorted_cuts + [duration]
    raw_segments = []
    for i in range(len(boundaries) - 1):
        seg_start = boundaries[i]
        seg_end = boundaries[i + 1]
        seg_dur = seg_end - seg_start
        if seg_dur >= min_segment:
            raw_segments.append(
                {"start": seg_start, "end": seg_end, "duracao": round(seg_dur, 2)}
            )

    if not raw_segments:
        return [
            {"start": 0, "end": min(duration, max_segment), "motivo": "video_completo"}
        ]

    merged = []
    current = raw_segments[0].copy()
    for seg in raw_segments[1:]:
        combined_dur = seg["end"] - current["start"]
        if combined_dur <= max_segment:
            current["end"] = seg["end"]
            current["duracao"] = round(combined_dur, 2)
        else:
            if current["duracao"] >= min_segment:
                motivo = "trecho_continuo"
                if current["duracao"] >= 30:
                    motivo = "trecho_longo_com_potencial"
                current["motivo"] = motivo
                merged.append(current)
            current = seg.copy()

    if current["duracao"] >= min_segment:
        current["motivo"] = "trecho_final"
        merged.append(current)

    return merged[:10]


def analyze(video_path: str) -> dict:
    if not os.path.exists(video_path):
        print(f"ERRO: Video nao encontrado: {video_path}")
        sys.exit(1)

    print(f"Analisando: {video_path}")

    print("  [1/4] Extraindo metadata...")
    metadata = get_metadata(video_path)
    print(
        f"         Duracao: {metadata['duracao']:.1f}s | Resolucao: {metadata['resolucao']} | FPS: {metadata['fps']}"
    )

    silences = []
    if metadata["tem_audio"]:
        print("  [2/4] Detectando silencios...")
        silences = detect_silences(video_path)
        print(f"         {len(silences)} silencios encontrados")

        print("  [3/4] Analisando loudness...")
        loudness = get_audio_loudness(video_path)
    else:
        print("  [2/4] Sem faixa de audio, pulando deteccao de silencios")
        print("  [3/4] Pulando loudness")
        loudness = {}

    print("  [4/4] Detectando mudancas de cena...")
    scenes = detect_scenes(video_path)
    print(f"         {len(scenes)} mudancas de cena")

    segments = find_interesting_segments(silences, scenes, metadata["duracao"])

    total_silence = sum(s["duracao"] for s in silences)
    speech_ratio = (
        1.0 - (total_silence / metadata["duracao"]) if metadata["duracao"] > 0 else 0
    )

    result = {
        "video": os.path.basename(video_path),
        "caminho": str(video_path),
        "metadata": metadata,
        "silencios": silences,
        "cenas": scenes,
        "loudness": loudness,
        "trechos_interessantes": segments,
        "resumo": {
            "total_silencios": len(silences),
            "duracao_total_silencios": round(total_silence, 2),
            "razao_fala": round(speech_ratio, 3),
            "total_cenas": len(scenes),
            "trechos_sugeridos": len(segments),
        },
    }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Analisa video para identificar pontos de corte"
    )
    parser.add_argument("--video", required=True, help="Caminho do video")
    parser.add_argument("--cliente", default=None, help="Nome do cliente")
    parser.add_argument(
        "--saida", default=None, help="Diretorio de saida para o relatorio"
    )
    parser.add_argument(
        "--noise-db",
        type=float,
        default=-35,
        help="Limiar de ruido em dB (default: -35)",
    )
    parser.add_argument(
        "--min-silence",
        type=float,
        default=0.5,
        help="Duracao minima de silencio (default: 0.5s)",
    )
    parser.add_argument(
        "--scene-threshold",
        type=float,
        default=0.3,
        help="Limiar de deteccao de cena (default: 0.3)",
    )
    args = parser.parse_args()

    result = analyze(args.video)

    base = os.path.splitext(args.video)[0]
    json_filename = f"{base}_analise.json"

    if args.saida:
        saida_dir = Path(args.saida)
        saida_dir.mkdir(parents=True, exist_ok=True)
        json_filename = str(saida_dir / f"{Path(args.video).stem}_analise.json")

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nRelatorio salvo: {json_filename}")

    r = result["resumo"]
    print(f"\n=== RESUMO ===")
    print(f"Duracao: {result['metadata']['duracao']:.1f}s")
    print(f"Resolucao: {result['metadata']['resolucao']}")
    print(f"Silencios: {r['total_silencios']} ({r['duracao_total_silencios']}s total)")
    print(f"Razao fala: {r['razao_fala'] * 100:.1f}%")
    print(f"Mudancas de cena: {r['total_cenas']}")
    print(f"Trechos sugeridos: {r['trechos_sugeridos']}")

    if result["trechos_interessantes"]:
        print(f"\n=== TRECHOS SUGERIDOS ===")
        for i, seg in enumerate(result["trechos_interessantes"], 1):
            print(
                f"  {i}. {seg['start']:.1f}s - {seg['end']:.1f}s ({seg['duracao']}s) [{seg['motivo']}]"
            )


if __name__ == "__main__":
    main()
