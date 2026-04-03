# Neuro Content Skills

Pipeline completo de criacao de conteudo para midias sociais, automatizado via Claude Code.

Automatiza todo o fluxo: desde a captacao de ideias com trends ate a publicacao e analise de metricas, passando por roteirizacao, gravacao e edicao.

## Pipeline

```
  1. IDEIAS          2. ROTEIRO         3. GRAVACAO        4. EDICAO
  (content-ideas) → (content-script) → (content-recording) → (content-editing)
                                                                    │
  6. METRICAS       5. PUBLICACAO                                    │
  (content-metrics) ← (content-publishing) ←─────────────────────────┘
```

## Skills

| Skill | Funcao | Recursos |
|-------|--------|----------|
| `content-workflow` | Orquestrador principal do pipeline | Comandos: `novo cliente`, `nova campanha`, `status` |
| `content-ideas` | Pesquisa de trends e captacao de ideias | Script: `fetch_trends.py` |
| `content-script` | Roteirizacao Hook → Desenvolvimento → CTA | Biblioteca de hooks por nicho |
| `content-recording` | Planejamento de gravacao e checklist | Guia de equipamentos por faixa de preco |
| `content-editing` | Edicao de video com Remotion | Templates 9:16 e 16:9, script de setup |
| `content-publishing` | Publicacao via TikTok e Instagram API | Script: `publish_video.py` |
| `content-metrics` | Analise de performance e insights | Script: `fetch_metrics.py` |
| `content-memory` | Memoria persistente e contexto do cliente | Schemas JSON documentados |
| `content-fs` | Estrutura de pastas e organizacao de midia | Estrutura completa documentada |

## Estrutura de Pastas

```
~/conteudo/
├── campanhas/
│   └── {cliente}/
│       ├── .env.cliente              (credenciais - NAO commitar)
│       ├── contexto.json             (preferencias e historico)
│       ├── historico.json            (log de publicacoes)
│       ├── posts-midias-sociais/
│       │   ├── ideias/               (.md)
│       │   ├── roteiros/             (.md)
│       │   ├── brutos/               (.mp4, .mov)
│       │   ├── editados/             (.mp4)
│       │   └── publicados/           (.mp4)
│       ├── criativos-anuncios/       (mesma sub-estrutura)
│       ├── briefings/                (.md, .pdf)
│       └── metricas/                 (.json, .md)
├── referencias/
│   ├── trends/                       (dados de pesquisa)
│   └── templates/                    (templates de script)
└── assets/
    ├── musicas/                      (audio royalty-free)
    ├── fontes/                       (fontes customizadas)
    └── overlays/                     (textos, lower thirds)
```

## Requisitos

- **Node.js** 18+
- **Python** 3.10+
- **FFmpeg** (processamento de video)
- **Remotion** (edicao programatica de video)
- **gh CLI** (GitHub CLI para publicacao)
- **pytrends** (Google Trends - `pip install pytrends`)

## Instalacao

### Claude Code Skills

Copie cada pasta de skill para o diretorio de skills do Claude Code:

```bash
cp -r content-* ~/.opencode/skills/
```

### Scripts Python

```bash
pip install pytrends requests python-dotenv
```

### Remotion + Next.js

Execute o script de setup automatico (cria o projeto Remotion se necessario):

```bash
bash ~/.opencode/skills/content-editing/scripts/setup_remotion.sh
```

## Uso

### Comandos Principais

| Comando | Descricao |
|---------|-----------|
| `novo cliente` | Onboarding completo: cria estrutura, inicializa memoria, configura APIs |
| `nova campanha [cliente]` | Inicia o pipeline completo de criacao de conteudo |
| `status` | Mostra status de todos os clientes e campanhas ativas |
| `continuar [cliente]` | Retoma o pipeline da ultima etapa pendente |

### Fluxo Tipico

1. **`novo cliente`** - Responde as perguntas interativas (niche, plataformas, tom, frequencia)
2. O pipeline inicia automaticamente na etapa de **Ideias**
3. A cada etapa, interaja com as perguntas e feedbacks
4. Ao final de **Publicacao**, as metricas sao coletadas automaticamente
5. Insights sao salvos e usados para otimizar os proximos conteudos

## Configuracao de APIs

As credenciais sao armazenadas em `~/conteudo/campanhas/{cliente}/.env.cliente` (nunca commitado).

### TikTok Content Posting API

1. Acesse [developers.tiktok.com](https://developers.tiktok.com)
2. Crie um App e ative "Content Posting"
3. Gere um Access Token
4. Configure: `TIKTOK_ACCESS_TOKEN`, `TIKTOK_APP_ID`

### Instagram Graph API

1. Acesse [developers.facebook.com](https://developers.facebook.com)
2. Crie um App Business vinculado a Pagina do Facebook
3. Ative Content Publishing para Instagram
4. Configure: `META_ACCESS_TOKEN`, `INSTAGRAM_BUSINESS_ACCOUNT_ID`, `FACEBOOK_PAGE_ID`

### Google Trends

Nenhuma chave necessaria. Usa a biblioteca `pytrends` (unofficial).

### Meta Ads Library API

1. Acesse [developers.facebook.com](https://developers.facebook.com)
2. Reutilize o App criado para Instagram
3. Configure: `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`

> Tutoriais detalhados em `content-ideas/references/api_setup.md` e `content-publishing/references/api_endpoints.md`

## Stack Tecnica

| Camada | Tecnologia |
|--------|-----------|
| Edicao de video | Remotion + Next.js + TypeScript |
| Scripts | Python 3.10+ (pytrends, requests, python-dotenv) |
| APIs | TikTok Content Posting API, Instagram Graph API v21, Meta Ads Library |
| Publicacao | TikTok Upload API, Instagram Reels via Graph API |
| Metricas | TikTok Research API, Instagram Insights via Graph API |

## Licenca

Este projeto esta sob a licenca [MIT](LICENSE).

Copyright (c) 2026 [monrars](https://github.com/monrars)
