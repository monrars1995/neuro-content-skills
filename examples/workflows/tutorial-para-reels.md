# Workflow: Tutorial para Reels

Workflow completo para transformar uma aula/tutorial em Reels educativos.

---

## Resumo

| Metrica | Valor |
|---|---|
| Video original | 15-45 min (aula) |
| Reels gerados | 5-8 |
| Tempo estimado | 30-45 min |
| Skills usadas | 4 |

---

## Passo a Passo

### 1. Setup
```
/iniciar-projeto cliente=maria nicho="design"
```

### 2. Ideias
```
/ideias maria --nicho "design"
```

### 3. Analisar Aula
```
/analisar maria brutos/aula_figma.mp4
```

### 4. Gerar Cortes
```
/cortar maria brutos/aula_figma.mp4 --plataforma reels --max-duracao 60
```

Gera 5-8 cortes, cada um com 1 dica ou conceito.

### 5. Pontuar e Filtrar
```
/pontuar maria editados/aula_figma_corte_01.mp4
```

Manter apenas cortes com pontuacao >= 55.

### 6. Legendas
```
/legendas editados/aula_figma_corte_01.mp4 maria
```

### 7. Edicao Dopaminergica
```
/dopamina maria editados/aula_figma_corte_01.mp4 --estilo medio --cor "#0066FF"
```

Tutorial usa estilo medio (cortes a cada 3-5s) com zoom suave.

### 8. Musica de Fundo
```
/musica maria --objetivo educacional --duracao 60
/mixar maria --video editados/aula_figma_corte_01.mp4 --musica brutos/musica_educacional.mp3
```

### 9. Publicar
```
/publicar maria editados/aula_figma_corte_01.mp4 --plataforma reels
```

---

## Dicas para Tutoriais

1. **1 conceito por Reel** — Nao tente resumir a aula inteira
2. **Comece com o resultado** — "Em 30s voce vai aprender..."
3. **Zoom em passos-chave** — Destaque os cliques e atalhos
4. **CTA: "salva pra usar depois"** — Alta taxa de save
5. **Texto overlay** — Mostre o passo atual (ex: "Passo 2/5")
