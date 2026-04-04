# Componentes Remotion para Edicao Dopaminergica

Componentes React prontos para usar em projetos Remotion.

---

## Instalacao

```bash
npx create-video@latest meu-projeto --template blank
cd meu-projeto
npm install remotion @remotion/cli @remotion/media-utils
```

---

## 1. DopamineSequence (Composicao Principal)

```typescript
// src/components/DopamineSequence.tsx
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
} from "remotion";

interface SubtitleWord {
  text: string;
  startFrame: number;
  endFrame: number;
}

interface ZoomPoint {
  frame: number;
  scale: number;
  duration: number;
}

interface Props {
  videoSrc: string;
  subtitles: SubtitleWord[];
  zoomPoints: ZoomPoint[];
  hookText: string;
  ctaText: string;
  style: "rapido" | "medio" | "cinematico";
  brandColor: string;
}

export const DopamineSequence: React.FC<Props> = ({
  videoSrc,
  subtitles,
  zoomPoints,
  hookText,
  ctaText,
  style,
  brandColor,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const zoomScale = getZoomScale(frame, zoomPoints);
  const isHookPhase = frame < fps * 3;
  const isCTAPhase = frame > durationInFrames - fps * 5;

  const hookOpacity = isHookPhase
    ? interpolate(frame, [0, 15], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
    : interpolate(frame, [fps * 3, fps * 3.5], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const hookScale = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });

  const ctaOpacity = isCTAPhase
    ? interpolate(frame, [durationInFrames - fps * 3, durationInFrames - fps * 2.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
    : 0;

  const currentWords = subtitles.filter(
    (w) => frame >= w.startFrame && frame <= w.endFrame
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* Video com zoom */}
      <AbsoluteFill
        style={{
          transform: `scale(${zoomScale})`,
          transition: "transform 0.3s ease-out",
        }}
      >
        {videoSrc && (
          <video
            src={videoSrc}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
            muted
          />
        )}
      </AbsoluteFill>

      {/* Barras laterais (letterbox) */}
      <div style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: 80,
        backgroundColor: "rgba(0,0,0,0.3)",
      }} />
      <div style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        width: "100%",
        height: 200,
        background: "linear-gradient(transparent, rgba(0,0,0,0.8))",
      }} />

      {/* Hook Text */}
      {hookText && (
        <div style={{
          position: "absolute",
          top: 100,
          left: "50%",
          transform: `translateX(-50%) scale(${hookScale})`,
          opacity: hookOpacity,
          textAlign: "center",
          width: "90%",
        }}>
          <div style={{
            fontSize: 52,
            fontWeight: 900,
            color: "#fff",
            textShadow: "0 4px 20px rgba(0,0,0,0.8)",
            lineHeight: 1.2,
          }}>
            {hookText}
          </div>
        </div>
      )}

      {/* Legendas Word-by-Word */}
      {currentWords.length > 0 && (
        <div style={{
          position: "absolute",
          bottom: 220,
          left: "50%",
          transform: "translateX(-50%)",
          width: "90%",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: 4,
        }}>
          {subtitles
            .filter((w) => w.endFrame <= currentWords[0].endFrame)
            .map((word, i) => {
              const isActive =
                frame >= word.startFrame && frame <= word.endFrame;
              const wordScale = isActive
                ? interpolate(
                    frame,
                    [word.startFrame, word.startFrame + 5],
                    [1, 1.15],
                    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
                  )
                : 1;
              return (
                <span
                  key={i}
                  style={{
                    fontSize: 42,
                    fontWeight: 700,
                    color: isActive ? brandColor : "#ffffff",
                    transform: `scale(${wordScale})`,
                    textShadow: "0 2px 8px rgba(0,0,0,0.9)",
                    display: "inline-block",
                  }}
                >
                  {word.text}
                </span>
              );
            })}
        </div>
      )}

      {/* CTA Card */}
      {ctaText && ctaOpacity > 0 && (
        <div style={{
          position: "absolute",
          bottom: 120,
          left: "50%",
          transform: `translateX(-50%)`,
          opacity: ctaOpacity,
          backgroundColor: brandColor,
          borderRadius: 16,
          padding: "16px 32px",
          textAlign: "center",
        }}>
          <div style={{
            fontSize: 36,
            fontWeight: 800,
            color: "#000",
          }}>
            {ctaText}
          </div>
          <div style={{
            fontSize: 20,
            color: "#333",
            marginTop: 4,
          }}>
            👆 Comente sua resposta
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

function getZoomScale(frame: number, zoomPoints: ZoomPoint[]): number {
  if (zoomPoints.length === 0) return 1;

  for (const point of zoomPoints) {
    if (frame >= point.frame && frame < point.frame + point.duration) {
      const progress = (frame - point.frame) / point.duration;
      const eased = Easing.out(Easing.cubic(progress));
      return interpolate(eased, [0, 1], [1, point.scale]);
    }
  }
  return 1;
}
```

---

## 2. WordByWordSubtitle (Legenda Isolada)

```typescript
// src/components/WordByWordSubtitle.tsx
import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface Word {
  text: string;
  startFrame: number;
  endFrame: number;
}

interface Props {
  words: Word[];
  style?: "hormozi" | "clean" | "bold" | "neon";
  position?: "bottom" | "center";
  maxWordsPerLine?: number;
}

export const WordByWordSubtitle: React.FC<Props> = ({
  words,
  style = "hormozi",
  position = "bottom",
  maxWordsPerLine = 6,
}) => {
  const frame = useCurrentFrame();

  const activeWordIndex = words.findIndex(
    (w) => frame >= w.startFrame && frame <= w.endFrame
  );
  if (activeWordIndex === -1) return null;

  const visibleWords = words.filter((w) => w.endFrame <= words[activeWordIndex].endFrame);
  const lines: Word[][] = [];
  for (let i = 0; i < visibleWords.length; i += maxWordsPerLine) {
    lines.push(visibleWords.slice(i, i + maxWordsPerLine));
  }

  const styles = {
    hormozi: {
      activeColor: "#FFD700",
      inactiveColor: "#FFFFFF",
      bgOpacity: 0.85,
      fontSize: 40,
      fontWeight: 800,
      bgPadding: "6px 4px",
      bgRadius: 6,
    },
    clean: {
      activeColor: "#FFFFFF",
      inactiveColor: "#AAAAAA",
      bgOpacity: 0.6,
      fontSize: 36,
      fontWeight: 600,
      bgPadding: "4px 2px",
      bgRadius: 4,
    },
    bold: {
      activeColor: "#00FF88",
      inactiveColor: "#FFFFFF",
      bgOpacity: 0.9,
      fontSize: 48,
      fontWeight: 900,
      bgPadding: "8px 6px",
      bgRadius: 8,
    },
    neon: {
      activeColor: "#FF00FF",
      inactiveColor: "#CCCCCC",
      bgOpacity: 0.7,
      fontSize: 38,
      fontWeight: 700,
      bgPadding: "6px 4px",
      bgRadius: 6,
    },
  };

  const s = styles[style];
  const topOffset = position === "center" ? "45%" : undefined;
  const bottomOffset = position === "bottom" ? 200 : undefined;

  return (
    <div
      style={{
        position: "absolute",
        left: "5%",
        right: "5%",
        top: topOffset,
        bottom: bottomOffset,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 8,
      }}
    >
      {lines.map((line, lineIdx) => (
        <div
          key={lineIdx}
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: 3,
          }}
        >
          {line.map((word, wordIdx) => {
            const isActive =
              frame >= word.startFrame && frame <= word.endFrame;
            const wordPop = isActive
              ? interpolate(frame, [word.startFrame, word.startFrame + 4], [1, 1.12], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                })
              : 1;
            return (
              <span
                key={wordIdx}
                style={{
                  fontSize: s.fontSize,
                  fontWeight: s.fontWeight,
                  color: isActive ? s.activeColor : s.inactiveColor,
                  backgroundColor: `rgba(0,0,0,${s.bgOpacity})`,
                  padding: s.bgPadding,
                  borderRadius: s.bgRadius,
                  transform: `scale(${wordPop})`,
                  display: "inline-block",
                  textShadow: "0 2px 4px rgba(0,0,0,0.5)",
                }}
              >
                {word.text}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};
```

---

## 3. ZoomContainer

```typescript
// src/components/ZoomContainer.tsx
import React, { Children } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

interface Props {
  zoomPoints: { frame: number; scale: number; duration: number }[];
  children: React.ReactNode;
}

export const ZoomContainer: React.FC<Props> = ({ zoomPoints, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  let scale = 1;
  for (const point of zoomPoints) {
    if (frame >= point.frame && frame < point.frame + point.duration) {
      const progress = (frame - point.frame) / point.duration;
      const halfProgress = progress < 0.5 ? progress * 2 : (1 - progress) * 2;
      scale = interpolate(halfProgress, [0, 1], [1, point.scale]);
      break;
    }
  }

  return (
    <AbsoluteFill style={{
      transform: `scale(${scale})`,
      transformOrigin: "center center",
    }}>
      {children}
    </AbsoluteFill>
  );
};
```

---

## 4. CTA Card

```typescript
// src/components/CTACard.tsx
import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

interface Props {
  text: string;
  subtext: string;
  color: string;
  emoji: string;
  showFromFrame: number;
}

export const CTACard: React.FC<Props> = ({ text, subtext, color, emoji, showFromFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [showFromFrame, showFromFrame + 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const slideUp = spring({ frame: showFromFrame, fps, config: { damping: 15, stiffness: 150 } });

  const bounceEmoji = frame % 30 < 15 ? 0 : -8;

  return (
    <div style={{
      position: "absolute",
      bottom: 100,
      left: "10%",
      right: "10%",
      opacity,
      transform: `translateY(${(1 - slideUp) * 100}px)`,
    }}>
      <div style={{
        backgroundColor: color,
        borderRadius: 20,
        padding: "20px 30px",
        textAlign: "center",
        boxShadow: `0 8px 30px ${color}66`,
      }}>
        <div style={{
          fontSize: 20,
          marginBottom: 8,
          transform: `translateY(${bounceEmoji}px)`,
        }}>
          {emoji}
        </div>
        <div style={{ fontSize: 32, fontWeight: 800, color: "#000" }}>
          {text}
        </div>
        <div style={{ fontSize: 18, color: "#333", marginTop: 6 }}>
          {subtext}
        </div>
      </div>
    </div>
  );
};
```

---

## 5. ProgressBar

```typescript
// src/components/ProgressBar.tsx
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

interface Props {
  color?: string;
  height?: number;
}

export const ProgressBar: React.FC<Props> = ({ color = "#FF0000", height = 4 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const progress = frame / durationInFrames;

  return (
    <AbsoluteFill style={{ padding: "12px 0" }}>
      <div style={{
        width: `${progress * 100}%`,
        height,
        backgroundColor: color,
        borderRadius: 2,
        transition: "width 0.1s linear",
      }} />
    </AbsoluteFill>
  );
};
```

---

## Render Commands

```bash
# Preview (rapido, baixa qualidade)
npx remotion preview src/index.ts

# Render vertical 1080x1920
npx remotion render src/index.ts DopamineVideo out/video.mp4 \
  --width=1080 --height=1920 --fps=30 --codec=h264 --crf=18

# Render GIF para preview
npx remotion render src/index.ts DopamineVideo out/preview.gif \
  --scale=0.5 --every-nth-frame=2

# Render frames (para composicao externa)
npx remotion render src/index.ts DopamineVideo out/frames/ \
  --image-format=png --sequence
```
