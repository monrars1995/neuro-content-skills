---
name: content-fs
description: "Gerencia estrutura de pastas e organizacao de arquivos de midia para campanhas de conteudo. Cria diretorios de clientes, organiza arquivos .mp4 .mov .png .jpg, analisa conteudos existentes para reuso. Use quando: criar campanha, organizar arquivos, analisar midia, verificar estrutura de pastas, listar conteudo de cliente, mover arquivos de midia. Comandos: /organizar, /listar-midias, /analisar-midia."
---

# content-fs

Gerencia o sistema de arquivos para campanhas de conteudo. Cria, organiza e analisa a estrutura completa de pastas e midias.

## Workspace

Raiz: `~/conteudo`

Sempre verifique se `~/conteudo` existe. Crie caso contrario:

```bash
mkdir -p ~/conteudo
```

## Funcoes

### ensure_client_dirs(client)

Cria a arvore completa de pastas para um cliente.

```bash
CLIENTE="nome-do-cliente"
BASE=~/conteudo/campanhas/$CLIENTE

mkdir -p "$BASE"/{posts-midias-sociais/{ideias,roteiros,brutos,editados,publicados}}
mkdir -p "$BASE"/{criativos-anuncios/{ideias,roteiros,brutos,editados,publicados}}
mkdir -p "$BASE"/{briefings,metricas}
mkdir -p "$BASE"/../referencias/{trends,templates}
mkdir -p "$BASE"/../assets/{musicas,fontes,overlays}
```

Apos criar, inicialize os arquivos base:

```bash
echo '{}' > "$BASE/contexto.json"
echo '{"entries":[]}' > "$BASE/historico.json"
touch "$BASE/.env.cliente"
```

Garanta que `.env.cliente` esta no `.gitignore`:

```bash
if [ -f ~/conteudo/.gitignore ]; then
  grep -qxF '.env.cliente' ~/conteudo/.gitignore || echo '.env.cliente' >> ~/conteudo/.gitignore
else
  echo '.env.cliente' > ~/conteudo/.gitignore
fi
```

### analyze_media_files(client, type)

Escaneia uma pasta de midia e retorna inventario com metadados.

**Parametros:**
- `client` - nome do cliente
- `type` - `posts-midias-sociais` ou `criativos-anuncios`

**Para videos** (.mp4, .mov, .avi, .mkv), use ffprobe:

```bash
for f in ~/conteudo/campanhas/$CLIENTE/$TYPE/*/; do
  for file in "$f"*.mp4 "$f"*.mov "$f"*.avi "$f"*.mkv; do
    [ -f "$file" ] || continue
    ffprobe -v quiet -print_format json -show_format -show_streams "$file"
  done
done
```

Extraia: duracao, resolucao, codec, tamanho, data de criacao.

**Para imagens** (.png, .jpg, .jpeg, .webp, .gif):

```bash
for file in ~/conteudo/campanhas/$CLIENTE/$TYPE/*/*.{png,jpg,jpeg,webp,gif}; do
  [ -f "$file" ] || continue
  echo "arquivo: $file"
  echo "tamanho: $(du -h "$file" | cut -f1)"
  echo "dimensoes: $(sips -g pixelWidth -g pixelHeight "$file" 2>/dev/null | grep pixel)"
  echo "criado: $(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$file")"
done
```

**Formatos suportados:**
- Video: .mp4, .mov, .avi, .mkv
- Imagem: .png, .jpg, .jpeg, .webp, .gif
- Audio: .mp3, .wav, .aac
- Documento: .pdf, .md, .json

Retorne um resumo estruturado com: total de arquivos, tamanho total, lista por fase, arquivos mais recentes.

### move_to_phase(client, type, phase, files)

Move arquivos entre fases do pipeline.

**Fases validas:** `brutos` -> `editados` -> `publicados`

```bash
DEST=~/conteudo/campanhas/$CLIENTE/$TYPE/$PHASE
mkdir -p "$DEST"
for file in "${FILES[@]}"; do
  mv "$file" "$DEST/"
done
```

Antes de mover, verifique se o arquivo de origem existe. Registre a movimentacao no historico.json do cliente.

### save_reference(ref_type, data)

Salva dados de referencia.

- `ref_type=trend` - salva em `~/conteudo/referencias/trends/`
- `ref_type=template` - salva em `~/conteudo/referencias/templates/`

```bash
DEST=~/conteudo/referencias/$REF_TYPE
mkdir -p "$DEST"
echo "$DATA" > "$DEST/$(date +%Y%m%d-%H%M%S).json"
```

## Onboarding Interativo

Quando um novo cliente for mencionado, pergunte:

1. **Nome do cliente** (slug para pastas)
2. **Nicho** (ex: restaurantes, saude, imobiliario)
3. **Plataformas alvo** (ex: instagram, tiktok, youtube)
4. **Tom de voz** (ex: formal, descontraido, educativo)

Com as respostas, execute `ensure_client_dirs` e popule `contexto.json` com os dados iniciais.

## Regras

- Nunca commite `.env.cliente` - sempre adicione ao `.gitignore`
- Ao criar pastas, use `mkdir -p` para evitar erros
- Ao mover arquivos, confirme existencia antes
- Ao analisar midias, trate arquivos corrompidos gracefully (pule e reporte)
- Mantenha nomes de pastas em minusculo, sem espacos (use hifen)
