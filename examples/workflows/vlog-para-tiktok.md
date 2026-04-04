# Workflow: Vlog para TikTok

Workflow completo para transformar vlogs em conteudo otimizado para TikTok.

---

## Resumo

| Metrica | Valor |
|---|---|
| Video original | 10-30 min (vlog) |
| TikToks gerados | 5-10 |
| Tempo estimado | 30-45 min |
| Skills usadas | 4 |

---

## Passo a Passo

### 1. Setup
```
/iniciar-projeto cliente=carlos nicho="viagens"
```

### 2. Analisar Vlog
```
/analisar carlos brutos/vlog_sp_01.mp4
```

### 3. Gerar Cortes
```
/cortar carlos brutos/vlog_sp_01.mp4 --plataforma tiktok --max-duracao 90
```

Para TikTok, usar max-duracao 90 (mas <60s performa melhor).

### 4. Pontuar
```
/pontuar carlos editados/vlog_sp_01_corte_01.mp4
```

### 5. Legendas
```
/legendas editados/vlog_sp_01_corte_01.mp4 carlos
```

### 6. Edicao Dopaminergica
```
/dopamina carlos editados/vlog_sp_01_corte_01.mp4 --estilo rapido --cor "#FF0080"
```

Vlog usa estilo rapido (cortes a cada 2-3s) com energia alta.

### 7. Musica Trending
```
/musica carlos --objetivo humor --duracao 45
/mixar carlos --video editados/vlog_sp_01_corte_01.mp4 --musica brutos/musica_humor.mp3
```

### 8. Publicar
```
/publicar carlos editados/vlog_sp_01_corte_01.mp4 --plataforma tiktok
```

---

## Dicas para Vlogs

1. **Momentos icone** — Corte nos picos emocionais (risadas, surpresas)
2. **Texto narrando** — Adicione contexto via texto overlay
3. **Corte no pico** — Corte exatamente no momento mais impactante
4. **Final aberto** — Deixe suspense para o proximo video
5. **Trending sounds** — Use audios trending do TikTok
6. **Hashtags** — 3-5 hashtags relevantes no primeiro comentario
