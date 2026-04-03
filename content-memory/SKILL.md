---
name: content-memory
description: "Sistema de memoria persistente para criacao de conteudo. Armazena preferencias do cliente, historico de performance, historias (pontos importantes aprendidos), dados de metricas e contexto de sessoes anteriores. Use quando: lembrar preferencias, consultar historico, salvar aprendizados, analisar performance passada, carregar contexto de cliente. Comandos: /lembrar, /historico, /stories, /contexto."
---

# content-memory

Sistema de memoria persistente para campanhas de conteudo. Armazena e recupera contexto, preferencias e metricas dos clientes.

## Arquivos

- `~/conteudo/campanhas/{cliente}/contexto.json` - Memoria ativa do cliente
- `~/conteudo/campanhas/{cliente}/historico.json` - Log historico de publicacoes

## Funcoes

### get_context(client)

Carrega o contexto completo de um cliente.

```bash
cat ~/conteudo/campanhas/$CLIENTE/contexto.json
```

Se o arquivo nao existir, retorne contexto vazio e pergunte se deseja inicializar.

Apos carregar, exiba um resumo:

```
Cliente: {nome}
Nicho: {nicho}
Plataformas: {plataformas}
Tom de voz: {tom_de_voz}
Total publicados: {metricas_resumo.total_publicados}
Engajamento medio: {metricas_resumo.avg_engagement}
Stories salvas: {stories.length}
```

Pergunte: "Ha alguma informacao que precisa atualizar?"

### save_story(client, title, content, tags)

Salva um aprendizado importante na memoria do cliente.

1. Carregue `contexto.json`
2. Gere um `id` unico (timestamp: `story_YYYYMMDDHHmmss`)
3. Adicione ao array `stories`:

```json
{
  "id": "story_20250115143000",
  "data": "2025-01-15",
  "titulo": "Titulo do aprendizado",
  "conteudo": "Descricao detalhada do que foi aprendido",
  "tags": ["engajamento", "formato", "horario"],
  "relevancia": "alta"
}
```

4. Salve o JSON atualizado

Relevancia padrao: `alta`. Aceita valores: `alta`, `media`, `baixa`.

### update_metrics_summary(client, new_metrics)

Atualiza o resumo de metricas agregadas.

Receba `new_metrics` com: engajamento, retencao, alcance, horario.

Carregue `contexto.json`, atualize `metricas_resumo`:

```json
{
  "total_publicados": 45,
  "avg_retention": "68.3%",
  "avg_engagement": "4.2%",
  "melhor_horario": "18:00",
  "ultima_atualizacao": "2025-01-15"
}
```

**Alerta automatico:** compare `avg_engagement` e `avg_retention` com os valores anteriores. Se a diferenca for maior que 20% (positivo ou negativo), sinalize:

```
ALERTA: Engajamento caiu 35% em relacao a media anterior (6.5% -> 4.2%).
```

### search_stories(client, query)

Busca stories por tags ou conteudo textual.

```bash
cat ~/conteudo/campanhas/$CLIENTE/contexto.json | \
  jq -r '.stories[] | select(.tags[] | test("QUERY"; "i")) or (.conteudo | test("QUERY"; "i"))'
```

Retorne resultados ordenados por data (mais recente primeiro) com titulo, data e tags.

### get_performance_insights(client)

Analisa o historico para identificar padroes.

Carregue `historico.json` e execute analises:

1. **Melhor dia da semana:** qual dia tem maior media de engajamento
2. **Melhor horario:** qual horario concentre melhor performance
3. **Tipo mais eficaz:** posts vs anuncios vs stories
4. **Tendencia:** engajamento subindo ou caindo nas ultimas 4 semanas
5. **Top 3 conteudos:** por engajamento

Retorne insights em formato conciso com recomendacoes.

## Schema - contexto.json

```json
{
  "cliente": {
    "nome": "string",
    "nicho": "string",
    "plataformas": ["string"],
    "tom_de_voz": "string",
    "cta_padrao": "string",
    "horarios_melhores": ["string"]
  },
  "preferencias": {
    "duracao_video": "string",
    "formato_preferido": "string",
    "estilo_edicao": "string",
    "cores_marca": ["string"]
  },
  "stories": [
    {
      "id": "string",
      "data": "YYYY-MM-DD",
      "titulo": "string",
      "conteudo": "string",
      "tags": ["string"],
      "relevancia": "alta|media|baixa"
    }
  ],
  "metricas_resumo": {
    "total_publicados": "number",
    "avg_retention": "string",
    "avg_engagement": "string",
    "melhor_horario": "string",
    "ultima_atualizacao": "YYYY-MM-DD"
  }
}
```

## Schema - historico.json

```json
{
  "entries": [
    {
      "id": "string",
      "data": "YYYY-MM-DD",
      "tipo": "post|anuncio|story",
      "titulo": "string",
      "plataformas": ["string"],
      "metricas": {
        "engajamento": "string",
        "alcance": "number",
        "retention": "string",
        "cliques": "number"
      },
      "notas": "string"
    }
  ]
}
```

## Regras

- Sempre valide JSON antes de salvar (use `jq .` para checar sintaxe)
- Nunca sobrescreva stories - sempre adicione ao array
- Mantenha datas no formato ISO `YYYY-MM-DD`
- Use `jq` para manipulacao de JSON quando disponivel
- Ao carregar contexto, pergunte se ha atualizacoes necessarias
- Ao receber metricas novas, compare automaticamente com historico
