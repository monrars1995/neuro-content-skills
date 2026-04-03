#!/usr/bin/env python3

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("Instale requests: pip3 install requests")
    sys.exit(1)

try:
    from pytrends.request import TrendReq
except ImportError:
    print("Instale pytrends: pip3 install pytrends")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Instale python-dotenv: pip3 install python-dotenv")
    sys.exit(1)


def load_env(cliente: str) -> dict:
    base = Path.home() / "conteudo" / "campanhas" / cliente
    env_path = base / ".env.cliente"
    if not env_path.exists():
        print(f"Arquivo .env.cliente nao encontrado: {env_path}")
        sys.exit(1)
    load_dotenv(env_path)
    return {
        "tiktok_research_key": os.getenv("TIKTOK_RESEARCH_API_KEY", ""),
        "tiktok_access_token": os.getenv("TIKTOK_ACCESS_TOKEN", ""),
        "tiktok_business_id": os.getenv("TIKTOK_BUSINESS_ID", ""),
        "tiktok_username": os.getenv("TIKTOK_USERNAME", ""),
        "meta_access_token": os.getenv("META_ACCESS_TOKEN", ""),
        "meta_ad_account_id": os.getenv("META_AD_ACCOUNT_ID", ""),
        "google_trends_geo": os.getenv("GOOGLE_TRENDS_GEO", "BR"),
        "google_trends_lang": os.getenv("GOOGLE_TRENDS_LANG", "pt"),
    }


def fetch_tiktok_trends(env: dict, nicho: str) -> list:
    api_key = env["tiktok_research_key"]
    if not api_key:
        print("[TikTok] API key nao configurada, pulando...")
        return []

    trends = []
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        resp = requests.get(
            "https://business-api.tiktok.com/open_api/v2/research/trending/hashtag/",
            headers=headers,
            params={"keyword": nicho, "count": 20},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("data", {}).get("list"):
            for item in data["data"]["list"][:20]:
                trends.append(
                    {
                        "hashtag": item.get("hashtag_name", ""),
                        "views": item.get("video_views", 0),
                        "fonte": "tiktok",
                    }
                )
    except Exception as e:
        print(f"[TikTok] Erro: {e}")

    return trends


def fetch_google_trends(env: dict, nicho: str) -> list:
    trends = []
    try:
        pytrends = TrendReq(
            hl=env["google_trends_lang"],
            tz=180,
            geo=env["google_trends_geo"],
        )
        pytrends.build_payload(
            kw_list=[nicho],
            timeframe="today 7-d",
        )
        interest = pytrends.interest_over_time()

        related_queries = pytrends.related_queries()
        if related_queries and nicho in related_queries:
            rq = related_queries[nicho]
            if rq.get("rising"):
                for _, row in rq["rising"].head(15).iterrows():
                    trends.append(
                        {
                            "termo": row.get("query", ""),
                            "crescimento": row.get("value", 0),
                            "fonte": "google_trends",
                        }
                    )

        if not interest.empty:
            latest = interest.iloc[-1]
            trends.append(
                {
                    "termo": nicho,
                    "indice_atual": int(latest.values[0])
                    if len(latest.values) > 0
                    else 0,
                    "fonte": "google_trends_principal",
                }
            )

    except Exception as e:
        print(f"[Google Trends] Erro: {e}")

    return trends


def fetch_meta_ads(env: dict, nicho: str) -> list:
    token = env["meta_access_token"]
    if not token:
        print("[Meta] Access token nao configurado, pulando...")
        return []

    ads = []
    try:
        url = (
            "https://graph.facebook.com/v19.0/ads_archive"
            f"?ad_reached_countries=BR&search_terms={nicho}"
            f"&access_token={token}&limit=10"
        )
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        for ad in data.get("data", []):
            ads.append(
                {
                    "id": ad.get("id", ""),
                    "titulo": ad.get("ad_creative_bodies", [""])[0]
                    if ad.get("ad_creative_bodies")
                    else "",
                    "pagina": ad.get("page_name", ""),
                    "fonte": "meta_ads_library",
                }
            )
    except Exception as e:
        print(f"[Meta Ads] Erro: {e}")

    return ads


def save_results(results: dict, nicho: str):
    output_dir = Path.home() / "conteudo" / "referencias" / "trends"
    output_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().strftime("%Y-%m-%d")
    filename = output_dir / f"{today}_{nicho.replace(' ', '_')}_trends.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Resultados salvos em: {filename}")
    return filename


def main():
    parser = argparse.ArgumentParser(description="Busca trends para conteudo")
    parser.add_argument("--nicho", required=True, help="Nicho para pesquisa")
    parser.add_argument("--cliente", required=True, help="Nome do cliente")
    args = parser.parse_args()

    env = load_env(args.cliente)

    print(f"Buscando trends para nicho: {args.nicho}")
    print(f"Cliente: {args.cliente}\n")

    tiktok = fetch_tiktok_trends(env, args.nicho)
    google = fetch_google_trends(env, args.nicho)
    meta = fetch_meta_ads(env, args.nicho)

    results = {
        "data": date.today().isoformat(),
        "nicho": args.nicho,
        "cliente": args.cliente,
        "tiktok_trends": tiktok,
        "google_trends": google,
        "meta_ads": meta,
    }

    filepath = save_results(results, args.nicho)

    print(f"\nResumo:")
    print(f"  TikTok trends: {len(tiktok)}")
    print(f"  Google Trends: {len(google)}")
    print(f"  Meta Ads: {len(meta)}")


if __name__ == "__main__":
    main()
