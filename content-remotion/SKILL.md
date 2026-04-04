---
name: content-remotion
description: "Framework de edicao dopaminergica com Remotion. Cria videos short-form com cortes rapidos, legendas dinamicas word-by-word, zoom animations, B-roll overlays, transicoes energeticas e formatos otimizados para Reels, Shorts e TikTok. Use quando: criar video dopaminergico, legendas dinamicas, zoom animations, remotion video, edicao rapida, formato viral, B-roll overlay. Comandos: /dopamina, /legendas-dinamicas, /zoom, /overlay, /render-remotion."
---

# Content Remotion

## Stack Tecnica

- **Remotion 4.x** — programacao de videos com React
- **React 18** — componentes de composicao
- **TypeScript** — tipagem estatica
- **FFmpeg** — pre-processamento e pos-processamento
- **Next.js** — projeto base opcional

---

## Onboarding Interativo

Ao iniciar um projeto de edicao dopaminergica, pergunte:

1. **Projeto Remotion** — Ja existe projeto? Se nao, executar `/setup`
2. **Video de entrada** — Qual video processar? (de `brutos/` ou `editados/`)
3. **Estilo dopaminergico** — Rapido (cortes a cada 2-3s), medio (3-5s), ou cinematico (5-8s)?
4. **Legendas** — Word-by-word (Alex Hormozi style), frase completa, ou nenhuma?
5. **Zoom** — Zoom rapido em palavras-chave, zoom suave, ou sem zoom?
6. **Overlays** — B-roll, emoji reactions, progress bar, ou limpo?
7. **Plataforma** — Reels, Shorts, TikTok, ou multiplataforma?

---

## Slash Commands

### `/dopamina [cliente] [video]` - Video Dopaminergico

Cria video short-form com formato dopaminergico completo.

1. Analisar video com content-cuts (`/analisar`)
2. Gerar cortes com smart_cut.py
3. Criar composicao Remotion com:
   - Hook text com scale animation (0-3s)
   - Legendas word-by-word com highlight
   - Zoom rapido em palavras-chave
   - Transicoes energeticas entre cenas
   - CTA end card
4. Renderizar com `npx remotion render`

```bash
# Gerar composicao
python3 scripts/generate_dopamine_comp.py --video brutos/entrevista.mp4 --cliente joao --estilo rapido

# Renderizar
npx remotion render src/index.ts DopamineVideo out/dopamina_corte_01.mp4 --codec h264
```

### `/legendas-dinamicas [cliente] [video]` - Legendas Word-by-Word

Gera legendas no estilo Alex Hormozi com highlight palavra-por-palavra.

1. Extrair transcricao com Whisper (content-editing `/legendas`)
2. Gerar composicao Remotion com:
   - Cada palavra aparece com scale animation
   - Palavra atual em amarelo/branco com fundo escuro
   - Palavras anteriores em branco
   - Posicao inferior central
3. Sincronizar com timestamps do video

```bash
python3 scripts/generate_subtitle_comp.py --video editados/corte_01.mp4 --cliente joao --estilo hormozi
```

### `/zoom [cliente] [video]` - Zoom Animations

Adiciona zoom dinamico ao video baseado em palavras-chave.

1. Analisar transcricao para identificar palavras-chave
2. Aplicar zoom-in rapido (1.2x → 1.4x) em palavras importantes
3. Zoom-out suave entre frases
4. Ken Burns effect sutil em cenas sem fala

```bash
python3 scripts/generate_zoom_comp.py --video editados/corte_01.mp4 --cliente joao --intensidade alta
```

### `/overlay [cliente] [video]` - B-roll e Overlays

Adiciona camadas visuais sobre o video.

1. B-roll overlay em momentos sem fala
2. Emoji reactions em pontos-chave
3. Progress bar no topo
4. Logo/branding no canto
5. Seta indicando direcao de scroll (para carrossel)

### `/render-remotion [cliente] [composicao]` - Renderizar

Renderiza composicao Remotion em multiplas qualidades.

```bash
# Preview rapido
npx remotion render src/index.ts DopamineVideo out/preview.mp4 --codec h264 --crf 28 --scale 0.5

# Qualidade final
npx remotion render src/index.ts DopamineVideo out/final.mp4 --codec h264 --crf 18

# Multiplas plataformas
npx remotion render src/index.ts DopamineVideo out/ --image-format png --sequence
```

---

## Formato Dopaminergico

### Principios

1. **Velocidade** — Cortes a cada 2-3 segundos (estilo rapido) ou 3-5s (medio)
2. **Zoom** — Zoom rapido em palavras-chave para manter atencao
3. **Legenda** — Word-by-word highlight prende o olhar
4. **Som** — Cada corte sincronizado com beat ou mudanca sonora
5. **Cor** — Cores vibrantes, contraste alto
6. **CTA** — End card com acao clara nos ultimos 3s

### Timing Padrao (60s video)

| Tempo | Elemento |
|---|---|
| 0-3s | Hook text: scale 0 → 1.2 + blur → sharp |
| 3-5s | Contexto rapido com legenda |
| 5-55s | Conteudo principal com cortes + zoom + legendas |
| 55-58s | Transicao para CTA |
| 58-60s | CTA card com texto + seta |

---

## Composicao Remotion Base

```typescript
import { Composition, staticFile, useVideoConfig } from "remotion";
import { DopamineSequence } from "./components/DopamineSequence";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="DopamineVideo"
        component={DopamineSequence}
        durationInFrames={1800}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          videoSrc: "",
          subtitles: [],
          zoomPoints: [],
          hookText: "",
          ctaText: "",
          style: "rapido",
          brandColor: "#FFD700",
        }}
      />
    </>
  );
};
```

---

## Componentes Disponiveis

Consulte `references/remotion_components.md` para codigo completo.

- `DopamineSequence` — composicao principal com todos os efeitos
- `WordByWordSubtitle` — legenda com highlight palavra-por-palavra
- `ZoomContainer` — container com zoom dinamico
- `HookText` — texto do hook com animacao de entrada
- `CTACard` — card de call-to-action final
- `ProgressBar` — barra de progresso no topo
- `B RollOverlay` — overlay de B-roll
- `EmojiReaction` — emoji animado sobreposto

---

## Scripts

- `scripts/generate_dopamine_comp.py` — gera composicao Remotion completa a partir do video
- `scripts/generate_subtitle_comp.py` — gera componente de legendas word-by-word
- `scripts/generate_zoom_comp.py` — gera pontos de zoom baseados na transcricao

---

## Referencias

- `references/remotion_components.md` — codigo completo de todos os componentes
- `references/dopaminergic_patterns.md` — padroes e tecnicas de edicao dopaminergica
- **Cortes**: content-cuts (`/analisar`, `/cortar`, `/pontuar`)
- **Legendas Whisper**: content-editing (`/legendas`)
- **Audio/Musica**: content-audio (`/voz`, `/musica`, `/mixar`)
- **Publicacao**: content-publishing (`/publicar`)
