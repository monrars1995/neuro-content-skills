# Referencia de Cortes para Short-Form

Guia completo de tecnicas de corte para Reels, Shorts e TikTok.

---

## Tipos de Corte

### Jump Cut
Corte seco entre frases. Remove hesitacoes, respiracoes e silencios.

**Quando usar:** Podcasts, entrevistas, talking heads.
**Como fazer:** Cortar no inicio da proxima frase, removendo a pausa anterior.
```bash
# FFmpeg: cortar trecho de 15s a 45s
ffmpeg -i input.mp4 -ss 15 -to 45 -c copy output.mp4
```

### L-Cut
Audio do proximo trecho inicia antes da troca de imagem.

**Quando usar:** Transicoes suaves, storytelling, B-roll.
**Efeito:** Cria antecipacao. O espectador ouve o proximo topico antes de ver.

### J-Cut
Imagem do proximo trecho aparece antes do audio.

**Quando usar:** Reacoes, revelacoes, contraste.
**Efeito:** O espectador ve algo antes de entender o contexto (curiosidade).

### Match Cut
Transicao visual entre cenas com elementos similares.

**Quando usar:** Tutoriais passo-a-passo, comparacoes, antes/depois.
**Efeito:** Conexao visual entre ideias diferentes.

### Smash Cut
Contraste brusco entre cenas para impacto.

**Quando usar:** Plot twist, humor, contraste (problema → solucao).
**Efeito:** Choque visual que retém atencao.

---

## Duracoes Otimas

### Reels (Instagram)
- **Otimo:** 30-60 segundos
- **Maximo:** 90 segundos
- **Minimo:** 15 segundos
- **Tipos:** Tutorial (45s), Historia (60s), Dica rapida (15-20s), Trend (30s)

### Shorts (YouTube)
- **Otimo:** 30-45 segundos
- **Maximo:** 60 segundos
- **Minimo:** 15 segundos
- **Tipos:** Dica (30s), Curiosidade (20s), Tutorial rapido (45s), Ranking (60s)

### TikTok
- **Otimo:** 45-90 segundos
- **Maximo:** 180 segundos (mas <60s performa melhor)
- **Minimo:** 15 segundos
- **Tipos:** Storytime (60-90s), Tutorial (45-60s), Trend (15-30s), React (30-60s)

---

## Estrutura HRC (Hook-Retention-CTA)

### Hook (0-3 segundos)
**Objetivo:** Parar o scroll.

Patterns de hook que funcionam:
1. **Curiosidade:** "O que ninguem te conta sobre..."
2. **Controversia:** "Esse e o pior erro que..."
3. **Numero:** "3 formas de..." / "90% das pessoas..."
4. **Mistake:** "Eu demorei 5 anos para descobrir..."
5. **Direto:** "Para de fazer X. Faca Y."
6. **Pergunta:** "Voce sabia que..."
7. **Resultado:** "Como fui de X para Y em 30 dias..."

### Retention (3s ate CTA)
**Objetivo:** Manter ate o final.

Tecnicas:
- Cortar silencios > 0.5s
- Jump cut a cada mudanca de ideia
- Manter 150-180 palavras/minuto
- Variar ritmo (acelerar em pontos chave)
- B-roll a cada 8-10s se talking head
- Text overlay para reforcar pontos

### CTA (ultimos 3-5 segundos)
**Objetivo:** Gerar acao.

CTAs que funcionam:
- **Pergunta:** "Comente aqui embaixo qual..."
- **Desafio:** "Tente fazer isso e me marque"
- **Compartilhe:** "Mande pra alguem que precisa ouvir isso"
- **Save:** "Salva pra assistir de novo"
- **Segue:** "Se voce concorda, segue pra mais"
- **Link:** "Link na bio pra..."

---

## Cortes por Tipo de Conteudo

### Podcast / Entrevista → Shorts
1. Identificar momentos de alta energia (risos, reacoes, controversia)
2. Cortar a pergunta e ir direto na resposta
3. Adicionar contexto via texto overlay nos primeiros 2s
4. Compactar: remover todas as pausas > 0.3s
5. Adicionar legenda dinamica

### Aula / Tutorial → Reels
1. Extrair 1 conceito por video (nao tentar resumir tudo)
2. Comecar com o resultado ("em 30 segundos voce vai aprender...")
3. Cortar entre passos com transicoes rapidas
4. Texto overlay com o passo atual
5. CTA: "salva pra usar depois"

### Vlog → TikTok
1. Identificar 3-5 momentos icone do vlog
2. Montar sequencia rapida com musica trending
3. Text overlay narrando a historia
4. Cortar no pico emocional de cada cena
5. Final aberto (continuacao nos proximos videos)

### Review / Unboxing → Shorts
1. Hook com a opiniao final ou dado surpreendente
2. Cortar direto pros pontos principais
3. Mostrar produto em uso (B-roll)
4. CTC (Call to Comment): "concorda? comenta ai"

---

## Formatos de Saida

### Vertical (9:16) — 1080x1920
```bash
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -preset fast -crf 23 output_vertical.mp4
```

### Quadrado (1:1) — 1080x1080
```bash
ffmpeg -i input.mp4 -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -preset fast -crf 23 output_square.mp4
```

### Horizontal (16:9) — 1920x1080
```bash
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -preset fast -crf 23 output_horizontal.mp4
```

---

## Checklist de Cortes

Antes de publicar, verificar:

- [ ] Hook nos primeiros 3 segundos
- [ ] Sem silencios > 0.5s (exceto intencionais)
- [ ] Legendas legiveis e sincronizadas
- [ ] Formato correto para a plataforma (9:16, 1:1, 16:9)
- [ ] Audio limpo e normalizado
- [ ] CTA nos ultimos 3-5 segundos
- [ ] Duracao dentro do otimo para a plataforma
- [ ] Sem marcas d'agua de outros apps
- [ ] Resolucao minima 720p
- [ ] Texto overlay centralizado e legivel em tela pequena
