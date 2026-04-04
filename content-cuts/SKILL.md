---
name: content-cuts
description: "Especialista em cortes virais para Reels, Shorts e TikTok. Analisa video para identificar pontos de corte otimos, detecta silencios e mudancas de cena, avalia potencial viral com rubrica de pontuacao e sugere repurposing de conteudo longo. Use quando: cortar video, criar reel, fazer short, cortar tiktok, analisar video, detectar silencios, pontuar video, repurpose conteudo. Comandos: /analisar, /cortar, /pontuar, /repurpose."
---

# Content Cuts

## Stack Tecnica

- **FFmpeg** — processamento de video e audio
- **ffprobe** — extracao de metadata e analise de stream
- **Python 3.10+** — scripts de analise e automacao
- **Silero VAD** — deteccao de voz/atividade de fala
- **scenedetect** — deteccao de mudancas de cena

---

## Onboarding Interativo

Ao iniciar uma sessao de cortes, pergunte ao usuario:

1. **Video de origem** — Qual video cortar? Liste de `brutos/`
2. **Plataforma destino** — Reels (9:16), Shorts (9:16), TikTok (9:16) ou Feed (16:9)?
3. **Duracao maxima** — Qual o limite? (Reels: 90s, Shorts: 60s, TikTok: 180s)
4. **Objetivo** — Engajamento (hook forte), educativo (retention), ou viral (share)?
5. **Estilo** — Cortes rapidos (jump cuts), suaves (J/L cuts), ou cinematico?

---

## Slash Commands

### `/analisar [cliente] [video]` - Analisar Video

Analisa completo do video bruto para identificar oportunidades de corte.

1. Executar `scripts/analyze_video.py` com o video
2. Extrair metadata (duracao, resolucao, fps, bitrate)
3. Detectar silencios (gap > 0.8s)
4. Detectar mudancas de cena
5. Calcular ritmo medio de fala (palavras por minuto)
6. Identificar trechos com alta densidade de informacao
7. Gerar relatorio JSON com timestamps de corte sugeridos

Exemplo:
```bash
python3 scripts/analyze_video.py --video brutos/entrevista.mp4 --cliente joao --saida analisado/
```

Saida esperada:
```json
{
  "metadata": { "duracao": 342.5, "resolucao": "1920x1080", "fps": 30 },
  "silencios": [
    { "start": 12.3, "end": 13.8, "duracao": 1.5 },
    { "start": 45.2, "end": 46.1, "duracao": 0.9 }
  ],
  "cenas": [
    { "timestamp": 34.5, "tipo": "hard_cut" },
    { "timestamp": 120.3, "tipo": "fade" }
  ],
  "trechos_interessantes": [
    { "start": 15.0, "end": 45.0, "motivo": "alta_densidade_fala" },
    { "start": 120.0, "end": 155.0, "motivo": "ponto_chave" }
  ]
}
```

### `/cortar [cliente] [video]` - Gerar Cortes Virais

Gera multiplos cortes otimizados para short-form a partir do video analise.

1. Ler analise gerada por `/analisar`
2. Selecionar trechos com maior potencial viral
3. Aplicar regras de corte para cada plataforma:
   - **Reels**: max 90s, hook nos primeiros 3s, CTA nos ultimos 5s
   - **Shorts**: max 60s, ritmo acelerado, legendas obrigatorias
   - **TikTok**: max 180s, trending sounds, text overlay no hook
4. Executar `scripts/smart_cut.py` para gerar os cortes
5. Salvar em `editados/` com nomenclatura: `{titulo}_corte_{n}.mp4`

Exemplo:
```bash
python3 scripts/smart_cut.py --video brutos/entrevista.mp4 --cliente joao --plataforma reels --max-duracao 90 --saida editados/
```

Regras de corte:
- Hook nos primeiros 3 segundos (frase de impacto)
- Remover silencios > 0.5s (compactar fala)
- Jump cuts a cada mudanca de ideia
- Manter ritmo de fala entre 150-180 palavras/minuto
- CTA nos ultimos 5 segundos

### `/pontuar [cliente] [video]` - Pontuar Potencial Viral

Avalia o potencial viral de um video com rubrica detalhada.

1. Executar `scripts/score_video.py` com o video
2. Avaliar cada criterio da rubrica (ver `references/scoring_rubric.md`)
3. Gerar pontuacao de 0 a 100 com breakdown por categoria
4. Sugerir melhorias especificas para aumentar pontuacao

Exemplo:
```bash
python3 scripts/score_video.py --video editados/corte_01.mp4 --cliente joao
```

Saida esperada:
```
=== PONTUACAO VIRAL ===
Pontuacao Total: 72/100

Breakdown:
  Hook (0-25):     20/25  ✓ Hook forte nos 2s
  Ritmo (0-20):    16/20  ✓ Bom ritmo, 2 trechos lentos
  Engajamento (0-20): 14/20  ~ Pergunta no CTA
  Formato (0-15):  12/15  ✓ Legenda, falta emoji
  Audio (0-10):     6/10  ~ Volume inconsistente
  CTA (0-10):      4/10  ✗ CTA generico

Sugestoes:
  1. Trocar CTA generico por pergunta especifica (+3 pts)
  2. Adicionar emojis nos primeiros 3s (+2 pts)
  3. Normalizar volume de audio (+3 pts)
```

### `/repurpose [cliente] [video]` - Repurposing de Conteudo

Gera multiplas versoes de um mesmo conteudo para diferentes plataformas.

1. Analisar video de origem
2. Gerar cortes otimizados para cada plataforma
3. Ajustar formato (vertical/horizontal/quadrado)
4. Sugerir legendas e hooks especificos por plataforma

Exemplo de repurposing:
- **Podcast 60min** → 8 Shorts + 3 Reels + 1 TikTok Longo + 5 Audiogramas
- **Aula 45min** → 5 Reels educativos + 2 Shorts Dicas + 1 Carrossel

---

## Metodologia de Cortes Virais

### Framework HRC (Hook-Retention-CTA)

1. **Hook (0-3s)** — Primeira frase deve ser impactante. Cortar na palavra que gera curiosidade.
2. **Retention (3s-CTA)** — Manter ritmo acelerado. Cortar silencios, hesitacoes, respiracoes audiveis.
3. **CTA (ultimos 5s)** — Frase de acao clara e especifica.

### Tecnicas de Corte

- **Jump Cut** — Corte seco entre frases. Remove hesitacoes.
- **L-Cut** — Audio do proximo trecho inicia antes da imagem.
- **J-Cut** — Imagem do proximo trecho aparece antes do audio.
- **Match Cut** — Transicao visual entre cenas similares.
- **Smash Cut** — Contraste brusco para impacto.

### Duracoes Otimas por Plataforma

| Plataforma | Minimo | Otimo | Maximo |
|---|---|---|---|
| Reels | 15s | 30-60s | 90s |
| Shorts | 15s | 30-45s | 60s |
| TikTok | 15s | 45-90s | 180s |

---

## Scripts Disponiveis

- `scripts/analyze_video.py` — analise completa com ffprobe (metadata, silencios, cenas)
- `scripts/smart_cut.py` — geracao de cortes com FFmpeg baseada na analise
- `scripts/score_video.py` — pontuacao de potencial viral com rubrica

---

## Referencias

- `references/scoring_rubric.md` — rubrica completa de pontuacao viral
- `references/cuts_reference.md` — tecnicas de corte e exemplos por plataforma
- **Edicao completa**: content-editing (`/editar`, `/render`, `/legendas`)
- **Publicacao**: content-publishing (`/publicar`)
- **Metricas**: content-metrics (`/metricas`)
