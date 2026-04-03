---
name: content-metrics
description: "Analise de metricas de performance de conteudo publicado. Coleta dados de retencao, engajamento, alcance e conversao via APIs das plataformas. Gera relatorios e insights para otimizar futuras publicacoes. Use quando: analisar metricas, ver performance, relatorio de conteudo, retencao do publico, engajamento, alcance, insights de performance, comparar videos."
---

# Content Metrics - Analise de Performance de Conteudo

## Onboarding Interativo

Ao iniciar analise de metricas:

1. Pergunte o periodo a analisar (ultima semana, ultimo mes, ou personalizado)
2. Pergunte qual cliente
3. Pergunte quais metricas priorizar (retencao, engajamento, alcance, conversao)
4. Pergunte se quer comparar com periodo anterior

## Metricas por Plataforma

### TikTok (via Research API)

- Views totais
- Likes, Comments, Shares, Saves
- Watch time / Average watch time
- Curva de retencao (segundo a segundo)
- Fonte de trafego (traffic source type)
- Crescimento de seguidores

### Instagram (via Graph API / Insights)

- Reach, Impressions
- Likes, Comments, Saves, Shares
- Video views, Average watch time
- Retencao (quando disponivel via Insights)
- Demografia de seguidores
- Melhores horarios para postar

## Metricas-Chave para Acompanhar

1. **Retencao nos 3s**: % que assiste os primeiros 3 segundos (critico!)
2. **Retencao total**: % que assiste ate o final
3. **Engajamento**: `(likes + comments + shares) / views`
4. **CTR**: cliques no link da bio / views (se aplicavel)
5. **Salvamentos**: indicador forte de valor percebido

## Workflow de Analise

1. Busque metricas das APIs usando credenciais de `.env.cliente`
2. Atualize `historico.json` com os novos dados
3. Calcule estatisticas agregadas em `contexto.json`
4. Gere insights comparando com a media historica
5. Salve relatorio em `~/conteudo/campanhas/{cliente}/metricas/`

## Template de Relatorio

```markdown
# Relatorio de Performance - {cliente}

**Periodo**: {inicio} a {fim}
**Total publicado**: X videos

## Resumo
- Views totais: X
- Engajamento medio: X%
- Retencao 3s media: X%
- Melhor video: [titulo] (X views, X% engajamento)

## Top 3 Videos
1. [titulo] - X views, X% retencao, X% engajamento
2. [titulo] - X views, X% retencao, X% engajamento
3. [titulo] - X views, X% retencao, X% engajamento

## Insights
- [insight sobre padrao de horario]
- [insight sobre tipo de conteudo]
- [insight sobre hook performance]
- [recomendacao para proximos videos]
```

## Motor de Insights

Analise padroes nos dados:

- **Tipos de hook** com melhor retencao (pergunta, controversia, promessa, cenario)
- **Duracao vs engajamento**: correlacao entre tamanho do video e engajamento
- **Horario vs alcance**: correlacao entre horario de postagem e alcance
- **Tipo de conteudo vs salvamentos**: quais topics geram mais saves
- **Trend-based vs evergreen**: compare performance de conteudo tendencia vs atemporal

Atualize o `contexto.json` do cliente com os insights para informar a criacao de conteudo futuro.

## Formato dos Dados

### historico.json (entrada)
```json
[
  {
    "id": "video_id",
    "titulo": "Titulo do video",
    "data_publicacao": "2025-01-15",
    "plataforma": "tiktok",
    "metricas": {
      "views": 15000,
      "likes": 800,
      "comments": 120,
      "shares": 60,
      "saves": 45,
      "retention_3s": 72,
      "retention_total": 35,
      "watch_time_avg": 18.5
    }
  }
]
```

### contexto.json (saida)
```json
{
  "cliente": "nome",
  "atualizado": "2025-01-20",
  "media_views": 12000,
  "media_engajamento": 5.8,
  "media_retention_3s": 68,
  "melhor_horario": "19:00",
  "melhor_dia": "quarta",
  "top_hooks": ["pergunta", "promessa"],
  "top_topics": ["educacao", "tutorial"],
  "insights": [
    "Videos com hook de pergunta tem 15% mais retencao",
    "Reels de 15-20s performam melhor que 30s"
  ]
}
```
