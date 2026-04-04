#!/usr/bin/env python3
"""Gera cortes otimizados para short-form baseados na analise do video."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def load_analysis(analysis_path: str) -> dict:
    if not os.path.exists(analysis_path):
        print(f"ERRO: Arquivo de analise nao encontrado: {analysis_path}")
        print("Execute analyze_video.py primeiro.")
        sys.exit(1)
    with open(analysis_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_best_segments(
    analysis: dict, max_duration: float, min_duration: float = 15.0
) -> list:
    segments = analysis.get("trechos_interessantes", [])
    silences = analysis.get("silencios", [])

    candidates = []
    for seg in segments:
        dur = seg["duracao"]
        if dur < min_duration:
            continue

        silences_in_seg = [
            s for s in silences if s["start"] >= seg["start"] and s["end"] <= seg["end"]
        ]
        silence_ratio = (
            sum(s["duracao"] for s in silences_in_seg) / dur if dur > 0 else 0
        )

        score = 0
        if 25 <= dur <= 60:
            score += 20
        elif 15 <= dur < 25:
            score += 15
        elif 60 < dur <= 90:
            score += 10
        elif dur > 90:
            score += 5

        if "potencial" in seg.get("motivo", ""):
            score += 15
        if "continuo" in seg.get("motivo", ""):
            score += 10

        score -= int(silence_ratio * 30)

        candidates.append(
            {
                **seg,
                "score": max(score, 0),
                "silencios_no_trecho": len(silences_in_seg),
            }
        )

    candidates.sort(key=lambda x: x["score"], reverse=True)

    selected = []
    used_ranges = []
    for c in candidates:
        if c["duracao"] > max_duration:
            c["end"] = c["start"] + max_duration
            c["duracao"] = max_duration

        overlap = False
        for u in used_ranges:
            if c["start"] < u["end"] and c["end"] > u["start"]:
                overlap = True
                break

        if not overlap:
            selected.append(c)
            used_ranges.append(c)

    return selected[:8]


def create_cut(
    video_path: str,
    start: float,
    end: float,
    output_path: str,
    target_width: int = 1080,
    target_height: int = 1920,
    remove_silences: bool = True,
    silence_threshold_db: float = -35,
    silence_min_duration: float = 0.4,
) -> bool:
    filters = []

    if target_height > target_width:
        filters.append(
            f"scale={target_width}:{target_height}:force_original_aspect_ratio=decrease"
        )
        filters.append(f"pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2:black")
    else:
        filters.append(
            f"scale={target_width}:{target_height}:force_original_aspect_ratio=decrease"
        )
        filters.append(f"pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2:black")

    vf = ",".join(filters)

    af = None
    if remove_silences:
        af = (
            f"silenceremove=start_periods=1:start_duration=0.1:start_threshold={silence_threshold_db}dB,"
            f"stop_periods=-1:stop_duration=0.1:stop_threshold={silence_threshold_db}dB,"
            f"areverse,silenceremove=start_periods=1:start_duration=0.1:start_threshold={silence_threshold_db}dB,"
            f"stop_periods=-1:stop_duration=0.1:stop_threshold={silence_threshold_db}dB,areverse"
        )

    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start),
        "-to",
        str(end),
        "-i",
        video_path,
        "-vf",
        vf,
    ]

    if af:
        cmd.extend(["-af", af])

    cmd.extend(
        [
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
            output_path,
        ]
    )

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"  ERRO FFmpeg: {result.stderr[-200:]}")
            return False
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  OK: {output_path} ({size_mb:.1f}MB)")
        return True
    except subprocess.TimeoutExpired:
        print(f"  ERRO: Timeout ao gerar {output_path}")
        return False
    except FileNotFoundError:
        print("  ERRO: FFmpeg nao encontrado. Instale: brew install ffmpeg")
        return False


def generate_cuts(
    video_path: str,
    analysis: dict,
    output_dir: str,
    plataforma: str,
    max_duration: float,
    remove_silences: bool = True,
) -> list:
    plataforma_dims = {
        "reels": (1080, 1920),
        "shorts": (1080, 1920),
        "tiktok": (1080, 1920),
        "feed": (1920, 1080),
        "stories": (1080, 1920),
        "quadrado": (1080, 1080),
    }

    dims = plataforma_dims.get(plataforma.lower(), (1080, 1920))
    segments = get_best_segments(analysis, max_duration)

    if not segments:
        print("Nenhum trecho adequado encontrado. Gerando corte do video completo...")
        dur = analysis["metadata"]["duracao"]
        segments = [
            {
                "start": 0,
                "end": min(dur, max_duration),
                "duracao": min(dur, max_duration),
                "score": 0,
                "motivo": "video_completo",
                "silencios_no_trecho": 0,
            }
        ]

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    base_name = Path(video_path).stem
    cuts = []

    print(
        f"\nGerando {len(segments)} cortes para {plataforma.upper()} ({dims[0]}x{dims[1]}):"
    )

    for i, seg in enumerate(segments, 1):
        filename = f"{base_name}_corte_{i:02d}.mp4"
        filepath = str(out_path / filename)

        print(
            f"  Corte {i}: {seg['start']:.1f}s - {seg['end']:.1f}s ({seg['duracao']}s) [score: {seg['score']}]"
        )

        success = create_cut(
            video_path=video_path,
            start=seg["start"],
            end=seg["end"],
            output_path=filepath,
            target_width=dims[0],
            target_height=dims[1],
            remove_silences=remove_silences,
        )

        cuts.append(
            {
                "arquivo": filename,
                "caminho": filepath,
                "start": seg["start"],
                "end": seg["end"],
                "duracao_original": seg["duracao"],
                "score": seg["score"],
                "plataforma": plataforma,
                "resolucao": f"{dims[0]}x{dims[1]}",
                "sucesso": success,
            }
        )

    return cuts


def main():
    parser = argparse.ArgumentParser(
        description="Gera cortes otimizados para short-form"
    )
    parser.add_argument("--video", required=True, help="Caminho do video de origem")
    parser.add_argument(
        "--analise",
        default=None,
        help="Arquivo JSON de analise (gerado por analyze_video.py)",
    )
    parser.add_argument("--cliente", default=None, help="Nome do cliente")
    parser.add_argument("--saida", required=True, help="Diretorio de saida dos cortes")
    parser.add_argument(
        "--plataforma",
        default="reels",
        choices=["reels", "shorts", "tiktok", "feed", "stories", "quadrado"],
    )
    parser.add_argument(
        "--max-duracao",
        type=float,
        default=60.0,
        help="Duracao maxima de cada corte (default: 60s)",
    )
    parser.add_argument(
        "--min-duracao",
        type=float,
        default=15.0,
        help="Duracao minima de cada corte (default: 15s)",
    )
    parser.add_argument(
        "--no-remove-silences",
        action="store_true",
        help="Nao remover silencios nos cortes",
    )
    args = parser.parse_args()

    analysis_path = args.analise
    if not analysis_path:
        base = os.path.splitext(args.video)[0]
        analysis_path = f"{base}_analise.json"
        if not os.path.exists(analysis_path):
            analysis_path = None

    if analysis_path:
        analysis = load_analysis(analysis_path)
    else:
        print("Nenhum arquivo de analise encontrado. Executando analise rapida...")
        parent_dir = Path(__file__).parent.parent
        analyze_script = parent_dir / "scripts" / "analyze_video.py"
        if analyze_script.exists():
            cmd = [sys.executable, str(analyze_script), "--video", args.video]
            if args.cliente:
                cmd.extend(["--cliente", args.cliente])
            subprocess.run(cmd, timeout=120)
            base = os.path.splitext(args.video)[0]
            analysis_path = f"{base}_analise.json"
            analysis = load_analysis(analysis_path)
        else:
            print("ERRO: analyze_video.py nao encontrado e nenhuma analise fornecida.")
            sys.exit(1)

    cuts = generate_cuts(
        video_path=args.video,
        analysis=analysis,
        output_dir=args.saida,
        plataforma=args.plataforma,
        max_duration=args.max_duracao,
        remove_silences=not args.no_remove_silences,
    )

    report = {
        "video_origem": os.path.basename(args.video),
        "plataforma": args.plataforma,
        "max_duracao": args.max_duracao,
        "cortes": cuts,
        "total_cortes": len(cuts),
        "cortes_sucesso": sum(1 for c in cuts if c["sucesso"]),
    }

    report_path = os.path.join(args.saida, "cortes_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nRelatorio: {report_path}")
    print(f"Cortes gerados: {report['cortes_sucesso']}/{report['total_cortes']}")


if __name__ == "__main__":
    main()
