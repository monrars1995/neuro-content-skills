#!/usr/bin/env python3
"""Gera pontos de zoom para Remotion baseado em palavras-chave da transcricao."""

import argparse
import json
import os
import sys
import re
from pathlib import Path


DEFAULT_KEYWORDS = {
    "universal": [
        "importante",
        "incrivel",
        "secreto",
        "resultado",
        "problema",
        "solucao",
        "erro",
        "acabou",
        "nunca",
        "sempre",
        "verdade",
        "mentira",
        "dica",
        "passo",
        "primeiro",
        "ultimo",
    ],
    "engajamento": [
        "comente",
        "responda",
        "opiniao",
        "concorda",
        "discorda",
        "voce",
        "qual",
        "qualquer",
        "todo mundo",
        "ninguem",
    ],
    "acao": [
        "faca",
        "comece",
        "pare",
        "use",
        "teste",
        "tente",
        "clique",
        "inscreva",
        "salve",
        "compartilhe",
    ],
    "impacto": [
        "10x",
        "100%",
        "milhoes",
        "viral",
        "explosao",
        "choque",
        "absurdo",
        "impossivel",
        "facil",
        "rapido",
    ],
}


def load_transcription(video_path: str) -> list:
    base = os.path.splitext(video_path)[0]
    for ext in ["_legendas.json", "_remotion_subtitles.json", "_analise.json"]:
        path = f"{base}{ext}"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "words" in data:
                return data["words"]
    return []


def find_keyword_zooms(words: list, keywords: list, fps: int = 30) -> list:
    zoom_points = []
    seen_frames = set()

    keyword_lower = [k.lower() for k in keywords]
    min_interval_frames = int(fps * 2)

    for w in words:
        text = w.get("word", "").strip().lower().rstrip(".,!?;:")
        if text in keyword_lower:
            frame = w.get("startFrame", int(w.get("start", 0) * fps))
            too_close = any(
                abs(frame - seen) < min_interval_frames for seen in seen_frames
            )
            if not too_close:
                zoom_points.append(
                    {
                        "frame": frame,
                        "scale": 1.3,
                        "duration": int(fps * 0.5),
                        "keyword": text,
                        "type": "keyword",
                    }
                )
                seen_frames.add(frame)

    return zoom_points


def find_phrase_zooms(words: list, fps: int = 30) -> list:
    zoom_points = []
    current_phrase = []
    phrase_start = 0

    for w in words:
        text = w.get("word", "").strip()
        if text:
            if not current_phrase:
                phrase_start = w.get("startFrame", int(w.get("start", 0) * fps))
            current_phrase.append(text)

        if text and text.endswith((".", "!", "?")):
            if len(current_phrase) >= 3:
                mid_idx = len(current_phrase) // 2
                mid_word = words[words.index(w) - len(current_phrase) + mid_idx]
                frame = mid_word.get("startFrame", int(mid_word.get("start", 0) * fps))
                zoom_points.append(
                    {
                        "frame": frame,
                        "scale": 1.15,
                        "duration": int(fps * 0.4),
                        "type": "phrase_mid",
                    }
                )
            current_phrase = []

    return zoom_points


def generate_zoom_timeline(words: list, intensity: str = "alta", fps: int = 30) -> list:
    all_keywords = []
    for category, kws in DEFAULT_KEYWORDS.items():
        all_keywords.extend(kws)

    keyword_zooms = find_keyword_zooms(words, all_keywords, fps)
    phrase_zooms = find_phrase_zooms(words, fps)

    scale_map = {
        "alta": {"keyword": 1.35, "phrase": 1.2, "interval": 2},
        "media": {"keyword": 1.25, "phrase": 1.15, "interval": 4},
        "baixa": {"keyword": 1.15, "phrase": 1.1, "interval": 6},
    }
    config = scale_map.get(intensity, scale_map["media"])

    for z in keyword_zooms:
        z["scale"] = config["keyword"]
        z["duration"] = int(fps * 0.4)
    for z in phrase_zooms:
        z["scale"] = config["phrase"]
        z["duration"] = int(fps * 0.3)

    all_zooms = keyword_zooms + phrase_zooms
    all_zooms.sort(key=lambda z: z["frame"])

    if intensity == "alta" and all_zooms:
        filled = []
        for i, z in enumerate(all_zooms):
            filled.append(z)
            if i < len(all_zooms) - 1:
                gap = all_zooms[i + 1]["frame"] - z["frame"]
                interval_frames = int(fps * config["interval"])
                if gap > interval_frames:
                    mid_frame = z["frame"] + interval_frames
                    filled.append(
                        {
                            "frame": mid_frame,
                            "scale": 1.1,
                            "duration": int(fps * 0.3),
                            "type": "fill",
                        }
                    )
        all_zooms = filled

    return all_zooms[:40]


def main():
    parser = argparse.ArgumentParser(
        description="Gera pontos de zoom baseados em palavras-chave"
    )
    parser.add_argument("--video", required=True, help="Video de entrada")
    parser.add_argument("--saida", default=None, help="Diretorio de saida")
    parser.add_argument(
        "--intensidade", default="alta", choices=["alta", "media", "baixa"]
    )
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument(
        "--keywords", default=None, help="Palavras-chave extras (comma-separated)"
    )
    args = parser.parse_args()

    words = load_transcription(args.video)
    if not words:
        print("ERRO: Nenhuma transcricao encontrada.")
        sys.exit(1)

    if args.keywords:
        extras = [k.strip() for k in args.keywords.split(",")]
        DEFAULT_KEYWORDS["custom"] = extras

    remotion_words = []
    for w in words:
        start = w.get("start", 0)
        text = w.get("word", "").strip()
        if text:
            remotion_words.append(
                {
                    "text": text,
                    "startFrame": int(start * args.fps),
                    "endFrame": int(w.get("end", start + 0.5) * args.fps),
                }
            )

    zoom_points = generate_zoom_timeline(remotion_words, args.intensidade, args.fps)

    result = {
        "video": os.path.basename(args.video),
        "intensidade": args.intensidade,
        "total_zooms": len(zoom_points),
        "zoom_points": zoom_points,
    }

    if args.saida:
        out_dir = Path(args.saida)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = str(out_dir / f"{Path(args.video).stem}_zoom_points.json")
    else:
        out_path = f"{os.path.splitext(args.video)[0]}_zoom_points.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Pontos de zoom: {out_path}")
    print(f"  Total: {len(zoom_points)}")
    print(f"  Intensidade: {args.intensidade}")

    keyword_count = sum(1 for z in zoom_points if z.get("type") == "keyword")
    phrase_count = sum(1 for z in zoom_points if z.get("type") == "phrase_mid")
    fill_count = sum(1 for z in zoom_points if z.get("type") == "fill")
    print(f"  Keyword: {keyword_count} | Phrase: {phrase_count} | Fill: {fill_count}")

    if zoom_points:
        print(f"\n  Primeiros 5:")
        for z in zoom_points[:5]:
            time_s = z["frame"] / args.fps
            print(
                f"    {time_s:.1f}s — scale {z['scale']}x ({z.get('type', 'unknown')})"
            )


if __name__ == "__main__":
    main()
