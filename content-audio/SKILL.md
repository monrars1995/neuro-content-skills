---
name: content-audio
description: "Audio e musica com ElevenLabs. Gera voz AI (TTS), narrações, musica de fundo baseada no objetivo do video, efeitos sonoros e mixagem completa. Integra com API do ElevenLabs ou MCP. Use quando: gerar voz AI, criar narracao, musica de fundo, efeitos sonoros, mixar audio, voiceover, elevenlabs, TTS, som para video. Comandos: /voz, /narracao, /musica, /efeitos, /mixar, /setup-audio."
---

# Content Audio

## Stack Tecnica

- **ElevenLabs API** — TTS e geracao de voz AI
- **ElevenLabs MCP** — integracao nativa com agentes (opcional)
- **FFmpeg** — processamento e mixagem de audio
- **Python 3.10+** — scripts de automacao
- **Sox** — processamento avancado de audio (opcional)

---

## Onboarding Interativo

Ao iniciar uma sessao de audio, pergunte:

1. **Credenciais** — ElevenLabs API key configurada? Verificar `.env.cliente`
2. **Tipo de audio** — Voz AI (TTS), musica de fundo, efeitos sonoros, ou mixagem completa?
3. **Video associado** — Qual video? (para sincronizar audio)
4. **Objetivo** — Qual o tom do video? (educativo, motivacional, humor, dramatico, relaxante)
5. **Idioma** — PT-BR, EN, ES?
6. **Voz** — Qual voz usar? (listar disponiveis com `/listar-vozes`)

---

## Setup de Credenciais

Adicione ao `.env.cliente` do cliente:

```bash
ELEVENLABS_API_KEY=sk_seu_key_aqui
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel (default)
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
ELEVENLABS_OUTPUT_FORMAT=mp3_44100_128
```

### Instalar MCP do ElevenLabs (opcional)

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "elevenlabs": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-elevenlabs"]
    }
  }
}
```

---

## Slash Commands

### `/voz [cliente] [texto]` - Gerar Voz AI

Gera audio de voz AI a partir de texto usando ElevenLabs.

1. Ler texto do roteiro (de `roteiros/`) ou receber via argumento
2. Selecionar voz (default do `.env.cliente` ou especifica)
3. Chamar ElevenLabs TTS API
4. Salvar audio em `brutos/audio_voz.mp3`

```bash
python3 scripts/elevenlabs_tts.py --texto "Bem-vindo ao canal" --cliente joao --voz 21m00Tcm4TlvDq8ikWAM
python3 scripts/elevenlabs_tts.py --arquivo roteiros/roteiro_01.txt --cliente joao
python3 scripts/elevenlabs_tts.py --arquivo roteiros/roteiro_01.txt --cliente joai --voz pNInz6obpgDQGcFmaJgB --modelo eleven_turbo_v2_5
```

### `/narracao [cliente] [video]` - Gerar Narracao Completa

Gera narracao completa sincronizada com o video.

1. Extrair transcricao do video (usar content-editing `/legendas`)
2. Identificar trechos sem fala ou com fala ruim
3. Gerar voz AI para trechos selecionados
4. Sincronizar timestamps
5. Salvar como trilha de narracao

```bash
python3 scripts/elevenlabs_tts.py --arquivo roteiros/roteiro_01.txt --cliente joao --timestamps --saida brutos/narracao.mp3
```

### `/musica [cliente] [objetivo]` - Gerar Musica de Fundo

Gera musica de fundo adequada ao objetivo do video.

1. Determinar mood baseado no objetivo:
   - **Motivacional**: upbeats, energetico, BPM 120-140
   - **Educacional**: calmo, clean, BPM 80-100
   - **Humor**: divertido, leve, BPM 110-130
   - **Dramatico**: intenso, build-up, BPM 90-120
   - **Relaxante**: soft, ambient, BPM 60-80
2. Usar ElevenLabs Sound Effects API ou gerar com prompts
3. Ajustar duracao para o video
4. Normalizar volume (-18 LUFS para fundo)

```bash
python3 scripts/generate_background_music.py --cliente joao --objetivo motivacional --duracao 60 --saida brutos/musica_fundo.mp3
```

### `/efeitos [cliente]` - Efeitos Sonoros

Gera efeitos sonoros para o video.

```bash
python3 scripts/generate_effects.py --cliente joao --efeitos "whoosh,impact,rise" --saida brutos/efeitos/
```

### `/mixar [cliente] [video]` - Mixagem Completa

Mixa todas as trilhas de audio em um video final.

1. Carregar video original
2. Adicionar voz AI (se gerada)
3. Adicionar musica de fundo
4. Adicionar efeitos sonoros
5. Balancear volumes (voz -14 LUFS, fundo -24 LUFS)
6. Exportar video final com audio mixado

```bash
python3 scripts/mix_audio.py --video editados/corte_01.mp4 --cliente joao --voz brutos/narracao.mp3 --musica brutos/musica_fundo.mp3 --saida editados/corte_01_final.mp4
```

### `/listar-vozes [idioma]` - Listar Vozes Disponiveis

Lista todas as vozes disponiveis na conta ElevenLabs.

```bash
python3 scripts/elevenlabs_tts.py --listar-vozes --idioma pt
```

---

## Vozes Recomendadas (PT-BR)

| Voz | ID | Estilo | Uso |
|---|---|---|---|
| Rachel | `21m00Tcm4TlvDq8ikWAM` | Natural, feminino | Geral |
| Adam | `pNInz6obpgDQGcFmaJgB` | Profissional, masculino | Educacao, negocios |
| Charlotte | `XB0fDUnXU5powFXDhCwa` | Energetico, feminino | Reels, trends |
| Callum | `bIHbv24MWmeRgasZH58o` | Jovem, masculino | Vlogs, humor |
| Antoni | `ErXwobaYiN019PkySvjV` | Apresentador, masculino | Podcasts |

---

## Niveis de Volume (LUFS)

| Trilha | LUFS Target | Uso |
|---|---|---|
| Voz principal | -14 a -12 | Fala clara, destaque |
| Musica de fundo | -24 a -20 | Subtil, nao compete com voz |
| Efeitos sonoros | -16 a -12 | Destaque em momentos chave |
| Voz + Musica mix | -14 total | Balance ideal |

---

## Scripts

- `scripts/elevenlabs_tts.py` — TTS com ElevenLabs (texto, arquivo, listar vozes)
- `scripts/generate_background_music.py` — geracao de musica de fundo por objetivo
- `scripts/mix_audio.py` — mixagem completa (voz + musica + efeitos + video)

---

## Referencias

- `references/elevenlabs_guide.md` — guia completo da API ElevenLabs
- `references/audio_mixing.md` — tecnicas de mixagem para short-form
- **Edicao Remotion**: content-remotion (`/dopamina`, `/legendas-dinamicas`)
- **Cortes**: content-cuts (`/analisar`, `/cortar`)
- **Legendas**: content-editing (`/legendas`)
