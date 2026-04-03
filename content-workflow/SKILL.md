---
name: content-workflow
description: "Orquestrador principal do pipeline de criacao de conteudo para midias sociais. Coordena todas as etapas: Ideias, Roteiro, Gravacao, Edicao (Remotion), Publicacao (TikTok/Instagram) e Metricas. Gerencia multiplos clientes, memoria persistente e estrutura de pastas. Use quando: criar conteudo, pipeline de video, campanha de midia social, workflow de conteudo, onboarding de cliente, status de campanha, gerenciar clientes, fluxo completo de criacao de conteudo. Comandos: /cliente-setup, /nova-campanha, /status, /continuar."
---

# Content Workflow - Pipeline Completo de Criacao de Conteudo

Orquestra o pipeline de 6 etapas para criacao de conteudo em midias sociais.

## Etapas do Pipeline

```
0. PLANEJAMENTO EDITORIAL (content-editorial)
   ↓
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
| content-editorial | Linha editorial e calendario de conteudo | Criar calendario, planejar conteudo |
| content-ideas | Pesquisa de trends e captacao de ideias | Buscar ideias, trends |
| content-script | Roteirizacao Hook-Desenvolvimento-CTA | Criar roteiro, script |
| content-recording | Planejamento de gravacao | Preparar gravacao, takes |
| content-editing | Edicao de video com Remotion | Editar video, montar |
| content-publishing | Publicacao via TikTok/Instagram API | Publicar, agendar |
| content-metrics | Analise de performance | Metricas, relatorios |

## Slash Commands

### `/cliente-setup [nome]` - Onboarding Completo de Cliente
Aciona quando usuario digita `/cliente-setup` ou `/cliente-setup <nome>`.
1. Se nome nao fornecido, perguntar: "Qual o nome do cliente?"
2. Verificar se cliente ja existe em ~/conteudo/campanhas/
3. Se existe, perguntar: "Cliente ja encontrado. Deseja atualizar as configuracoes?"
4. Se novo, iniciar onboarding interativo:
   - "Qual o nicho/segmento do cliente?" (ex: fitness, finanzas, gastronomia, educacao)
   - "Quais plataformas vai publicar?" (TikTok, Instagram Reels, YouTube Shorts, todas)
   - "Qual a frequencia de publicacao?" (diaria, 3x semana, semanal, quinzenal)
   - "Qual o tom de voz?" (educativo, humor, inspiracional, provocativo, vendas)
   - "Qual o CTA principal padrao?" (siga, comente, salve, link na bio)
   - "Quais horarios preferidos para publicacao?"
5. Criar estrutura de pastas completa (content-fs)
6. Inicializar contexto.json e historico.json (content-memory)
7. Perguntar: "Deseja configurar as APIs de publicacao agora? (TikTok, Instagram)"
8. Se sim, guiar setup de cada API (content-publishing)
9. Resumo final: "Cliente `{nome}` configurado com sucesso! Pasta: ~/conteudo/campanhas/{nome}/"

### `/nova-campanha [cliente]` - Iniciar Pipeline de Conteudo
Aciona quando usuario digita `/nova-campanha` ou `/nova-campanha <cliente>`.
1. Se cliente nao fornecido, listar clientes disponiveis e pedir selecao
2. Carregar contexto do cliente (content-memory)
3. Exibir resumo: nicho, plataformas, tom, frequencia, metricas recentes
4. Perguntar tipo de conteudo:
   - Post organico (feed/reels)
   - Criativo para anuncio
   - Serie de conteudo (3+ videos)
   - Conteudo sazonal (datas comemorativas)
5. Confirmar e iniciar pipeline na etapa 1 (Ideias)
6. A cada etapa concluida, perguntar: "Deseja avancar para a proxima etapa?"

### `/status` - Painel de Status
Aciona quando usuario digita `/status`.
1. Escanear ~/conteudo/campanhas/ para todos os clientes
2. Para cada cliente, exibir:
   ```
   📁 {cliente} ({nicho})
   ├── 📝 Ideias pendentes: X
   ├── 📜 Roteiros prontos: X
   ├── 🎬 Gravacoes brutos: X
   ├── ✂️ Editados prontos: X
   ├── 🚀 Publicados esta semana: X
   ├── 📊 Metricas avg: X% engajamento | X% retencao 3s
   └── 📍 Etapa atual: [etapa]
   ```
3. Sugerir proximas acoes por cliente
4. Destacar clientes sem atividade recente (>7 dias)

### `/continuar [cliente]` - Retomar Pipeline
Aciona quando usuario digita `/continuar` ou `/continuar <cliente>`.
1. Se cliente nao fornecido, listar clientes com pipeline ativo
2. Carregar contexto do cliente
3. Identificar ultima etapa concluida via historico.json
4. Resumir o que ja foi feito
5. Perguntar: "Deseja retomar de [proxima etapa]?"
6. Se sim, iniciar workflow dessa etapa

## Fluxo de Uma Campanha

### Etapa 0: Planejamento Editorial
- Verificar se existe linha editorial para o cliente (content-editorial)
- Se nao existe, sugerir `/create-linha-editorial`
- Se existe, carregar calendario editorial atual
- Alinhar conteudo do pipeline com o calendario

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
