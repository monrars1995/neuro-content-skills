# Workflow: Podcast para Shorts

Workflow completo para transformar um podcast de 60 minutos em multiplos Shorts otimizados.

---

## Resumo

| Metrica | Valor |
|---|---|
| Video original | 60 min (podcast) |
| Shorts gerados | 8-12 |
| Tempo estimado | 45-60 min |
| Skills usadas | 5 |

---

## Passo a Passo

### 1. Setup do Cliente
```
/iniciar-projeto cliente=joao nicho="negocios digitais"
```

Cria estrutura:
```
~/conteudo/campanhas/joao/
  .env.cliente
  posts-midias-sociais/
    ideias/
    roteiros/
    brutos/
    editados/
    publicados/
```

### 2. Ideias e Trending
```
/ideias joao --nicho "negocios digitais"
```

Busca trends no TikTok, Google Trends e Meta Ads Library.
Salva ideias em `posts-midias-sociais/ideias/`.

### 3. Analisar o Podcast
```
/analisar joao brutos/podcast_ep01.mp4
```

Gera `brutos/podcast_ep01_analise.json` com:
- Silencios detectados
- Mudancas de cena
- Trechos interessantes (pontuados por score)

### 4. Gerar Cortes
```
/cortar joao brutos/podcast_ep01.mp4 --plataforma shorts --max-duracao 45
```

Gera 8-12 cortes em `editados/`:
- `podcast_ep01_corte_01.mp4` (45s)
- `podcast_ep01_corte_02.mp4` (38s)
- ...

### 5. Pontuar Cortes
```
/pontuar joao editados/podcast_ep01_corte_01.mp4
```

Avalia cada corte com rubrica viral (0-100).
Sugere melhorias para cada corte.

### 6. Gerar Legendas
```
/legendas editados/podcast_ep01_corte_01.mp4 joao --formato todos
```

Gera SRT, JSON e Remotion JSON.

### 7. Edicao Dopaminergica (Opcional)
```
/dopamina joao editados/podcast_ep01_corte_01.mp4 --estilo rapido
```

Gera composicao Remotion com:
- Hook animado
- Legendas word-by-word
- Zoom em palavras-chave
- CTA card

### 8. Audio (Opcional)
```
/musica joao --objetivo educacional --duracao 45
/mixar joao --video editados/podcast_ep01_corte_01.mp4 --musica brutos/musica_educacional.mp3
```

### 9. Publicar
```
/publicar joao editados/podcast_ep01_corte_01.mp4 --plataforma shorts
```

---

## Comandos Rapidos (Copiar e Colar)

```bash
# Analise + cortes de uma vez
python3 ~/.opencode/skills/content-cuts/scripts/analyze_video.py --video brutos/podcast.mp4 --cliente joao
python3 ~/.opencode/skills/content-cuts/scripts/smart_cut.py --video brutos/podcast.mp4 --cliente joao --plataforma shorts --saida editados/

# Pontuar todos os cortes
for f in editados/*_corte_*.mp4; do
  python3 ~/.opencode/skills/content-cuts/scripts/score_video.py --video "$f" --cliente joao
done

# Gerar composicao Remotion para o melhor corte
python3 ~/.opencode/skills/content-remotion/scripts/generate_dopamine_comp.py --video editados/corte_01.mp4 --cliente joao --estilo rapido --saida remotion/
```
