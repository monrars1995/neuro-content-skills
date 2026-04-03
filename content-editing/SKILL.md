---
name: content-editing
description: "Edicao de video usando Remotion com Next.js e TypeScript. Montagem automatica e manual de videos, aplicacao de templates, overlays, texto animado, transicoes e exportacao. Use quando: editar video, montar video com remotion, aplicar template, adicionar legendas, criar transicoes, exportar video, renderizar com remotion. Comandos: /editar, /render, /legendas, /template."
---

# Content Editing

## Stack Tecnica

- **Remotion** — programacao de videos com React
- **Next.js** — framework base do projeto
- **TypeScript** — tipagem estatica
- **FFmpeg** — processamento adicional de video/audio

---

## Onboarding Interativo

Ao iniciar uma edicao, pergunte ao usuario:

1. **Projeto** — Ja existe projeto Remotion? Se nao, guiar setup
2. **Conteudo bruto** — Qual conteudo editar? Liste de `brutos/`
3. **Template** — Qual template/estilo usar? Liste disponiveis
4. **Legendas** — Legendas automaticas ou manuais?
5. **Resolucao** — Qual resolucao de saida? (1080x1920 vertical, 1920x1080 horizontal)

---

## Setup do Projeto Remotion

Se nao existir projeto Remotion em `~/conteudo/` ou na pasta do cliente:

```bash
npx create-video@latest ~/conteudo/editor --template next
```

Configure `tsconfig.json` para Remotion e crie os templates base.

Consulte `scripts/setup_remotion.sh` para setup automatizado.

---

## Templates Disponiveis

Consulte `references/remotion_templates.md` para codigo detalhado dos componentes.

### Vertical (9:16) — TikTok / Reels / Shorts

- Hook text animation (scale in)
- Subtitle style (word-by-word highlight)
- Lower third para branding
- CTA end card com logo

### Horizontal (16:9) — YouTube / Feed

- Title card com animacao
- Layout side-by-side para comparacoes
- Transicoes com overlay B-roll
- End card subscribe/follow

---

## Workflow de Edicao

1. **Analisar bruto** — Extraia metadata (duracao, resolucao) com `ffprobe`
2. **Selecionar takes** — Use o plano de gravacao para escolher os melhores takes
3. **Montar timeline** — Organize clips na ordem do roteiro
4. **Aplicar template** — Adicione texto, transicoes, overlays
5. **Legendas** — Gere ou aplique trilha de legendas
6. **Preview** — Renderize preview em baixa qualidade
7. **Ajustes** — Ajuste timing, texto e transicoes
8. **Exportar** — Renderize o video final em qualidade completa

---

## Remotion Component Pattern

```typescript
import { Composition } from "remotion";
import { VideoSequence } from "./components/VideoSequence";

export const VideoComposition: React.FC = () => {
  return (
    <Composition
      id="VideoFinal"
      component={VideoSequence}
      durationInFrames={150}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        clips: [],
        subtitles: [],
        hookText: "",
        ctaText: "",
        brandColor: "#fff",
      }}
    />
  );
};
```

---

## Comandos de Exportacao

```bash
npx remotion render src/index.ts VideoFinal out/{cliente}_{titulo}.mp4 --codec h264
```

Salve videos editados em:
```
~/conteudo/campanhas/{cliente}/{tipo}/editados/
```

---

## Referencias

- `references/remotion_templates.md` — componentes Remotion detalhados
- `scripts/setup_remotion.sh` — setup automatizado do projeto
