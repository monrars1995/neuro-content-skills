#!/usr/bin/env python3
"""Coleta metricas de performance do TikTok e Instagram."""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

BASE_DIR = Path.home() / "conteudo"


def load_credentials(client: str) -> dict:
    env_path = BASE_DIR / "campanhas" / client / ".env.cliente"
    if not env_path.exists():
        raise FileNotFoundError(f"Credenciais nao encontradas: {env_path}")
    creds = {}
    for line in env_path.read_text().strip().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            creds[key.strip()] = val.strip()
    return creds


def fetch_tiktok_metrics(creds: dict, start_date: str, end_date: str) -> list:
    log.info("Coletando metricas do TikTok (%s a %s)...", start_date, end_date)
    headers = {"Authorization": f"Bearer {creds['TIKTOK_ACCESS_TOKEN']}"}

    videos = []
    try:
        resp = requests.post(
            "https://open.tiktokapis.com/v2/research/video/query/",
            headers=headers,
            json={
                "query": {
                    "and": [
                        {
                            "operation": "IN",
                            "field_name": "username",
                            "field_values": [creds.get("TIKTOK_USERNAME", "")],
                        },
                        {
                            "operation": "GE",
                            "field_name": "create_time",
                            "field_values": [start_date],
                        },
                        {
                            "operation": "LE",
                            "field_name": "create_time",
                            "field_values": [end_date],
                        },
                    ]
                },
                "max_count": 100,
                "fields": [
                    "id",
                    "title",
                    "create_time",
                    "video_description",
                    "like_count",
                    "comment_count",
                    "share_count",
                    "view_count",
                    "save_count",
                    "avg_watch_time",
                    "total_watch_time",
                ],
            },
        )
        data = resp.json()
        if "data" in data and "videos" in data["data"]:
            for v in data["data"]["videos"]:
                videos.append(
                    {
                        "id": v.get("id", ""),
                        "titulo": v.get("title", ""),
                        "data_publicacao": v.get("create_time", ""),
                        "plataforma": "tiktok",
                        "metricas": {
                            "views": v.get("view_count", 0),
                            "likes": v.get("like_count", 0),
                            "comments": v.get("comment_count", 0),
                            "shares": v.get("share_count", 0),
                            "saves": v.get("save_count", 0),
                            "watch_time_avg": v.get("avg_watch_time", 0),
                            "watch_time_total": v.get("total_watch_time", 0),
                        },
                    }
                )
            log.info("TikTok: %d videos coletados", len(videos))
    except Exception as e:
        log.error("Erro ao coletar TikTok: %s", e)

    return videos


def fetch_instagram_metrics(creds: dict, since: str, until: str) -> list:
    log.info("Coletando metricas do Instagram (%s a %s)...", since, until)
    token = creds["META_ACCESS_TOKEN"]
    ig_user_id = creds["INSTAGRAM_BUSINESS_ACCOUNT_ID"]

    videos = []
    try:
        resp = requests.get(
            f"https://graph.facebook.com/v21.0/{ig_user_id}/media",
            params={
                "fields": "id,caption,timestamp,media_type,like_count,comments_count,insights,permalink",
                "access_token": token,
                "since": since,
                "until": until,
                "limit": 100,
            },
        )
        data = resp.json()
        media_list = data.get("data", [])

        for item in media_list:
            if item.get("media_type") != "REELS":
                continue

            insights_raw = item.get("insights", {}).get("data", [])
            metrics = {
                "likes": item.get("like_count", 0),
                "comments": item.get("comments_count", 0),
            }
            for ins in insights_raw:
                name = ins.get("name", "")
                values = ins.get("values", [])
                val = values[0].get("value", 0) if values else 0
                if name == "impressions":
                    metrics["impressions"] = val
                elif name == "reach":
                    metrics["reach"] = val
                elif name == "saved":
                    metrics["saves"] = val
                elif name == "shares":
                    metrics["shares"] = val
                elif name == "total_video_views":
                    metrics["views"] = val
                elif name == "average_watch_time":
                    metrics["watch_time_avg"] = val

            videos.append(
                {
                    "id": item.get("id", ""),
                    "titulo": (item.get("caption", "") or "")[:100],
                    "data_publicacao": item.get("timestamp", ""),
                    "plataforma": "instagram",
                    "url": item.get("permalink", ""),
                    "metricas": metrics,
                }
            )
        log.info("Instagram: %d reels coletados", len(videos))
    except Exception as e:
        log.error("Erro ao coletar Instagram: %s", e)

    return videos


def generate_report(client: str, videos: list, period: str) -> str:
    if not videos:
        return f"Nenhum video encontrado no periodo {period}."

    total_views = sum(v["metricas"].get("views", 0) for v in videos)
    eng_rates = []
    retention_3s_list = []

    for v in videos:
        m = v["metricas"]
        views = m.get("views", 0) or m.get("impressions", 0)
        if views > 0:
            eng = (
                (m.get("likes", 0) + m.get("comments", 0) + m.get("shares", 0)) / views
            ) * 100
            eng_rates.append(eng)

    avg_eng = sum(eng_rates) / len(eng_rates) if eng_rates else 0

    sorted_by_views = sorted(
        videos, key=lambda v: v["metricas"].get("views", 0) or 0, reverse=True
    )
    top3 = sorted_by_views[:3]

    report = f"# Relatorio de Performance - {client}\n\n"
    report += f"**Periodo**: {period}\n"
    report += f"**Total publicado**: {len(videos)} videos\n\n"
    report += "## Resumo\n"
    report += f"- Views totais: {total_views:,}\n"
    report += f"- Engajamento medio: {avg_eng:.1f}%\n"
    report += f"- Melhor video: [{top3[0]['titulo'][:50]}] ({top3[0]['metricas'].get('views', 0):,} views)\n\n"
    report += "## Top 3 Videos\n"
    for i, v in enumerate(top3, 1):
        m = v["metricas"]
        views = m.get("views", 0)
        eng = (
            (
                (m.get("likes", 0) + m.get("comments", 0) + m.get("shares", 0))
                / views
                * 100
            )
            if views
            else 0
        )
        report += (
            f"{i}. [{v['titulo'][:50]}] - {views:,} views, {eng:.1f}% engajamento\n"
        )

    return report


def save_results(client: str, videos: list, report: str, period: str):
    campaign_dir = BASE_DIR / "campanhas" / client
    metrics_dir = campaign_dir / "metricas"
    metrics_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    metrics_path = metrics_dir / f"metricas_{ts}.json"
    metrics_path.write_text(json.dumps(videos, indent=2, ensure_ascii=False))
    log.info("Metricas salvas em %s", metrics_path)

    report_path = metrics_dir / f"relatorio_{ts}.md"
    report_path.write_text(report)
    log.info("Relatorio salvo em %s", report_path)


def main():
    parser = argparse.ArgumentParser(
        description="Coleta metricas de plataformas sociais"
    )
    parser.add_argument("--cliente", required=True, help="Nome do cliente")
    parser.add_argument(
        "--dias", type=int, default=7, help="Dias a retroagir (default: 7)"
    )
    parser.add_argument("--data-inicio", default=None, help="Data inicio (YYYY-MM-DD)")
    parser.add_argument("--data-fim", default=None, help="Data fim (YYYY-MM-DD)")
    parser.add_argument(
        "--saida", default="json", choices=["json", "relatorio", "ambos"]
    )
    args = parser.parse_args()

    end_date = args.data_fim or datetime.now().strftime("%Y-%m-%d")
    start_date = args.data_inicio or (
        datetime.now() - timedelta(days=args.dias)
    ).strftime("%Y-%m-%d")
    period = f"{start_date} a {end_date}"

    creds = load_credentials(args.cliente)
    all_videos = []

    if "TIKTOK_ACCESS_TOKEN" in creds:
        all_videos.extend(fetch_tiktok_metrics(creds, start_date, end_date))

    if "META_ACCESS_TOKEN" in creds:
        ig_since = start_date.replace("-", "")
        ig_until = end_date.replace("-", "")
        all_videos.extend(fetch_instagram_metrics(creds, ig_since, ig_until))

    report = generate_report(args.cliente, all_videos, period)
    save_results(args.cliente, all_videos, report, period)

    if args.saida in ("json", "ambos"):
        print(json.dumps(all_videos, indent=2, ensure_ascii=False))
    if args.saida in ("relatorio", "ambos"):
        print("\n" + report)


if __name__ == "__main__":
    main()
