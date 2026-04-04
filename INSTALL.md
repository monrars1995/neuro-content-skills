# neuro-content-skills - Guia de Instalacao

Pipeline completo de criacao de conteudo para midias sociais com 10 skills para agentes de IA.

## Requisitos

- Python 3.10+ com `requests`, `pytrends`, `python-dotenv`
- Node.js 18+ (para edicao com Remotion)
- FFmpeg (para processamento de video)
- jq (para validacao de JSON)
- Conta de desenvolvedor nas APIs desejadas (TikTok, Instagram/Meta)

## Instalacao das Dependencias

```bash
# Python
pip3 install requests pytrends python-dotenv

# Node.js (se for usar edicao Remotion)
# Instale em https://nodejs.org (versao 18+)

# FFmpeg
brew install ffmpeg          # macOS
# sudo apt install ffmpeg   # Ubuntu/Debian

# jq
brew install jq              # macOS
# sudo apt install jq       # Ubuntu/Debian

# Whisper (opcional, para legendas automaticas)
pip3 install openai-whisper  # ou use OpenAI API via OPENAI_API_KEY
```

---

## Instalacao por Ferramenta de IA

### 1. OpenCode

Skills nativas. Copie as pastas de skills para o diretorio do OpenCode:

```bash
# Clonar o repositorio
git clone https://github.com/monrars1995/neuro-content-skills.git /tmp/neuro-content-skills

# Copiar skills para o diretorio do OpenCode
cp -r /tmp/neuro-content-skills/content-* ~/.opencode/skills/

# Validar instalacao
ls ~/.opencode/skills/
# Deve listar: content-workflow, content-editorial, content-ideas, content-script,
# content-recording, content-editing, content-publishing, content-metrics,
# content-memory, content-fs
```

Pronto! O OpenCode carrega skills automaticamente desse diretorio.

**Uso:** Digite `/iniciar-projeto` para comecar.

---

### 2. Claude Code (Anthropic)

Claude Code usa o diretorio `.claude/commands/` para slash commands personalizados.

```bash
# Clonar o repositorio
git clone https://github.com/monrars1995/neuro-content-skills.git /tmp/neuro-content-skills

# Copiar instrucoes para o projeto
cp -r /tmp/neuro-content-skills/claude/ ~/.claude/
```

Alternativamente, adicione ao `CLAUDE.md` do seu projeto:

```bash
cat >> ~/conteudo/CLAUDE.md << 'EOF'

## Neuro Content Skills

Voce tem acesso a um pipeline completo de criacao de conteudo para midias sociais.

### Comandos disponiveis:
- `/iniciar-projeto` - Setup completo do workspace e primeiro cliente
- `/cliente-setup [nome]` - Onboarding de cliente adicional
- `/nova-campanha [cliente]` - Iniciar pipeline de conteudo
- `/status` - Painel de status de todos os clientes
- `/continuar [cliente]` - Retomar pipeline interrompido
- `/create-linha-editorial [cliente]` - Criar linha editorial
- `/create-editorial [cliente]` - Gerar calendario mensal
- `/trends [cliente]` - Pesquisar trends do nicho
- `/ideias [cliente]` - Gerar ideias de conteudo
- `/roteiro [cliente]` - Criar roteiro de video
- `/gravar [cliente]` - Planejar gravacao
- `/editar [cliente]` - Editar video com Remotion
- `/legendas [video] [cliente]` - Gerar legendas automaticas
- `/render [cliente]` - Renderizar video final
- `/publicar [cliente]` - Publicar nas plataformas
- `/metricas [cliente]` - Analisar metricas de performance
- `/relatorio [cliente]` - Gerar relatorio de performance
- `/lembrar [cliente]` - Consultar memoria do cliente
- `/historico [cliente]` - Ver historico de publicacoes

### Workspace:
- Raiz: ~/conteudo
- Clientes: ~/conteudo/campanhas/{cliente}/
- Referencias: ~/conteudo/referencias/
- Assets: ~/conteudo/assets/

### Comportamento:
- Toda comunicacao em PT-BR
- Um passo por vez, sempre confirme com o usuario
- Sempre valide JSON apos criar/editar
- Nunca publique sem aprovacao do usuario
EOF
```

**Uso:** Digite `/iniciar-projeto` ou qualquer slash command listado acima.

---

### 3. Cursor

Cursor usa o arquivo `.cursorrules` na raiz do projeto para instrucoes do agente.

```bash
# Clonar o repositorio
git clone https://github.com/monrars1995/neuro-content-skills.git /tmp/neuro-content-skills

# Copiar regras para o workspace
cp /tmp/neuro-content-skills/cursor/.cursorrules ~/conteudo/.cursorrules
```

Ou crie manualmente `~/conteudo/.cursorrules` com o conteudo do arquivo copiado.

**No Cursor:**
1. Abra o workspace `~/conteudo` no Cursor
2. O agente tera acesso a todas as instrucoes
3. Use o chat com comandos como: "Inicie um novo projeto com /iniciar-projeto"

---

### 4. Gemini CLI (Google)

Gemini CLI usa o arquivo `GEMINI.md` na raiz do projeto.

```bash
# Clonar o repositorio
git clone https://github.com/monrars1995/neuro-content-skills.git /tmp/neuro-content-skills

# Copiar instrucoes para o workspace
cp /tmp/neuro-content-skills/gemini/GEMINI.md ~/conteudo/GEMINI.md
```

**No Gemini CLI:**
1. Navegue ate o workspace: `cd ~/conteudo`
2. O Gemini carrega GEMINI.md automaticamente como contexto
3. Use: "Execute /iniciar-projeto para configurar o workspace"

---

### 5. OpenClaw

OpenClaw usa o diretorio `.openclaw/skills/` para skills personalizadas.

```bash
# Clonar o repositorio
git clone https://github.com/monrars1995/neuro-content-skills.git /tmp/neuro-content-skills

# Copiar skills para o diretorio do OpenClaw
mkdir -p ~/.openclaw/skills
cp -r /tmp/neuro-content-skills/content-* ~/.openclaw/skills/
```

**Uso:** Digite `/iniciar-projeto` para comecar.

---

### 6. Antigravity

Antigravity usa o diretorio `.antigravity/skills/` para skills personalizadas.

```bash
# Clonar o repositorio
git clone https://github.com/monrars1995/neuro-content-skills.git /tmp/neuro-content-skills

# Copiar skills para o diretorio do Antigravity
mkdir -p ~/.antigravity/skills
cp -r /tmp/neuro-content-skills/content-* ~/.antigravity/skills/
```

**Uso:** Digite `/iniciar-projeto` para comecar.

---

### 7. Codex (OpenAI)

Codex CLI usa o arquivo `AGENTS.md` na raiz do projeto.

```bash
# Clonar o repositorio
git clone https://github.com/monrars1995/neuro-content-skills.git /tmp/neuro-content-skills

# Copiar instrucoes para o workspace
cp /tmp/neuro-content-skills/codex/AGENTS.md ~/conteudo/AGENTS.md
```

**No Codex:**
1. Navegue ate o workspace: `cd ~/conteudo`
2. O Codex carrega AGENTS.md automaticamente
3. Use: "Execute o setup do projeto"

---

## Estrutura do Workspace

Apos `/iniciar-projeto`, a estrutura sera:

```
~/conteudo/
├── campanhas/
│   └── {cliente}/
│       ├── contexto.json          # Memoria ativa do cliente
│       ├── historico.json         # Log de publicacoes
│       ├── .env.cliente          # Credenciais de API (NUNCA commitar!)
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

## Scripts Disponiveis

| Script | Localizacao | Funcao |
|--------|-------------|--------|
| fetch_trends.py | content-ideas/scripts/ | Busca trends no TikTok, Google e Meta Ads |
| generate_subtitles.py | content-editing/scripts/ | Gera legendas com Whisper local ou OpenAI API |
| publish_video.py | content-publishing/scripts/ | Publica videos no TikTok e Instagram via API |
| fetch_metrics.py | content-metrics/scripts/ | Coleta metricas de performance das plataformas |
| validate_schema.py | content-memory/scripts/ | Valida schemas de contexto.json e historico.json |
| setup_remotion.sh | content-editing/scripts/ | Setup automatizado do projeto Remotion |

## Suporte

- **Issues**: https://github.com/monrars1995/neuro-content-skills/issues
- **Autor**: monrars1995
- **Instagram**: [@monrars](https://instagram.com/monrars)
- **Licenca**: MIT
