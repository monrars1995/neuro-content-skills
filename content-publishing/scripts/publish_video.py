#!/usr/bin/env python3
"""Publica videos no TikTok e Instagram via API."""

import argparse
import json
import logging
import os
import sys
import time
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


def publish_tiktok(
    creds: dict, video_path: str, title: str, description: str, hashtags: list
) -> dict:
    log.info("Iniciando publicacao no TikTok...")
    headers = {"Authorization": f"Bearer {creds['TIKTOK_ACCESS_TOKEN']}"}
    video_size = os.path.getsize(video_path)

    chunk_size = 5 * 1024 * 1024
    chunk_count = (video_size + chunk_size - 1) // chunk_size

    init_resp = requests.post(
        "https://open.tiktokapis.com/v2/post/publish/video/init/",
        headers=headers,
        json={
            "post_info": {
                "title": title[:150],
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
            },
            "source_info": {
                "video_size": video_size,
                "video_chunk_size": chunk_size,
                "video_chunk_count": chunk_count,
            },
        },
    )
    init_data = init_resp.json()
    if "error" in init_data and init_data["error"].get("code") != "ok":
        raise RuntimeError(f"TikTok init falhou: {init_data}")

    publish_id = init_data["data"]["publish_id"]
    upload_url = init_data["data"]["upload_url"]
    log.info("Upload URL obtida. Public ID: %s", publish_id)

    with open(video_path, "rb") as f:
        offset = 0
        part = 1
        while offset < video_size:
            end = min(offset + chunk_size, video_size)
            chunk = f.read(chunk_size)
            range_header = f"bytes {offset}-{end - 1}/{video_size}"
            put_resp = requests.put(
                upload_url,
                headers={
                    "Content-Range": range_header,
                    "Content-Type": "application/octet-stream",
                },
                data=chunk,
            )
            if put_resp.status_code not in (200, 201):
                raise RuntimeError(
                    f"Upload chunk {part} falhou: {put_resp.status_code}"
                )
            log.info(
                "Chunk %d/%d enviado (%d/%d bytes)", part, chunk_count, end, video_size
            )
            offset = end
            part += 1

    log.info("Todos os chunks enviados. Aguardando processamento...")
    time.sleep(5)

    for attempt in range(3):
        status_resp = requests.get(
            "https://open.tiktokapis.com/v2/post/publish/status/fetch/",
            headers=headers,
            params={"publish_id": publish_id},
        )
        status_data = status_resp.json()
        status = status_data.get("data", {}).get("status", "UNKNOWN")
        log.info("Tentativa %d - Status: %s", attempt + 1, status)

        if status == "COMPLETE":
            return {
                "platform": "tiktok",
                "publish_id": publish_id,
                "video_url": status_data["data"].get("video_url", ""),
                "status": "published",
            }
        elif status == "FAILED":
            raise RuntimeError(f"Publicacao falhou: {status_data}")
        time.sleep(10 * (attempt + 1))

    return {"platform": "tiktok", "publish_id": publish_id, "status": "pending_check"}


def publish_instagram(creds: dict, video_path: str, caption: str) -> dict:
    log.info("Iniciando publicacao no Instagram...")
    token = creds["META_ACCESS_TOKEN"]
    ig_user_id = creds["INSTAGRAM_BUSINESS_ACCOUNT_ID"]

    create_resp = requests.post(
        f"https://graph.facebook.com/v21.0/{ig_user_id}/media",
        params={
            "access_token": token,
            "media_type": "REELS",
            "video_url": video_path,
            "caption": caption[:2200],
            "share_to_feed": "true",
        },
    )
    create_data = create_resp.json()
    if "id" not in create_data:
        raise RuntimeError(f"Instagram container falhou: {create_data}")

    container_id = create_data["id"]
    log.info("Container criado: %s", container_id)

    for attempt in range(10):
        status_resp = requests.get(
            f"https://graph.facebook.com/v21.0/{container_id}",
            params={"fields": "status_code", "access_token": token},
        )
        status = status_resp.json().get("status_code", "UNKNOWN")
        log.info("Tentativa %d - Status: %s", attempt + 1, status)

        if status == "FINISHED":
            pub_resp = requests.post(
                f"https://graph.facebook.com/v21.0/{ig_user_id}/media_publish",
                params={"creation_id": container_id, "access_token": token},
            )
            pub_data = pub_resp.json()
            if "id" in pub_data:
                media_id = pub_data["id"]
                perm_resp = requests.get(
                    f"https://graph.facebook.com/v21.0/{media_id}",
                    params={"fields": "permalink", "access_token": token},
                )
                permalink = perm_resp.json().get("permalink", "")
                return {
                    "platform": "instagram",
                    "media_id": media_id,
                    "permalink": permalink,
                    "status": "published",
                }
            raise RuntimeError(f"Publish falhou: {pub_data}")
        elif status == "ERROR":
            raise RuntimeError(f"Container erro: {status_resp.json()}")
        time.sleep(10)

    return {"platform": "instagram", "container_id": container_id, "status": "timeout"}


def save_history(client: str, result: dict, video: str, metadata: dict):
    campaign_dir = BASE_DIR / "campanhas" / client
    history_path = campaign_dir / "historico.json"
    history_data = {"entries": []}
    if history_path.exists():
        raw = json.loads(history_path.read_text())
        if isinstance(raw, list):
            history_data["entries"] = raw
        elif isinstance(raw, dict) and "entries" in raw:
            history_data = raw

    entry = {
        "id": f"pub_{int(time.time())}",
        "data": time.strftime("%Y-%m-%d"),
        "tipo": "post",
        "titulo": metadata.get("titulo", ""),
        "plataformas": [result["platform"]],
        "data_publicacao": time.strftime("%Y-%m-%d %H:%M:%S"),
        "video": os.path.basename(video),
        "id_plataforma": result.get("publish_id") or result.get("media_id"),
        "url": result.get("video_url") or result.get("permalink", ""),
        "status": result["status"],
        "metricas": {},
        "notas": json.dumps(metadata, ensure_ascii=False),
    }
    history_data["entries"].append(entry)
    history_path.write_text(json.dumps(history_data, indent=2, ensure_ascii=False))
    log.info("Registro salvo em historico.json")

    publicados_dir = campaign_dir / "publicados"
    publicados_dir.mkdir(parents=True, exist_ok=True)
    dest = publicados_dir / os.path.basename(video)
    if os.path.exists(video):
        os.rename(video, dest)
        log.info("Video movido para publicados/")


def main():
    parser = argparse.ArgumentParser(description="Publica video em plataformas sociais")
    parser.add_argument("--cliente", required=True, help="Nome do cliente")
    parser.add_argument("--video", required=True, help="Caminho do video")
    parser.add_argument(
        "--plataforma", required=True, choices=["tiktok", "instagram", "ambos"]
    )
    parser.add_argument("--titulo", default="")
    parser.add_argument("--descricao", default="")
    parser.add_argument("--hashtags", default="", help="Hashtags separadas por virgula")
    args = parser.parse_args()

    creds = load_credentials(args.cliente)
    hashtags = (
        [h.strip() for h in args.hashtags.split(",") if h.strip()]
        if args.hashtags
        else []
    )
    caption = (
        f"{args.descricao}\n\n{' '.join('#' + h for h in hashtags)}"
        if hashtags
        else args.descricao
    )
    metadata = {
        "titulo": args.titulo,
        "descricao": args.descricao,
        "hashtags": hashtags,
    }

    results = []

    if args.plataforma in ("tiktok", "ambos"):
        if "TIKTOK_ACCESS_TOKEN" not in creds:
            log.error("TIKTOK_ACCESS_TOKEN nao configurado")
        else:
            results.append(
                publish_tiktok(creds, args.video, args.titulo, args.descricao, hashtags)
            )

    if args.plataforma in ("instagram", "ambos"):
        if "META_ACCESS_TOKEN" not in creds:
            log.error("META_ACCESS_TOKEN nao configurado")
        else:
            results.append(publish_instagram(creds, args.video, caption))

    for r in results:
        save_history(args.cliente, r, args.video, metadata)

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
