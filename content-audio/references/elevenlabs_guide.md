# Guia da API ElevenLabs

Referencia completa para usar a API do ElevenLabs em projetos de conteudo.

---

## Setup

### 1. Obter API Key
1. Criar conta em https://elevenlabs.io
2. Acessar Settings → API Keys
3. Copiar a key e adicionar ao `.env.cliente`:
   ```bash
   ELEVENLABS_API_KEY=sk_seu_key_aqui
   ```

### 2. Verificar Instalacao
```bash
pip3 install requests python-dotenv
```

---

## Modelos Disponiveis

| Modelo | ID | Descricao |
|---|---|---|
| Multilingual v2 | `eleven_multilingual_v2` | 29 idiomas, melhor qualidade |
| Turbo v2.5 | `eleven_turbo_v2_5` | Mais rapido, custo menor |
| Turbo v2 | `eleven_turbo_v2` | Rapido, boa qualidade |
| English v1 | `eleven_monolingual_v1` | Apenas ingles, alta qualidade |

**Recomendacao:** `eleven_multilingual_v2` para PT-BR, `eleven_turbo_v2_5` para geracao rapida.

---

## Endpoints Principais

### Text-to-Speech
```
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
```

Headers:
```
xi-api-key: {ELEVENLABS_API_KEY}
Content-Type: application/json
Accept: audio/mpeg
```

Body:
```json
{
  "text": "Texto a ser convertido em fala",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": true
  }
}
```

### Listar Vozes
```
GET https://api.elevenlabs.io/v1/voices
```

Headers:
```
xi-api-key: {ELEVENLABS_API_KEY}
```

### Stream Text-to-Speech (longo)
```
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream
```
Ideal para textos longos (>2500 caracteres). Retorna chunks de audio.

### Sound Effects
```
POST https://api.elevenlabs.io/v1/sound-generation
```
Body:
```json
{
  "text": "whoosh sound effect for video transition",
  "duration_seconds": 2.0,
  "prompt_influence": 0.3
}
```

---

## Voice Settings

### Estabilidade (stability)
- `0.0` — Mais variacao/expressiva (risco de inconsistencia)
- `0.5` — Balance (recomendado)
- `1.0` — Mais consistente (menos expressivo)

### Similaridade (similarity_boost)
- `0.0` — Menos similar ao original da voz
- `0.75` — Balance (recomendado)
- `1.0` — Maxima similaridade

### Estilo (style)
- `0.0` — Sem estilo extra (recomendado)
- `1.0` — Maximo estilo (pode distorcer)

### Exemplos por Cenario

```json
// Narracao profissional
{ "stability": 0.6, "similarity_boost": 0.8, "style": 0.0 }

// Reels/TikTok (energetico)
{ "stability": 0.3, "similarity_boost": 0.7, "style": 0.2 }

// Podcast (conversa natural)
{ "stability": 0.4, "similarity_boost": 0.75, "style": 0.1 }

// Dramatico (narracao intensa)
{ "stability": 0.2, "similarity_boost": 0.8, "style": 0.3 }
```

---

## Custo Estimado

| Modelo | Custo por 1000 chars | ~1 min de audio |
|---|---|---|
| Multilingual v2 | $0.30 | ~$0.18 |
| Turbo v2.5 | $0.15 | ~$0.09 |
| Turbo v2 | $0.18 | ~$0.11 |
| Sound Effects | $0.10/efeito | - |

**Plano free:** 10.000 caracteres/mes

---

## Limites da API

- **Texto maximo por request:** 5.000 caracteres (streaming)
- **Rate limit:** ~100 requests/minuto (free tier)
- **Audio maximo:** ~5 minutos por request
- **Formatos:** mp3, ogg, pcm, ulaw

---

## Integracao com FFmpeg

### Adicionar voz ao video
```bash
ffmpeg -i video.mp4 -i voz.mp3 \
  -c:v copy -c:a aac -b:a 128k \
  -shortest video_com_voz.mp4
```

### Ajustar volume da voz
```bash
ffmpeg -i voz.mp3 -af "loudnorm=I=-14:TP=-1:LRA=11" voz_normalizada.mp3
```

### Mixar voz + musica
```bash
ffmpeg -i voz.mp3 -i musica.mp3 \
  -filter_complex "[0:a]volume=1.0[voz];[1:a]volume=0.3[musica];[voz][musica]amix=inputs=2:duration=first" \
  mix.mp3
```
