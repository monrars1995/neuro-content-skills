# Padroes de Edicao Dopaminergica

Tecnicas de edicao para maximizar retencao e engajamento em videos short-form.

---

## O que e Edicao Dopaminergica?

Edicao projetada para manter o cerebro constantemente estimulado, evitando que o espectador perca interesse. Usa:
- Cortes frequentes
- Mudancas visuais constantes
- Zoom dinamico
- Legendas animadas
- Transicoes energeticas
- Som sincronizado

---

## Principios Fundamentais

### 1. Regra dos 3 Segundos
A cada 3 segundos, algo novo deve acontecer na tela:
- Corte de cena
- Zoom in/out
- Mudanca de texto
- Nova informacao visual
- Transicao de overlay

### 2. Pattern Interrupt
Quebre o padrao visual periodicamente:
- Contraste de cores (claro → escuro)
- Mudanca de velocidade (rapido → lento → rapido)
- Troca de angulo ou perspectiva
- Insercao de emoji ou grafico

### 3. Antecipacao Visual
Mostre o resultado antes do processo:
- "Em 30 segundos voce vai aprender X" → conteudo → "Aprendeu?"
- Preview do final → como fazer → resultado

### 4. Progressao Constante
Sempre avance. Nunca repita:
- Informacao nova a cada frase
- Cenário novo a cada 10-15s
- Visual novo a cada 5-8s

---

## Tecnicas por Estilo

### Estilo Rapido (Cortes a cada 2-3s)

**Ideal para:** TikTok trends, dicas rapidas, memes, humor.

- Cortes secos (jump cuts) a cada mudanca de frase
- Zoom 1.2x-1.4x em palavras-chave
- Legendas word-by-word com highlight rapido
- Sem transicoes (corte direto)
- B-roll a cada 2 cenas de talking head
- Musica trending em volume medio-alto

**Timing 30s:**
```
0-2s   Hook (zoom + texto)
2-5s   Contexto (2 frases)
5-10s  Ponto 1 (zoom em key word)
10-15s Ponto 2 (corte + novo angulo)
15-20s Ponto 3 (B-roll overlay)
20-25s Resultado/demo
25-28s CTA
28-30s End card
```

### Estilo Medio (Cortes a cada 3-5s)

**Ideal para:** Tutoriais, storytelling, reviews.

- Cortes com transicoes curtas (0.2s)
- Zoom suave 1.1x-1.2x em pontos-chave
- Legendas word-by-word com highlight suave
- Transicoes: fade rapido, wipe, slide
- B-roll contextual a cada 3-4 cenas
- Musica de fundo em volume baixo

**Timing 60s:**
```
0-3s    Hook (texto animado + zoom)
3-8s    Apresentacao do problema
8-15s   Ponto 1 (zoom + legenda)
15-22s  Ponto 2 (transicao + novo cenario)
22-30s  Ponto 3 (B-roll + demo)
30-38s  Ponto 4 (plot twist ou dado surpreendente)
38-48s  Ponto 5 (resolucao)
48-53s  Resultado
53-57s  CTA
57-60s  End card
```

### Estilo Cinematico (Cortes a cada 5-8s)

**Ideal para:** Documentario, vlog artistico, storytelling longo.

- Cortes com L-cuts e J-cuts
- Ken Burns effect (zoom e pan suaves)
- Legendas clean, frase por frase
- Transicoes: crossfade, dissolve, match cut
- B-roll atmosferico
- Musica cinematografica em volume equilibrado

---

## Animacoes de Zoom

### Zoom Rapido (Estilo Hormozi)
```
Frame 0:   scale(1.0)
Frame 3:   scale(1.3) — ease-out rapido
Frame 15:  scale(1.3) — mantem
Frame 18:  scale(1.0) — ease-in rapido
```

### Zoom Suave (Estilo Cinematico)
```
Frame 0:   scale(1.0)
Frame 30:  scale(1.15) — ease-in-out
Frame 60:  scale(1.15) — mantem
Frame 90:  scale(1.0) — ease-in-out
```

### Zoom Pulse (Palavra-chave)
```
Frame 0:   scale(1.0)
Frame 2:   scale(1.25) — ease-out
Frame 8:   scale(1.2) — mantem
Frame 10:  scale(1.0) — ease-in
```

---

## Paleta de Cores por Objetivo

| Objetivo | Cor Principal | Cor Destaque | Background |
|---|---|---|---|
| Viral/Entretenimento | #FF0000 | #FFD700 | #000000 |
| Educacao | #0066FF | #00FF88 | #0A0A2E |
| Luxo/Premium | #FFD700 | #FFFFFF | #1A1A2E |
| Tecnologia | #00D4FF | #7B2FFF | #0D1117 |
| Saude/Fitness | #00FF88 | #FF6B6B | #1A1A1A |
| Negocios | #FF8C00 | #FFFFFF | #1E293B |
| Humor | #FF69B4 | #FFD700 | #1A1A2E |

---

## Checklist Dopaminergico

Antes de renderizar:

- [ ] Hook nos primeiros 2-3s com animacao
- [ ] Cortes a cada 2-5s (conforme estilo)
- [ ] Zoom em palavras-chave
- [ ] Legendas word-by-word com highlight
- [ ] Gradiente escuro no inferior (para legibilidade)
- [ ] Barras laterais para focar atencao
- [ ] B-roll em momentos sem fala
- [ ] Musica sincronizada com cortes
- [ ] CTA animado nos ultimos 3-5s
- [ ] Progress bar sutil no topo
- [ ] Sem momentos "mortos" (tela parada > 1s)
- [ ] Contraste alto em textos sobre video
