# Templates Remotion

## Componente Base: VideoSequence

```typescript
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { HookText } from "./HookText";
import { WordByWordSubtitle } from "./WordByWordSubtitle";
import { LowerThird } from "./LowerThird";
import { CTAEndCard } from "./CTAEndCard";

type Clip = {
  src: string;
  startFrame: number;
  durationInFrames: number;
};

type SubtitleEntry = {
  text: string;
  startFrame: number;
  endFrame: number;
};

type VideoSequenceProps = {
  clips: Clip[];
  subtitles: SubtitleEntry[];
  hookText: string;
  ctaText: string;
  brandColor: string;
  brandLogo?: string;
};

export const VideoSequence: React.FC<VideoSequenceProps> = ({
  clips,
  subtitles,
  hookText,
  ctaText,
  brandColor,
  brandLogo,
}) => {
  const { durationInFrames, fps } = useVideoConfig();
  const totalClipFrames = clips.reduce((acc, c) => acc + c.durationInFrames, 0);
  const hookDuration = Math.floor(fps * 2);
  const ctaStartFrame = totalClipFrames;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {clips.map((clip, i) => {
        const startFrame = clips
          .slice(0, i)
          .reduce((acc, c) => acc + c.durationInFrames, 0);

        return (
          <Sequence
            key={i}
            from={startFrame}
            durationInFrames={clip.durationInFrames}
          >
            <video
              src={clip.src}
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
              autoPlay
              muted
            />
          </Sequence>
        );
      })}

      <Sequence from={0} durationInFrames={hookDuration}>
        <HookText text={hookText} color={brandColor} />
      </Sequence>

      {subtitles.map((sub, i) => (
        <Sequence
          key={i}
          from={sub.startFrame}
          durationInFrames={sub.endFrame - sub.startFrame}
        >
          <WordByWordSubtitle text={sub.text} color={brandColor} />
        </Sequence>
      ))}

      <Sequence from={Math.floor(fps * 1)} durationInFrames={Math.floor(fps * 3)}>
        <LowerThird brand={brandLogo || ""} color={brandColor} />
      </Sequence>

      <Sequence from={ctaStartFrame} durationInFrames={Math.floor(fps * 4)}>
        <CTAEndCard text={ctaText} color={brandColor} logo={brandLogo} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

---

## HookText (animacao scale-in)

```typescript
import React from "react";
import { AbsoluteFill, useCurrentFrame, spring, useVideoConfig } from "remotion";

type HookTextProps = {
  text: string;
  color: string;
};

export const HookText: React.FC<HookTextProps> = ({ text, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 200, mass: 0.5 },
  });

  const opacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 40,
      }}
    >
      <div
        style={{
          fontSize: 64,
          fontWeight: 900,
          color: color,
          textAlign: "center",
          textShadow: "2px 2px 8px rgba(0,0,0,0.7)",
          transform: `scale(${scale})`,
          opacity,
          lineHeight: 1.2,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
```

---

## WordByWordSubtitle

```typescript
import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";

type WordByWordSubtitleProps = {
  text: string;
  color: string;
};

export const WordByWordSubtitle: React.FC<WordByWordSubtitleProps> = ({
  text,
  color,
}) => {
  const frame = useCurrentFrame();
  const words = text.split(" ");
  const wordsPerSecond = 2.5;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 120,
        paddingInline: 30,
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: 6,
        }}
      >
        {words.map((word, i) => {
          const wordStartFrame = Math.floor((i / wordsPerSecond) * 30);
          const wordOpacity = interpolate(
            frame,
            [wordStartFrame, wordStartFrame + 5],
            [0.3, 1],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          );

          return (
            <span
              key={i}
              style={{
                fontSize: 42,
                fontWeight: 800,
                color: "white",
                backgroundColor: "rgba(0,0,0,0.6)",
                padding: "4px 8px",
                borderRadius: 6,
                opacity: wordOpacity,
                textShadow: `0 0 10px ${color}`,
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

---

## LowerThird

```typescript
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";

type LowerThirdProps = {
  brand: string;
  color: string;
};

export const LowerThird: React.FC<LowerThirdProps> = ({ brand, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideIn = spring({
    frame,
    fps,
    config: { damping: 20, stiffness: 150 },
  });

  const slideOut = interpolate(
    frame,
    [fps * 2.5, fps * 3],
    [0, -400],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const translateX = frame < fps * 2.5 ? -400 * (1 - slideIn) : slideOut;

  return (
    <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "flex-start", paddingTop: 80 }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          paddingLeft: 30,
          transform: `translateX(${translateX}px)`,
        }}
      >
        <div
          style={{
            width: 4,
            height: 40,
            backgroundColor: color,
            borderRadius: 2,
          }}
        />
        <span
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: "white",
            textShadow: "1px 1px 4px rgba(0,0,0,0.8)",
          }}
        >
          {brand}
        </span>
      </div>
    </AbsoluteFill>
  );
};
```

---

## CTAEndCard

```typescript
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";

type CTAEndCardProps = {
  text: string;
  color: string;
  logo?: string;
};

export const CTAEndCard: React.FC<CTAEndCardProps> = ({ text, color, logo }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bgOpacity = interpolate(frame, [0, 15], [0, 0.85], {
    extrapolateRight: "clamp",
  });

  const scale = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 100 },
  });

  const pulseScale = interpolate(
    Math.sin(frame * 0.08),
    [-1, 1],
    [1, 1.05]
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: `rgba(0,0,0,${bgOpacity})`,
        justifyContent: "center",
        alignItems: "center",
        gap: 24,
      }}
    >
      {logo && (
        <img
          src={logo}
          style={{ width: 80, height: 80, borderRadius: 20, objectFit: "contain" }}
        />
      )}
      <div
        style={{
          fontSize: 48,
          fontWeight: 900,
          color: color,
          textAlign: "center",
          transform: `scale(${scale * pulseScale})`,
          textShadow: "0 0 20px rgba(0,0,0,0.5)",
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Transicoes

### Fade

```typescript
import { AbsoluteFill, Sequence, useCurrentFrame, interpolate } from "remotion";

export const FadeTransition: React.FC<{
  children: React.ReactNode;
  direction: "in" | "out";
}> = ({ children, direction }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [0, 15],
    direction === "in" ? [0, 1] : [1, 0],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ opacity }}>
      {children}
    </AbsoluteFill>
  );
};
```

### Slide

```typescript
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

export const SlideTransition: React.FC<{
  children: React.ReactNode;
  direction: "left" | "right" | "up" | "down";
}> = ({ children, direction }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const offset = 400;

  const progress = spring({ frame, fps, config: { damping: 20, stiffness: 100 } });
  const distance = offset * (1 - progress);

  const translateMap = {
    left: `${distance}px, 0`,
    right: `${-distance}px, 0`,
    up: `0, ${distance}px`,
    down: `0, ${-distance}px`,
  };

  return (
    <AbsoluteFill style={{ transform: `translate(${translateMap[direction]})` }}>
      {children}
    </AbsoluteFill>
  );
};
```

### Zoom

```typescript
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";

export const ZoomTransition: React.FC<{
  children: React.ReactNode;
  direction: "in" | "out";
}> = ({ children, direction }) => {
  const frame = useCurrentFrame();
  const scale = interpolate(
    frame,
    [0, 20],
    direction === "in" ? [1.5, 1] : [1, 1.5],
    { extrapolateRight: "clamp" }
  );
  const opacity = interpolate(
    frame,
    [0, 15],
    direction === "in" ? [0, 1] : [1, 0],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ transform: `scale(${scale})`, opacity }}>
      {children}
    </AbsoluteFill>
  );
};
```
