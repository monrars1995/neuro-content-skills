---
name: content-ideas
description: "Captacao de ideias e pesquisa de trends para conteudo. Integra com TikTok Trends API, Google Trends e analise de trends do Instagram. Pesquisa referencias, analise concorrencia e gera banco de ideias. Use quando: pesquisar trends, buscar ideias de conteudo, analisar trends do tiktok, consultar google trends, encontrar referencias, criar banco de ideias, pesquisar concorrentes. Comandos: /trends, /ideias, /concorrentes."
---

# Content Ideas - Pesquisa de Tendencias e Ideias

## Onboarding Interativo

Na primeira utilizacao para um cliente, pergunte:

1. Qual o nicho/segmento do cliente? (ex: fitness, financas, gastronomia)
2. Quais plataformas ele publica? (TikTok, Instagram Reels, YouTube Shorts)
3. Quais concorrentes ou referencias ele acompanha?
4. Qual a frequencia de publicacao desejada? (diaria, 3x semana, semanal)

Salve as respostas em `~/conteudo/campanhas/{cliente}/perfil-cliente.md`.

## APIs e Credenciais

Todas as credenciais ficam em `~/conteudo/campanhas/{cliente}/.env.cliente`.

Consulte `references/api_setup.md` para tutoriais detalhados de configuracao de cada API.

Variaveis necessarias por API:

- **TikTok Content Posting API**: `TIKTOK_ACCESS_TOKEN`, `TIKTOK_BUSINESS_ID`
- **TikTok Trend API**: `TIKTOK_RESEARCH_API_KEY`
- **TikTok Metrics**: `TIKTOK_USERNAME` (necessario para coletar metricas do perfil)
- **Google Trends**: `GOOGLE_TRENDS_GEO` (padrao: BR), `GOOGLE_TRENDS_LANG` (padrao: pt)
- **Meta Ads Library API**: `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`

## Workflow

### 1. Trend Research

Consulte TikTok trends e Google Trends para o nicho do cliente.

- Execute `scripts/fetch_trends.py` com o nicho como argumento
- Revise os resultados JSON gerados em `~/conteudo/referencias/trends/`
- Identifique trends com potencial para o nicho

### 2. Competitor Analysis

- Acesse Meta Ads Library via API para buscar anuncios de concorrentes no nicho
- Liste os top 10 anuncios mais relevantes
- Salve em `~/conteudo/referencias/concorrentes/{concorrente}/`

### 3. Reference Collection

- Salve referencias interessantes em `~/conteudo/referencias/trends/`
- Organize por data e plataforma
- Inclua screenshot/link e breve descricao do por que e relevante

### 4. Idea Generation

Com base nas trends e no contexto do cliente:
- Cruze trends com o posicionamento do cliente
- Gere pelo menos 10 ideias por sessao de pesquisa
- Classifique por potencial (alto/medio/baixo)

### 5. Save Ideas

Armazene em `~/conteudo/campanhas/{cliente}/posts-midias-sociais/ideias/` como arquivos `.md`.

Crie o diretorio se nao existir:
```bash
mkdir -p ~/conteudo/campanhas/{cliente}/posts-midias-sociais/ideias/
```

## Template de Ideia

Cada ideia salva como markdown:

```markdown
# [Titulo da Ideia]
- **Data**: YYYY-MM-DD
- **Fonte**: [TikTok Trends / Google Trends / Meta Ads / Manual]
- **Tendencia**: [nome da trend]
- **Nicho**: [nicho do cliente]
- **Plataformas**: [tiktok, instagram, youtube]
- **Referencia**: [link ou descricao]
- **Conceito**: [descricao do conceito do video]
- **Potencial**: [alto/medio/baixo]
- **Tags**: [tag1, tag2, tag3]
```

## Scripts

### fetch_trends.py

Localizado em `scripts/fetch_trends.py`.

Uso:
```bash
python3 scripts/fetch_trends.py --nicho "fitness" --cliente "joao-academia"
```

O script:
- Le `.env.cliente` para chaves de API
- Busca hashtags em alta via TikTok Research API
- Busca dados do Google Trends via pytrends
- Gera JSON combinado com os dados de trends
- Salva em `~/conteudo/referencias/trends/{data}_trends.json`
