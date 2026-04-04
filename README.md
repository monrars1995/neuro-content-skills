# Neuro Content Skills

Pipeline completo de criacao de conteudo para midias sociais — 13 skills para Claude Code, OpenCode, Cursor, Gemini CLI e mais.

Automatiza todo o fluxo: desde a captacao de ideias com trends ate a publicacao e analise de metricas, passando por roteirizacao, gravacao, edicao dopaminergica, cortes virais e audio AI.

## Pipeline

```
  1. IDEIAS          2. ROTEIRO         3. GRAVACAO        4. EDICAO
  (content-ideas) → (content-script) → (content-recording) → (content-editing)
      │                                                        │
      │                                            ┌───────────┴───────────┐
      │                                     5b. CORTES            5c. REMOTION
      │                                   (content-cuts)        (content-remotion)
      │                                            │                   │
      │                                      5d. AUDIO              │
      │                                    (content-audio)         │
      │                                            │                   │
      └────────────────────────────────────────────┘                   │
                                                                       │
  7. METRICAS       6. PUBLICACAO                                    │
  (content-metrics) ← (content-publishing) ←─────────────────────────┘

  PLANEJAMENTO
  /cliente-setup → /create-linha-editorial → /create-editorial → /nova-campanha
```

## As 13 Skills

| # | Skill | Funcao | Comandos Principais |
|---|-------|--------|-------------------|
| 1 | `content-workflow` | Orquestrador principal | `/setup`, `/pipeline`, `/status`, `/continuar` |
| 2 | `content-editorial` | Calendario e pilar de conteudo | `/calendario`, `/pilar`, `/tom` |
| 3 | `content-ideas` | Trends e brainstorming | `/trends`, `/brainstorm`, `/hashtags` |
| 4 | `content-script` | Roteiros Hook(3s) > Desenvolvimento > CTA | `/roteiro`, `/hook`, `/cta` |
| 5 | `content-recording` | Checklist de gravacao | `/checklist`, `/gravar`, `/equipamento` |
| 6 | `content-editing` | Edicao + legendas Whisper | `/editar`, `/legendas`, `/exportar` |
| 7 | `content-cuts` | Cortes virais para short-form | `/analisar`, `/cortar`, `/pontuar`, `/repurpose` |
| 8 | `content-remotion` | Edicao dopaminergica Remotion | `/dopamina`, `/legendas-dinamicas`, `/zoom`, `/render-remotion` |
| 9 | `content-audio` | TTS ElevenLabs + mixagem | `/voz`, `/narracao`, `/musica`, `/efeitos`, `/mixar`, `/listar-vozes` |
| 10 | `content-publishing` | Publicacao multi-plataforma | `/publicar`, `/agendar`, `/formatar` |
| 11 | `content-metrics` | Metricas e analise | `/metricas`, `/relatorio`, `/comparar` |
| 12 | `content-memory` | Memoria persistente por cliente | `/contexto`, `/historico`, `/salvar` |
| 13 | `content-fs` | Gestao de arquivos e pastas | `/pastas`, `/mover`, `/organizar` |

## Instalacao Rapida

```bash
git clone https://github.com/monrars1995/neuro-content-skills.git
cd neuro-content-skills
chmod +x setup_completo.sh
./setup_completo.sh
```

O `setup_completo.sh` configura:
- Estrutura de pastas (`~/conteudo/campanhas/`)
- Credenciais de API (interativo, 6 APIs)
- Claude Code / OpenCode / Cursor / Gemini CLI / Codex
- CLI unificado `neuro`
- MCP Server para Claude Desktop

Veja `INSTALL.md` para instrucoes detalhadas de cada ferramenta.

## Estrutura de Pastas

```
~/conteudo/
  campanhas/
    {cliente}/
      posts-midias-sociais/
        ideias/ roteiros/ brutos/ editados/ publicados/
      criativos-anuncios/
        ideias/ roteiros/ brutos/ editados/ publicados/
      briefings/
      metricas/
      contexto.json      # Memoria persistente
      historico.json     # Historico de publicacoes
      .env.cliente       # Credenciais (nunca committado)
  referencias/
    trends/              # Dados de pesquisa
    templates/           # Templates de script
  assets/
    musicas/             # Audio royalty-free
    fontes/              # Fontes customizadas
    overlays/            # Textos, lower thirds
```

## APIs Utilizadas

| API | Uso | Variaveis |
|-----|-----|-----------|
| OpenAI Whisper | Transcricao para legendas | `OPENAI_API_KEY` |
| ElevenLabs | TTS / voz AI | `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` |
| TikTok Research API | Trends e hashtags | `TIKTOK_RESEARCH_API_KEY` |
| TikTok Content Posting | Publicacao | `TIKTOK_ACCESS_TOKEN`, `TIKTOK_APP_ID` |
| Meta Graph API | Instagram + Ads Library | `META_ACCESS_TOKEN`, `INSTAGRAM_BUSINESS_ACCOUNT_ID` |
| Google Trends (pytrends) | Trends de nicho | `GOOGLE_TRENDS_GEO`, `GOOGLE_TRENDS_LANG` |

## CLI Unificado (`neuro`)

```bash
neuro setup                 # Configura workspace
neuro status                # Painel de clientes
neuro novo-cliente NOME     # Cria cliente
neuro config CLIENTE        # Edita .env.cliente
neuro pipeline CLIENTE      # Roda pipeline completa
neuro cortes VIDEO          # Cortes virais
neuro audio TEXTO           # Gera voz AI
neuro memoria CLIENTE       # Consulta contexto
```

## MCP Server

Expoe 12 ferramentas para Claude Desktop e outros clientes MCP:

```json
{
  "mcpServers": {
    "neuro-content": {
      "command": "python3",
      "args": ["/caminho/para/neuro-content-skills/mcp_server.py"]
    }
  }
}
```

Ferramentas disponiveis: `neuro_status`, `neuro_criar_cliente`, `neuro_contexto`, `neuro_historico`, `neuro_listar_midias`, `neuro_analisar_video`, `neuro_gerar_cortes`, `neuro_pontuar_video`, `neuro_legendas`, `neuro_voz`, `neuro_musicas`, `neuro_trends`.

## Fluxo Recomendado

```
1. /cliente-setup Acme Corp         → Configura cliente
2. /create-linha-editorial Acme Corp → Define estrategia de conteudo
3. /create-editorial Acme Corp      → Gera calendario do mes
4. /nova-campanha Acme Corp         → Inicia pipeline
   ├── /trends Acme Corp            → Pesquisa trends e gera ideias
   ├── /roteiro Acme Corp           → Cria roteiro
   ├── /gravar Acme Corp            → Plano de gravacao
   ├── /editar Acme Corp            → Edita no Remotion
   ├── /cortar Acme Corp            → Cortes virais para shorts/reels
   ├── /voz Acme Corp               → Narracao AI
   ├── /publicar Acme Corp          → Publica nas plataformas
   └── /metricas Acme Corp          → Analisa performance
5. /insights Acme Corp             → Gera insights para proximo ciclo
```

## Stack Tecnica

| Camada | Tecnologia |
|--------|-----------|
| Edicao de video | Remotion + Next.js + TypeScript |
| Scripts | Python 3.9+ (pytrends, requests, python-dotenv) |
| Audio | ElevenLabs TTS + FFmpeg |
| APIs | TikTok, Instagram Graph API v21, Meta Ads Library |
| Publicacao | TikTok Upload API, Instagram Reels via Graph API |
| Metricas | TikTok Research API, Instagram Insights via Graph API |

## Testes

```bash
python3 test_integration.py
# Resultado esperado: 11/11 passaram
```

## Compatibilidade

| Ferramenta | Instalacao |
|-----------|-----------|
| Claude Code | `claude/commands/` |
| OpenCode | Copiar skills para `~/.opencode/skills/` |
| Cursor | `cursor/.cursorrules` |
| Gemini CLI | `gemini/GEMINI.md` |
| Codex | `codex/AGENTS.md` |
| Claude Desktop | MCP Server (`mcp_server.py`) |

## Licenca

MIT — Copyright (c) 2026 [monrars1995](https://github.com/monrars1995)

Instagram: [@monrars](https://instagram.com/monrars)
