# Estrutura de Pastas - content-fs

Raiz do workspace: `~/conteudo`

```
~/conteudo/
├── campanhas/                        # Pasta principal de clientes
│   └── {cliente}/                    # Um diretorio por cliente (slug, minusculo, sem espacos)
│       ├── .env.cliente              # Credenciais e tokens (NUNCA committar ao git)
│       ├── contexto.json             # Memoria do cliente: preferencias, nicho, tom de voz
│       ├── historico.json            # Log de conteudos publicados com metricas
│       ├── posts-midias-sociais/     # Pipeline de posts organicos
│       │   ├── ideias/               # Rascunhos e brainstorm (textos, scripts)
│       │   ├── roteiros/             # Scripts prontos para gravacao
│       │   ├── brutos/               # Gravacoes brutas (.mp4, .mov, .avi, .mkv)
│       │   ├── editados/             # Videos finais prontos (.mp4)
│       │   └── publicados/           # Arquivos ja publicados (copia de backup)
│       ├── criativos-anuncios/       # Pipeline de anuncios pagos
│       │   ├── ideias/               # Ideias de criativos
│       │   ├── roteiros/             # Scripts de anuncios
│       │   ├── brutos/               # Gravacoes brutas
│       │   ├── editados/             # Criativos finais
│       │   └── publicados/           # Criativos ja publicados
│       ├── briefings/                # Documentos de briefing (.md, .pdf)
│       └── metricas/                 # Relatorios e dados de performance (.json, .md)
├── referencias/                      # Dados de referencia compartilhados
│   ├── trends/                       # Pesquisas de tendencia (.json, .md)
│   └── templates/                    # Templates de scripts, biblioteca de hooks
└── assets/                           # Recursos compartilhados
    ├── musicas/                      # Audios livres de direitos (.mp3, .wav, .aac)
    ├── fontes/                       # Fontes customizadas (.ttf, .otf, .woff)
    └── overlays/                     # Overlays, lower thirds, molduras
```

## Formatos Suportados

| Tipo      | Extensoes                                  |
|-----------|--------------------------------------------|
| Video     | .mp4, .mov, .avi, .mkv                     |
| Imagem    | .png, .jpg, .jpeg, .webp, .gif             |
| Audio     | .mp3, .wav, .aac                           |
| Documento | .pdf, .md, .json                            |

## Pipeline de Midia

Os arquivos seguem um fluxo linear entre as fases:

```
ideias/ -> roteiros/ -> brutos/ -> editados/ -> publicados/
```

Cada fase representa um estagio de producao. Arquivos sao movidos (nao copiados) entre fases conforme avancam na producao.

## Regras de Nomenclatura

- Nomes de clientes: minusculo, sem espacos, hifens no lugar de espacos
- Exemplo: `restaurante-sabor`, `dra-maria-saude`
- Arquivos de midia: incluir data no inicio quando possivel (ex: `20250115-reels-bruto.mp4`)
