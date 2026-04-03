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

  PLANEJAMENTO
  /create-linha-editorial → /create-editorial → /nova-campanha → pipeline
```

## Skills

| Skill | Funcao | Slash Commands |
|-------|--------|---------------|
| `content-workflow` | Orquestrador principal do pipeline | `/cliente-setup`, `/nova-campanha`, `/status`, `/continuar` |
| `content-editorial` | Linha editorial e calendario | `/create-linha-editorial`, `/create-editorial` |
| `content-ideas` | Pesquisa de trends e captacao de ideias | `/trends`, `/ideias`, `/concorrentes` |
| `content-script` | Roteirizacao Hook → Desenvolvimento → CTA | `/roteiro`, `/hook`, `/cta` |
| `content-recording` | Planejamento de gravacao e checklist | `/gravar`, `/plano-gravacao`, `/checklist` |
| `content-editing` | Edicao de video com Remotion | `/editar`, `/render`, `/legendas`, `/template` |
| `content-publishing` | Publicacao via TikTok e Instagram API | `/publicar`, `/agendar`, `/setup-api` |
| `content-metrics` | Analise de performance e insights | `/metricas`, `/relatorio`, `/insights` |
| `content-memory` | Memoria persistente e contexto do cliente | `/lembrar`, `/historico`, `/stories`, `/contexto` |
| `content-fs` | Estrutura de pastas e organizacao de midia | `/organizar`, `/listar-midias`, `/analisar-midia` |

## Comandos Slash

### Planejamento e Setup

| Comando | Descricao | Uso |
|---------|-----------|-----|
| `/cliente-setup [nome]` | Onboarding completo de novo cliente | `/cliente-setup`, `/cliente-setup Acme Corp` |
| `/create-linha-editorial [cliente]` | Cria linha editorial (pilares, formatos, frequencia) | `/create-linha-editorial`, `/create-linha-editorial Acme Corp` |
| `/create-editorial [cliente] [mes]` | Gera calendario editorial mensal | `/create-editorial`, `/create-editorial Acme Corp 2026-04` |

### Pipeline de Criacao

| Comando | Descricao | Uso |
|---------|-----------|-----|
| `/nova-campanha [cliente]` | Inicia pipeline completo de conteudo | `/nova-campanha`, `/nova-campanha Acme Corp` |
| `/status` | Painel de status de todos os clientes | `/status` |
| `/continuar [cliente]` | Retoma pipeline da etapa pendente | `/continuar`, `/continuar Acme Corp` |

### Pesquisa e Ideias

| Comando | Descricao | Uso |
|---------|-----------|-----|
| `/trends [cliente]` | Busca trends atuais por nicho do cliente | `/trends`, `/trends Acme Corp` |
| `/ideias [cliente]` | Gera ideias de conteudo baseadas em trends | `/ideias`, `/ideias Acme Corp` |
| `/concorrentes [cliente]` | Analisa anuncios de concorrentes (Meta Ads Library) | `/concorrentes`, `/concorrentes Acme Corp` |

### Criacao de Conteudo

| Comando | Descricao | Uso |
|---------|-----------|-----|
| `/roteiro [cliente]` | Cria roteiro completo Hook-Desenvolvimento-CTA | `/roteiro`, `/roteiro Acme Corp` |
| `/hook` | Gera hooks de alta retencao para video | `/hook` |
| `/cta` | Sugere CTAs relevantes por nicho | `/cta` |
| `/gravar [roteiro]` | Gera plano de gravacao com checklist | `/gravar`, `/gravar meu-video` |
| `/plano-gravacao [roteiro]` | Plano detalhado de takes por cena | `/plano-gravacao` |
| `/checklist` | Checklist de pre-gravacao | `/checklist` |

### Edicao e Publicacao

| Comando | Descricao | Uso |
|---------|-----------|-----|
| `/editar [cliente]` | Edita video bruto no Remotion | `/editar`, `/editar Acme Corp` |
| `/render [projeto]` | Renderiza video final | `/render` |
| `/legendas [video]` | Gera ou aplica legendas | `/legendas` |
| `/template` | Lista e aplica templates de edicao | `/template` |
| `/publicar [video] [plataforma]` | Publica video no TikTok ou Instagram | `/publicar video.mp4 tiktok` |
| `/agendar [video] [data] [plataforma]` | Agenda publicacao futura | `/agendar video.mp4 2026-04-10 tiktok` |
| `/setup-api` | Configura APIs de publicacao | `/setup-api` |

### Analise e Memoria

| Comando | Descricao | Uso |
|---------|-----------|-----|
| `/metricas [cliente]` | Coleta metricas recentes | `/metricas`, `/metricas Acme Corp` |
| `/relatorio [cliente] [periodo]` | Gera relatorio de performance | `/relatorio Acme Corp semana` |
| `/insights [cliente]` | Analisa padroes e gera insights | `/insights`, `/insights Acme Corp` |
| `/lembrar [cliente]` | Carrega contexto completo do cliente | `/lembrar`, `/lembrar Acme Corp` |
| `/historico [cliente]` | Lista historico de publicacoes | `/historico`, `/historico Acme Corp` |
| `/stories [cliente]` | Lista aprendizados salvos | `/stories`, `/stories Acme Corp` |
| `/contexto [cliente]` | Mostra resumo do contexto | `/contexto`, `/contexto Acme Corp` |

### Organizacao de Arquivos

| Comando | Descricao | Uso |
|---------|-----------|-----|
| `/organizar [cliente]` | Organiza arquivos de midia por fase | `/organizar`, `/organizar Acme Corp` |
| `/listar-midias [cliente]` | Lista todos os arquivos de midia | `/listar-midias`, `/listar-midias Acme Corp` |
| `/analisar-midia [arquivo]` | Analisa metadata de arquivo de midia | `/analisar-midia video.mp4` |

## Fluxo Recomendado

```
1. /cliente-setup Acme Corp         → Configura cliente
2. /create-linha-editorial Acme Corp → Define estrategia de conteudo
3. /create-editorial Acme Corp      → Gera calendario do mes
4. /nova-campanha Acme Corp         → Inicia pipeline
   ├── /ideias Acme Corp            → Pesquisa trends e gera ideias
   ├── /roteiro Acme Corp           → Cria roteiro
   ├── /gravar Acme Corp            → Plano de gravacao
   ├── /editar Acme Corp            → Edita no Remotion
   ├── /publicar Acme Corp          → Publica nas plataformas
   └── /metricas Acme Corp          → Analisa performance
5. /insights Acme Corp             → Gera insights para proximo ciclo
```

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
