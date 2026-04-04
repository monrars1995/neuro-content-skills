#!/usr/bin/env bash
set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${CYAN}${BOLD}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}${BOLD}[OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}${BOLD}[AVISO]${NC} $1"; }
erro()  { echo -e "${RED}${BOLD}[ERRO]${NC} $1"; }

CONTEUDO_DIR="$HOME/conteudo"

cat << "BANNER"

  ╔══════════════════════════════════════════════════════╗
  ║     NEURO CONTENT SKILLS - SETUP COMPLETO           ║
  ║     Pipeline de Conteudo para Midias Sociais        ║
  ╚══════════════════════════════════════════════════════╝

BANNER

echo ""
echo "Este script vai:"
echo "  1. Verificar e instalar TODAS as dependencias do sistema"
echo "  2. Instalar pacotes Python necessarios"
echo "  3. Instalar pacotes Node.js necessarios"
echo "  4. Criar o workspace ~/conteudo com toda a estrutura"
echo "  5. Gerar template .env.cliente com todas as APIs"
echo "  6. Rodar testes de conexao com as APIs configuradas"
echo ""
read -rp "Pressione ENTER para comecar (Ctrl+C para cancelar)... " _

echo ""
echo "=========================================="
echo -e "${BOLD}ETAPA 1/6: DEPENDENCIAS DO SISTEMA${NC}"
echo "=========================================="
echo ""

OS="$(uname -s)"
PKG_MANAGER=""

if command -v brew &>/dev/null; then
    PKG_MANAGER="brew"
elif command -v apt-get &>/dev/null; then
    PKG_MANAGER="apt-get"
elif command -v dnf &>/dev/null; then
    PKG_MANAGER="dnf"
else
    warn "Gerenciador de pacotes nao detectado. Instale manualmente."
fi

install_pkg() {
    local pkg="$1"
    if command -v "$pkg" &>/dev/null; then
        ok "$pkg ja instalado"
    else
        info "Instalando $pkg..."
        if [ "$PKG_MANAGER" = "brew" ]; then
            brew install "$pkg"
        elif [ "$PKG_MANAGER" = "apt-get" ]; then
            sudo apt-get install -y "$pkg"
        elif [ "$PKG_MANAGER" = "dnf" ]; then
            sudo dnf install -y "$pkg"
        else
            erro "Instale $pkg manualmente"
            return 1
        fi
        ok "$pkg instalado"
    fi
}

install_pkg "jq"
install_pkg "ffmpeg"
install_pkg "ffprobe"
install_pkg "git"

if command -v sox &>/dev/null; then
    ok "sox ja instalado (opcional - processamento avancado de audio)"
else
    warn "sox nao instalado (opcional - use: brew install sox)"
fi

echo ""
echo "Verificando Python..."
if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
    PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 10 ]; then
        ok "Python $PY_VERSION (compativel)"
    else
        warn "Python $PY_VERSION detectado. Recomendado: 3.10+"
    fi
else
    erro "Python 3.10+ nao encontrado. Instale em python.org"
    exit 1
fi

echo ""
echo "Verificando Node.js..."
if command -v node &>/dev/null; then
    NODE_VERSION=$(node --version 2>&1 | sed 's/v//' | cut -d. -f1)
    if [ "$NODE_VERSION" -ge 18 ]; then
        ok "Node.js $(node --version) (compativel)"
    else
        warn "Node.js $(node --version) detectado. Recomendado: 18+"
    fi
else
    warn "Node.js 18+ nao encontrado (necessario para Remotion)"
    info "Instale em https://nodejs.org (versao LTS 18+)"
fi

if command -v npx &>/dev/null; then
    ok "npx disponivel"
else
    warn "npx nao encontrado (necessario para Remotion)"
fi

echo ""
echo "=========================================="
echo -e "${BOLD}ETAPA 2/6: PACOTES PYTHON${NC}"
echo "=========================================="
echo ""

PIP_PACKAGES=(
    "requests"
    "pytrends"
    "python-dotenv"
    "openai-whisper"
    "scenedetect[opencv]"
)

for pkg in "${PIP_PACKAGES[@]}"; do
    PKG_NAME=$(echo "$pkg" | cut -d'[' -f1)
    if python3 -c "import ${PKG_NAME//-/_}" 2>/dev/null; then
        ok "$PKG_NAME ja instalado"
    else
        info "Instalando $pkg..."
        if pip3 install "$pkg" --quiet 2>/dev/null; then
            ok "$PKG_NAME instalado"
        else
            warn "Falha ao instalar $pkg. Execute manualmente: pip3 install $pkg"
        fi
    fi
done

echo ""
echo "=========================================="
echo -e "${BOLD}ETAPA 3/6: PACOTES NODE.JS${NC}"
echo "=========================================="
echo ""

if command -v node &>/dev/null; then
    info "Verificando Remotion..."
    if npx --yes remotion --version &>/dev/null 2>&1; then
        ok "Remotion disponivel via npx"
    else
        warn "Nao foi possivel verificar Remotion. Sera instalado no primeiro uso."
    fi
else
    warn "Node.js nao instalado - pulando pacotes Node.js"
    warn "Instale Node.js 18+ para usar Remotion (edicao de video)"
fi

echo ""
echo "=========================================="
echo -e "${BOLD}ETAPA 4/6: WORKSPACE${NC}"
echo "=========================================="
echo ""

if [ -d "$CONTEUDO_DIR" ]; then
    ok "Workspace ~/conteudo ja existe"
else
    info "Criando workspace ~/conteudo..."
    mkdir -p "$CONTEUDO_DIR"/{campanhas,referencias/{trends,templates},assets/{musicas,fontes,overlays}}
    ok "Workspace criado"
fi

mkdir -p "$CONTEUDO_DIR"/referencias/{trends,templates}
mkdir -p "$CONTEUDO_DIR"/assets/{musicas,fontes,overlays}

if [ ! -f "$CONTEUDO_DIR/.gitignore" ]; then
    cat > "$CONTEUDO_DIR/.gitignore" << 'GITIGNORE'
.env.cliente
*.mp4
*.mov
*.mp3
*.wav
*.aac
__pycache__/
node_modules/
.DS_Store
GITIGNORE
    ok ".gitignore criado"
else
    if ! grep -q ".env.cliente" "$CONTEUDO_DIR/.gitignore" 2>/dev/null; then
        echo ".env.cliente" >> "$CONTEUDO_DIR/.gitignore"
        ok ".gitignore atualizado"
    else
        ok ".gitignore ja configurado"
    fi
fi

echo ""
echo "=========================================="
echo -e "${BOLD}ETAPA 5/6: TEMPLATE .ENV.CLIENTE${NC}"
echo "=========================================="
echo ""

cat << 'ENVTEMPLATE'

  O arquivo .env.cliente contem TODAS as chaves de API.
  Ele fica em: ~/conteudo/campanhas/{cliente}/.env.cliente
  Cada cliente tem o proprio arquivo de credenciais.

  Abaixo esta o template COMPLETO com todas as APIs suportadas:

ENVTEMPLATE

echo ""
cat << 'ENVFILE'
# ============================================================
# NEURO CONTENT SKILLS - TEMPLATE DE CREDENCIAIS
# Copie para: ~/conteudo/campanhas/{cliente}/.env.cliente
# ============================================================
# Preencha APENAS as APIs que voce vai usar.
# Deixe as outras comentadas ou com valor vazio.
# ============================================================

# --- TIKTOK ---
# Content Posting API (publicacao de videos)
TIKTOK_ACCESS_TOKEN=
TIKTOK_APP_ID=
TIKTOK_USERNAME=
# Research API (tendencias e metricas)
TIKTOK_RESEARCH_API_KEY=
TIKTOK_BUSINESS_ID=

# --- INSTAGRAM / META ---
# Graph API (publicacao de Reels e metricas)
META_ACCESS_TOKEN=
INSTAGRAM_BUSINESS_ACCOUNT_ID=
FACEBOOK_PAGE_ID=
META_AD_ACCOUNT_ID=

# --- OPENAI / WHISPER ---
# API key para Whisper API (legendas automaticas)
# Alternativa: instale Whisper localmente (pip3 install openai-whisper)
OPENAI_API_KEY=

# --- ELEVENLABS ---
# TTS (voz AI), musica de fundo e efeitos sonoros
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
ELEVENLABS_OUTPUT_FORMAT=mp3_44100_128

# --- GOOGLE TRENDS ---
# Configuracao regional (nao precisa de API key)
GOOGLE_TRENDS_GEO=BR
GOOGLE_TRENDS_LANG=pt

# --- WHISPER LOCAL (opcional) ---
# Modelo Whisper para uso offline (mais pesado)
# WHISPER_MODEL=base
# WHISPER_DEVICE=cpu
ENVFILE

echo ""
info "O template acima sera copiado para cada cliente criado."
echo ""

echo "=========================================="
echo -e "${BOLD}ETAPA 6/6: GUIA DE CONFIGURACAO DAS APIs${NC}"
echo "=========================================="
echo ""

cat << 'APIS'

  ╔══════════════════════════════════════════════════════════╗
  ║  GUIA PASSO A PASSO DE CADA API                        ║
  ╚══════════════════════════════════════════════════════════╝

  ┌─────────────────────────────────────────────────────────┐
  │ 1. TIKTOK - Content Posting API                        │
  │    (publicacao de videos)                               │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  a) Acesse: https://developers.tiktok.com               │
  │  b) Crie uma conta de desenvolvedor                     │
  │  c) Crie um novo App no dashboard                      │
  │  d) Ative "Content Posting" nas APIs do App             │
  │  e) Gere um Access Token com scopes:                    │
  │     - video.upload                                      │
  │     - video.publish                                     │
  │  f) Copie: TIKTOK_ACCESS_TOKEN                          │
  │  g) Copie: TIKTOK_APP_ID                                │
  │  h) Copie: TIKTOK_USERNAME (seu @ no TikTok)           │
  │                                                         │
  │  Teste: python3 scripts/publish_video.py --test         │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ 2. TIKTOK - Research API                               │
  │    (tendencias, hashtags, metricas de perfil)           │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  a) Acesse: https://developers.tiktok.com               │
  │  b) No App criado acima, ative "Research" API          │
  │  c) Gere uma Research API Key                           │
  │  d) Copie: TIKTOK_RESEARCH_API_KEY                      │
  │  e) Copie: TIKTOK_BUSINESS_ID                           │
  │                                                         │
  │  Teste: python3 content-ideas/scripts/fetch_trends.py   │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ 3. INSTAGRAM / META - Graph API                         │
  │    (publicacao de Reels e metricas)                     │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  a) Acesse: https://developers.facebook.com             │
  │  b) Crie um App (tipo Business)                         │
  │  c) Adicione "Instagram Basic Display API"              │
  │  d) Vincule a Pagina do Facebook do cliente             │
  │  e) Ative "Content Publishing" para a Pagina            │
  │  f) Gere um Long-lived Access Token                     │
  │  g) Obtenha o Instagram Business Account ID             │
  │  h) Copie: META_ACCESS_TOKEN                            │
  │  i) Copie: INSTAGRAM_BUSINESS_ACCOUNT_ID                │
  │  j) Copie: FACEBOOK_PAGE_ID                             │
  │  k) Copie: META_AD_ACCOUNT_ID (para anuncios)          │
  │                                                         │
  │  Teste: python3 scripts/publish_video.py --test         │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ 4. OPENAI - Whisper API (opcional)                      │
  │    (legendas automaticas via API - alternativa local)   │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  a) Acesse: https://platform.openai.com/api-keys        │
  │  b) Crie uma API Key                                    │
  │  c) Copie: OPENAI_API_KEY                               │
  │                                                         │
  │  NOTA: Se nao quiser usar a API, instale Whisper local:  │
  │        pip3 install openai-whisper                      │
  │        (requer ~2GB de modelo, funciona offline)        │
  │                                                         │
  │  Teste: python3 content-editing/scripts/                │
  │         generate_subtitles.py --test                    │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ 5. ELEVENLABS - TTS, Musica e Efeitos                   │
  │    (voz AI, musica de fundo, efeitos sonoros)          │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  a) Acesse: https://elevenlabs.io                       │
  │  b) Crie uma conta (free: 10.000 caracteres/mes)       │
  │  c) Acesse: https://elevenlabs.io/app/settings/api-keys │
  │  d) Crie uma API Key                                    │
  │  e) Copie: ELEVENLABS_API_KEY                           │
  │  f) Escolha uma voz padrao (recomendadas PT-BR):        │
  │                                                         │
  │     Rachel    = 21m00Tcm4TlvDq8ikWAM  (natural, fem)   │
  │     Adam      = pNInz6obpgDQGcFmaJgB  (profissional)   │
  │     Charlotte = XB0fDUnXU5powFXDhCwa  (energetico)     │
  │     Callum    = bIHbv24MWmeRgasZH58o  (jovem)          │
  │     Antoni    = ErXwobaYiN019PkySvjV  (apresentador)   │
  │                                                         │
  │  g) Copie: ELEVENLABS_VOICE_ID (ID da voz escolhida)   │
  │                                                         │
  │  Modelos:                                               │
  │     eleven_multilingual_v2 = melhor qualidade PT-BR     │
  │     eleven_turbo_v2_5      = mais rapido, boa qualidade │
  │                                                         │
  │  Teste: python3 content-audio/scripts/elevenlabs_tts.py \
  │           --listar-vozes --idioma pt                    │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ 6. GOOGLE TRENDS (nao precisa de API key!)              │
  │    (pesquisa de tendencias)                             │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  Nao precisa de configuracao! Usa pytrends.             │
  │                                                         │
  │  Variaveis opcionais:                                   │
  │    GOOGLE_TRENDS_GEO=BR  (pais, padrao: BR)            │
  │    GOOGLE_TRENDS_LANG=pt (idioma, padrao: pt)           │
  │                                                         │
  │  Teste: python3 content-ideas/scripts/fetch_trends.py   │
  │         --nicho "fitness" --teste                       │
  └─────────────────────────────────────────────────────────┘

APIS

echo ""
echo "=========================================="
echo -e "${BOLD}RESUMO DA INSTALACAO${NC}"
echo "=========================================="
echo ""

check_mark() { [ "$1" = "0" ] && echo -e "  ${GREEN}[OK]${NC} $2" || echo -e "  ${RED}[X]${NC} $2"; }

check_mark "$(command -v jq &>/dev/null && echo 0 || echo 1)" "jq"
check_mark "$(command -v ffmpeg &>/dev/null && echo 0 || echo 1)" "ffmpeg"
check_mark "$(command -v ffprobe &>/dev/null && echo 0 || echo 1)" "ffprobe"
check_mark "$(command -v python3 &>/dev/null && echo 0 || echo 1)" "python3"
check_mark "$(python3 -c "import requests" 2>/dev/null && echo 0 || echo 1)" "python: requests"
check_mark "$(python3 -c "import pytrends" 2>/dev/null && echo 0 || echo 1)" "python: pytrends"
check_mark "$(python3 -c "import dotenv" 2>/dev/null && echo 0 || echo 1)" "python: python-dotenv"
check_mark "$(python3 -c "import whisper" 2>/dev/null && echo 0 || echo 1)" "python: openai-whisper"
check_mark "$(python3 -c "import scenedetect" 2>/dev/null && echo 0 || echo 1)" "python: scenedetect"
check_mark "$(command -v node &>/dev/null && echo 0 || echo 1)" "node.js"
check_mark "[ -d ~/conteudo ] && echo 0 || echo 1" "workspace ~/conteudo"

echo ""
echo -e "${BOLD}PROXIMOS PASSOS:${NC}"
echo ""
echo "  1. Configure as APIs que precisa (veja guia acima)"
echo "  2. Use o agente de IA e digite: /iniciar-projeto"
echo "  3. O agente vai criar o primeiro cliente com .env.cliente"
echo "  4. Cole as chaves de API quando solicitado"
echo "  5. Comece a criar conteudo!"
echo ""
echo -e "${GREEN}Setup concluido!${NC}"
echo ""
