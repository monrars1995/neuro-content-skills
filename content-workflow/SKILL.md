---
name: content-workflow
description: "Orquestrador principal do pipeline de criacao de conteudo para midias sociais. Coordena todas as etapas: Ideias, Roteiro, Gravacao, Edicao (Remotion), Publicacao (TikTok/Instagram) e Metricas. Gerencia multiplos clientes, memoria persistente e estrutura de pastas. Use quando: criar conteudo, pipeline de video, campanha de midia social, workflow de conteudo, onboarding de cliente, status de campanha, gerenciar clientes, fluxo completo de criacao de conteudo."
---

# Content Workflow - Pipeline Completo de Criacao de Conteudo

Orquestra o pipeline de 6 etapas para criacao de conteudo em midias sociais.

## Etapas do Pipeline

```
1. IDEIAS (content-ideas)
   ↓
2. ROTEIRO (content-script)
   ↓
3. GRAVACAO (content-recording)
   ↓
4. EDICAO (content-editing)
   ↓
5. PUBLICACAO (content-publishing)
   ↓
6. METRICAS (content-metrics)
```

## Skills do Pacote

| Skill | Funcao | Trigger |
|-------|--------|---------|
| content-fs | Estrutura de pastas e organizacao de midia | Criar campanha, organizar arquivos |
| content-memory | Memoria persistente e contexto do cliente | Lembrar preferencias, historico |
| content-ideas | Pesquisa de trends e captacao de ideias | Buscar ideias, trends |
| content-script | Roteirizacao Hook-Desenvolvimento-CTA | Criar roteiro, script |
| content-recording | Planejamento de gravacao | Preparar gravacao, takes |
| content-editing | Edicao de video com Remotion | Editar video, montar |
| content-publishing | Publicacao via TikTok/Instagram API | Publicar, agendar |
| content-metrics | Analise de performance | Metricas, relatorios |

## Comandos

### `novo cliente` - Onboarding Completo
1. Perguntar nome do cliente
2. Perguntar nicho/segmento
3. Perguntar plataformas (TikTok, Instagram, YouTube Shorts)
4. Perguntar frequencia de publicacao
5. Perguntar tom de voz e estilo
6. Criar estrutura de pastas (content-fs)
7. Inicializar contexto e historico (content-memory)
8. Perguntar se quer configurar APIs agora (content-publishing)

### `nova campanha` - Iniciar Pipeline
1. Carregar contexto do cliente (content-memory)
2. Resumo do cliente: nicho, preferencias, metricas recentes
3. Perguntar tipo de conteudo (post organic, anuncio, serie)
4. Iniciar pipeline na etapa 1 (Ideias)

### `status` - Status do Pipeline
1. Listar clientes com campanhas ativas
2. Para cada: etapa atual, conteudos em cada fase, metricas recentes
3. Sugerir proximas acoes

### `continuar [cliente]` - Retomar Pipeline
1. Carregar contexto do cliente
2. Identificar ultima etapa concluida
3. Retomar da proxima etapa pendente

## Fluxo de Uma Campanha

### Etapa 1: Ideias
- Carregar trends recentes (content-ideas)
- Analisar concorrentes via Meta Ads Library
- Gerar 5-10 ideias com base em trends + nicho
- Salvar ideias aprovadas

### Etapa 2: Roteiro
- Selecionar ideia aprovada
- Gerar roteiro Hook-Desenvolvimento-CTA
- Ajustar tom e duracao
- Salvar roteiro

### Etapa 3: Gravacao
- Gerar plano de gravacao a partir do roteiro
- Checklist de equipamento e preparacao
- Apos gravacao: organizar arquivos brutos

### Etapa 4: Edicao
- Selecionar melhores takes
- Montar no Remotion com template
- Aplicar legendas e overlays
- Exportar video final

### Etapa 5: Publicacao
- Gerar metadata (descricao, hashtags)
- Publicar nas plataformas configuradas
- Salvar registro de publicacao

### Etapa 6: Metricas
- Coletar metricas apos 24h/48h/7d
- Analisar retencao e engajamento
- Gerar insights
- Salvar aprendizados (stories) no contexto

## Regras

- Sempre carregar contexto do cliente antes de qualquer acao
- Sempre salvar aprendizados apos cada publicacao
- Sempre perguntar antes de avancar etapa
- Sempre respeitar a estrutura de pastas padrao
- Nunca publicar sem preview/approvacao do usuario
- Nunca commitar arquivos .env.cliente
