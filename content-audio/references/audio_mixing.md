# Tecnicas de Mixagem para Short-Form

Guia de mixagem de audio para videos Reels, Shorts e TikTok.

---

## Principios Fundamentais

### 1. Voz e Sempre Voz
A voz deve ser sempre o elemento mais alto. Tudo mais e suporte.

### 2. Menos e Mais
Audio limpo e simples e melhor que muitas camadas complexas.

### 3. Consistencia
Mantenha o mesmo nivel de volume ao longo do video.

---

## Niveis de Volume (LUFS)

LUFS (Loudness Units Full Scale) e o padrao de medicao de volume.

### Por Tipo de Conteudo

| Conteudo | LUFS Target | True Peak |
|---|---|---|
| Reels/TikTok | -14 a -12 LUFS | -1.0 dBTP |
| Shorts/YouTube | -14 LUFS | -1.0 dBTP |
| Podcast | -16 LUFS | -1.0 dBTP |
| Musica pura | -14 a -16 LUFS | -1.0 dBTP |

### Por Trilha

| Trilha | Volume Relativo | LUFS |
|---|---|---|
| Voz principal | 0 dB (referencia) | -14 LUFS |
| Musica de fundo | -12 a -18 dB abaixo | -24 a -30 LUFS |
| Efeitos sonoros | -6 a -12 dB abaixo | -18 a -24 LUFS |
| Voz + fundo mix | -14 LUFS total | -1.0 dBTP |

---

## Mixagem com FFmpeg

### Normalizar voz para -14 LUFS
```bash
ffmpeg -i voz_bruta.mp3 \
  -af "loudnorm=I=-14:TP=-1:LRA=11:print_format=json" \
  -y voz_normalizada.mp3
```

### Ajustar volume da musica para fundo
```bash
# Reduzir musica em 12dB (bom para fundo)
ffmpeg -i musica.mp3 -af "volume=-12dB" musica_fundo.mp3

# Reduzir musica em 18dB (fundo mais suave)
ffmpeg -i musica.mp3 -af "volume=-18dB" musica_fundo_suave.mp3
```

### Ducking automatico (baixar musica quando ha fala)
```bash
ffmpeg -i voz.mp3 -i musica.mp3 \
  -filter_complex \
  "[1:a]asplit=3[sub1][sub2][sub3]; \
   [sub1]volume=enable='between(t,0,3)':volume=0.8[aux1]; \
   [sub2]volume=enable='between(t,3,57)':volume=0.15[aux2]; \
   [sub3]volume=enable='gte(t,57)':volume=0.8[aux3]; \
   [aux1][aux2][aux3]concat=n=3:v=0:a=1[out]; \
   [0:a][out]amix=inputs=2:duration=first:dropout_transition=3" \
  mix_ducking.mp3
```

### Fade in/out da musica
```bash
ffmpeg -i musica.mp3 \
  -af "afade=t=in:st=0:d=2,afade=t=out:st=58:d=2" \
  musica_fades.mp3
```

### Comprimir audio dinamica (mais uniforme)
```bash
ffmpeg -i audio.mp3 \
  -af "acompressor=threshold=-20dB:ratio=4:attack=5:release=50" \
  audio_comprimido.mp3
```

---

## Comandos de Mixagem Completa

### Video + Voz + Musica
```bash
ffmpeg -i video.mp4 \
  -i voz_normalizada.mp3 \
  -i musica_fundo.mp3 \
  -filter_complex \
  "[0:a]anull; \
   [1:a]volume=0dB[voz]; \
   [2:a]volume=-14dB[musica]; \
   [musica]afade=t=in:st=0:d=1,afade=t=out:st=58:d=1[musica_f]; \
   [voz][musica_f]amix=inputs=2:duration=first:dropout_transition=2[aout]" \
  -map 0:v -map "[aout]" \
  -c:v copy -c:a aac -b:a 192k \
  -shortest video_final.mp4
```

### Apenas audio (para preview)
```bash
ffmpeg -i voz.mp3 -i musica.mp3 \
  -filter_complex "[1:a]volume=0dB[v];[2:a]volume=-14dB[m];[m]afade=t=in:st=0:d=1,afade=t=out:st=58:d=1[mf];[v][mf]amix=inputs=2:duration=first:dropout_transition=2" \
  -c:a mp3 \
  mix_preview.mp3
```

---

## Musicas por Objetivo

### Motivacional / Empreendedor
- BPM: 120-140
- Genero: Lo-fi hip hop, corporate upbeat
- Instrumentos: Piano, bateria eletronica, sintetizador
- Caracteristica: Build-up no inicio, climax no meio

### Educacional / Tutorial
- BPM: 80-100
- Genero: Ambient, lo-fi study
- Instrumentos: Piano suave, guitarra acustica
- Caracteristica: Constante, sem surpresas, nao distrai

### Humor / Entretenimento
- BPM: 110-130
- Genero: Funk, pop, comedy
- Instrumentos: Baixo, sintetizadores divertidos
- Caracteristica: Ritmo marcante, mudancas divertidas

### Dramatico / Storytelling
- BPM: 90-120
- Genero: Cinematic, orchestral
- Instrumentos: Cordas, piano dramatico, percussao
- Caracteristica: Build-up gradual, climax emocional

### Relaxante / Lifestyle
- BPM: 60-80
- Genero: Ambient, chill, acoustic
- Instrumentos: Guitarra suave, nature sounds, piano
- Caracteristica: Calmo, minimalista, espacoso

---

## Problemas Comuns e Solucoes

| Problema | Causa | Solucao |
|---|---|---|
| Audio clipa | True peak > 0 dBTP | `loudnorm=TP=-1` |
| Musica abafa voz | Musica muito alta | Reduzir musica 12-18dB |
| Volume inconsistente | Variacao de LUFS | `loudnorm` + `acompressor` |
| Eco/reverb demais | Gravacao com reverb | `aecho=0.5:0.7:0` para reduzir |
| Silencios estranhos | Cortes mal feitos | Fade de 0.05s entre cortes |
| Musica nao sincroniza | BPM errado | `atempo` para ajustar BPM |

---

## Checklist de Mixagem

- [ ] Voz normalizada em -14 LUFS
- [ ] Musica de fundo em -24 a -30 LUFS
- [ ] Fade in/out na musica (1-2s)
- [ ] Ducking da musica quando ha fala
- [ ] True peak abaixo de -1 dBTP
- [ ] Sem cliques ou pops entre cortes
- [ ] LRA (Dynamic Range) abaixo de 15 LU
- [ ] Duracao do audio = duracao do video
- [ ] Formato: AAC 192kbps ou MP3 320kbps
- [ ] Testar em alto-falante de celular (volume baixo)
