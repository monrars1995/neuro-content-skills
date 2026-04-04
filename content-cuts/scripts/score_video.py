#!/usr/bin/env python3
"""Pontua potencial viral de videos short-form usando rubrica detalhada."""

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
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return {}


def get_duration(video_path: str) -> float:
    data = run_ffprobe(video_path, ["-print_format", "json", "-show_format"])
    return float(data.get("format", {}).get("duration", 0))


def get_resolution(video_path: str) -> tuple:
    data = run_ffprobe(video_path, ["-print_format", "json", "-show_streams"])
    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            return stream.get("width", 0), stream.get("height", 0)
    return 0, 0


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
            silences.append({"start": start, "end": end, "duracao": end - start})
    return silences


def get_loudness_stats(video_path: str) -> dict:
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

    stats = {}
    for line in result.stderr.splitlines():
        line = line.strip().strip("{}").strip(",")
        if not line:
            continue
        try:
            key, val = line.split(":", 1)
            key = key.strip().strip('"')
            val = val.strip().strip('"')
            stats[key] = float(val)
        except (ValueError, AttributeError):
            continue
    return stats


def extract_first_frame_text(video_path: str, timestamp: float = 2.0) -> str:
    output = "/tmp/first_frame_check.jpg"
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(timestamp),
        "-i",
        video_path,
        "-vframes",
        "1",
        "-q:v",
        "2",
        output,
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30)
        if os.path.exists(output):
            os.remove(output)
            return "frame_ok"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return "frame_error"


def score_hook(duration: float) -> dict:
    score = 0
    feedback = []

    if duration > 0:
        feedback.append(f"Duracao do video: {duration:.1f}s")
        if duration <= 15:
            score = 12
            feedback.append("Video muito curto - pode ser fraco em conteudo")
        elif duration <= 30:
            score = 18
            feedback.append("Duracao otima para hook rapido")
        elif duration <= 60:
            score = 16
            feedback.append("Duracao boa, mas hook precisa ser mais forte")
        elif duration <= 90:
            score = 13
            feedback.append("Duracao longa - hook critico nos 2s")
        else:
            score = 8
            feedback.append("Video muito longo para short-form")
    else:
        score = 5
        feedback.append("Nao foi possivel determinar duracao")

    return {"score": score, "max": 25, "feedback": feedback}


def score_pacing(silences: list, duration: float) -> dict:
    score = 0
    feedback = []

    if duration <= 0:
        return {"score": 0, "max": 20, "feedback": ["Duracao desconhecida"]}

    total_silence = sum(s["duracao"] for s in silences)
    silence_ratio = total_silence / duration

    long_silences = [s for s in silences if s["duracao"] > 1.0]

    if silence_ratio < 0.05:
        score = 18
        feedback.append("Excelente ritmo - quase sem silencios")
    elif silence_ratio < 0.10:
        score = 15
        feedback.append("Bom ritmo - poucos silencios")
    elif silence_ratio < 0.20:
        score = 11
        feedback.append("Ritmo irregular - alguns trechos lentos")
    elif silence_ratio < 0.35:
        score = 7
        feedback.append("Muitos silencios - ritmo lento")
    else:
        score = 3
        feedback.append("Excesso de silencios - precisa de edicao pesada")

    if long_silences:
        score -= min(len(long_silences) * 2, 6)
        feedback.append(f"{len(long_silences)} silencios longos (>1s) encontrados")

    cuts_estimate = len(silences) + 5
    cuts_per_minute = (cuts_estimate / duration) * 60 if duration > 0 else 0
    feedback.append(f"~{cuts_per_minute:.0f} cortes/minuto estimados")

    return {"score": max(score, 0), "max": 20, "feedback": feedback}


def score_engagement(duration: float) -> dict:
    score = 8
    feedback = ["Nota base: sem analise de transcricao"]

    feedback.append("Para pontuacao completa, gere legendas com content-editing")
    feedback.append("e reavalie com transricao disponivel")

    if 30 <= duration <= 60:
        score = 10
        feedback.append("Duracao adequada para engajamento")

    return {"score": score, "max": 20, "feedback": feedback}


def score_format(width: int, height: int, duration: float) -> dict:
    score = 0
    feedback = []

    if width == 1080 and height == 1920:
        score = 12
        feedback.append("Formato vertical 9:16 correto")
    elif width == 1920 and height == 1080:
        score = 6
        feedback.append("Formato horizontal 16:9 - considere recortar para 9:16")
    elif width == 1080 and height == 1080:
        score = 8
        feedback.append("Formato quadrado 1:1 - aceitavel para feed")
    elif width >= 720 and height > width:
        score = 9
        feedback.append("Formato vertical, mas resolucao nao otima")
    else:
        score = 4
        feedback.append(f"Formato nao otimizado: {width}x{height}")

    if width >= 1080 and height >= 1920:
        feedback.append("Resolucao HD ou superior")
    elif width >= 720:
        feedback.append("Resolucao adequada")
    else:
        score -= 3
        feedback.append("Resolucao baixa - considere re-encode")

    return {"score": max(score, 0), "max": 15, "feedback": feedback}


def score_audio(loudness: dict, silences: list) -> dict:
    score = 0
    feedback = []

    lufs = loudness.get("input_i", 0)
    tp = loudness.get("input_tp", 0)
    lra = loudness.get("input_lra", 0)

    if lufs:
        if -16 <= lufs <= -13:
            score = 8
            feedback.append(f"LUFS ideal: {lufs:.1f}")
        elif -20 <= lufs <= -10:
            score = 6
            feedback.append(f"LUFS aceitavel: {lufs:.1f}")
        else:
            score = 4
            feedback.append(f"LUFS fora do range ideal: {lufs:.1f}")

    if tp:
        if tp <= -1.0:
            feedback.append(f"True peak seguro: {tp:.1f} dBTP")
        elif tp <= 0.0:
            score -= 1
            feedback.append(f"True peak proximo do limite: {tp:.1f} dBTP")
        else:
            score -= 3
            feedback.append(f"CLIPPING DETECTADO: {tp:.1f} dBTP")

    if lra:
        if lra <= 10:
            feedback.append(f"LRA bom: {lra:.1f} LU")
        elif lra <= 20:
            feedback.append(f"LRA moderado: {lra:.1f} LU")
        else:
            score -= 2
            feedback.append(f"LRA alto (dinamica excessiva): {lra:.1f} LU")

    if not lufs:
        score = 5
        feedback.append("Nao foi possivel medir loudness")

    return {"score": max(score, 0), "max": 10, "feedback": feedback}


def score_cta(duration: float) -> dict:
    score = 5
    feedback = ["Nota base: sem analise de transcricao do final"]

    if duration > 5:
        feedback.append(f"Video tem {duration:.0f}s - verifique CTA nos ultimos 5s")
    feedback.append("Para pontuacao completa, gere legendas e reavalie")

    return {"score": score, "max": 10, "feedback": feedback}


def generate_suggestions(scores: dict) -> list:
    suggestions = []
    total = scores["total"]

    if scores["hook"]["score"] < 18:
        suggestions.append(
            "1. Reforce o hook nos primeiros 3s com frase de impacto (+3-5 pts)"
        )

    if scores["pacing"]["score"] < 14:
        suggestions.append("2. Remova silencios longos e acelere o ritmo (+3-5 pts)")

    if scores["engagement"]["score"] < 14:
        suggestions.append(
            "3. Adicione pergunta ou controversia para engajamento (+3-5 pts)"
        )

    if scores["format"]["score"] < 10:
        suggestions.append("4. Ajuste formato para 9:16 vertical 1080x1920 (+3-5 pts)")

    if scores["audio"]["score"] < 7:
        suggestions.append("5. Normalize audio com loudness target -14 LUFS (+3-4 pts)")

    if scores["cta"]["score"] < 7:
        suggestions.append("6. Adicione CTA especifico nos ultimos 3-5s (+3-5 pts)")

    if not suggestions:
        suggestions.append("Video bem otimizado! Considere impulsionar com ads.")

    return suggestions


def main():
    parser = argparse.ArgumentParser(
        description="Pontua potencial viral de videos short-form"
    )
    parser.add_argument("--video", required=True, help="Caminho do video")
    parser.add_argument("--cliente", default=None, help="Nome do cliente")
    parser.add_argument(
        "--saida",
        default=None,
        help="Diretorio de saida (default: mesmo diretorio do video)",
    )
    parser.add_argument(
        "--json", action="store_true", help="Saida apenas em JSON (sem texto)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERRO: Video nao encontrado: {args.video}")
        sys.exit(1)

    print(f"Avaliando: {args.video}")

    duration = get_duration(args.video)
    width, height = get_resolution(args.video)
    silences = detect_silences(args.video)
    loudness = get_loudness_stats(args.video)

    scores = {
        "hook": score_hook(duration),
        "pacing": score_pacing(silences, duration),
        "engagement": score_engagement(duration),
        "format": score_format(width, height, duration),
        "audio": score_audio(loudness, silences),
        "cta": score_cta(duration),
    }

    total = sum(s["score"] for s in scores.values())
    scores["total"] = total
    scores["max_total"] = 100
    scores["classificacao"] = _classify(total)

    if not args.json:
        _print_report(args.video, scores)

    report = {
        "video": os.path.basename(args.video),
        "caminho": str(args.video),
        "duracao": round(duration, 2),
        "resolucao": f"{width}x{height}",
        "pontuacao": {
            "total": total,
            "max": 100,
            "classificacao": scores["classificacao"],
        },
        "categorias": {
            key: {
                "pontuacao": val["score"],
                "max": val["max"],
                "feedback": val["feedback"],
            }
            for key, val in scores.items()
            if key not in ("total", "max_total", "classificacao")
        },
        "sugestoes": generate_suggestions(scores),
        "metadata": {
            "silencios": len(silences),
            "loudness": loudness,
        },
    }

    if args.saida:
        out_dir = Path(args.saida)
        out_dir.mkdir(parents=True, exist_ok=True)
        json_path = str(out_dir / f"{Path(args.video).stem}_pontuacao.json")
    else:
        json_path = f"{os.path.splitext(args.video)[0]}_pontuacao.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    if not args.json:
        print(f"\nRelatorio salvo: {json_path}")


def _classify(total: int) -> str:
    if total >= 85:
        return "viral_garantido"
    elif total >= 70:
        return "alto_potencial"
    elif total >= 55:
        return "potencial_medio"
    elif total >= 40:
        return "precisa_melhorar"
    return "descartar_ou_refazer"


def _print_report(video: str, scores: dict):
    status_icons = {
        "viral_garantido": "🔥 VIRAL GARANTIDO",
        "alto_potencial": "🚀 ALTO POTENCIAL",
        "potencial_medio": "📊 POTENCIAL MEDIO",
        "precisa_melhorar": "⚠️ PRECISA MELHORAR",
        "descartar_ou_refazer": "❌ DESCARTAR OU REFazer",
    }

    print(f"\n{'=' * 40}")
    print(f"  PONTUACAO VIRAL")
    print(f"{'=' * 40}")
    print(f"  Total: {scores['total']}/100")
    print(
        f"  Status: {status_icons.get(scores['classificacao'], scores['classificacao'])}"
    )
    print(f"{'=' * 40}\n")

    categories = [
        ("Hook", scores["hook"]),
        ("Ritmo", scores["pacing"]),
        ("Engajamento", scores["engagement"]),
        ("Formato", scores["format"]),
        ("Audio", scores["audio"]),
        ("CTA", scores["cta"]),
    ]

    for name, cat in categories:
        pct = cat["score"] / cat["max"] * 100
        bar_len = 15
        filled = int(pct / 100 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"  {name:12} {cat['score']:2}/{cat['max']:<2} [{bar}]")

    suggestions = generate_suggestions(scores)
    if suggestions:
        print(f"\nSugestoes:")
        for s in suggestions:
            print(f"  {s}")


if __name__ == "__main__":
    main()
