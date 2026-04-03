# Configuracao de APIs - Tutorial Completo

## 1. TikTok Content Posting API

### Passo a passo

1. Acesse https://developers.tiktok.com
2. Crie uma conta de desenvolvedor (se nao tiver)
3. Clique em "Create App" no dashboard
4. Selecione "Business" como tipo de app
5. Preencha nome e descricao do app
6. Na secao "Manage Apps", copie o App ID e App Secret
7. Configure OAuth 2.0: adicione redirect URI
8. Solicite permissoes: `video.publish`, `user.info.basic`
9. Gere o access token via OAuth flow
10. Copie o access token e o Business ID

### Variaveis de ambiente

```env
TIKTOK_ACCESS_TOKEN=seu_access_token_aqui
TIKTOK_BUSINESS_ID=seu_business_id_aqui
```

### Limites

- 100 posts por dia por app
- Rate limit: 100 requests por minuto
- Videos devem seguir as diretrizes da comunidade

### Referencia

- Documentacao: https://developers.tiktok.com/doc/content-posting-api-get-started/

---

## 2. TikTok Trend / Research API

### Passo a passo

1. Acesse https://developers.tiktok.com
2. Crie um app (se ja nao tiver)
3. Na secao "Products", ative "Research API"
4. Aguarde aprovacao (pode levar dias)
5. Apos aprovacao, gere uma API key
6. Configure as permissoes de pesquisa

### Variaveis de ambiente

```env
TIKTOK_RESEARCH_API_KEY=sua_research_api_key_aqui
```

### Endpoints uteis

- Trending hashtags: `/open_api/v2/research/trending/hashtag/`
- Trending videos: `/open_api/v2/research/trending/video/`
- Keyword research: `/open_api/v2/research/video/query/`

### Limites

- Acesso pode requerer verificacao de negocio
- Rate limits variam por endpoint

---

## 3. Google Trends (pytrends)

### Instalacao

```bash
pip3 install pytrends
```

### Configuracao

Nao requer API key. Configure apenas a regiao e idioma.

### Variaveis de ambiente

```env
GOOGLE_TRENDS_GEO=BR
GOOGLE_TRENDS_LANG=pt
```

### Codigos GEO uteis

| Regiao | Codigo |
|--------|--------|
| Brasil | BR |
| Portugal | PT |
| EUA | US |
| Global | (vazio) |

### Uso basico

```python
from pytrends.request import TrendReq

pytrends = TrendReq(hl='pt-BR', tz=180, geo='BR')
pytrends.build_payload(kw_list=['fitness'], timeframe='today 7-d')
interest = pytrends.interest_over_time()
related = pytrends.related_queries()
```

### Timeframes disponiveis

- `now 1-H`: ultima hora
- `now 4-H`: ultimas 4 horas
- `now 1-d`: ultimo dia
- `today 7-d`: ultimos 7 dias
- `today 1-m`: ultimo mes
- `today 3-m`: ultimos 3 meses
- `today 12-m`: ultimo ano
- `all`: desde 2004

### Limitacoes

- Nao e API oficial do Google
- Rate limits implicitos (evite requests consecutivos)
- Dados podem ter atraso de 1-2 dias

---

## 4. Meta Ads Library API

### Passo a passo

1. Acesse https://developers.facebook.com
2. Crie uma conta de desenvolvedor
3. Crie um novo app tipo "Business"
4. Va em "App Review" e solicite permissoes:
   - `ads_read`
   - `ad_library`
5. Va em "Settings" > "Advanced" > "Security"
6. Adicione seu usuario como desenvolvedor
7. Gere um access token de longa duracao
8. Para tokens de longa duracao, use o endpoint:
   ```
   GET /oauth/access_token
   ?grant_type=fb_exchange_token
   &client_id={app-id}
   &client_secret={app-secret}
   &fb_exchange_token={short-lived-token}
   ```

### Variaveis de ambiente

```env
META_ACCESS_TOKEN=seu_access_token_aqui
META_AD_ACCOUNT_ID=seu_ad_account_id_aqui
```

### Endpoint principal

```
GET https://graph.facebook.com/v19.0/ads_archive
  ?ad_reached_countries=BR
  &search_terms={nicho}
  &access_token={token}
  &limit=10
  &ad_active_status=ALL
```

### Campos retornados

- `ad_creative_bodies`: texto do anuncio
- `page_name`: nome da pagina
- `ad_delivery_start_time`: inicio da veiculacao
- `currency`: moeda
- `spend`: valor gasto (estimado)

### Limites

- 200 requests por hora por token
- Dados disponiveis apenas para paises selecionados
- Ads antigos podem ter campos faltando
