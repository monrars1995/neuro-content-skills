#!/usr/bin/env bash
set -euo pipefail

MIN_NODE="18"
PROJECT_DIR="${1:-$HOME/conteudo/editor}"

echo "=== Setup Remotion + Next.js ==="

if ! command -v node &>/dev/null; then
  echo "ERRO: Node.js nao encontrado. Instale em https://nodejs.org"
  exit 1
fi

NODE_MAJOR=$(node -e "process.stdout.write(process.versions.node.split('.')[0])")
if [ "$NODE_MAJOR" -lt "$MIN_NODE" ]; then
  echo "ERRO: Node.js $MIN_NODE+ necessario. Versao atual: $(node -v)"
  exit 1
fi
echo "OK: Node.js $(node -v) detectado"

if [ -d "$PROJECT_DIR" ]; then
  echo "AVISO: Projeto ja existe em $PROJECT_DIR"
  read -rp "Sobrescrever? (s/N): " confirm
  if [ "$confirm" != "s" ] && [ "$confirm" != "S" ]; then
    echo "Operacao cancelada."
    exit 0
  fi
  rm -rf "$PROJECT_DIR"
fi

echo "Criando projeto Remotion + Next.js em $PROJECT_DIR..."
npx create-video@latest "$PROJECT_DIR" --template next

cd "$PROJECT_DIR"

echo "Instalando dependencias..."
npm install

mkdir -p src/components src/templates

cat > src/components/HookText.tsx << 'COMPONENT'
import React from "react";
import { AbsoluteFill, useCurrentFrame, spring, useVideoConfig } from "remotion";

export const HookText: React.FC<{ text: string; color: string }> = ({ text, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 200, mass: 0.5 } });
  const opacity = frame < 10 ? frame / 10 : 1;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: 40 }}>
      <div style={{
        fontSize: 64, fontWeight: 900, color, textAlign: "center",
        textShadow: "2px 2px 8px rgba(0,0,0,0.7)",
        transform: `scale(${scale})`, opacity, lineHeight: 1.2,
      }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};
COMPONENT

cat > src/components/WordByWordSubtitle.tsx << 'COMPONENT'
import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";

export const WordByWordSubtitle: React.FC<{ text: string; color: string }> = ({ text, color }) => {
  const frame = useCurrentFrame();
  const words = text.split(" ");
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 120, paddingInline: 30 }}>
      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: 6 }}>
        {words.map((word, i) => {
          const start = Math.floor((i / 2.5) * 30);
          const opacity = interpolate(frame, [start, start + 5], [0.3, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <span key={i} style={{
              fontSize: 42, fontWeight: 800, color: "white",
              backgroundColor: "rgba(0,0,0,0.6)", padding: "4px 8px", borderRadius: 6, opacity,
            }}>
              {word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
COMPONENT

cat > src/components/LowerThird.tsx << 'COMPONENT'
import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

export const LowerThird: React.FC<{ brand: string; color: string }> = ({ brand, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const slideIn = spring({ frame, fps, config: { damping: 20, stiffness: 150 } });
  const slideOut = interpolate(frame, [fps * 2.5, fps * 3], [0, -400], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const translateX = frame < fps * 2.5 ? -400 * (1 - slideIn) : slideOut;
  return (
    <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "flex-start", paddingTop: 80 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12, paddingLeft: 30, transform: `translateX(${translateX}px)` }}>
        <div style={{ width: 4, height: 40, backgroundColor: color, borderRadius: 2 }} />
        <span style={{ fontSize: 28, fontWeight: 700, color: "white", textShadow: "1px 1px 4px rgba(0,0,0,0.8)" }}>{brand}</span>
      </div>
    </AbsoluteFill>
  );
};
COMPONENT

cat > src/components/CTAEndCard.tsx << 'COMPONENT'
import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

export const CTAEndCard: React.FC<{ text: string; color: string; logo?: string }> = ({ text, color, logo }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const bgOpacity = interpolate(frame, [0, 15], [0, 0.85], { extrapolateRight: "clamp" });
  const scale = spring({ frame, fps, config: { damping: 10, stiffness: 100 } });
  const pulse = interpolate(Math.sin(frame * 0.08), [-1, 1], [1, 1.05]);
  return (
    <AbsoluteFill style={{ backgroundColor: `rgba(0,0,0,${bgOpacity})`, justifyContent: "center", alignItems: "center", gap: 24 }}>
      {logo && <img src={logo} style={{ width: 80, height: 80, borderRadius: 20, objectFit: "contain" }} />}
      <div style={{ fontSize: 48, fontWeight: 900, color, textAlign: "center", transform: `scale(${scale * pulse})`, textShadow: "0 0 20px rgba(0,0,0,0.5)" }}>{text}</div>
    </AbsoluteFill>
  );
};
COMPONENT

echo ""
echo "=== Setup concluido ==="
echo "Projeto: $PROJECT_DIR"
echo ""
echo "Para iniciar:"
echo "  cd $PROJECT_DIR"
echo "  npx remotion studio"
echo ""
echo "Para renderizar:"
echo "  npx remotion render src/index.ts VideoFinal out/video.mp4 --codec h264"
