---
name: content-publishing
description: "Publicacao e agendamento de videos em TikTok e Instagram via API. Integra com TikTok Content Posting API e Instagram Graph API para postagem/agendamento automatico de Reels e videos curtos. Use quando: publicar video, agendar post, postar no tiktok, postar no instagram, subir reel, agendar conteudo, configurar api de publicacao. Comandos: /publicar, /agendar, /setup-api."
---

# Content Publishing - Publicacao de Conteudo via API

## Onboarding Interativo

Ao configurar publicacao para um cliente:

1. Diga: "Vou te guiar na configuracao das APIs de publicacao. Vamos comecar!"
2. Pergunte quais plataformas configurar (TikTok, Instagram, ou ambos)
3. Para cada plataforma, acompanhe o tutorial de setup abaixo
4. Teste a conexao apos cada configuracao
5. Salve credenciais em `~/conteudo/campanhas/{cliente}/.env.cliente`

## Setup Tutorial - TikTok Content Posting API

1. Acesse https://developers.tiktok.com
2. Crie uma conta de desenvolvedor
3. Crie um novo App no dashboard
4. Ative "Content Posting" nas APIs do App
5. Gere um Access Token com scopes: `video.upload`, `video.publish`
6. Anote: `TIKTOK_ACCESS_TOKEN` e `TIKTOK_APP_ID`
7. Salve no `.env.cliente`:
    ```
    TIKTOK_ACCESS_TOKEN=seu_token_aqui
    TIKTOK_APP_ID=seu_app_id_aqui
    TIKTOK_USERNAME=username_do_perfil
    ```

## Setup Tutorial - Instagram Graph API (via Facebook)

1. Acesse https://developers.facebook.com
2. Crie um App (tipo Business)
3. Adicione Instagram Basic Display API
4. Vincule a Pagina do Facebook do cliente
5. Ative Content Publishing para a Pagina
6. Gere um Long-lived Access Token
7. Obtenha o Instagram Business Account ID vinculado a Pagina
8. Anote as credenciais
9. Salve no `.env.cliente`:
   ```
   META_ACCESS_TOKEN=seu_token_aqui
   INSTAGRAM_BUSINESS_ACCOUNT_ID=id_da_conta
   FACEBOOK_PAGE_ID=id_da_pagina
   ```

## API Integration Patterns

### TikTok Upload Flow

1. Inicializar upload:
   ```
   POST https://open.tiktokapis.com/v2/post/publish/video/init/
   Headers: Authorization: Bearer {token}
   Body: { "post_info": { "title": "...", "privacy_level": "PUBLIC_TO_EVERYONE" }, "source_info": { "video_size": 12345, "video_chunk_size": 5242880 } }
   ```
2. Fazer upload do video (PUT para a `upload_url` retornada)
3. Criar post:
   ```
   POST https://open.tiktokapis.com/v2/post/publish/content/init/
   Body: { "post_info": { "title": "...", "description": "...", "hashtags": ["tag1", "tag2"] }, "source_info": { "source": "PULL_FROM_URL", "video_url": "..." } }
   ```
4. Verificar status:
   ```
   GET https://open.tiktokapis.com/v2/post/publish/status/fetch/?publish_id={id}
   ```

### Instagram Reel Upload Flow

1. Criar container:
   ```
   POST graph.facebook.com/v21.0/{ig-user-id}/media
   Body: { video_url: "...", media_type: "REELS", caption: "...", share_to_feed: true }
   ```
2. Aguardar processamento:
   ```
   GET graph.facebook.com/v21.0/{container-id}?fields=status_code
   ```
3. Publicar:
   ```
   POST graph.facebook.com/v21.0/{ig-user-id}/media_publish
   Body: { creation_id: "{container-id}" }
   ```

## Publishing Workflow

1. Carregue credenciais do cliente de `.env.cliente`
2. Selecione o video de `~/conteudo/campanhas/{cliente}/{tipo}/editados/`
3. Gere metadados (titulo, descricao, hashtags, tags)
4. Faca upload para a(s) plataforma(s) selecionada(s)
5. Salve registro de publicacao em `historico.json`
6. Mova o arquivo para `publicados/`
7. Retorne as URLs de publicacao

## Geracao de Metadados

Gere automaticamente com base no contexto do cliente e roteiro:

- **Descricao**: Baseada no roteiro + tom do cliente
- **Hashtags**: Baseada no nicho + tendencias (dados de content-ideas)
- **Tags**: Baseada no tipo de conteudo
- **Horario**: Baseado nos melhores horarios do cliente (dados de metrics)

## Agendamento

Para agendar publicacoes:

1. Salve em um arquivo de schedule com data/hora
2. Proponha instrucoes `cron` ou `at` para execucao automatica
3. Use agendamento nativo da plataforma se disponivel

## Error Handling

- **Token expirado**: Guie re-autenticacao e renovacao
- **Upload falhou**: Retry com exponential backoff (3 tentativas)
- **Video rejeitado**: Logue o motivo, sugira correcoes (formato, duracao, conteudo)
## Referencias

- **Endpoints das APIs**: `references/api_endpoints.md`
- **Setup das APIs**: `references/api_setup.md`
- **Memoria do cliente**: content-memory (`/historico`, `/contexto`)
- **Estrutura de pastas**: content-fs (`/organizar`)
- **Metricas**: content-metrics (`/metricas`)
