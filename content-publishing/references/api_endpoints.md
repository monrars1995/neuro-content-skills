# Referencia de Endpoints de API

## TikTok Content Posting API v2

Base URL: `https://open.tiktokapis.com/v2`

Auth: Bearer token no header `Authorization`

### 1. Inicializar Upload de Video

```
POST /post/publish/video/init/
```

Request:
```json
{
  "post_info": {
    "title": "string",
    "privacy_level": "PUBLIC_TO_EVERYONE | FOLLOWERS_ONLY | PRIVATE",
    "disable_duet": false,
    "disable_comment": false,
    "disable_stitch": false
  },
  "source_info": {
    "video_size": 12345678,
    "video_chunk_size": 5242880,
    "video_chunk_count": 3
  }
}
```

Response:
```json
{
  "data": {
    "publish_id": "string",
    "upload_url": "https://...",
    "video_id": "string"
  },
  "error": {
    "code": "string",
    "message": "string"
  }
}
```

### 2. Upload de Chunk de Video

```
PUT {upload_url}
```

Headers:
- `Content-Range: bytes {start}-{end}/{total}`

Body: chunk binario do video

### 3. Criar Post com Video

```
POST /post/publish/content/init/
```

Request:
```json
{
  "post_info": {
    "title": "string",
    "description": "string",
    "hashtags": ["tag1", "tag2"],
    "privacy_level": "PUBLIC_TO_EVERYONE"
  },
  "source_info": {
    "source": "PULL_FROM_URL",
    "video_url": "https://..."
  },
  "post_mode": "DIRECT_POST | UPLOAD_TO_DRAFT"
}
```

Response:
```json
{
  "data": {
    "publish_id": "string"
  },
  "error": {
    "code": "string",
    "message": "string"
  }
}
```

### 4. Verificar Status de Publicacao

```
GET /post/publish/status/fetch/?publish_id={publish_id}
```

Response:
```json
{
  "data": {
    "publish_id": "string",
    "status": "PUBLISHING | COMPLETE | FAILED",
    "create_time": 1234567890,
    "video_url": "https://...",
    "error_code": "string",
    "error_message": "string"
  }
}
```

### Codigos de Erro TikTok

| Codigo | Descricao |
|--------|-----------|
| `ok` | Sucesso |
| `video.upload.init.failed` | Falha ao iniciar upload |
| `video.upload.failed` | Falha no upload do video |
| `video.publish.failed` | Falha na publicacao |
| `content.violation` | Conteudo viola diretrizes |
| `invalid_token` | Token invalido ou expirado |
| `rate.limit.exceeded` | Rate limit atingido |

### Rate Limits TikTok

- Upload init: 100 requests/dia
- Content publish: 100 requests/dia
- Status fetch: 1000 requests/dia

---

## Instagram Graph API v21.0

Base URL: `https://graph.facebook.com/v21.0`

Auth: Bearer token no header `Authorization` ou `access_token` param

### 1. Criar Container de Media (Reel)

```
POST /{ig-user-id}/media
```

Params:
- `access_token`: Long-lived access token
- `video_url`: URL do video (MP4, acessivel publicamente)
- `media_type`: `REELS`
- `caption`: Legenda do post
- `share_to_feed`: `true` para compartilhar no feed
- `title`: Titulo do Reel

Response:
```json
{
  "id": "container_id_string"
}
```

### 2. Verificar Status do Container

```
GET /{container-id}?fields=status_code
```

Response:
```json
{
  "status_code": "IN_PROGRESS | FINISHED | ERROR",
  "id": "container_id_string"
}
```

### 3. Publicar Media

```
POST /{ig-user-id}/media_publish
```

Params:
- `access_token`: Long-lived access token
- `creation_id`: ID do container aprovado

Response:
```json
{
  "id": "media_id_string"
}
```

### 4. Obter Permalinks

```
GET /{media-id}?fields=permalink,media_type,timestamp,like_count,comments_count
```

### Codigos de Erro Instagram

| Codigo | Descricao |
|--------|-----------|
| `OAuthException` | Token invalido ou sem permissao |
| `IG-API-Usage-Limit-Reached` | Rate limit atingido |
| `Unsupported video type` | Formato de video nao suportado |
| `VideoTooLong` | Video excede duracao maxima (90s Reels) |
| `VideoTooShort` | Video muito curto |
| `Invalid media source` | URL do video invalida ou inacessivel |

### Rate Limits Instagram

- Container creation: 25 calls/user/hora
- Publish: 25 calls/user/hora
- Insights: 200 calls/user/hora

### Formatos Suportados

| Plataforma | Formato | Resolucao | Duracao | Tamanho Max |
|-----------|---------|-----------|---------|-------------|
| TikTok | MP4, MOV | 1080x1920 (9:16) | 3s - 10min | 287MB |
| Instagram Reels | MP4 | 1080x1920 (9:16) | 3s - 90s | 650MB |
