# neuro-content-skills

Pipeline completo de criacao de conteudo para midias sociais — 13 skills para agentes de IA.

## Requisitos

### Sistema

| Dependencia | Versao Minima | Necessidade | Instalacao |
|---|---|---|---|
| Python | 3.10+ | Obrigatorio | [python.org](https://python.org) |
| Node.js | 18+ | Obrigatorio (Remotion) | [nodejs.org](https://nodejs.org) |
| FFmpeg | 6.0+ | Obrigatorio | `brew install ffmpeg` |
| ffprobe | (vem com FFmpeg) | Obrigatorio | (vem com FFmpeg) |
| jq | 1.6+ | Obrigatorio | `brew install jq` |
| git | 2.x | Obrigatorio | (ja instalado) |
| sox | 14.x | Opcional (audio) | `brew install sox` |

### Pacotes Python

```bash
pip3 install requests pytrends python-dotenv openai-whisper "scenedetect[opencv]"
```

| Pacote | Para que | Skill |
|---|---|---|
| `requests` | Chamadas de API HTTP | Todas com API |
| `pytrends` | Google Trends (sem API key) | content-ideas |
| `python-dotenv` | Leitura de .env.cliente | Todos os scripts |
| `openai-whisper` | Legendas automaticas (local ou API) | content-editing |
| `scenedetect` | Deteccao de mudancas de cena | content-cuts |

### Pacotes Node.js

Remotion e instalado via npx (nao precisa de install global):

```bash
# Verificacao
npx --yes remotion --version
```

---

## Setup Rapido (1 comando)

```bash
# Clonar
git clone https://github.com/monrars1995/neuro-content-skills.git /tmp/neuro-content-skills

# Copiar skills para OpenCode
cp -r /tmp/neuro-content-skills/content-* ~/.opencode/skills/

# Rodar setup completo (instala deps + cria workspace + guia de APIs)
bash ~/.opencode/skills/content-workflow/scripts/setup_completo.sh
```

O script `setup_completo.sh` faz TUDO automaticamente:
1. Verifica e instala dependencias do sistema (jq, ffmpeg, etc.)
2. Instala pacotes Python
3. Verifica Node.js e Remotion
4. Cria workspace `~/conteudo/` com toda a estrutura
5. Gera `.gitignore` para proteger credenciais
6. Mostra guia completo de configuracao de cada API
7. Exibe resumo da instalacao

---

## APIs Suportadas

Cada API tem seu proprio tutorial de configuracao. Todas as credenciais ficam em `~/conteudo/campanhas/{cliente}/.env.cliente`.

### 1. TikTok Content Posting API

**Para:** `/publicar`, `/agendar`

| Passo | Acao |
|---|---|
| 1 | Acesse https://developers.tiktok.com |
| 2 | Crie conta de desenvolvedor |
| 3 | Crie um App no dashboard |
| 4 | Ative "Content Posting" nas APIs |
| 5 | Gere Access Token (scopes: `video.upload`, `video.publish`) |
| 6 | Copie `TIKTOK_ACCESS_TOKEN`, `TIKTOK_APP_ID`, `TIKTOK_USERNAME` |

### 2. TikTok Research API

**Para:** `/trends`, `/metricas`, `/concorrentes`

| Passo | Acao |
|---|---|
| 1 | No mesmo App do TikTok, ative "Research" API |
| 2 | Gere uma Research API Key |
| 3 | Copie `TIKTOK_RESEARCH_API_KEY`, `TIKTOK_BUSINESS_ID` |

### 3. Instagram / Meta Graph API

**Para:** `/publicar`, `/metricas`, `/concorrentes`

| Passo | Acao |
|---|---|
| 1 | Acesse https://developers.facebook.com |
| 2 | Crie um App (tipo Business) |
| 3 | Adicione "Instagram Basic Display API" |
| 4 | Vincule a Pagina do Facebook do cliente |
| 5 | Ative Content Publishing para a Pagina |
| 6 | Gere Long-lived Access Token |
| 7 | Obtenha Instagram Business Account ID |
| 8 | Copie `META_ACCESS_TOKEN`, `INSTAGRAM_BUSINESS_ACCOUNT_ID`, `FACEBOOK_PAGE_ID`, `META_AD_ACCOUNT_ID` |

### 4. OpenAI Whisper API

**Para:** `/legendas` (via API)

| Passo | Acao |
|---|---|
| 1 | Acesse https://platform.openai.com/api-keys |
| 2 | Crie uma API Key |
| 3 | Copie `OPENAI_API_KEY` |

**Alternativa local:** `pip3 install openai-whisper` (funciona offline, ~2GB de modelo)

### 5. ElevenLabs

**Para:** `/voz`, `/narracao`, `/musica`, `/efeitos`, `/mixar`, `/listar-vozes`

| Passo | Acao |
|---|---|
| 1 | Acesse https://elevenlabs.io |
| 2 | Crie conta (free: 10.000 chars/mes) |
| 3 | Acesse Settings > API Keys |
| 4 | Crie API Key |
| 5 | Copie `ELEVENLABS_API_KEY` |
| 6 | Escolha voz padrao (veja tabela abaixo) |

**Vozes recomendadas PT-BR:**

| Voz | ID | Estilo | Melhor para |
|---|---|---|---|
| Rachel | `21m00Tcm4TlvDq8ikWAM` | Natural, feminino | Geral |
| Adam | `pNInz6obpgDQGcFmaJgB` | Profissional, masculino | Educacao, negocios |
| Charlotte | `XB0fDUnXU5powFXDhCwa` | Energetico, feminino | Reels, trends |
| Callum | `bIHbv24MWmeRgasZH58o` | Jovem, masculino | Vlogs, humor |
| Antoni | `ErXwobaYiN019PkySvjV` | Apresentador, masculino | Podcasts |

**Modelos TTS:**

| Modelo | Qualidade | Velocidade | Uso |
|---|---|---|---|
| `eleven_multilingual_v2` | Melhor PT-BR | Normal | Recomendado |
| `eleven_turbo_v2_5` | Boa | Rapido | Longos textos |

### 6. Google Trends

**Para:** `/trends`, `/create-editorial`

**Nao precisa de API key!** Usa a biblioteca `pytrends` automaticamente.

Variaveis opcionais (ja configuradas por padrao):
- `GOOGLE_TRENDS_GEO=BR`
- `GOOGLE_TRENDS_LANG=pt`

---

## Instalacao por Ferramenta de IA

### OpenCode (nativo)

```bash
cp -r /tmp/neuro-content-skills/content-* ~/.opencode/skills/
# Digite: /iniciar-projeto
```

### Claude Code

```bash
cp -r /tmp/neuro-content-skills/claude/ ~/.claude/
# Ou adicione ao CLAUDE.md do projeto
# Digite: /iniciar-projeto
```

### Cursor

```bash
cp /tmp/neuro-content-skills/cursor/.cursorrules ~/conteudo/.cursorrules
# Abra ~/conteudo no Cursor e use o chat
```

### Gemini CLI

```bash
cp /tmp/neuro-content-skills/gemini/GEMINI.md ~/conteudo/GEMINI.md
# cd ~/conteudo e use: /iniciar-projeto
```

### Codex (OpenAI)

```bash
cp /tmp/neuro-content-skills/codex/AGENTS.md ~/conteudo/AGENTS.md
# cd ~/conteudo e use
```

### OpenClaw / Antigravity

```bash
mkdir -p ~/.openclaw/skills && cp -r /tmp/neuro-content-skills/content-* ~/.openclaw/skills/
# ou
mkdir -p ~/.antigravity/skills && cp -r /tmp/neuro-content-skills/content-* ~/.antigravity/skills/
```

---

## Comandos Disponiveis

| Comando | Funcao | Skill |
|---|---|---|
| `/iniciar-projeto` | Setup completo do workspace + primeiro cliente | content-workflow |
| `/cliente-setup [nome]` | Onboarding de cliente adicional | content-workflow |
| `/nova-campanha [cliente]` | Iniciar pipeline de conteudo | content-workflow |
| `/status` | Painel de status de todos os clientes | content-workflow |
| `/continuar [cliente]` | Retomar pipeline interrompido | content-workflow |
| `/create-linha-editorial` | Criar linha editorial | content-editorial |
| `/create-editorial` | Gerar calendario mensal | content-editorial |
| `/trends` | Pesquisar trends do nicho | content-ideas |
| `/ideias` | Gerar ideias de conteudo | content-ideas |
| `/concorrentes` | Analisar anuncios de concorrentes | content-ideas |
| `/roteiro` | Criar roteiro de video | content-script |
| `/hook` | Gerar hooks alternativos | content-script |
| `/gravar` | Planejar gravacao | content-recording |
| `/plano-gravacao` | Gerar plano de gravacao | content-recording |
| `/analisar` | Analisar video para cortes | content-cuts |
| `/cortar` | Gerar cortes virais | content-cuts |
| `/pontuar` | Pontuar potencial viral | content-cuts |
| `/repurpose` | Repurposing multi-plataforma | content-cuts |
| `/editar` | Editar video com Remotion | content-editing |
| `/legendas` | Gerar legendas automaticas | content-editing |
| `/render` | Renderizar video final | content-editing |
| `/dopamina` | Video dopaminergico completo | content-remotion |
| `/legendas-dinamicas` | Legendas word-by-word (Hormozi) | content-remotion |
| `/zoom` | Zoom animations em palavras-chave | content-remotion |
| `/overlay` | B-roll e overlays | content-remotion |
| `/render-remotion` | Renderizar composicao Remotion | content-remotion |
| `/voz` | Gerar voz AI (TTS) | content-audio |
| `/narracao` | Narracao completa sincronizada | content-audio |
| `/musica` | Musica de fundo por objetivo | content-audio |
| `/efeitos` | Efeitos sonoros | content-audio |
| `/mixar` | Mixagem completa de audio | content-audio |
| `/listar-vozes` | Listar vozes ElevenLabs | content-audio |
| `/publicar` | Publicar nas plataformas | content-publishing |
| `/agendar` | Agendar publicacao | content-publishing |
| `/metricas` | Analisar metricas | content-metrics |
| `/relatorio` | Gerar relatorio de performance | content-metrics |
| `/insights` | Insights de performance | content-metrics |
| `/contexto` | Consultar memoria do cliente | content-memory |
| `/historico` | Ver historico de publicacoes | content-memory |
| `/organizar` | Organizar arquivos de midia | content-fs |

---

## Estrutura do Workspace

```
~/conteudo/
├── campanhas/
│   └── {cliente}/
│       ├── contexto.json          # Memoria ativa do cliente
│       ├── historico.json         # Log de publicacoes
│       ├── .env.cliente          # Credenciais (NUNCA commitar!)
│       ├── posts-midias-sociais/
│       │   ├── ideias/
│       │   ├── roteiros/
│       │   ├── brutos/
│       │   ├── editados/
│       │   └── publicados/
│       ├── criativos-anuncios/
│       │   ├── ideias/
│       │   ├── roteiros/
│       │   ├── brutos/
│       │   ├── editados/
│       │   └── publicados/
│       ├── briefings/
│       └── metricas/
├── referencias/
│   ├── trends/
│   └── templates/
└── assets/
    ├── musicas/
    ├── fontes/
    └── overlays/
```

---

## Scripts Disponiveis

| Script | Skill | Funcao |
|---|---|---|
| `setup_completo.sh` | content-workflow | Setup completo (deps + workspace + APIs) |
| `validate_schema.py` | content-memory | Valida JSONs do cliente |
| `fetch_trends.py` | content-ideas | Busca trends (TikTok + Google + Meta) |
| `generate_subtitles.py` | content-editing | Legendas (Whisper local ou OpenAI API) |
| `setup_remotion.sh` | content-editing | Setup automatizado do projeto Remotion |
| `publish_video.py` | content-publishing | Publica no TikTok e Instagram |
| `fetch_metrics.py` | content-metrics | Coleta metricas das plataformas |
| `analyze_video.py` | content-cuts | Analise completa de video |
| `smart_cut.py` | content-cuts | Geracao de cortes automaticos |
| `score_video.py` | content-cuts | Pontuacao viral (rubrica 0-100) |
| `generate_dopamine_comp.py` | content-remotion | Composicao dopaminergica |
| `generate_subtitle_comp.py` | content-remotion | Legendas word-by-word |
| `generate_zoom_comp.py` | content-remotion | Zoom animations |
| `elevenlabs_tts.py` | content-audio | TTS + listar vozes |
| `generate_background_music.py` | content-audio | Musica de fundo por objetivo |
| `mix_audio.py` | content-audio | Mixagem completa (LUFS) |

---

## Exemplos e Templates

Consulte a pasta `examples/` no repositorio:

- **Workflows**: `podcast-para-shorts.md`, `tutorial-para-reels.md`, `vlog-para-tiktok.md`
- **Templates**: `hooks_library.md`, `cta_templates.md`, `briefing_template.md`, `roteiro_template.md`
- **Samples**: `analise_sample.json`, `pontuacao_sample.json`, `cortes_report_sample.json`

---

## Suporte

- **Issues**: https://github.com/monrars1995/neuro-content-skills/issues
- **Autor**: monrars1995
- **Licenca**: MIT
